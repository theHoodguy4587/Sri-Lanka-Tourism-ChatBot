from langchain_community.vectorstores import FAISS
from embedding_model import embeddings
from data_loader import chunks

vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever( search_kwargs={"k": 8})