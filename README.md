## Chat over Documents

A Python RAG application built with the LangChain framework that allows conversational chat over documents. 

Concepts used in the project:

- RAG: Used advanced retrieval algorithms like hybrid search (keyword and semantic search) and reranking. This is an effective approach to improve the retrieval step of a RAG application. Utilised the BM25 retriever for keyword search, traditional semantic search through a vectorstore, Ensemble retriever that does Reciprocal Rank Fusion and Cohere for the reranking. (Reference to a Microsoft blogpost on the performance of this retrieval method: https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-ai-search-outperforming-vector-search-with-hybrid/ba-p/3929167)
- Agent with access to the retriever tool. The use of an agent provides conversational and retriever tool use flexibility. An agent gives the flexibility of using the retriever when needed and not use it if the user only want to be conversational like saying hi. Without this flexibility, the system will be performing retrieval and returning source documents even when the user says ‘hi my name is bob’. Utilised LangChain’s built-in openai_tools_agent which is an agent specifically optimized for doing retrieval when necessary and holding a conversation.
- Included conversational memory to have a chat-like user experience and for the agent to reference chat history in contextualising the user's question.
- Prompt engineering including few-shot prompting to guide the output format of the answer.
- Use of LangChain's indexing API to help with management of indexing of documents in vectorstore
- Streamlit - a Python package to build the UI.

Files:
- Offline indexing code in notebook: indexing.ipynb
- Application code in the python files: main.py, agent.py, retriever.py
