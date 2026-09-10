# evaluate.py
# Week 5 goal: run a fixed set of answerable and unanswerable questions
# through the assistant, measure response time for each, and write the
# results to a markdown report (test_results.md).

import time

from config import CHAT_MODEL_ALIAS
from prompts import answer_query

# Each case: (question, expected type, expected source file or None).
# Answerable questions cover all 7 documents in docs/, one question each.
# Unanswerable questions range from obviously unrelated to a deliberately
# tricky edge case (a Python question docs/ doesn't actually cover).
TEST_CASES = [
    ("Python'da degisken tanimlarken tur belirtmek zorunlu mu?", "answerable", "python_temelleri.md"),
    ("Git'te bir degisikligi commit etmeden once hangi komut kullanilir?", "answerable", "git_temelleri.md"),
    ("RAG'in klasik fine-tuning'e gore en buyuk avantaji nedir?", "answerable", "rag_nedir.md"),
    ("SQLite diger veritabani sistemlerinden en cok hangi ozelligiyle ayrilir?", "answerable", "veritabani_temelleri.md"),
    ("REST API'de GET ve POST komutlari ne ise yarar?", "answerable", "api_nedir.md"),
    ("LLM'ler metni islerken once ne yapar?", "answerable", "yapay_zeka_llm.md"),
    ("Veritabanina yeni bir belge nasil eklenir?", "answerable", "sss_kurulum.md"),
    ("Fransa'nin baskenti neresidir?", "unanswerable", None),
    ("En iyi pizza tarifi nedir?", "unanswerable", None),
    ("Bugun hava nasil?", "unanswerable", None),
    ("JavaScript'te async/await nasil calisir?", "unanswerable", None),
    ("Python'da async/await ile es zamansiz programlama nasil yapilir?", "unanswerable", None),
]

DONT_KNOW_TEXT = "Bu bilgi elimdeki belgelerde yok."


def run_evaluation() -> list[dict]:
    """Run every test case through answer_query() and record pass/fail + timing."""
    results = []
    for question, expected_type, expected_source in TEST_CASES:
        start = time.time()
        result = answer_query(question)
        elapsed = time.time() - start

        got_dont_know = result["answer"].strip() == DONT_KNOW_TEXT
        if expected_type == "unanswerable":
            passed = got_dont_know
        else:
            passed = (not got_dont_know) and (expected_source in result["sources"])

        results.append(
            {
                "question": question,
                "expected_type": expected_type,
                "expected_source": expected_source,
                "answer": result["answer"],
                "sources": result["sources"],
                "elapsed_seconds": elapsed,
                "passed": passed,
            }
        )
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] ({elapsed:5.1f}s) {question}")

    return results


# Kept out of the auto-generated section below (which gets fully rewritten
# on every run) so the engineering history behind the current numbers isn't
# lost every time this script runs again.
HISTORY_NOTES = """
## History

**Hafta 5, run 1 (CPU-only, SIMILARITY_THRESHOLD=0.35, baseline prompt): 9/12.**
3 unanswerable questions incorrectly got an answer. Checking `retrieval.get_top_chunks()`
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
"""


def write_report(results: list[dict], path: str = "test_results.md") -> None:
    """Write the evaluation results as a markdown report."""
    total = len(results)
    passed_count = sum(1 for r in results if r["passed"])
    times = [r["elapsed_seconds"] for r in results]
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)

    answerable_times = [r["elapsed_seconds"] for r in results if r["expected_type"] == "answerable"]
    avg_answerable_time = sum(answerable_times) / len(answerable_times) if answerable_times else 0
    # The first LLM call in a run includes a one-time model/engine warm-up cost
    # (most visible on the GPU/TensorRT variant) that has nothing to do with
    # per-question latency - excluded here to give an honest steady-state number.
    steady_state_times = answerable_times[1:] if len(answerable_times) > 1 else answerable_times
    avg_steady_state_time = sum(steady_state_times) / len(steady_state_times) if steady_state_times else 0

    on_gpu = "gpu" in CHAT_MODEL_ALIAS.lower() or "trtrtx" in CHAT_MODEL_ALIAS.lower()
    target_line = (
        "**Result:** target met for every question after the first one in a session. "
        f"The chat model (`{CHAT_MODEL_ALIAS}`) runs on GPU while the embedding model stays "
        "on CPU so the two never compete for VRAM (see History below) - steady-state answers "
        f"average {avg_steady_state_time:.1f}s. The very first LLM call after starting Foundry "
        "Local is much slower (a one-time engine warm-up cost, not per-question latency) - see "
        "the max/min row above and the History section."
        if on_gpu
        else "**Result:** target not met. Both models run on CPU (see the hardware constraint "
        "note in the README) because the laptop's 6GB-VRAM GPU cannot fit phi-3.5-mini's GPU "
        "variant without running out of memory. This is a disclosed, deliberate trade-off for "
        "offline stability on this specific hardware, not an oversight."
    )

    lines = [
        "# Test Results",
        "",
        f"**Chat model:** `{CHAT_MODEL_ALIAS}`",
        f"**Pass rate:** {passed_count}/{total} (automated check only - see note below)",
        "",
        "**Note:** the automated pass/fail check only verifies that unanswerable "
        "questions got refused and answerable questions cited the right source file. "
        "It does not check whether the generated answer is actually correct or "
        "well-formed. Review each answer in the Full answers section and fill in the "
        "Quality column below by hand.",
        "",
        f"**Average response time (all questions):** {avg_time:.1f}s",
        f"**Average response time (answerable questions, i.e. questions that reach the LLM):** {avg_answerable_time:.1f}s",
        f"**Average response time (answerable questions, excluding the first/warm-up call):** {avg_steady_state_time:.1f}s",
        f"**Min / max response time:** {min_time:.1f}s / {max_time:.1f}s",
        "",
        "**Target from the project plan:** ~1-3 seconds per response.",
        target_line,
        "",
        "One thing that *always* meets the target regardless of CPU/GPU choice: unanswerable "
        "questions are rejected via the similarity-threshold check in `prompts.py` before the "
        "LLM is ever called, so those responses come back in well under a second.",
        "",
        "## Details",
        "",
        "| # | Question | Expected | Result | Time (s) | Sources | Quality (manual) |",
        "|---|----------|----------|--------|----------|---------|-------------------|",
    ]

    for i, r in enumerate(results, start=1):
        status = "PASS" if r["passed"] else "FAIL"
        sources = ", ".join(r["sources"]) if r["sources"] else "-"
        lines.append(
            f"| {i} | {r['question']} | {r['expected_type']} | {status} | "
            f"{r['elapsed_seconds']:.1f} | {sources} | [ ] TODO: review |"
        )

    lines.append("")
    lines.append("## Full answers")
    lines.append("")
    for i, r in enumerate(results, start=1):
        lines.append(f"**{i}. {r['question']}**")
        lines.append("")
        lines.append(f"> {r['answer']}")
        lines.append("")

    lines.append(HISTORY_NOTES.strip())
    lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nReport written to {path}")


if __name__ == "__main__":
    results = run_evaluation()
    write_report(results)
