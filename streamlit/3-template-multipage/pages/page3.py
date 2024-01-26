import streamlit as st
from datetime import datetime


# ---------------------------- SET SESSION STATE TO AVOID THE RESET WHEN THE USER SWITCH BETWEEN PAGES ----------------------------
# sources: https://stackoverflow.com/questions/74968179/session-state-is-reset-in-streamlit-multipage-app
st.session_state['text_page_main'] = st.session_state['text_page_main']
st.session_state['number_page_main'] = st.session_state['number_page_main']
st.session_state['text_page_3'] = st.session_state['text_page_3']


st.write("#### PAGE 3")
######## TEST PAGE 3 - SAVE SESSION STATE HERE TOO. To see if the value of the variables are lost or no


# ---------------------------- Write text unique for page 3 ----------------------------
st.text_input("Save a string in page tree - session state", placeholder="Write a text", key = 'text_page_3')
st.write(f"Text save page 3: {st.session_state['text_page_3']}")



# ---------------------------- Show a all session states ----------------------------
st.divider()
st.divider()
st.write("### Show all session states")
st.write(st.session_state)