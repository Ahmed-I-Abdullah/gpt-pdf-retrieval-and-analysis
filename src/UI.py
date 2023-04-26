import asyncio
import streamlit as st
from .VectorStore import VectorStore
from .PDFChat import PDFChat
import io
from concurrent.futures import ThreadPoolExecutor


class UI:
    @staticmethod
    def _run_async_function(async_function):
        loop = asyncio.new_event_loop()
        with ThreadPoolExecutor() as pool:
            return loop.run_until_complete(pool.submit(asyncio.run, async_function))

    @staticmethod
    def _load_css(file_path):
        with open(file_path) as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    @staticmethod
    def _display_title():
        st.markdown("<h1 class='title'>PDFChat AI 🤖</h1>",
                    unsafe_allow_html=True)

    @staticmethod
    async def _display_uploaded_file(uploaded_file, pdf_chat):
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                uploaded_file.seek(0)
                file = uploaded_file.read()
                vectors = await VectorStore.get_doc_embeddings(io.BytesIO(file), uploaded_file.name)
                pdf_chat.load_vectors(vectors)

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


    @staticmethod
    def _display_chat_history(messages_container):
        for i in range(len(st.session_state.get('answers', []))):
            messages_container.markdown(f"<p class='user-message'>You:</p>", unsafe_allow_html=True)
            messages_container.markdown(f"<p class='message-text'>{st.session_state['questions'][i]}</p>", unsafe_allow_html=True)
            messages_container.markdown(f"<p class='pdfchat-message'>PDFChat:</p>", unsafe_allow_html=True)
            messages_container.markdown(f"<p class='message-text'>{st.session_state['answers'][i]}</p>", unsafe_allow_html=True)
            messages_container.markdown("<div class='message-spacing'></div>", unsafe_allow_html=True)


    @staticmethod
    def _display_chat_form(messages_container, pdf_chat):
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("Type your question here:", placeholder="e.g: Provide a brief overview of the paper in a few sentences", key='input', height=100)
            st.form_submit_button(label='Send', on_click=asyncio.run(UI._process_user_input(user_input, messages_container, pdf_chat)))


    @staticmethod
    async def _process_user_input(user_input, messages_container, pdf_chat):
        if user_input:
            messages_container.markdown(f"<p class='user-message'>You:</p>", unsafe_allow_html=True)
            messages_container.markdown(f"<p class='message-text'>{user_input}</p>", unsafe_allow_html=True)
            with st.spinner("Processing your question..."):
                output = await pdf_chat.conversational_chat(user_input)
                st.session_state['questions'].append(user_input)
                st.session_state['answers'].append(output)

            messages_container.markdown(f"<p class='pdfchat-message'>PDFChat:</p>", unsafe_allow_html=True)
            messages_container.markdown(f"<p class='message-text'>{output}</p>", unsafe_allow_html=True)
            messages_container.markdown("<div class='message-spacing'></div>", unsafe_allow_html=True)

    @staticmethod
    def run():
        if 'questions' not in st.session_state:
            st.session_state['questions'] = []

        if 'answers' not in st.session_state:
            st.session_state['answers'] = []

        pdf_chat = PDFChat()

        st.set_page_config(page_title='PDFChat', page_icon="🤖", layout='wide')
        UI._load_css("static/css/main.css")
        UI._display_title()

        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        asyncio.run(UI._display_uploaded_file(uploaded_file, pdf_chat))

        response_container = st.container()
        UI._display_chat_history(response_container)

        if uploaded_file:
            UI._display_chat_form(response_container, pdf_chat)
