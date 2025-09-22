# API Dokümantasyonu

Bu dokümantasyon, backend servislerinin kısa özetidir. Tam şema için `openapi.yaml` dosyasına bakınız.

## Sağlık
- `GET /` → `200 OK`

## Telemetry
- `POST /telemetry`  
  **Body (JSON):**
  ```json
  {
    "userId": "user123",
    "enerji": 12.5,
    "sure": 3600,
    "voltaj": 220,
    "akim": 5.7,
    "timestamp": "2025-09-12 13:57:12",
    "nonce": "UUID-or-random",
    "hash": "hex-hmac"
  }
  ```
  **Response (JSON):**
  ```json
  {"status":"ok","id": 42, "riskScore": -0.137}
  ```

## ML Skor
- `POST /ml`
  **Body (JSON):**
  ```json
  {"energy": 12.5, "duration": 3600, "hour": 13, "temperature": 25.0, "vehicle_age": 3.0}
  ```
  **Response (JSON):**
  ```json
  {"prediction": "normal", "riskScore": -0.042, "riskLevel": "dusuk"}
  ```

## Seanslar
- `GET /sessions?limit=50`
  **Response (JSON):**
  ```json
  {
    "sessions": [
      {"id": 42, "userId":"user123","enerji":12.5,"sure":3600,"voltaj":220,"akim":5.7,"created_at":"2025-09-19 19:12:31","riskScore":-0.137}
    ],
    "count": 1
  }
  ```

- `POST /sessions/{id}/stop`
  **Response (JSON):**
  ```json
  {"status":"ok","stopped":true,"id":42}
  ```
