import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Configuring API Keys
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
hf_token = os.getenv('HF_TOKEN')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv("QDRANT_URL")

#Loading the Knwledge using Directory Loader
data_dir = 'txt_data'
loader = DirectoryLoader(path = data_dir, glob= "**/*.md", show_progress=True)
docs = loader.load()

#print(len(docs))

#Splitting the data
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(docs)

#Embedding Model 
embedding = HuggingFaceInferenceAPIEmbeddings(api_key= hf_token)

#Indexing the documents in on vectorDB
qdrant = Qdrant.from_documents(
    docs,
    embedding,
    url=qdrant_url,
    prefer_grpc=True,
    api_key=qdrant_api_key,
    collection_name="langchat",
)

print("Indexing done!")