import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Professor Nova AI",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------
# LOAD FAQ
# -----------------------------------

faq = pd.read_csv("faq.csv")

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #050816,
        #0f172a,
        #111827
    );
}

.main-title{
    text-align:center;
    padding:20px;
}

.main-title h1{
    color:#00e5ff;
    font-size:55px;
}

.main-title p{
    color:#cbd5e1;
    font-size:20px;
}

.orb{
    text-align:center;
    font-size:90px;
    animation: pulse 2s infinite;
}

@keyframes pulse{
    0%{transform:scale(1);}
    50%{transform:scale(1.08);}
    100%{transform:scale(1);}
}

.user-card{
    background:#7c3aed;
    color:white;
    padding:15px;
    border-radius:20px;
    margin-top:10px;
    margin-bottom:10px;
    text-align:right;
    font-size:18px;
}

.bot-card{
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    color:white;
    padding:20px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.2);
    margin-bottom:20px;
    font-size:18px;
}

.info-card{
    background:rgba(255,255,255,0.08);
    color:white;
    padding:20px;
    border-radius:20px;
    margin-top:20px;
}

.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("""
<div class="orb">
🔮
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
<h1>Professor Nova AI</h1>
<p>Your Personal Learning Assistant</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("🎓 Professor Nova")

    st.success("System Online")

    st.write("---")

    st.subheader("📚 Subjects")

    st.write("""
    • Artificial Intelligence
    
    • Machine Learning
    
    • Python
    
    • NLP
    
    • SQL
    
    • Database
    """)

    st.write("---")

    st.subheader("⚡ Features")

    st.write("""
    ✔ Instant Answers
    
    ✔ AI Search
    
    ✔ FAQ Knowledge Base
    
    ✔ Modern Interface
    """)

# -----------------------------------
# INPUT
# -----------------------------------

question = st.text_input(
    "Ask Question",
    placeholder="Example: What is Machine Learning?"
)

# -----------------------------------
# FIND ANSWER
# -----------------------------------

if st.button("🚀 Ask Nova"):

    if question.strip():

        questions = faq["Question"].tolist()

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            questions + [question]
        )

        similarity = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        )

        score = similarity.max()

        index = similarity.argmax()

        if score < 0.20:

            answer = """
Sorry Student,

I couldn't find a matching answer in my knowledge base.

Please try another question.
"""

        else:

            answer = faq.iloc[index]["Answer"]

        st.session_state.chat_history.append(
            (question, answer)
        )

# -----------------------------------
# CHAT HISTORY
# -----------------------------------

for user_msg, bot_msg in reversed(
        st.session_state.chat_history):

    st.markdown(
        f"""
        <div class="user-card">
        👨‍🎓 {user_msg}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="bot-card">
        <h3>🎓 Professor Nova Says:</h3>
        <hr>
        {bot_msg}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------
# WELCOME PANEL
# -----------------------------------

if len(st.session_state.chat_history) == 0:

    st.markdown("""
    <div class="info-card">
    <h2>👋 Welcome Student</h2>

    Ask any question from the FAQ knowledge base.

    Examples:

    • What is AI?

    • What is Machine Learning?

    • What is Python?

    • What is NLP?

    • What is SQL?
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("""
<div class="footer">
<hr>
Professor Nova AI • Powered by Python + Streamlit + NLP
</div>
""", unsafe_allow_html=True)