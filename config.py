# config.py
# Central settings and the Foundry Local connection helpers shared by the
# other modules.

import json
import subprocess

import openai

# Chat model variant. Pinned to GPU; embedding model below stays on CPU so the two don't compete for VRAM.
CHAT_MODEL_ALIAS = "phi-3.5-mini-instruct-trtrtx-gpu"

# Embedding model variant. CPU variant - same VRAM constraint as above, and
# fast enough on CPU since the model is small.
EMBEDDING_MODEL_ALIAS = "qwen3-embedding-0.6b-generic-cpu"

# Approximate character length of each chunk when splitting documents.
CHUNK_SIZE = 500

# Overlapping characters between consecutive chunks, to preserve context.
CHUNK_OVERLAP = 50

# Number of most-relevant chunks fetched from the database per question.
TOP_K = 3

# Below this score, a question is treated as unrelated to the documents and answered with "I don't know" without calling the LLM.
SIMILARITY_THRESHOLD = 0.40

# Path to the SQLite database file.
DATABASE_PATH = "rag_assistant.db"


def start_foundry_service() -> str:
    """Ensure the Foundry Local service is running and return its base URL.

    'foundry server start' is a no-op if already running.
    """
    subprocess.run(
        ["foundry", "server", "start"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    # Port can change on every start, so read it from the CLI instead of
    # hardcoding it.
    status = subprocess.run(
        ["foundry", "server", "status", "-o", "json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    info = json.loads(status.stdout)

    if not info.get("running") or not info.get("webUrls"):
        raise RuntimeError(
            "Could not start the Foundry Local service. Check its status with "
            "'foundry server status' in the terminal."
        )

    return info["webUrls"][0]


# Tracks which models have been checked/loaded in this process, so
# ensure_model_ready() doesn't re-run 'foundry model load' on every call.
_prepared_models: set[str] = set()


def ensure_model_ready(model_alias: str) -> None:
    """Download and load the model if needed. No-op if already prepared."""
    if model_alias in _prepared_models:
        return

    print(f"Preparing model '{model_alias}' (this may take a while on first run)...")
    result = subprocess.run(
        ["foundry", "model", "load", model_alias],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        print(f"Warning: failed to load model '{model_alias}': {result.stderr.strip()}")

    _prepared_models.add(model_alias)


# Cached after the first call, so get_openai_client() doesn't re-run
# 'foundry server start'/'status' on every request. If the Foundry service
# is restarted while the app is running, this URL goes stale - acceptable
# since restarting the service means restarting the app too.
_cached_base_url: str | None = None


def get_openai_client() -> openai.OpenAI:
    """Return an OpenAI client pointed at the local Foundry Local service."""
    global _cached_base_url
    if _cached_base_url is None:
        _cached_base_url = start_foundry_service()
    return openai.OpenAI(base_url=f"{_cached_base_url}/v1", api_key="not-needed")
