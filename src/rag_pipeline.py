from .vector_store import retriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import CrossEncoder
import re

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 

query = "What are the top tourist attractions in Sri Lanka?"

def ask_question(query,top_k=4,max_length=512):
    
    docs = retriever.invoke(query)

    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)
    ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in ranked_docs[:top_k]]


    def clean_text(text):
        text = re.sub(r'\([^)]*\)', '', text)
        text = re.sub(r'[^A-Za-z0-9.,\s-]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    context = "\n\n".join([clean_text(doc.page_content) for doc in top_docs])

        
   
    prompt = f"""
    You are a Sri Lanka tourism guide.

    Using the context below, explain the place in a clear and natural way.

    Write 1–2 short paragraphs covering:
    - what the place is
    - why it is popular with tourists
    - main attractions

    Ignore unrelated details.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
    outputs = model.generate(**inputs, max_length=250,min_length=100,num_beams=5,no_repeat_ngram_size=2)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer