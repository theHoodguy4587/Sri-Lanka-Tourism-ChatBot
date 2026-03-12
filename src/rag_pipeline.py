from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from vector_store import retriever

llm = ChatOpenAI(model="gpt-4")

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
response = qa.run("What are the top tourist attractions in Sri Lanka?")
print(response)

