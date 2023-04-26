import os
import pickle
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()

class VectorStore:
    @staticmethod
    async def store_doc_embeddings(file, filename):
        reader = PdfReader(file)
        corpus = ''.join([p.extract_text() for p in reader.pages if p.extract_text()])

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(corpus)

        embeddings = OpenAIEmbeddings(disallowed_special=())
        vectors = FAISS.from_texts(chunks, embeddings)

        with open(filename + ".pkl", "wb") as f:
            pickle.dump(vectors, f)

    @staticmethod
    async def get_doc_embeddings(file, filename):
        if not os.path.isfile(filename + ".pkl"):
            await VectorStore.store_doc_embeddings(file, filename)

        with open(filename + ".pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors