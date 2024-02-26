import os
import streamlit as st
import time
import faiss  # Ensure FAISS is imported
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env (especially openai api key)

st.title("RockyBot: News Research Tool 📈")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.index"  # Changed file extension for clarity

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

# Initialize vectorstore_openai here to ensure it's defined outside the if blocks
vectorstore_openai = None  # Placeholder, replace with actual initialization as needed

if process_url_clicked:
    # Load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    # Split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)
    # Create embeddings and save it to FAISS index
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)  # Proper initialization
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # Save the FAISS index to a file
    faiss.write_index(vectorstore_openai.index, file_path)

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        # Ensure vectorstore_openai is initialized before loading the index
        if vectorstore_openai is None:
            # Properly initialize vectorstore_openai if it hasn't been already
            # This should match the initialization in the 'process_url_clicked' block
            vectorstore_openai = FAISS()  # Adjust this line based on your actual initialization needs

        # Load the FAISS index from a file into vectorstore_openai
        vectorstore_openai.index = faiss.read_index(file_path)

        # Assuming vectorstore_openai is now properly set up, proceed with using it
        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore_openai.as_retriever())
        result = chain({"question": query}, return_only_outputs=True)
        st.header("Answer")
        st.write(result["answer"])

        # Display sources, if available
        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write(source)

