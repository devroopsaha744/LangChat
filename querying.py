import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.prompts import PromptTemplate

#Configuring API keys
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
hf_token = os.getenv('HF_TOKEN')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = "https://2cd21b4f-0bc8-433d-9b3f-45d49542ffa1.us-east4-0.gcp.cloud.qdrant.io"

#Instantiating the LLM
chat = ChatGoogleGenerativeAI(model = 'gemini-pro', google_api_key = google_api_key)

#Embedding Model 
embedding = HuggingFaceInferenceAPIEmbeddings(api_key= hf_token)

# Connect to Qdrant
qdrant_client = QdrantClient(
    url= qdrant_url,
    api_key= qdrant_api_key
)

# Initialize the LangChain Qdrant wrapper
vectorstore = Qdrant(
    client=qdrant_client,
    collection_name="langchat",
    embeddings= embedding
)

#Setting up the retriever
retriever = vectorstore.as_retriever()

#Prompt Template
template = '''
You are an expert python developer. Using the provided context, answer the qeuries 
accordingly generate relevant code according to the given context to answer the questions

{context}:
{Question}:

Answer:

'''
prompt_template = PromptTemplate.from_template(template=template)

#Setting up the chain
set_ret = RunnableParallel(
    {"context": retriever, "Question": RunnablePassthrough()} 
)
rag_chain = set_ret |  prompt_template | chat | StrOutputParser()

#Defining the response function
def generate_response(text):
    response = rag_chain.invoke(text)
    return response


print("Querying done!")



