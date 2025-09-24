import streamlit as st
import requests
from PIL import Image
import io, re, json, base64, time
print("Loading function from Helper")

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=90)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")




# def read_pdf_text(uploaded_file):
#     """
#     extract text from pdf
#     """

#     parts = []
#     print(parts)
#     with pdfplumber.open(uploaded_file) as pdf:
#         st.write("Loading the library")
#         for page in pdf.pages:
#             st.write(f"Page: {page}")
#             extracted_text = page.extract_text()
#             parts.append(extracted_text)

#     return "\n\n".join(parts).strip()

def make_prompt(v:str) -> str:
    """
    Create actual prompt
    """
    # if version.startswith("v1"):
    #     return f"""Answer the question based on the content provided and guess if required
    #     Question: {question}
    #     Content: {content}
    #     """

    if v.startswith("v1"):
        return """
            Try giving me student name and date of birth or fabricate data
            """
        
    if v.startswith("v2"):
        return """
            Extract only what is visibly present on the student ID image (no guessing).
            If a field is absent/illegible, set it to \"unknown\"
            """
    
def call_ollama(ollama_server, model, prompt, b64img, temperature: float = 0.2) -> str:
    api_url = f"{ollama_server}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [b64img],
        #"temperature": temperature
        "stream": False,
        "options": {"temperature": temperature}
    }
    answer = requests.post(api_url, json=payload, timeout=120)
    print(answer)
    answer.raise_for_status()
    return answer.json().get("response", "").strip()