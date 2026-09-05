# app.py
# Streamlit chat interface.
#
# Color theme is applied in two layers: .streamlit/config.toml sets
# Streamlit's built-in widget colors, and the CSS block below handles what
# the theme system doesn't cover (chat bubble borders, source label color).

import streamlit as st

from prompts import answer_query

# Color palette (chosen by the user):
COLOR_DARK_BLUE = "#3368A0"    # title, buttons, assistant name
COLOR_LIGHT_BLUE = "#66A3BF"   # source citation, accents
COLOR_BORDER = "#C8DFDB"       # borders, thin dividing lines
COLOR_BACKGROUND = "#F2EFE7"   # overall page background

st.set_page_config(
    page_title="Document Assistant",
    page_icon="📄",
    layout="centered",
)

# Extra CSS for details config.toml doesn't cover. Plain borders instead of
# rounded/gradient chat-bubble styling, to avoid a generic "AI chatbot" look.
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {COLOR_BACKGROUND};
        }}
        h1, h1 span {{
            color: {COLOR_DARK_BLUE} !important;
            font-weight: 600;
        }}
        [data-testid="stChatMessage"] {{
            border: 1px solid {COLOR_BORDER};
            border-radius: 6px;
            background-color: white;
        }}
        .source-label {{
            color: {COLOR_LIGHT_BLUE};
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }}
        [data-testid="stChatInput"] {{
            border-color: {COLOR_BORDER};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Document Assistant")
st.caption("Answers questions based on your own documents. Runs completely offline.")

# Chat history persists across reruns within a session.
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About")
    st.write(
        "This assistant answers based on the documents in the `docs/` folder. "
        "The source is always shown below each answer."
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# Streamlit reruns the whole script on every interaction, so past messages
# must be redrawn each time.
for message in st.session_state.messages:
    avatar = "📄" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        if message.get("sources"):
            sources = ", ".join(message["sources"])
            st.markdown(f'<div class="source-label">Source: {sources}</div>', unsafe_allow_html=True)

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.write(question)

    with st.chat_message("assistant", avatar="📄"):
        with st.spinner("Searching documents and preparing an answer..."):
            result = answer_query(question)
        st.write(result["answer"])
        if result["sources"]:
            sources = ", ".join(result["sources"])
            st.markdown(f'<div class="source-label">Source: {sources}</div>', unsafe_allow_html=True)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        }
    )
