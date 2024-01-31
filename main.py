from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st

from agent import invoke_agent


def main():

    st.header("Chat with your documents :books:")

    # Initialise messages (chat history)
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display chat messages from history
    #messages = st.session_state.get('messages', [])
    for msg in st.session_state['messages']:
        if isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)


    # Next conversation - user input and assistant response
    if prompt := st.chat_input("Ask a question "):

        # Display user message and append to session state messages
        st.chat_message("user").write(prompt)

        # Get AI response based on the user input
        with st.chat_message("assistant"):

            with st.spinner("AI is thinking ..."):
                response = invoke_agent(prompt, st.session_state['messages'])

            st.write(response)

        save_chat_history(st.session_state['messages'], prompt, response)


def save_chat_history(messages: list, question: str, answer: str) -> None:
    messages.extend([
        HumanMessage(content=question),
        AIMessage(content=answer)
    ])


if __name__ == "__main__":
    main()


    # # For upload of documents
    # with st.sidebar:
    #     st.subheader("Your documents")
    #     pdf_files = st.file_uploader(
    #         "Upload your PDF here and click on 'Process'",
    #         accept_multiple_files=True            
    #         )
    #     if st.button("Process"):

    #         uploaded_filepaths = upload_files(pdf_files)

    #         with st.spinner("Embedding..."):
    #             embed_documents(uploaded_filepaths)

    #         with st.spinner("Initialise chatbot..."):  
    #             st.session_state.conversation = Conversation()
        
    #     st.subheader("Uploaded documents")

    #     for file in os.listdir(upload_file_directory):
    #         st.markdown(file)