import streamlit as st
from googletrans import Translator

translator = Translator()

# Page Configuration
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.title {
    text-align: center;
    color: #1f4e79;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}

.stTextArea textarea {
    border-radius: 10px;
}

.result-box {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 10px;
    font-size: 20px;
    color: #2e7d32;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<p class="title">🌍 AI Language Translator</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Translate text instantly into multiple languages</p>',
    unsafe_allow_html=True
)

# Input
text = st.text_area(
    "✍ Enter Text",
    height=150,
    placeholder="Type your text here..."
)

# Language Selection
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "📥 Source Language",
        ["English", "Hindi", "Marathi"]
    )

with col2:
    target_lang = st.selectbox(
        "📤 Target Language",
        ["English", "Hindi", "Marathi"]
    )

# Translate Button
if st.button("🚀 Translate"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        translated = translator.translate(
            text,
            src=source_lang,
            dest=target_lang
        )

        st.markdown("### ✅ Translation Result")

        st.markdown(
            f"""
            <div class="result-box">
            {translated.text}
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ using Python & Streamlit</center>",
    unsafe_allow_html=True
)