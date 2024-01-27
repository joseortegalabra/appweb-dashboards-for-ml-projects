import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz
import pandas as pd

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# update every 10 seg interval = (minutes) * (seconds) * 1000
st_autorefresh(interval = 10 * 1000, key="dataframerefresh")



# ------- GET ACTUAL TIME -------
def get_time_now():
    """
    Get actual time chile in time zone Chile and format: "%H:%M:%S %d/%m/%Y"
    """

    # get actual time chile
    chile_timezone = pytz.timezone('Chile/Continental')
    now = datetime.now(chile_timezone)
    format_time_chile = now.strftime("%H:%M:%S %d/%m/%Y")

    # obtener valores individuales
    time_now = now.strftime("%H:%M:%S")
    hour_now = now.strftime("%H")
    minute_now = now.strftime("%M")
    second_now = now.strftime("%S")

    # trasnformar a numeros
    hour_now = int(hour_now)
    minute_now = int(minute_now)
    second_now = int(second_now)

    return format_time_chile, time_now, hour_now, minute_now, second_now



# -------------------------- SHOW THE ACTUAL TIME IN A PLOTLY BARPLOT  --------------------------

def get_dataframe_time(hour_now, minute_now, second_now):
    '''
    Transform the value of time in a dataframe to plot it
    '''

    df_time = pd.DataFrame([
        ['hora', hour_now],
        ['minuto', minute_now],
        ['segundo', second_now]
    ],
    columns = ['variable', 'value']
    )

    return df_time


def plot_barplot(df):
    '''
    Do barplot with time
    '''
    # plot vertical barplot
    fig = px.bar(df, y='value', x='variable' , orientation='v', text_auto = True)

    # add values to barplot
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    # add tittle
    fig.update_layout(
      #height = 800,
      #width = 1000,
      title_text = 'Gráfico de barras',
      title_x = 0.5
    )

    # return fig plotly
    return fig




# ------- show information -------
if __name__ == "__main__":
    # Tittle app
    st.title("Example Auto refresh page - 1 seconds")

    # get the actual time chile
    actual_time_chile, time, hour, minute, second = get_time_now()


    # Subheader - actual time chile
    st.subheader(f"The time is: {actual_time_chile}")


    # Plot a barplot with the actual time
    df = get_dataframe_time(hour, minute, second)
    fig_barplot = plot_barplot(df)
    st.plotly_chart(fig_barplot)