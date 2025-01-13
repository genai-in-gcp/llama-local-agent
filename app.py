import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, PromptTemplate
import os
import uuid
import gc
import re

# Session initialization
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

session_id = st.session_state.id

def validate_query(query):
    """Validate the user query to prevent malicious inputs and prompt injection."""
    forbidden_patterns = [
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return False
    return True

def format_response(raw_response):
    """Format the raw response object to be polite, concise, and clean."""
    if hasattr(raw_response, "response"):
        response = raw_response.response.strip()
        return (response[:300] + "..." if len(response) > 300 else response) + "\n\nThank you for asking! Let me know if I can assist further."
    return "I'm sorry, I couldn't process your request. Please try again."

def reset_chat():
    st.session_state.messages = []
    gc.collect()

# Streamlit app definition
st.title("Secure and Polite PDF-based Q&A Chatbot")

# Pre-uploaded data directory
data_dir = "./data"
if not os.path.exists(data_dir):
    st.error("Error: Pre-uploaded data directory not found.")
    st.stop()

st.write("Loading documents from:", data_dir)

# Initialize the LLM and embedding models
llm = Ollama(model="llama3.2", request_timeout=120.0)
embed_model = HuggingFaceEmbedding(model_name="nomic-ai/modernbert-embed-base", 
                                   trust_remote_code=True, 
                                   cache_folder='./hf_cache')
Settings.llm = llm
Settings.embed_model = embed_model

# Load documents
try:
    loader = SimpleDirectoryReader(input_dir=data_dir, required_exts=[".pdf"], recursive=True)
    docs = loader.load_data()
    if not docs:
        st.error("No valid PDF documents found in the directory.")
        st.stop()
except Exception as e:
    st.error(f"Failed to load documents: {str(e)}")
    st.stop()

# Create the index
try:
    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    query_engine = index.as_query_engine(streaming=True)
except Exception as e:
    st.error(f"Failed to create the index: {str(e)}")
    st.stop()

# Set up the prompt template
qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Using the context above, provide a concise, polite, and friendly response to the query. "
    "If you don't know the answer, respond with 'I'm sorry, I don't know the answer to that.'.\n"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
try:
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})
except Exception as e:
    st.error(f"Failed to update prompt templates: {str(e)}")
    st.stop()

st.success("Documents successfully loaded and indexed!")

# Chat UI
col1, col2 = st.columns([6, 1])
with col1:
    st.header("Chat with Documents")
with col2:
    st.button("Clear ↺", on_click=reset_chat)

# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your question below:"):
    if validate_query(prompt):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                streaming_response = query_engine.query(prompt)
                for chunk in streaming_response.response_gen:
                    full_response += chunk
                    formatted_chunk = format_response({"response": full_response})
                    message_placeholder.markdown(formatted_chunk + "▌")
                final_response = format_response({"response": full_response})
                message_placeholder.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
            except Exception as e:
                st.error(f"An error occurred while processing your query: {str(e)}")
    else:
        st.error("Can't answer your question.")

# Secure app hosting settings (optional)
if __name__ == '__main__':
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "true"
