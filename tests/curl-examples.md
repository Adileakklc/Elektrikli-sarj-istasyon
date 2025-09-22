# curl examples

## Telemetry 
```bash
curl -X POST http://localhost:5000/telemetry   -H "Content-Type: application/json"   -d '{
    "userId":"user123",
    "enerji":12.5,
    "sure":3600,
    "voltaj":220,
    "akim":5.7,
    "timestamp":"2025-09-12 13:57:12",
    "nonce":"TEST-NONCE-123",
    "hash":"<buraya-esp-tarafindan-hesaplanmis-hex-hmac>"
  }'
```

## ML skor
```bash
curl -X POST http://localhost:5000/ml   -H "Content-Type: application/json"   -d @tests/ml-samples/normal.json
```
