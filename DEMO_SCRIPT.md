# Demo Video Senaryosu (2 dakika)

Bu, Hafta 6'nın "2 dakikalık demo videosu" gereksinimi için bir storyboard. Format:
problem → mimari → canlı demo → öğrenilenler.

**Yöneticiden gelen güncel talimat:** "Sadece ne yaptığınızı ve ne öğrendiğinizi
anlatan bir video linki, bir de source code'un olduğu bir link (github mesela)."
Yani katı bir problem/mimari/demo şablonu şart değil — asıl önemli olan **ne yaptık**
(mimari + canlı demo bunu gösteriyor) ve **ne öğrendik** (öğrenilenler bölümü).
Bu yüzden öğrenilenler bölümüne daha fazla zaman ayırdık; asıl "hikaye" burada.

**Ayrıca gerekli:** Kaynak koduna bir link (GitHub). Proje şu an bir git deposu değil —
bunu hazırlamak istersen (git init, commit, GitHub'a push) ayrıca söyle, senin
GitHub hesabınla depo oluşturman/push etmen gerekecek, ben o kısmı senin adına
yapamam ama yerel git kurulumunu hazırlayabilirim.

**Önemli pratik not:** Chat modeli artık GPU'da çalışıyor, bu yüzden bir sorudan
cevap almak ~1.5-3.5 saniye sürüyor — gerçek zamanlı göstermek için yeterince hızlı,
kurguya/hızlandırmaya gerek yok. Tek istisna: **uygulamayı (ya da Foundry Local
servisini) yeniden başlattıktan sonraki ilk soru** GPU motorunun "ısınması" nedeniyle
~50 saniye sürebilir. Bu yüzden kayda başlamadan önce bir kere "ısıtma sorusu" sor
(ekranda gösterme), sonra kayda geç — böylece gösterdiğin her soru hızlı olur.

---

## 0:00 – 0:15 (15 sn) — Problem

**Söylenecekler (örnek):**
> "Ders notlarım, FAQ'larım, teknik dokümanlarım var ama aralarında arama yapmak zor.
> Bulut AI asistanları yardımcı olabilir ama özel belgelerimi üçüncü parti bir API'ye
> göndermek istemiyorum, her zaman internet de olmayabilir. Bu proje, kendi
> belgelerime dayalı soruları tamamen kendi bilgisayarımda, internete hiç çıkmadan
> cevaplıyor."

**Ekranda gösterilecek:** Belki `docs/` klasöründeki birkaç belge (dosya gezgininde),
sonra uygulamanın ana ekranı.

---

## 0:15 – 0:35 (20 sn) — Mimari

**Söylenecekler (örnek, biraz daha hızlı/kısa):**
> "Bu, RAG mimarisi — Retrieval-Augmented Generation. Önce sorunun embedding'i
> çıkarılıp veritabanındaki en alakalı belge parçaları kosinüs benzerliğiyle
> bulunuyor. Sonra bu parçalar soruyla birlikte yerel bir dil modeline gönderiliyor,
> model sadece bunlara dayanarak cevap veriyor. Her şey Microsoft Foundry Local ile
> tamamen yerel çalışıyor, hiçbir veri bilgisayarımdan çıkmıyor."

**Ekranda gösterilecek:** README'deki mimari diyagramı (ASCII kutular) ya da
`ingest.py` → `retrieval.py` → `prompts.py` → `app.py` dosyalarının kısa bir taraması.
İstersen bu diyagramı okurken ekranda tutmak için README.md'yi açık bırak.

---

## 0:35 – 1:30 (55 sn) — Canlı Demo

**Sahne 1 (cevaplanabilir soru, ~25 sn, gerçek zamanlı):**
- Streamlit arayüzünde bir soru sor, örn. "RAG nedir?"
- Cevap ~2-3 saniyede geliyor — bekleme neredeyse yok, doğal konuşarak devam edebilirsin.
- Cevabın altındaki kaynak etiketini ("Source: rag_nedir.md") vurgula — "İşte burada,
  cevabın hangi belgeye dayandığını görebiliyorsunuz."

**Sahne 2 (cevaplanamaz soru, ~15 sn, gerçek zamanlı gösterilebilir çünkü ~1 saniyede dönüyor):**
- "Fransa'nın başkenti neresidir?" gibi alakasız bir soru sor
- Anında gelen "Bu bilgi elimdeki belgelerde yok." cevabını göster
- "Model, elindeki belgelerde olmayan bir şeyi uydurmuyor — bunu kod seviyesinde
  garanti altına aldım."

**Not:** Her iki sahne de artık gerçek zamanlı, kesintisiz kaydedilebilir — kurguda
hızlandırma/kesme yapmana gerek yok, yeter ki kayıttan önce bir ısıtma sorusu sormuş ol.

---

## 1:30 – 2:00 (30 sn) — Öğrenilenler

Yöneticinin talimatı gereği asıl vurgu burada — "ne yaptık, ne öğrendik" videonun
can alıcı kısmı. İki ayrı, basit problem→çözüm anlatımı:

**Söylenecekler (örnek):**
> "Yol boyunca iki önemli şey öğrendim.
>
> Birincisi, performansla ilgili somut bir sorun yaşadım: yerel model CPU'da
> çalışırken bir cevap almak 30 saniyeye kadar sürüyordu — kullanılabilir değildi.
> Çözüm olarak chat modelini GPU'ya taşımayı denedim, ama laptop'umun GPU'sunda
> sadece 6 GB bellek var — iki modeli (chat ve embedding) aynı anda GPU'ya
> sığdıramadım. Embedding modelini CPU'da bırakıp sadece chat modelini GPU'ya
> vererek bunu çözdüm; yanıt süresi 2-3 saniyeye indi.
>
> İkincisi, küçük dil modellerinin talimatlara her zaman tam uymadığını gördüm —
> bazen 'bilmiyorum' demesi gerekirken kendi bilgisinden cevap uydurdu. Bu yüzden
> 'bilmiyorsan söyle' kuralını sadece prompt'a değil, koddaki bir benzerlik eşiğine
> de bağladım, böylece garanti altına aldım."

**Ekranda gösterilecek:** `test_results.md`'den kısa bir kesit (pass rate, süre
istatistikleri — özellikle "30s → 2-3s" karşılaştırması somut ve etkileyici bir
kapanış olur).

---

## Kayıt için pratik ipuçları

- Ekran kaydı için Windows'un yerleşik Xbox Game Bar'ı (Win+G) veya OBS Studio kullanılabilir.
- **Kayda başlamadan önce mutlaka bir "ısıtma sorusu" sor** (kayıt dışı) — Foundry Local
  servisi yeniden başlatıldıysa ilk soru GPU motorunun derlenmesi nedeniyle ~50 saniye
  sürebilir. Bu ısıtma sorusundan sonra her soru hızlı olur.
- Demo videosu için sadece Streamlit uygulamasını açık tut, tarayıcı donanım
  hızlandırmasını kapat — GPU belleğinde başka hiçbir şeyin pay yemesini istemezsin.
- Ses kaydı ayrı yapılıp video kurgusunda senkronize edilebilir; bu, konuşurken
  duraksamaları/tekrarları temizlemeyi kolaylaştırır.
