# DB Migration — riskScore Kolonu

Mevcut `telemetry` tablosu üzerinde `riskScore` kolonu yoksa eklemek için:

```sql
ALTER TABLE telemetry ADD COLUMN riskScore REAL;
```

> Geriye dönük kayıtlar için `riskScore` `NULL` kalacaktır. Uygulama tarafında `NULL` değerleri uygun şekilde ele alınız (ör. panelde rozet yerine `—` gösterimi).
