# prompts.py
# System prompt and answer_query(): combines retrieval results with the
# chat model to produce a grounded, cited answer (the "generation" step of
# the RAG pipeline).

from config import (
    CHAT_MODEL_ALIAS,
    SIMILARITY_THRESHOLD,
    TOP_K,
    ensure_model_ready,
    get_openai_client,
)
from retrieval import get_top_chunks

# Rules the model must follow on every request.
#
# Kept in Turkish: the documents and user questions are Turkish, and the
# "[Kaynak: ...]" citation format the model is told to produce needs to
# match.
SYSTEM_PROMPT = """Sen, kullanicinin kendi belgelerine dayanarak soru cevaplayan bir asistansin.

Kurallar:
1. SADECE asagida sana verilen "Belgeler" bolumundeki CUMLELERE dayanarak cevap ver. Kendi genel bilgini KULLANMA.
2. Belgeler soruyu tam olarak cevaplamiyorsa - konuyla ilgili gorunse bile sorunun cevabini icermiyorsa - tahmin etme veya uydurma; acikca "Bu bilgi elimdeki belgelerde yok." de. Kismen ilgili bir belge parcasi gormek, o parcanin soruyu cevapladigi anlamina gelmez.
3. Cevabinin sonunda hangi belge(ler)e dayandigini belirt, ornegin: "(Kaynak: git_temelleri.md)"
4. Kisa ve net cevap ver, gereksiz uzatma."""


def _build_context_text(chunks: list[dict]) -> str:
    """Format retrieved chunks with their sources into one text block for the prompt.

    Uses "Kaynak:" (Turkish) to match SYSTEM_PROMPT's citation format.
    """
    parts = [f"[Kaynak: {chunk['source']}]\n{chunk['content']}" for chunk in chunks]
    return "\n\n---\n\n".join(parts)


def answer_query(question: str, top_k: int = TOP_K) -> dict:
    """Answer a question: retrieve relevant chunks, then generate a grounded answer.

    Returns {"answer": str, "sources": list[str]}.
    """
    relevant_chunks = get_top_chunks(question, top_k=top_k)

    if not relevant_chunks:
        return {
            "answer": "The database has no documents yet. Run 'python ingest.py' first.",
            "sources": [],
        }

    # Below the threshold, the question isn't covered by the documents -
    # answer directly without calling the LLM.
    best_similarity = relevant_chunks[0]["similarity"]
    if best_similarity < SIMILARITY_THRESHOLD:
        return {
            "answer": "Bu bilgi elimdeki belgelerde yok.",
            "sources": [],
        }

    context = _build_context_text(relevant_chunks)
    user_message = f"Belgeler:\n{context}\n\nSoru: {question}"

    ensure_model_ready(CHAT_MODEL_ALIAS)
    client = get_openai_client()

    response = client.chat.completions.create(
        model=CHAT_MODEL_ALIAS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        # 250, not 400: the GPU (TensorRT-RTX) chat model reserves VRAM
        # sized to max_tokens up front. 400 ran out of memory on a cold
        # start with full 3-chunk context; 250 fits and still lets answers
        # finish naturally.
        max_tokens=250,
        temperature=0.2,
    )

    sources = sorted({chunk["source"] for chunk in relevant_chunks})

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
    }


if __name__ == "__main__":
    # Quick manual test: python prompts.py
    result = answer_query("RAG nedir?")
    print(result["answer"])
    print("Sources:", ", ".join(result["sources"]))
