from .vector_store import retriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import CrossEncoder
import re

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 

query = "What are the top tourist attractions in Sri Lanka?"

def ask_question(query, top_k=4, max_length=512):
    docs = retriever.invoke(query)

    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)
    ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in ranked_docs[:top_k]]

    def clean_text(text):
        # Remove content in parentheses but keep main text
        text = re.sub(r'\([^)]*\)', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text

    # Join context with better formatting
    context_parts = []
    for doc in top_docs:
        cleaned = clean_text(doc.page_content)
        if cleaned and len(cleaned) > 20:  # Filter out very short passages
            context_parts.append(cleaned)

    context = "\n".join(context_parts[:3])  # Use top 3 most relevant chunks

    # Improved prompt with better instructions
    prompt = f"""You are a helpful Sri Lanka tourism expert. Answer the question clearly and concisely using ONLY the context provided.

Rules:
- Provide a focused, well-structured answer
- Use 2-3 sentences maximum
- Only mention information directly from the context
- Avoid listing unrelated information
- If context lacks relevant information, say so clearly

Context:
{context}

Question: {query}

Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
    outputs = model.generate(
        **inputs,
        max_length=150,  # Reduced for more concise answers
        min_length=30,
        num_beams=4,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Post-process answer to fix common issues
    answer = answer.replace(' ,', ',')
    answer = answer.replace(' .', '.')
    answer = answer.replace('  ', ' ')

    return answer.strip()