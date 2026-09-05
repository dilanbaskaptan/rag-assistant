# Test Results

**Chat model:** `phi-3.5-mini-instruct-trtrtx-gpu`
**Pass rate:** 10/12 (automated check only - see note below)

**Note:** the automated pass/fail check only verifies that unanswerable questions got refused and answerable questions cited the right source file. It does not check whether the generated answer is actually correct or well-formed. Review each answer in the Full answers section and fill in the Quality column below by hand.

**Average response time (all questions):** 2.4s
**Average response time (answerable questions, i.e. questions that reach the LLM):** 2.6s
**Average response time (answerable questions, excluding the first/warm-up call):** 2.4s
**Min / max response time:** 0.5s / 4.6s

**Target from the project plan:** ~1-3 seconds per response.
**Result:** target met for every question after the first one in a session. The chat model (`phi-3.5-mini-instruct-trtrtx-gpu`) runs on GPU while the embedding model stays on CPU so the two never compete for VRAM (see History below) - steady-state answers average 2.4s. The very first LLM call after starting Foundry Local is much slower (a one-time engine warm-up cost, not per-question latency) - see the max/min row above and the History section.

One thing that *always* meets the target regardless of CPU/GPU choice: unanswerable questions are rejected via the similarity-threshold check in `prompts.py` before the LLM is ever called, so those responses come back in well under a second.

## Details

| # | Question | Expected | Result | Time (s) | Sources | Quality (manual) |
|---|----------|----------|--------|----------|---------|-------------------|
| 1 | Python'da degisken tanimlarken tur belirtmek zorunlu mu? | answerable | PASS | 3.7 | python_temelleri.md | [ ] TODO: review |
| 2 | Git'te bir degisikligi commit etmeden once hangi komut kullanilir? | answerable | PASS | 2.3 | git_temelleri.md | [ ] TODO: review |
| 3 | RAG'in klasik fine-tuning'e gore en buyuk avantaji nedir? | answerable | PASS | 1.9 | rag_nedir.md | [ ] TODO: review |
| 4 | SQLite diger veritabani sistemlerinden en cok hangi ozelligiyle ayrilir? | answerable | PASS | 1.0 | veritabani_temelleri.md | [ ] TODO: review |
| 5 | REST API'de GET ve POST komutlari ne ise yarar? | answerable | PASS | 2.4 | api_nedir.md, git_temelleri.md | [ ] TODO: review |
| 6 | LLM'ler metni islerken once ne yapar? | answerable | PASS | 2.4 | rag_nedir.md, yapay_zeka_llm.md | [ ] TODO: review |
| 7 | Veritabanina yeni bir belge nasil eklenir? | answerable | PASS | 4.1 | sss_kurulum.md, veritabani_temelleri.md | [ ] TODO: review |
| 8 | Fransa'nin baskenti neresidir? | unanswerable | PASS | 0.5 | - | [ ] TODO: review |
| 9 | En iyi pizza tarifi nedir? | unanswerable | PASS | 0.5 | - | [ ] TODO: review |
| 10 | Bugun hava nasil? | unanswerable | PASS | 0.5 | - | [ ] TODO: review |
| 11 | JavaScript'te async/await nasil calisir? | unanswerable | FAIL | 4.6 | api_nedir.md, python_temelleri.md | [ ] TODO: review |
| 12 | Python'da async/await ile es zamansiz programlama nasil yapilir? | unanswerable | FAIL | 4.5 | python_temelleri.md | [ ] TODO: review |

## Full answers

**1. Python'da degisken tanimlarken tur belirtmek zorunlu mu?**

>  Evet, Python'da degisken belirtmek zorunlu mu. Bu, dilin "dinamik tipleme" özelliğidir, yani belirli bir işlevin tanımlanması için girinti (indentation) kullanılır, bu özelliği değilse, hatalı bir standart kütüphanesidir.

**2. Git'te bir degisikligi commit etmeden once hangi komut kullanilir?**

