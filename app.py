from flask import Flask, request, jsonify, send_from_directory
import sqlite3, hmac, hashlib, pickle
from time import time
from datetime import datetime
from collections import defaultdict, deque
import numpy as np
import pandas as pd  # pip install pandas
# sklearn sadece model dosyalarını yüklerken uyarı önlemek için; yoksa da sorun olmaz
try:
    import sklearn  # noqa: F401
except Exception:
    pass

# -------------------------------------------------
# Flask app
# -------------------------------------------------
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

DB_PATH = "telemetry.db"
SHARED_SECRET = b"MY_SHARED_SECRET_32CHARS"  # ESP ile birebir aynı olmalı
_rate = defaultdict(deque)  # userId -> deque[timestamps]

# -------------------------------------------------
# ML - eğitimde kullandığın kolon isimleri
# -------------------------------------------------
FEATURE_COLUMNS = [
    "Energy Consumed (kWh)",
    "Duration_min",
    "Energy_per_min",
    "Start_Hour",
    "Temperature (°C)",
    "Vehicle Age (years)",
]

# -------------------------------------------------
# Statik (index.html / panel.html / js / css) servis
# -------------------------------------------------
@app.get("/")
def serve_index():
    return send_from_directory(".", "index.html")

@app.get("/panel")
def serve_panel():
    return send_from_directory(".", "panel.html")

# js, css, images/ gibi diğer dosyalar
@app.get("/<path:filename>")
def serve_any(filename):
    return send_from_directory(".", filename)

# Basit sağlık
@app.get("/health")
def health():
    return "OK", 200

# -------------------------------------------------
# Yardımcılar
# -------------------------------------------------
def ts_to_epoch(ts):
    """epoch sayı veya 'YYYY-MM-DD HH:MM:SS' stringini epoch'a çevirir"""
    if isinstance(ts, (int, float)) or (isinstance(ts, str) and ts.isdigit()):
        return int(ts)
    return int(datetime.strptime(str(ts), "%Y-%m-%d %H:%M:%S").timestamp())

def validate_rules(d):
    enerji = float(d["enerji"])
    sure   = int(d["sure"])
    if not (0 < sure <= 86400):
        return False, "bad duration"
    if not (0 <= enerji <= 200):
        return False, "bad energy"
    # dakika başına 2 kWh üstünü anormal say
    if (enerji / (max(sure/60.0, 1e-6))) > 2.0:
        return False, "too fast"
    return True, None

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS telemetry(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          userId TEXT,
          enerji REAL,
          sure INTEGER,
          voltaj REAL,
          akim REAL,
          timestamp TEXT,
          nonce TEXT UNIQUE,
          hash TEXT,
          created_at DATETIME DEFAULT (datetime('now','localtime')),
          riskScore REAL
        )
        """)
        # riskScore kolonu yoksa ekle
        cols = c.execute("PRAGMA table_info(telemetry)").fetchall()
        colnames = {r[1] for r in cols}
        if "riskScore" not in colnames:
            c.execute("ALTER TABLE telemetry ADD COLUMN riskScore REAL")
init_db()

def make_signing_str(d):
    enerji = f"{float(d['enerji']):.3f}"
    voltaj = f"{float(d['voltaj']):.1f}"
    akim   = f"{float(d['akim']):.3f}"
    return f"{d['userId']}|{enerji}|{int(d['sure'])}|{voltaj}|{akim}|{d['timestamp']}|{d['nonce']}"

def hmac_hex(signing: str) -> str:
    return hmac.new(SHARED_SECRET, signing.encode("utf-8"), hashlib.sha256).hexdigest()

# -------------------------------------------------
# ML modellerini yükle (varsa)
# -------------------------------------------------
ML_SCALER = None
ML_MODEL  = None
try:
    with open("models/scaler.pkl", "rb") as f:
        ML_SCALER = pickle.load(f)
    with open("models/iso.pkl", "rb") as f:
        ML_MODEL = pickle.load(f)
    print("[ML] Modeller yüklendi.")
except FileNotFoundError:
    print("[ML] Uyarı: models/scaler.pkl veya models/iso.pkl bulunamadı. Skor hesaplanmayacak.")

def ml_features_from_json(d: dict) -> pd.DataFrame:
    """ /ml endpoint'i için JSON → eğitim kolonları """
    energy = float(d["energy"])
    dur_s  = float(d["duration"])
    hour   = int(d["hour"])
    temp   = float(d["temperature"])
    vage   = float(d["vehicle_age"])

    dur_min = max(dur_s / 60.0, 1e-6)
    epm = energy / dur_min

    row = {
        "Energy Consumed (kWh)": energy,
        "Duration_min": dur_min,
        "Energy_per_min": epm,
        "Start_Hour": hour,
        "Temperature (°C)": temp,
        "Vehicle Age (years)": vage,
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)

def ml_features_from_raw_telemetry(enerji: float, sure: int, voltaj: float, akim: float,
                                   hour: int, temperature: float, vehicle_age: float) -> pd.DataFrame:
    """ /telemetry sonrası özellik üretimi """
    dur_min = max(sure / 60.0, 1e-6)
    epm = enerji / dur_min
    row = {
        "Energy Consumed (kWh)": enerji,
        "Duration_min": dur_min,
        "Energy_per_min": epm,
        "Start_Hour": int(hour),
        "Temperature (°C)": float(temperature),
        "Vehicle Age (years)": float(vehicle_age),
    }
    return pd.DataFrame([row], columns=FEATURE_COLUMNS)

# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.post("/telemetry")
def telemetry():
    data = request.get_json(silent=True) or {}

    required = ["userId","enerji","sure","voltaj","akim","timestamp","nonce","hash"]
    if not all(k in data for k in required):
        return jsonify({"status":"error","msg":"missing fields"}), 400

    # timestamp
    try:
        now = int(time())
        ts_epoch = ts_to_epoch(data["timestamp"])
    except Exception:
        return jsonify({"status":"error","msg":"bad timestamp format"}), 400
    if now - ts_epoch > 60:
        return jsonify({"status":"error","msg":"stale timestamp"}), 400

    # HMAC
    signing = make_signing_str(data)
    expected = hmac_hex(signing)
    if not hmac.compare_digest(expected, str(data["hash"]).lower()):
        return jsonify({"status":"error","msg":"bad signature"}), 401

    # Rate limit (5sn içinde >3 istek → 429)
    dq = _rate[data["userId"]]
    dq.append(now)
    while dq and now - dq[0] > 5:
        dq.popleft()
    if len(dq) > 3:
        return jsonify({"status":"error","msg":"rate limited"}), 429

    # Kurallar
    ok, reason = validate_rules(data)
    if not ok:
        return jsonify({"status":"error","msg":reason}), 400

    # INSERT + nonce tekilliği
    try:
        with sqlite3.connect(DB_PATH) as c:
            c.execute("""
            INSERT INTO telemetry (userId, enerji, sure, voltaj, akim, timestamp, nonce, hash)
            VALUES (?,?,?,?,?,?,?,?)
            """, (
                data["userId"], float(data["enerji"]), int(data["sure"]),
                float(data["voltaj"]), float(data["akim"]),
                data["timestamp"], data["nonce"], str(data["hash"]).lower()
            ))
            row_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    except sqlite3.IntegrityError:
        return jsonify({"status":"error","msg":"replay detected"}), 409

    # ML skor hesapla (varsa) ve DB'ye yaz
    risk_val = None
    try:
        if ML_SCALER is not None and ML_MODEL is not None:
            hour = datetime.fromtimestamp(int(ts_epoch)).hour
            temperature = float(data.get("temperature", 25.0))
            vehicle_age = float(data.get("vehicle_age", 5.0))

            X_df = ml_features_from_raw_telemetry(
                enerji=float(data["enerji"]),
                sure=int(data["sure"]),
                voltaj=float(data["voltaj"]),
                akim=float(data["akim"]),
                hour=int(hour),
                temperature=temperature,
                vehicle_age=vehicle_age,
            )
            Xs = ML_SCALER.transform(X_df)
            risk_val = float(ML_MODEL.decision_function(Xs)[0])  # <0: anomali

            with sqlite3.connect(DB_PATH) as c2:
                c2.execute("UPDATE telemetry SET riskScore=? WHERE id=?", (risk_val, row_id))
    except Exception as e:
        print("[ML] scoring error:", e)

    return jsonify({"status": "ok", "id": row_id, "riskScore": risk_val})

@app.post("/ml")
def ml_score():
    if ML_SCALER is None or ML_MODEL is None:
        return jsonify({"status":"error","msg":"model files missing"}), 503

    data = request.get_json(silent=True) or {}
    required = ["energy","duration","hour","temperature","vehicle_age"]
    if not all(k in data for k in required):
        return jsonify({"status":"error","msg":"missing fields"}), 400

    try:
        X_df = ml_features_from_json(data)
        Xs   = ML_SCALER.transform(X_df)
        score = float(ML_MODEL.decision_function(Xs)[0])
        label = "anomaly" if score < 0.0 else "normal"

        if score < -0.2:
            risk = "yuksek"
        elif score < 0.0:
            risk = "orta"
        else:
            risk = "dusuk"

        return jsonify({
            "prediction": label,
            "riskScore": round(score, 3),
            "riskLevel": risk
        })
    except Exception as e:
        return jsonify({"status":"error","msg":str(e)}), 500

@app.get("/sessions")
def sessions():
    try:
        limit = int(request.args.get("limit", 50))
    except Exception:
        limit = 50
    limit = max(1, min(limit, 500))

    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """
            SELECT id, userId, enerji, sure, voltaj, akim, created_at,
                   COALESCE(riskScore, NULL) AS riskScore
            FROM telemetry
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
    data = [dict(r) for r in rows]
    return jsonify({"sessions": data, "count": len(data)})

@app.post("/sessions/<int:sid>/stop")
def stop_session(sid):
    try:
        with sqlite3.connect(DB_PATH) as c:
            row = c.execute("SELECT id FROM telemetry WHERE id=?", (sid,)).fetchone()
        if not row:
            return jsonify({"status":"error","msg":"session not found"}), 404
    except Exception as e:
        return jsonify({"status":"error","msg":str(e)}), 500

    print(f"[SESSIONS] stop requested for id={sid} at {datetime.now().isoformat()}")
    return jsonify({"status":"ok","stopped": True, "id": sid}), 200

# -------------------------------------------------
# run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
