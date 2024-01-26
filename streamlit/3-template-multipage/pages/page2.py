import streamlit as st
from datetime import datetime


# ---------------------------- SET SESSION STATE TO AVOID THE RESET WHEN THE USER SWITCH BETWEEN PAGES ----------------------------
# sources: https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app
st.session_state['text_page_main'] = st.session_state['text_page_main']
st.session_state['number_page_main'] = st.session_state['number_page_main']
st.session_state['text_page_3'] = st.session_state['text_page_3']


st.write("#### PAGE 2")


# ---------------------------- Write text unique for page 2 ----------------------------
text_page2 = st.text_input("Save a string in page two - local variable", placeholder="Write you answer")
st.write(f"Text save page 2: {text_page2}")


# ---------------------------- Show a all session states ----------------------------
st.divider()
st.divider()
st.write("### Show all session states")
st.write(st.session_state)