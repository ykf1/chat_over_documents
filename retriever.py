import pickle

from dotenv import load_dotenv

from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

persist_directory = 'vectordb'
embedding = OpenAIEmbeddings(model='text-embedding-ada-002')

with open('bm25_retriever', 'rb') as bm25result_file:
    bm25_retriever = pickle.load(bm25result_file)

bm25_retriever.k = 3 # Return top 3 documents

vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)
vectordb_retriever = vectordb.as_retriever(search_kwargs={"k": 3}) # Return top 3 documents

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vectordb_retriever], weights=[0.5, 0.5]
)

compressor = CohereRerank(model='rerank-english-v2.0', top_n=3) # Return top 3 out of 6 documents

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, 
    base_retriever=ensemble_retriever
)

