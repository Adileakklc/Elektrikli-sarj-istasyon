import time, hmac, hashlib, json, random

SHARED_SECRET = b"MY_SHARED_SECRET_32CHARS"  # app.py ile aynı

def sign_payload(d):
    # app.py'deki make_signing_str ile aynı format:
    enerji = f"{float(d['enerji']):.3f}"
    voltaj = f"{float(d['voltaj']):.1f}"
    akim   = f"{float(d['akim']):.3f}"
    signing = f"{d['userId']}|{enerji}|{int(d['sure'])}|{voltaj}|{akim}|{d['timestamp']}|{d['nonce']}"
    return hmac.new(SHARED_SECRET, signing.encode(), hashlib.sha256).hexdigest()

now = int(time.time())
payload = {
    "userId": "ESP01",
    "enerji": 12.5,
    "sure": 3600,
    "voltaj": 220,
    "akim": 5.7,
    "timestamp": now,  # epoch saniye (app.py bunu kabul ediyor)
    "nonce": f"N-{now}-{random.randrange(1_000_000):06d}"
}
payload["hash"] = sign_payload(payload)

with open("request.json","w", encoding="utf-8") as f:
    json.dump(payload, f)
print("request.json yazıldı:", payload)
