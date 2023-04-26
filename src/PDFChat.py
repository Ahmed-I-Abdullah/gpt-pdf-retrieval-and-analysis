from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

load_dotenv()


class PDFChat:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.chain = load_qa_chain(self.llm, chain_type="stuff")
        self.history = []
        

    async def conversational_chat(self, query):
        result = self.qa({"question": query, "chat_history": self.history})
        self.history.append((query, result["answer"]))
        return result["answer"]

    def load_vectors(self, vectors):
        self.qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(model_name="gpt-3.5-turbo"),
            retriever=vectors.as_retriever(search_type="similarity", search_kwargs={"k": 2}),
            return_source_documents=True,
        )
        
