import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.prompts import PromptTemplate

#Configuring API keys
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
hf_token = os.getenv('HF_TOKEN')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
qdrant_url = os.getenv("QDRANT_URL")

#Instantiating the Chat model
chat = ChatGroq(groq_api_key= groq_api_key, model= "llama3-8b-8192")

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



