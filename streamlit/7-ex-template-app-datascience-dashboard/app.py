import streamlit as st
from google.cloud import bigquery

import os
from dotenv import load_dotenv

import pytz
from datetime import datetime

import pandas as pd
import numpy as np

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly



################################# READ ENV VARIABLES - CREDENTIALS TO CONNECT TO BQ - saved in .env file #################################
load_dotenv()
env_var_project_gcp = os.environ.get("PROJECT_GCP", "")
env_var_path_sa = os.environ.get("PATH_SA", "")

PROJECT_ID = env_var_project_gcp
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_var_path_sa




################################# FUNTION SHOW ACTUAL TIME #################################

# actual time in chile timezone continental
def get_actual_time():
    """
    Get actual time chile in time zone Chile and format: "%H:%M:%S %d/%m/%Y"
    """
    chile_timezone = pytz.timezone('Chile/Continental')
    now = datetime.now(chile_timezone)
    format_time_chile = now.strftime("%H:%M:%S  %d/%m/%Y")
    return format_time_chile


################################# FUNCTION TO QUERY A DATAFRAME #################################
def GCPQuery2BigQuery(Project,InputQuery):
    """
    Execute query (string) given as input and return the output as a pandas dataframe

    Args:
        Project (string): project GCP
        InputQuery (string): query SQL string - bigquery

    Returns:
        df_results (dataframe): dataframe output of the query
    """
    client = bigquery.Client(project = Project)
    query_job = client.query(InputQuery)
    results = query_job.result()
    df_results = results.to_dataframe()
    return df_results



################################# FUNCTION TO GET COLOR OF A STRING ALERT #################################
def get_color_alerta_prediction(name_alert_prediction):
    """
    Given a string color of alert (low, medium, high // bajo, medio, alto) get a color to show in the app
    Map of colors:
    - bajo: green
    - medio: orange
    - alto: red

    Args:
        alert_prediction (string): name of the alert
    
    Returns:
        (string): color of the alert
    """
    if name_alert_prediction == "bajo":
        return "green"
    if name_alert_prediction == "medio":
        return "orange"
    if name_alert_prediction == "alto":
        return "red"


################################# XXXXX #################################
def identify_actual_alert_to_traffic_light(nivel_alert):
    """
    Auxiliar function feature 1.2 - traffic light actual level of alert. Identity the actual level of alert and generate an output for the traffic light plotly plot

    Output traffic light alerts
        colors = ['rgb(50, 50, 50)', 'orange', 'rgb(50, 50, 50)']
        sizes = [50, 75, 50]
    
    When it is turn off (no alert), the color take the values "rgb(50, 50, 50)" and the size of circle is "50"

    When it is turn on (alert), it take the values "green" and the size of circle is "75"
    """

    print('Actual level of alert: ', nivel_alert)

    # generar colors y size por defecto todo apagado. ORDEN: ['red', 'orange', 'green']
    colors = ['rgb(50, 50, 50)', 'rgb(50, 50, 50)', 'rgb(50, 50, 50)']
    sizes = [50, 50, 50]

    # encender (color y tamaño) del nivel de alerta actual
    if nivel_alert == "green":
        colors[2] = "green"
        sizes[2] = 75

    if nivel_alert == "orange":
        colors[1] = "orange"
        sizes[1] = 75

    if nivel_alert == "red":
        colors[0] = "red"
        sizes[0] = 75
        
    return colors, sizes

def make_plot_semaforo(nivel_alert):
    """
    Given the actual level of alert, make a traffic light with turn on the level of alert
    """
    #### get colors and size of the traffic light - this configuration change according to the color alert "green", "orange", "red"
    colors, sizes = identify_actual_alert_to_traffic_light(nivel_alert)

    # PARAMS
    x_coords = [0.5, 0.5, 0.5]
    y_coords = [0.8, 0.5, 0.2]
    values = [1, 2, 3]
    labels = ['Red', 'Yellow', 'Green']

    #Do plot
    texts = [f"{label}<br>Value: {value}" for label, value in zip(labels, values)]
    hoverinfos = ['text', 'text', 'text']

    fig = go.Figure()

    for i in range(3):
        fig.add_trace(
            go.Scatter(
                x=[x_coords[i]],
                y=[y_coords[i]],
                text=texts[i],
                hoverinfo=hoverinfos[i],
                mode='markers',
                marker=dict(
                    color=colors[i],
                    size=sizes[i],
                    line=dict(
                        color='black',
                        width=2
                    )
                )
            )
        )

    fig.update_layout(
        xaxis=dict(
            range=[0, 1],
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, 1],
            showticklabels=False,
            zeroline=False
        ),
        height=600,
        width=300,
        showlegend=False
    )
    return fig



################################# XXXXX #################################
def trend_true_vs_predicted(df, save_json = False):
    """
    Graficar real vs predicho
    """
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
     
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['Value_prediction'], mode='lines', name='Valor predicho', line=dict(color='blue', width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['Value_true'], mode='lines', name='Valor real', line=dict(color='grey', width=3)), row=1, col=1)

    fig.update_layout(
        title='Tendencia Kappa real vs Predicho (últimas 8 horas)',
        xaxis_title='Fecha y hora',
        yaxis_title='Valor',
        yaxis_title_standoff=30, # ajustar el valor según la distancia deseada
        height=600, 
        width=1000,
        title_x=0.5
    )

    # show plot - desactivado porque sino abre el plot en otra pestaña
    # fig.show()
    
    # json to html
    if save_json == True:
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON



################################# XXXXX #################################






if __name__ == "__main__":
    st.header("Example dashboard app that show the result of a ML model running in other cloud service")


    # show actual time
    time_now = get_actual_time()
    st.write(f"Actual timezone: {time_now}")


    ########### FEATURE 1 - INFO PREDICTION ACTUAL ###########

    # query table instance_predictions
    query_instance_prediction = f"""SELECT * FROM `cmpc-innovation-cd4ml-test.template_research_and_development_mvp_stacking.front_instance_predictions`"""
    table_instance_predictions = GCPQuery2BigQuery('cmpc-innovation-cd4ml-test', query_instance_prediction)

    # feature 1.1 info prediction actual
    FECHA_ULTIMA_ACTUALIZACION = table_instance_predictions['datetime'][0].strftime('%Y-%m-%d %H:%M:%S')
    FECHA_PREDICCION = table_instance_predictions['datetime_forecast'][0].strftime('%Y-%m-%d %H:%M:%S')
    VALOR_PREDICCION = np.round(table_instance_predictions['Value_prediction'].values[0], 2)
    ALERTA_PREDICCION = table_instance_predictions['Alert_prediction'].values[0]
    COLOR_ALERTA_PREDICCION = get_color_alerta_prediction(ALERTA_PREDICCION)

    # feature 1.2 traffic light -> alert actual prediction
    FIG_TRAFFIC_LIGHT = make_plot_semaforo(nivel_alert = COLOR_ALERTA_PREDICCION)



    ########### FEATURE 2 - TRENDS ###########

    # query tables tendency_predictions
    query_tendency_predictions = f"""
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.template_research_and_development_mvp_stacking.front_tendency_predictions`
    order by datetime asc
    """
    table_tendency_predictions = GCPQuery2BigQuery('cmpc-innovation-cd4ml-test', query_tendency_predictions)


    # feature 2.1 graficar tendencia numérica real vs predicho
    FIG_TREND_TRUE_VS_PRED = trend_true_vs_predicted(df = table_tendency_predictions)

    
    # feature 2.2 graficar tendencia alertas generadas
    FIG_TREND_BARPLOT_ALERTS = tendencia_alertas_predichas(df = table_tendency_predictions)
    