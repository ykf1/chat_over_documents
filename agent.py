from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from retriever import compression_retriever


load_dotenv()

tool = create_retriever_tool(
    compression_retriever,
    "search_knowledge_base",
    "Searches and returns excerpts from the knowledge base. Input should be a clearly constructed question.",
)
tools = [tool]

template = """
You are a helpful assistant whose objective is to provide concise answers to a user with the help of the following tool: \
Tool name: search_knowledge_base
Tool description: Searches and returns excerpts from the knowledge base. Input should be a clearly constructed question.

You may or may not choose to use the tool. If the user is engaging you in simple conversation like saying hi, \
you can respond to the user without using the tool.

If you choose to use the tool, note that the tool accepts a question as input and returns a list of source documents \
that are relevant to the question. You can rephrase the user question to make it more clear and easy to understand. \
There may be multiple source documents returned from the tool and you may not need to use all of the source \
documents to formulate your answer. You must only answer the user based on information returned from the tool \
and must not use your own knowledge. If you cannot answer the question from using the tool, just say you don't know.

Cite those relevant source documents returned from the tool that are used in your answer. You should display the \
'source' and 'page' from the 'metadata' of the document. You should not cite source documents returned from the tool that \
are not relevant to the answer.

When answering the user question with information from the knowledge base, your answer to the user should follow \
the following format:
<answer>

Sources:
<source_documents>

Example output format:

Question: What is the highest grossing film of all time?

Answer: Avatar, released in the year 2009, is the highest grossing film of all time with a worldwide gross of $2.9 billion. 

Sources:
List_of_highest-grossing_films.pdf (page 1)
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

agent_executor = AgentExecutor(
    agent=create_openai_tools_agent(llm, tools, prompt), 
    tools=tools, 
    verbose=True
)

def invoke_agent(question: str, chat_history: list) -> str:
    """invokes the agent executor. Returns the output of the agent"""

    response = agent_executor.invoke({
        "input": question, 
        'chat_history': chat_history
    })

    # agent response output format is {'input': question, 'output': answer}
    return response["output"]