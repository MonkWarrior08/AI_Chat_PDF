import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
import tempfile
import os

# Page configuration
st.set_page_config(page_title="Chat with PDF", layout="wide")
st.title("Chat with your PDF 📚")
st.write("By [Nino(Dimitri) M.](https://github.com/MonkWarrior08?tab=overview&from=2024-11-01&to=2024-11-28)")

# Initialize session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processComplete" not in st.session_state:
    st.session_state.processComplete = None

def process_pdf(uploaded_file):
    # Get the temporary directory
    temp_dir = tempfile.gettempdir()
    
    # Save the uploaded file temporarily
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # Load the PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    document_chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and store in vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(document_chunks, embeddings)
    
    # Create conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(
            model_name="gpt-4",
            temperature=0.7
        ),
        retriever=vectorstore.as_retriever(search_kwargs={"k": 6}),
        return_source_documents=True,
        verbose=False
    )
    
    return conversation_chain

# Initialize OpenAI API key input
api_key = st.text_input("Enter your OpenAI API key:", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# File upload
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file and api_key:
    if not st.session_state.processComplete:
        with st.spinner("Processing PDF... This may take a moment."):
            st.session_state.conversation = process_pdf(uploaded_file)
            st.session_state.processComplete = True

# Chat interface
if st.session_state.conversation:
    # Use a form to handle the input and submission
    with st.form(key='question_form'):
        user_question = st.text_input("Ask a question about your PDF:")
        submit_button = st.form_submit_button("Ask")

    if submit_button and user_question:
        with st.spinner("Generating response..."):
            # Get response from conversation chain
            response = st.session_state.conversation({
                "question": user_question,
                "chat_history": st.session_state.chat_history
            })
            
            # Update chat history
            st.session_state.chat_history.append((user_question, response["answer"]))
            
            # Display newest response first
            st.write(f"👤 **User:** {user_question}")
            st.write(f"🤖 **Assistant:** {response['answer']}")
            st.write("---")

    # Display previous chat history
    for question, answer in reversed(st.session_state.chat_history[:-1]):
        st.write(f"👤 **User:** {question}")
        st.write(f"🤖 **Assistant:** {answer}")
        st.write("---")

# Display helpful messages
if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
if not uploaded_file:
    st.warning("Please upload a PDF file to begin.") 