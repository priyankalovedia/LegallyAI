# streamlit run streamlit_final_app.py

import streamlit as st
import json
import os
from fetch_case_data_and_summarize import query_ai_model, IKApi
from utils.openai_api import query_openai  # ✅ Correct import
from utils.chat_history import load_chat_history, save_chat_history  # ✅ Correct Import

# File for chat history storage
CHAT_HISTORY_FILE = "chat_history.json"

# ---------------- Utility Functions ----------------
def load_chat_history():
    """Loads chat history from JSON file."""
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump([], f)  # Empty list for chat history

    with open(CHAT_HISTORY_FILE, "r") as f:
        return json.load(f)

def save_chat_history(chat_history):
    """Saves chat history to JSON file."""
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chat_history, f, indent=4)

# ---------------- Initialize Session State ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None

st.set_page_config(page_title="AI Legal Assistant", layout="wide")

# ---------------- Sticky Navbar ----------------
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #f9fafb;
        
    }

    </style>

    
""", unsafe_allow_html=True)



# ---------------- Begin Main Content ----------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ---------------- Sidebar: Chat History Section ----------------
st.sidebar.title("Chat History")

if st.sidebar.button("New Chat", key="new_chat"):
    st.session_state.selected_chat = None

# Display past chats in the sidebar
for idx, chat in enumerate(st.session_state.chat_history):
    if st.sidebar.button(chat["query"], key=f"chat_{idx}"):
        st.session_state.selected_chat = idx  # Select chat index

st.sidebar.write("---")
st.sidebar.write("© 2024 AI Legal Assistant")

# ---------------- Main Content ----------------
st.title("AI-Based Legal Research Assistant")

query = st.text_input("Enter your legal query:")

if st.button("Search"):
    if query.strip():
        ikapi = IKApi(maxpages=5)
        doc_ids = ikapi.fetch_all_docs(query)

        all_summaries = []
        for docid in doc_ids[:2]:  # Fetch and summarize top 2 cases
            case_details = ikapi.fetch_doc(docid)
            if not case_details:
                continue
            title = case_details.get("title", "No Title")
            main_text = ikapi.clean_text(case_details.get("doc", ""))
            summary = ikapi.summarize(main_text)
            all_summaries.append(f"**Title:** {title}\n\n**Summary:** {summary}")

        combined_summary = "\n\n".join(all_summaries)
        response = query_ai_model(query, combined_summary)

        # Save chat history
        new_chat = {
            "query": query,
            "response": response,
            "summary": combined_summary,
        }
        st.session_state.chat_history.append(new_chat)
        save_chat_history(st.session_state.chat_history)

        st.session_state.selected_chat = len(st.session_state.chat_history) - 1  # Set last chat as selected

# ---------------- Display Chat History ----------------
if st.session_state.selected_chat is not None:
    selected_chat = st.session_state.chat_history[st.session_state.selected_chat]
    st.subheader("Query:")
    st.write(selected_chat["query"])
    st.subheader("AI Response:")
    st.write(selected_chat["response"])

# ---------------- End Main Content ----------------
st.markdown('</div>', unsafe_allow_html=True)
