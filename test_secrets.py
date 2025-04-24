import streamlit as st

try:
    st.write("API Key:", st.secrets["openai"]["API_KEY"])
except KeyError:
    st.error("OpenAI API key not found! Check secrets.toml file.")
