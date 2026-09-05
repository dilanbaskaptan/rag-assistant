# main.py
# Smoke test: send one question to phi-3.5-mini via Foundry Local and print
# the response.
#
# Foundry Local exposes an OpenAI-compatible REST API on localhost, so the
# official 'openai' client works unmodified - only base_url points at the
# local machine instead of OpenAI's cloud. Connection logic is in config.py.

from config import CHAT_MODEL_ALIAS, ensure_model_ready, get_openai_client


def main() -> None:
    ensure_model_ready(CHAT_MODEL_ALIAS)
    client = get_openai_client()

    # Turkish on purpose: the assistant answers Turkish questions about
    # Turkish documents, so this is a realistic smoke test.
    response = client.chat.completions.create(
        model=CHAT_MODEL_ALIAS,
        messages=[
            {"role": "user", "content": "Merhaba! Kendini tek cumlede tanit."},
        ],
        max_tokens=100,
    )

    print("\nModel's response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
