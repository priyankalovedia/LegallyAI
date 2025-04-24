import streamlit as st

def load_chat_history():
    return st.session_state.get("chat_history", [])

def save_chat_history(new_message):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.session_state.chat_history.append(new_message)
