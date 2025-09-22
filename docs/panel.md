---
layout: page
title: Operatör Paneli
---

# Operatör Paneli

Bu panel, son yüklenen seansları ve ML risk skorlarını gösterir.  
Dosyalar: `panel.html`, `panel.js`

## Özellikler
- **Tablo**: id, userId, enerji, süre, V/A, risk rozeti, oluşturulma zamanı
- **Risk Rozeti**: 
  - Skor < -0.2 → **Yüksek**
  - Skor < 0 → **Orta**
  - Aksi → **Düşük**
- **Yenile**: `GET /sessions?limit=N`
- **Seansı Durdur**: `POST /sessions/{id}/stop` (şimdilik log + 200)

## Örnek Akış
1. ESP → `POST /telemetry` ile veri gönderir.
2. Backend insert sonrası ML skoru üretir ve satıra kaydeder.
3. Panel `GET /sessions` ile tabloyu doldurur.
4. Operatör gerekli görürse **Seansı Durdur**’a basar → backend loglar ve 200 döner.
