# PDFChat

PDFChat is a web application that allows users to upload a PDF document and ask questions about its content. The application uses the OpenAI GPT-3.5-turbo model to answer user queries, and it's built with Python, Streamlit, and asyncio.

## Features

- Upload and process PDF documents
- Chat-like interface for asking questions about the uploaded document
- Utilizes OpenAI GPT-3.5-turbo model for generating responses
- Stylish and responsive design

## Installation and Setup

To get started with PDFChat, follow these steps:

1. Clone the repository:
```bash
git clone git@github.com:Ahmed-I-Abdullah/gpt-pdf-retrieval-and-analysis.git
```


2. Change to the `pdfchat` directory:
```bash
cd pdfchat
```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```


4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Set your OpenAI API key in a .env file
```
# .env
OPENAI_API_KEY=<your_api_key>
```

6. Run the Streamlit application:

```bash
streamlit run main.py
```


7. Open the provided link in your browser to start using PDFChat.

## Usage
1. Upload a PDF document using the file uploader.
2. Wait for the application to process the document and load the chat interface.
3. Type your questions about the document in the chat input box and press "Send".
4. PDFChat will provide answers based on the content of the uploaded document.







