import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz

# update every 1 seg interval = (minutes) * (seconds) * 1000
st_autorefresh(interval = 1 * 1000, key="dataframerefresh")



# ------- calculations -------
# get actual time chile
chile_timezone = pytz.timezone('Chile/Continental')
actual_time = datetime.now(chile_timezone)
format_time = actual_time.strftime("%H:%M:%S %d/%m/%Y")



# ------- show information -------
# Give your app a title
st.title("Example Auto refresh page - 1 seconds")

# Subheader
st.subheader(f"The time is: {format_time}")