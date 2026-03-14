from vector_store import retriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

query = "What are the top tourist attractions in Sri Lanka?"

attractions = []
docs = retriever.invoke(query)

for doc in docs:

    
    prompt = f"""
    You are a tourism assistant.
    List all tourist attractions (places, cities, beaches, temples, national parks) mentioned in the following text:

    {doc.page_content}

    Answer as a comma-separated list.
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=50)
    partial_attractions = tokenizer.decode(outputs[0], skip_special_tokens=True)
    attractions.extend([a.strip() for a in partial_attractions.split(",")])

unique_attractions = list(set(attractions))
print("Answer:", ", ".join(unique_attractions))