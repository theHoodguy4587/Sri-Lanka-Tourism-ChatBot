from src.vector_store import retriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import CrossEncoder

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
    context = "\n\n".join([doc.page_content for doc in top_docs])

        
   
    prompt = f"""
    You are a knowledgeable Sri Lanka tourism guide.

    Using the context below, answer the question in a detailed and engaging way.

    Include:
    - A short description of the place
    - Why it is famous
    - Key features or attractions
    - Travel tips if possible

    Context:
    {context}

    Question: {query}

    Answer in a well-structured paragraph.
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
    outputs = model.generate(**inputs, max_length=250,min_length=100,num_beams=5,no_repeat_ngram_size=2)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer