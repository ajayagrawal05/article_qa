import streamlit as st
from langchain.document_loaders import UnstructuredURLLoader

st.title("Scrapper Application 🏭")
st.sidebar.title("Article URL")

url = st.sidebar.text_input("URL")

process_url_clicked = st.sidebar.button("Process URL")

if process_url_clicked and url: 
    loader = UnstructuredURLLoader(urls=[url])  
    st.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    
    if data:
        st.text("Data Loaded Successfully...✅✅✅")
        st.header("Scraped Text:")
        st.write(data[0])  # Display the text from the URL
    else:
        st.error("Failed to load data from the URL. Please check the URL and try again.")