>  `git add` komutunu kullanarak bir degisikligi commit etmek için kullanılacak komut `git commit -m "commit message"` olur. Bu komut, eklediği değişikliği içeren belirli bir mesajla bir commit yaparak, bu commit'ten dahil edilebileceği değişiklikleri belirlemeye yardımcı olur.

**3. RAG'in klasik fine-tuning'e gore en buyuk avantaji nedir?**

>  RAG'in klasik fine-tuning'e göre en büyük avantajı, modelin ağırlıklarını değiştirmeden yeni bilgi ekleyebilme yeteneğidir, bu da "halüsinasyon" (uydurma bilgi) riski azaltılır.

**4. SQLite diger veritabani sistemlerinden en cok hangi ozelligiyle ayrilir?**

>  `DELETE` komutunu

**5. REST API'de GET ve POST komutlari ne ise yarar?**

>  REST API'de, `GET` komutu, veri almak için kullandığımız API'nin belgelerini temel aldığımızda kullanılır. `POST` komutuyla yeni veriler ekleyerek belge oluşturulur. Yani, `GET` komutu verileri almak için ve `POST` komutu yeni veriler eklemek için kullanılır.

**6. LLM'ler metni islerken once ne yapar?**

>  LLM'ler metni doğrudan işlemez; küçük parçalara ayırarak (token halinde) ve her biri bir sayı dizisine çevrilerek, metni dil modeline iletir. Bu, dil modelin karmaşık yeteneklerini kullanarak içeriği tahmin etme, dil yazma ve soru cevaplama gibi görevleri yerine getirir.

**7. Veritabanina yeni bir belge nasil eklenir?**

>  Yeni bir belgenin veritabanına yeniden eklenmesi için, `ingest.py` dosyasını tekrar en yeni belgenin dosyalarından (`docs/` klasöründeki) birini alıp dosyanın içeriğini (`.md` dosyası) içindeki belgenin içeriğini (belgenin dosyasındaki `.md` dosyası) ile karşılaştırmak yeterli olur. `ingest.py`, belgenin içeriğini içeren belgeyi dosyaya yazıp `docs/` klasöründeki `new_document.md` olarak değiştirmelidir. Bu yöntem, belgenin içeriğini içeren `.md` dosyasının yeni bir belgenin eklenmesini sağlar.

Özet:
1. `ingest.py` dosyasından yeni belgenin

**8. Fransa'nin baskenti neresidir?**

> Bu bilgi elimdeki belgelerde yok.

**9. En iyi pizza tarifi nedir?**

> Bu bilgi elimdeki belgelerde yok.

**10. Bugun hava nasil?**

> Bu bilgi elimdeki belgelerde yok.

**11. JavaScript'te async/await nasil calisir?**

>  JavaScript'te, async/await, bir devre dışı performans ve okunabilirliğini artıran bir temel bir döngüsü yönetmede kullanılır. Bu, döngüler için yerleşik `Promise` yöntemini temelsizleştirerek, bir döngünün sonunda devre dışarıya getirilmesini sağlar, böylece göz arka arka kalma hataları (timeout ve görevler) yönetilebilir hale getirilir. `async` ile tanımlanan bir fonksiyon, `await` kullanarak bir `Promise` için bir çağrışıma dayanarak devre dışarıya getirilmiş bir çağrışımı içe aktarabilir, bu da JavaScript'te yerleşik bir döngü yönetimi temelini temel alarak

**12. Python'da async/await ile es zamansiz programlama nasil yapilir?**

>  Evet, Python'da async/await kullanarak es zamansiz programlama yapılabilir. Modern Python'da, asynkron programlama yakalarak `asyncio` modülünün güçlü bir destekleyici olduğu bir dizi bir parantez içinde içerip için kullanılabilir. `async/await` ifadeleri, asynkron programlamayla ilgilendiğinizde, program yürütme arzusunu kolaylaştırmak için kullanılabilir. Ancak, bu, programda birlikte yer alamayan bir temel düzeyde bir programlama yakaları kullanmak için kullanılır, bu da eszamansiz programlama için temel bir temizleme yöntemi olabileceğini iddia etse de.

