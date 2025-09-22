import json

d = json.load(open("request.json"))
# 3 dakika geri al – HMAC'i BİLEREK yenileme (önce timestamp kontrolü yakalayacak)
d["timestamp"] = int(d["timestamp"]) - 180

with open("request_old.json","w") as f:
    json.dump(d, f)

print("request_old.json hazır")
