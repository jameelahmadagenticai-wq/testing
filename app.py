import streamlit as st
import requests

st.title("Autonomous News Analyzer")

topic = st.text_input("Enter topic")

if st.button("Analyze"):
    if topic:
        url = f"http://127.0.0.1:8000/analyze?topic={topic}"

        with st.spinner("Processing..."):
            res = requests.get(url, stream=True)

            result = ""
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    text = chunk.decode("utf-8")
                    result += text
                    st.text(result)