# Document Assistant

An offline, local RAG (Retrieval-Augmented Generation) chatbot that answers questions based on your own documents — course notes, manuals, FAQs — using [Microsoft Foundry Local](https://github.com/microsoft/Foundry-Local). Built as part of the Microsoft AI Innovators program.

No internet connection is required once the models are downloaded. Everything — the language model, the embedding model, and the document database — runs on your own machine.

## The problem

Students and professionals accumulate a pile of notes, manuals, and FAQs they rarely search efficiently. Cloud AI assistants can help, but sending private documents to a third-party API isn't always acceptable, and isn't always available offline. This project answers questions about a personal document collection entirely on-device.

## Architecture

```
                    ┌─────────────┐
  docs/*.md ──────► │  ingest.py  │ ── splits into chunks, embeds each one
                    └──────┬──────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  SQLite database │  (documents table: content, embedding, source)
                  └────────┬─────────┘
                           │
   question ──────► retrieval.py ──── cosine similarity search (find_relevant)
                           │
                           ▼
                  top-k relevant chunks
                           │
                           ▼
                    prompts.py ──── builds prompt, calls the chat model
                           │
                           ▼
                  answer + cited sources
                           │
                           ▼
                    app.py (Streamlit UI)
```

This is the standard two-step RAG pattern:

1. **Retrieval** — the question is turned into an embedding vector (`qwen3-embedding-0.6b`), compared against every stored chunk's embedding with cosine similarity, and the top-k most relevant chunks are returned (`retrieval.py`).
2. **Generation** — the retrieved chunks are placed into a prompt together with the question and sent to a chat model (`phi-3.5-mini`), which is instructed to answer only from those chunks and to cite its source (`prompts.py`).

Both models run locally through **Foundry Local**, which exposes an OpenAI-compatible REST API on `127.0.0.1`. This means the official `openai` Python library works unmodified — only the `base_url` points at the local machine instead of OpenAI's cloud.

## Tech stack

| Layer | Choice |
|---|---|
| Language model | `phi-3.5-mini` (via Foundry Local) |
| Embedding model | `qwen3-embedding-0.6b` (via Foundry Local) |
| Retrieval | Cosine similarity over stored embedding vectors |
| Database | SQLite (`rag_assistant.db`) |
| UI | Streamlit |
| Language | Python |

## Project structure

```
rag-assistant/
├── main.py          # Week 1 "Hello Model" smoke test
├── app.py            # Streamlit chat interface
├── ingest.py          # Reads docs/, chunks, embeds, saves to SQLite
├── retrieval.py       # Embeddings + cosine similarity + find_relevant()
├── database.py        # SQLite access layer
├── prompts.py          # System prompt + answer_query()
├── config.py           # Settings + Foundry Local connection helpers
├── evaluate.py         # Test suite (answerable/unanswerable questions, timing)
├── docs/               # Your source documents (.md)
├── test_results.md    # Generated evaluation report (see below)
├── requirements.txt
└── .streamlit/config.toml   # Color theme
```

## Setup

**Prerequisites:**
- Python 3.10+
- [Foundry Local](https://github.com/microsoft/Foundry-Local) installed and available as the `foundry` command

**Install dependencies:**

```bash
pip install -r requirements.txt
```

Foundry Local downloads the two models (~2.1 GB and ~500 MB) the first time they're used — this happens automatically, no manual download step needed. A GPU with at least ~6 GB of free VRAM is recommended for a fast chat model (see [Design decisions](#design-decisions)); without a capable GPU, edit `CHAT_MODEL_ALIAS` in `config.py` to the CPU variant instead (slower, but requires no VRAM).

## Usage

**1. Add your documents.** Drop `.md` files into `docs/`. A handful of sample documents (Python, Git, RAG, SQL, API, and LLM basics, plus a project FAQ) are included so the app works out of the box.

**2. Build the knowledge base:**

```bash
python ingest.py
```

This splits every document in `docs/` into overlapping chunks, computes an embedding for each, and stores them in `rag_assistant.db`. Re-run this any time `docs/` changes — it rebuilds the database from scratch each time, so there's never stale or duplicate data.

**3. Run the app:**

```bash
streamlit run app.py
```

This opens a chat interface in your browser. Ask a question; the assistant retrieves the most relevant chunks and answers based only on them, citing its source underneath.

**4. (Optional) Run the evaluation suite:**

```bash
python evaluate.py
```

Runs a fixed set of answerable and unanswerable test questions and writes `test_results.md` with pass/fail results and response times.

## Design decisions

**Streamlit over Flask.** The project's original plan called for a Flask backend with a hand-built HTML/CSS/JS frontend. Partway through, the plan changed to Streamlit — it gets a working chat UI (message bubbles, input box, session state) without writing any HTML/CSS/JS by hand, at the cost of some fine-grained layout control. The color theme (`#3368A0` / `#66A3BF` / `#C8DFDB` / `#F2EFE7`) is applied through Streamlit's native `.streamlit/config.toml` theme system, with a small amount of extra CSS in `app.py` for details the theme system doesn't cover (chat bubble borders, the source-citation label color).

**The chat model runs on GPU, the embedding model runs on CPU.** The development laptop's GPU (RTX 3060, laptop variant) has only 6 GB of VRAM — not enough to run both models on the GPU at once (`phi-3.5-mini`'s GPU/TensorRT-RTX variant alone needs roughly 2.4 GB of transient working memory beyond its 2.1 GB of weights). Splitting the two models across CPU and GPU instead of running both on one device cut the average answer time from ~25-40s down to ~1.5-3.5s, right around the plan's original "~1-3 saniye" target.

This split is a deliberately accepted risk, not a guaranteed-safe configuration: steady-state VRAM usage settles at roughly 5.76 GB out of 6.14 GB (~380 MB of headroom), confirmed stable across many consecutive questions in testing but with no safety margin to spare for another GPU-using app running at the same time. One specific gotcha worth knowing if you ever touch `max_tokens` in `prompts.py`: ONNX Runtime GenAI reserves GPU working memory sized to `max_tokens` up front, regardless of how much text actually gets generated — `max_tokens=400` reliably ran out of memory with a full 3-chunk context, `max_tokens=250` doesn't. If the OOM error comes back (e.g. after increasing `max_tokens` or `TOP_K`), the documented fallback is switching `CHAT_MODEL_ALIAS` in `config.py` back to `Phi-3.5-mini-instruct-generic-cpu` — slower, but always fits. The full debugging story is in `test_results.md`'s History section.

**A similarity threshold guards against hallucinated answers.** Small language models don't always reliably follow "say so if you don't know" instructions. Rather than relying on the prompt alone, `answer_query()` in `prompts.py` checks the top retrieved chunk's cosine similarity against `SIMILARITY_THRESHOLD` (0.40) before ever calling the LLM. Below that threshold, the question is treated as unrelated to the documents and answered directly with "Bu bilgi elimdeki belgelerde yok." — faster, and not dependent on model behavior.

**Chunking preserves paragraph boundaries.** `ingest.py` splits documents into ~500-character chunks along paragraph breaks (not mid-sentence), with a 50-character overlap between consecutive chunks so context isn't lost at the boundary.

**The RAG conversation itself stays in Turkish.** The source documents in `docs/` are Turkish course notes, and the system prompt, the citation format, and the "I don't know" response are all Turkish to match. Everything else — code, comments, the Streamlit UI, console output — is in English.

## Known limitations

Documented in detail in `test_results.md` (generated by `evaluate.py`); summary:

- **The first question after starting the app is much slower than the rest (~50s vs ~1.5-3.5s).** That's a one-time cost per Foundry Local restart — the GPU/TensorRT execution provider builds and optimizes its inference engine on the first real call. Every question after that in the same session is fast. If the GPU split above isn't usable on a given machine (e.g. a GPU with less VRAM), falling back to CPU for both models makes every answer ~25-40s instead, with no first-call spike.
- **The GPU/CPU split has a real, accepted stability risk** — see the design decision above and `test_results.md`'s History section for the full debugging story (a restart-timing gotcha and a `max_tokens`-vs-VRAM gotcha both had to be worked around).
- **The similarity threshold can't catch every false positive.** A question that shares vocabulary/topic with a document but isn't actually answered by it (e.g. asking about `async/await` in JavaScript against a Python-basics document) can score similarly to genuinely answerable questions. This has to be handled by the system prompt at generation time instead — which helps, but phi-3.5-mini (3.8B parameters) still occasionally falls back on its own general knowledge instead of admitting the documents don't cover something. This is a known weakness of small models' instruction-following, not a bug specific to this project.
- **Turkish output quality varies.** phi-3.5-mini's Turkish is decent but not perfect, and occasionally produces slightly awkward phrasing.

## What was learned

- Foundry Local's Python SDK has two very different generations: an older, simple `FoundryLocalManager` + OpenAI-client pattern (used in most public tutorials) and a newer, much lower-level native-binding SDK (what actually ships today). Driving the already-running `foundry` CLI service directly via its OpenAI-compatible REST API turned out to be the simplest, most reliable integration path.
- Small local models need real guardrails, not just prompt instructions — the similarity-threshold check ended up doing more reliable work than the system prompt alone for the "say I don't know" behavior.
- Hardware constraints (6 GB VRAM) are a first-class design input for local AI apps, not an afterthought — they directly decided the CPU-vs-GPU trade-off and the resulting latency budget.
- "It worked in my test" isn't the same as "it's reliable." An initial GPU speedup looked stable after several successful calls, but that testing had accidentally always run on an already-warmed-up engine — the real failure mode only showed up on a genuine cold start with the app's actual (longer) prompt. Isolating the actual variable (`max_tokens`, not context length as first suspected) took deliberately re-testing from a confirmed-clean GPU state multiple times rather than trusting one success.
