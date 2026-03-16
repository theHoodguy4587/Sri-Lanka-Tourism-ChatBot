from src.vector_store import retriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import CrossEncoder

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 

query = "What are the top tourist attractions in Sri Lanka?"

def ask_question(query,top_k=3,max_length=512):
    
    docs = retriever.invoke(query)

    pairs = [(query, doc.page_content) for doc in docs]
    scores = reranker.predict(pairs)
    ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    top_docs = [doc for doc, score in ranked_docs[:top_k]]
    context = "\n\n".join([doc.page_content for doc in top_docs])

        
   
    prompt = f"""
    You are a Sri Lanka tourism assistant.

    Using the context below, answer the question and list important tourist places.

    Context:
    {context}

    Question: {query}

    Answer with a short list of places.
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_length)
    outputs = model.generate(**inputs, max_length=120,num_beams=5)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer