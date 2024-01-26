import streamlit as st
from datetime import datetime

#### SOURCES: https://docs.streamlit.io/library/advanced-features/multipage-apps


# ------- calculations -------
# get actual time
actual_time = datetime.now()
format_time = actual_time.strftime("%H:%M:%S %d/%m/%Y")



# ------- show information -------
# Give your app a title
st.title("Hello World update streamlit")

# Header
st.header("Hello World update streamlit")

# Subheader
st.subheader(f"The time is: {format_time}")