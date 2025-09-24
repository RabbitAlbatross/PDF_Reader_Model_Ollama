import streamlit as st
import pdfplumber
import requests

def read_pdf_text(uploaded_file):
    """
    extract text from pdf
    """

    parts = []
    print(parts)
    with pdfplumber.open(uploaded_file) as pdf:
        st.write("Loading the library")
        for page in pdf.pages:
            st.write(f"Page: {page}")
            extracted_text = page.extract_text()
            parts.append(extracted_text)

    return "\n\n".join(parts).strip()

def make_prompt(version, question, content):
    """
    Create actual prompt
    """

    if version.startswith("v1"):
        return f"""Answer the question based on the content provided and guess if required
        Question: {question}
        Content: {content}
        """
    
def call_ollama(ollama_server, model, prompt, temperature, max_tokens=512):
    api_url = f"{ollama_server}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        #"temperature": temperature
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens}
    }
    answer = requests.post(api_url, json=payload, timeout=120)
    print(answer)
    answer.raise_for_status()
    return (answer.json().get("response") or "").strip()