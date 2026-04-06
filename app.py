import streamlit as st
from src.rag_pipeline import ask_question

# Configure page
st.set_page_config(
    page_title="Sri Lanka Tourism Chatbot",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    /* Root colors - Sri Lanka inspired */
    :root {
        --primary-blue: #1e3c72;
        --primary-orange: #ff7a5c;
        --accent-green: #2ecc71;
        --light-gold: #f7b731;
        --bg-gradient-start: #0f2027;
        --bg-gradient-mid: #203a43;
        --bg-gradient-end: #2c5364;
    }

    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Global text */
    body {
        font-family: 'Poppins', sans-serif;
    }

    /* Title styling */
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #ff7a5c 0%, #f7b731 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Playfair Display', serif;
        font-size: 3em;
        margin-bottom: 5px;
        text-shadow: none;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .subtitle {
        text-align: center;
        background: linear-gradient(135deg, #2ecc71 0%, #00bcd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3em;
        margin-bottom: 40px;
        font-weight: 500;
        letter-spacing: 1px;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #ff7a5c;
        padding: 15px 20px;
        font-size: 1.05em;
        background-color: rgba(255, 255, 255, 0.95);
        color: #1e3c72;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 122, 92, 0.15);
    }

    .stTextInput > div > div > input:focus {
        border-color: #f7b731;
        box-shadow: 0 6px 25px rgba(255, 122, 92, 0.25);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff7a5c 0%, #f7b731 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 1.05em;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 6px 20px rgba(255, 122, 92, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(255, 122, 92, 0.4);
    }

    .stButton > button:active {
        transform: translateY(-1px);
    }

    /* Secondary buttons in answer actions */
    .stButton button {
        width: 100%;
        font-weight: 600;
    }

    /* Example questions buttons */
    .example-btn {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.2) 0%, rgba(0, 188, 212, 0.2) 100%);
        border: 2px solid #2ecc71;
        border-radius: 12px;
        padding: 14px 16px;
        margin: 8px 4px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-weight: 500;
        font-family: 'Poppins', sans-serif;
    }

    .example-btn:hover {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.4) 0%, rgba(0, 188, 212, 0.4) 100%);
        border-color: #00bcd4;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(46, 204, 113, 0.3);
    }

    /* Card styling */
    .answer-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.99) 0%, rgba(245, 252, 255, 0.99) 100%);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15), 0 0 1px rgba(255, 122, 92, 0.5);
        border-left: 7px solid #ff7a5c;
        border-top: 3px solid rgba(46, 204, 113, 0.4);
        border-right: 1px solid rgba(46, 204, 113, 0.15);
        border-bottom: 1px solid rgba(46, 204, 113, 0.15);
        animation: slideInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }

    .answer-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(255, 122, 92, 0.05) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Answer heading */
    .answer-card h3 {
        color: #ff7a5c;
        font-size: 1.6em;
        font-weight: 700;
        margin-bottom: 20px;
        margin-top: 0;
        font-family: 'Playfair Display', serif;
        letter-spacing: 1px;
        position: relative;
        z-index: 1;
    }

    .answer-card p {
        color: #1e3c72;
        line-height: 1.9;
        font-size: 1.1em;
        font-weight: 400;
        margin: 0;
        position: relative;
        z-index: 1;
        word-wrap: break-word;
        white-space: normal;
    }

    /* Success message */
    .stSuccess {
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.15) 0%, rgba(0, 188, 212, 0.15) 100%);
        border-left: 4px solid #2ecc71;
        padding: 15px;
    }

    /* Section headers */
    h2 {
        color: #ff7a5c;
        font-family: 'Playfair Display', serif;
        font-size: 2em;
        margin-top: 30px;
        margin-bottom: 20px;
        font-weight: 700;
    }

    h3 {
        color: #2ecc71;
        font-weight: 600;
        font-size: 1.3em;
    }

    /* Horizontal divider */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff7a5c, transparent);
        margin: 30px 0;
    }

    /* Sidebar styling */
    .sidebar .block-container {
        background: rgba(30, 60, 114, 0.1);
        border-radius: 15px;
        padding: 20px;
    }

    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(30, 60, 114, 0.1) 0%, rgba(46, 204, 113, 0.05) 100%);
        border-radius: 12px;
        border-left: 4px solid #2ecc71;
        padding: 15px;
    }

    /* Spinner animation */
    .stSpinner {
        text-align: center;
    }

    /* Text styling */
    .stMarkdown {
        font-family: 'Poppins', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Header section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1>🇱🇰 Sri Lanka Tourism Chatbot</h1>", unsafe_allow_html=True)
    st.markdown('<div class="subtitle">✨ Discover the Pearl of the Indian Ocean ✨</div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 About This Chatbot")
    st.info("🤖 **Your AI-Powered Travel Guide**\n\nAsk anything about Sri Lanka's amazing attractions, culture, travel tips, and hidden gems!")

    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. **Ask a Question** - Type or select from examples below
    2. **Get Instant Answers** - AI analyzes Sri Lanka tourism data
    3. **Learn More** - Get detailed, accurate information
    """)

    st.markdown("### 📍 Search Tips")
    st.markdown("""
    - Ask about specific places (beaches, mountains, temples)
    - Ask about activities and adventure sports
    - Ask about cultural experiences
    - Ask about best travel times
    """)

# Main content
# Create two columns for input
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "Ask a question about Sri Lanka Tourism:",
        placeholder="🔍 e.g., What are the best beaches in Sri Lanka?",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Ask", use_container_width=True)

# Example questions section with better styling
st.markdown("### 💡 Popular Questions")
st.markdown("*Click any question or type your own:*")

example_questions = [
    "🏖️ Best beaches in Sri Lanka?",
    "🗿 Tell me about Sigiriya Rock",
    "🌤️ Best time to visit?",
    "🏛️ Cultural & temple sites",
    "🪂 Adventure activities"
]

cols = st.columns(5)
for idx, question in enumerate(example_questions):
    with cols[idx]:
        if st.button(question, key=f"example_{idx}", use_container_width=True):
            query = question.replace("🏖️ ", "").replace("🗿 ", "").replace("🌤️ ", "").replace("🏛️ ", "").replace("🪂 ", "")
            search_button = True

# Process query
if search_button and query:
    st.markdown("---")
    with st.spinner("🔄 Finding the best answer for you..."):
        answer = ask_question(query)

    # Display answer with improved formatting
    answer_text = answer.strip()
    if answer_text:
        # Create a complete HTML card with all content inside
        html_content = f"""
        <div class="answer-card">
            <h3>✨ Answer</h3>
            <p>{answer_text}</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

        # Add some spacing
        st.markdown("")

        # Copy and share section
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("📋 Copy Answer", key="copy_btn", help="Copy answer to clipboard"):
                st.success("✅ Answer copied to clipboard!")
        with col2:
            if st.button("❤️ Helpful?", key="helpful_btn", help="Mark as helpful"):
                st.success("Thanks for your feedback! 😊")
        with col3:
            st.markdown("**💬 Ask another question below to continue exploring!**")
    else:
        st.error("❌ Could not generate an answer. Please try another question with different keywords.")

elif search_button and not query:
    st.warning("⚠️ Please enter a question or select an example question above!")