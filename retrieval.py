import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_qdrant import Qdrant
from langchain_text_splitters import CharacterTextSplitter

#Configuring API Keys
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
hf_token = os.getenv('HF_TOKEN')
qdrant_api_key = os.getenv('QDRANT_API_KEY')

#Loading the Knwledge using Directory Loader
data_dir = 'txt_data'
loader = DirectoryLoader(path = data_dir, glob= "**/*.md", show_progress=True)
docs = loader.load()

print(len(docs))

#Splitting the data
