import streamlit as st
import requests

st.set_page_config(page_title="PDF Chat Assistant", layout="centered")

st.title("📄 Chat with your PDFs")

# Initialize Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = "user_123"

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")
    if st.button("Process Files"):
        if uploaded_files:
            files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
            response = requests.post("http://localhost:8000/upload", files=files)
            st.success(response.json().get("message"))
        else:
            st.warning("Please select files first.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about your PDFs"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI Streaming Endpoint
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Request to FastAPI
        payload = {"question": prompt, "session_id": st.session_state.session_id}
        
        with requests.post("http://localhost:8000/ask", json=payload, stream=True) as r:
            for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})