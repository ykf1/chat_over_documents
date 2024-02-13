from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

from agent import invoke_agent


def main():

    st.header("Chat with your documents :books:")

    # Initialise messages list (chat history) if does not exist on first run 
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display chat messages from history
    for msg in st.session_state['messages']:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)

    # Next conversation - user input and AI response
    if prompt := st.chat_input("Ask a question "):

        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):

            with st.spinner("AI is thinking ..."):
                response = invoke_agent(prompt, st.session_state['messages'])

            st.write(response)

        save_chat_history(st.session_state['messages'], prompt, response)


def save_chat_history(messages: list, question: str, answer: str) -> None:
    """Adds the question and answer to the messages list"""
    messages.extend([
        HumanMessage(content=question),
        AIMessage(content=answer)
    ])


if __name__ == "__main__":
    main()
