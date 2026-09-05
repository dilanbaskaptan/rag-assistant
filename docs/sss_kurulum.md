# SSS: Kurulum ve Çalıştırma

**Soru: Bu uygulamayı çalıştırmak için internet bağlantısı gerekiyor mu?**
Hayır. Foundry Local, phi-3.5-mini (soru-cevap) ve qwen3-embedding-0.6b (embedding) modellerini bilgisayarınızda yerel olarak çalıştırır. Modeller bir kere indirildikten sonra uygulama tamamen çevrimdışı (offline) çalışabilir.

**Soru: Veritabanına yeni bir belge nasıl eklenir?**
Yeni bir `.md` dosyasını `docs/` klasörüne koyup `ingest.py` dosyasını tekrar çalıştırmak yeterlidir. `ingest.py`, `docs/` klasöründeki tüm belgeleri okuyup parçalara (chunk) böler, her parça için embedding hesaplar ve SQLite veritabanına kaydeder.

**Soru: Model soruyu bilmiyorsa ne olur?**
Sistem promptunda modele, veritabanındaki belgelerde cevabı bulamadığında bunu açıkça belirtmesi ve bilgi uydurmaması gerektiği söylenir. Bu, "halüsinasyon" riskini azaltmak için önemlidir.
