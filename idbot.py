# 3 sections
# section 1: Input for Ollama Server, Model, Temperature(Slider), Prompt Style
# Section 2(left): title, fileuploader, success message with char length of pdf, expandable section for pdf extracted text
# Section 3(right): subheader, question input box, ask pdf button, display response, expandable section for prompt


import streamlit as st
from PIL import Image
import time
import helper_id as helper
import requests


st.set_page_config(layout = "wide")

OLLAMA = st.sidebar.text_input("Ollama Server", "http://localhost:11434")

MODEL = st.sidebar.text_input("Model", "gemma3:1b")

temp = st.sidebar.slider("Temperature", 0.0,1.0,0.2,0.1)

prompt_style = st.sidebar.radio("Prompt Style", ["v1(1)", "v2(2)"])

left, right = st.columns(2, gap = "large")

with left:
    st.title("Student ID")
    up = st.file_uploader("Image upload", type=["jpg", "jpeg"])
    if up:
        img = Image.open(up)
        st.image(img, caption="Uploaded ID", use_container_width=True)
    else:
        st.info("Upload a JPG/JPEG image of student ID.")

with right:
    st.subheader("Extract DOB & Name")
    
    run = st.button("Extract", type = "primary", use_container_width=True)
    
    if run:

        if not up:
            st.warning("Please upload the image first")
        
        else:
            prompt = helper.make_prompt(prompt_style) #make_prompt()
            b64 = helper.image_to_base64(img)
            with st.spinner(f"Calling model: {MODEL}"):
                try:
                    t0 = time.time()            
                    ans = helper.call_ollama(OLLAMA, MODEL, prompt, b64, temp) #call_ollama() 
                    elapsed = time.time() - t0
                    
                except requests.RequestException as e:
                    st.error(str(e))
                    resp, elapsed = "", 0
            if ans: 

                st.markdown("**Results**")
                st.write(f"**{ans}**")
                st.write(f"** Time Taken: {elapsed: .2f} seconds")

                st.caption(f"Model: '{MODEL}' | Prompt: {prompt_style} | Temperature: {temp}")