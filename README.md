# AI_Chat_PDF
A web-based interface that allows users to have interactive conversations with their PDF documents using OpenAI's GPT-4o model and Streamlit.

## 🌟 Features

- Upload and process PDF documents
- Interactive chat interface
- Secure API key handling
- Real-time response generation
- Chat history tracking
- Mobile-responsive design

## 🛠️ Technologies Used

- [Streamlit](https://streamlit.io/) - Web interface
- [LangChain](https://python.langchain.com/) - PDF processing and chat chain
- [OpenAI GPT-4](https://openai.com/) - Language model
- [FAISS](https://github.com/facebookresearch/faiss) - Vector store for embeddings
- Python 3.7+

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-chat-assistant.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📝 Usage

1. Enter your OpenAI API key in the designated field
2. Upload a PDF document
3. Wait for the processing to complete
4. Start asking questions about your document
5. View the AI-generated responses and chat history

## ⚙️ Configuration

The application uses the following key configurations:
- GPT-4o model with temperature 0.7
- Character text splitter with 1000 chunk size and 200 chunk overlap
- FAISS vector store for efficient document retrieval
- Top 6 most relevant chunks for context

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