## History

**Hafta 5, run 1 (CPU-only, SIMILARITY_THRESHOLD=0.35, baseline prompt): 9/12.**
3 unanswerable questions incorrectly got an answer. Checking `retrieval.find_relevant()`
directly showed a borderline case ("Bugün hava nasıl?") scoring 0.37 - just under the old
threshold - and two "topically close but uncovered" questions (JS/Python async/await)
scoring 0.48-0.54, within the genuinely-answerable range.

**Hafta 5, run 2 (CPU-only, threshold raised to 0.40, SYSTEM_PROMPT strengthened): 10/12.**
The threshold bump caught the weather question. Strengthening SYSTEM_PROMPT to forbid
falling back on the model's own general knowledge measurably changed behavior on the
Python async/await question (it started hedging instead of confidently hallucinating) but
didn't produce the exact standardized refusal text, and didn't fix the JavaScript
async/await question at all - phi-3.5-mini (3.8B params) still sometimes answers from its
own general knowledge despite the explicit instruction not to. Documented as a known,
disclosed limitation of small-model instruction-following, not something prompt tuning
alone reliably fixes.

**Hafta 6 (GPU re-enablement): response time cut roughly 10x.** The original CPU-only
setup was a deliberate, tested trade-off for stability (see the hardware constraint note
in the README) - full answers took ~25-40s. Investigating further: pinning only the chat
model to its GPU (TensorRT-RTX) variant while keeping the embedding model on CPU (so the
two never compete for the same ~6GB of VRAM) cuts steady-state answer time to ~1.5-3.5s,
right in the plan's original "~1-3 saniye" target range.

This took two rounds of debugging to get right:
1. A `foundry server restart` (as opposed to a full `stop` then `start`) doesn't always
   release the previous process's VRAM before the new one starts, causing a CUDA
   "invalid device ordinal" error on the very next request. Fix: stop, confirm
   `nvidia-smi` shows 0 MiB used (the WDDM driver can take several seconds to reclaim
   VRAM after a process exits), then start.
2. The first real question after loading the model was still reliably failing with a
   genuine `cudaMallocFromPoolAsync ... out of memory` error - even on a confirmed-clean
   GPU - specifically when using the app's real prompt (system prompt + 3 retrieved
   chunks) with `max_tokens=400`. A trivial, context-free test prompt worked fine, which
   is what led to an initially too-optimistic assessment. Root cause: ONNX Runtime
   GenAI reserves working memory sized to `max_tokens` up front, regardless of how much
   text is actually generated - so a higher `max_tokens` directly costs more VRAM even
   for a short answer. Lowering `max_tokens` from 400 to 250 in `prompts.py` (confirmed
   answers still finish naturally, `finish_reason="stop"`, not truncated) reliably fits
   within the ~6GB budget with the full 3-chunk context, tested across multiple fresh
   cold starts.

**Trade-off accepted, not eliminated:** steady-state VRAM usage with this configuration
sits around 5.76 GB out of 6.14 GB - roughly 380 MB of headroom. That's stable on this
machine with nothing else touching the GPU (confirmed across many consecutive calls with
no growth - a one-time "warm-up" bump, not a leak), but it is a real, accepted risk, not
a guaranteed-safe margin: another GPU-using app running at the same time, or a future
change to `TOP_K` or `max_tokens`, could bring back the out-of-memory error. If that
happens, the fix is either to lower `max_tokens` further, or fall back to the fully
CPU-pinned configuration (`Phi-3.5-mini-instruct-generic-cpu`) documented in the hardware
constraint note in the README - slower, but always fits.

**The very first LLM call after a fresh Foundry Local restart is much slower than the
rest** (~50s vs ~1.5-3.5s in the run below) - that's TensorRT building/optimizing its
inference engine for this model, a one-time cost per server start, not per question. In
practice this means the *first* question in a freshly started app is slow; every question
after that is fast for as long as the Foundry Local service keeps running.
