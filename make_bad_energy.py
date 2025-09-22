import time, hmac, hashlib, json, random
SHARED_SECRET = b"MY_SHARED_SECRET_32CHARS"

def sign(d):
    s = f"{d['userId']}|{d['enerji']:.3f}|{int(d['sure'])}|{d['voltaj']:.1f}|{d['akim']:.3f}|{d['timestamp']}|{d['nonce']}"
    return hmac.new(SHARED_SECRET, s.encode(), hashlib.sha256).hexdigest()

d = {
    "userId":"ESP01",
    "enerji":-1.0,     # negatif enerji → 400 beklenir
    "sure":600,
    "voltaj":220.0,
    "akim":2.0,
    "timestamp":int(time.time()),
    "nonce":f"N-{int(time.time())}-{random.randrange(1_000_000):06d}"
}
d["hash"] = sign(d)
open("bad_energy.json","w").write(json.dumps(d))
print("bad_energy.json yazıldı")
