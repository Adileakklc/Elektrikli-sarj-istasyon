import time, hmac, hashlib, json, random
SHARED_SECRET = b"MY_SHARED_SECRET_32CHARS"

def sign(d):
    s = f"{d['userId']}|{d['enerji']:.3f}|{int(d['sure'])}|{d['voltaj']:.1f}|{d['akim']:.3f}|{d['timestamp']}|{d['nonce']}"
    return hmac.new(SHARED_SECRET, s.encode(), hashlib.sha256).hexdigest()

# 50 kWh / 1 dk  →  2 kWh/dk eşiğini aşar → 400 bekleriz
d = {
    "userId":"ESP01",
    "enerji":50.0,
    "sure":60,
    "voltaj":220.0,
    "akim":20.0,
    "timestamp":int(time.time()),
    "nonce":f"N-{int(time.time())}-{random.randrange(1_000_000):06d}"
}
d["hash"] = sign(d)
open("bad_ratio.json","w").write(json.dumps(d))
print("bad_ratio.json yazıldı")
