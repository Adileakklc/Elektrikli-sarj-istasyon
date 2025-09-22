# tests/send_telemetry.py
import time, hmac, hashlib, json, requests, secrets, string

API = "http://127.0.0.1:5000/telemetry"
SHARED_SECRET = b"MY_SHARED_SECRET_32CHARS"  # app.py ile birebir aynı yap

def nonce(n=12):
    return ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(n))

payload = {
    "userId": "ESP01",
    "enerji": 12.5,
    "sure": 3600,
    "voltaj": 220.0,
    "akim": 5.7,
    "timestamp": int(time.time()),
    "nonce": nonce(),
}

signing = f"{payload['userId']}|{payload['enerji']:.3f}|{int(payload['sure'])}|{payload['voltaj']:.1f}|{payload['akim']:.3f}|{payload['timestamp']}|{payload['nonce']}"
payload["hash"] = hmac.new(SHARED_SECRET, signing.encode(), hashlib.sha256).hexdigest()

print("Gönderilen JSON:", json.dumps(payload, indent=2))
r = requests.post(API, json=payload, timeout=10)
print("Sunucu yanıtı:", r.status_code, r.text)
