from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader,TextLoader

loader = DirectoryLoader("tourism_data", glob="**/*.txt", loader_cls=TextLoader,loader_kwargs={"encoding": "utf-8"})
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = splitter.split_documents(documents)

print(f"Loaded {len(chunks)} chunks from the tourism data.")