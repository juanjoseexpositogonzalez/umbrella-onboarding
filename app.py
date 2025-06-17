import logging
from typing import Dict, List

import streamlit as st
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from assistant import Assistant
from data.employees import generate_employee_data
from gui import AssistantGUI
from models import AIModel, prepare_environmnet
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE


def main():
    """Main function to run the Streamlit app."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Prepare the environment for the AI model
    prepare_environmnet()
    model = AIModel.LLAMA_VERSATILE
    # Set the AI model to use
    st.set_page_config(
        page_title="Umbrella Corporation Employee Data",
        page_icon=":guardsman:",
        layout="wide",
    )

    @st.cache_data(ttl=3600, show_spinner="Loading Employee Data...")
    def get_user_data() -> Dict[str, str | float | List[str]]:
        """Get the user data from the sidebar."""
        return generate_employee_data(num_employees=1)[0]

    @st.cache_resource(ttl=3600, show_spinner="Initializing Vector Store...")
    def init_vectorstore(
        pdf_path: str = "data/umbrella_corp_policies.pdf",
    ) -> None | Chroma:
        """Initialize the vector store."""
        try:
            loader = PyPDFLoader(pdf_path)  # type: ignore[call-arg]
            docs = loader.load()  # type: ignore[call-arg]
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=4000, chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)  # type: ignore[call-arg]

            embedding_function = OpenAIEmbeddings()
            persistent_path = "./data/vectorstore"

            vectorstore = Chroma.from_documents(  # type: ignore[call-arg]
                documents=splits,
                embedding=embedding_function,
                persist_directory=persistent_path,
            )

            return vectorstore  # type: ignore[return-value]
        except (FileNotFoundError, ValueError, ImportError) as e:
            logging.error("Error initializing vector store: %s", str(e))
            st.error(f"Failed to initialize vector store: {str(e)}.")
            return None

    # Initialize the vector store and the user data
    customer_data = get_user_data()
    vector_store = init_vectorstore("data/umbrella_corp_policies.pdf")

    if "customer" not in st.session_state:
        st.session_state["customer"] = customer_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]

    llm = ChatGroq(model=model)

    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        vector_store=vector_store,  # type: ignore[arg-type]
        employee_information=st.session_state.customer,
    )

    gui = AssistantGUI(assistant)
    gui.render()


if __name__ == "__main__":
    main()
