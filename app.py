import streamlit as st
from src.rag_pipeline import ask_question

st.title("Sri Lanka Tourism Chatbot 🇱🇰")

query = st.text_input("Ask a question about Sri Lanka Tourism:")

if st.button("Ask"):

    if query:
        with st.spinner("Finding the best answer..."):
            answer = ask_question(query)
        st.success("Here's what I found:")
        st.write(answer)
    else:
        st.warning("Please enter a question to ask.")