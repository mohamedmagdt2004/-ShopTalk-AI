import streamlit as st

def normalize_question(question):

    return question.lower().strip()

def save_cache(question, result):

    key = normalize_question(question)

    if "cache" not in st.session_state:
        st.session_state.cache = {}

    st.session_state.cache[key] = result

def get_cache(question):

    key = normalize_question(question)

    if "cache" not in st.session_state:
        st.session_state.cache = {}

    return st.session_state.cache.get(key)
    if "cache_hits" not in st.session_state:
        st.session_state.cache_hits = 0