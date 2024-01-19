import os
import json
import time
import datetime

from flask import Flask, render_template, Response, request, stream_with_context, redirect, url_for, session
from flask_caching import Cache
from google.cloud import bigquery

import pandas as pd
import numpy as np

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from queue import Queue



""" Read env variables """
env_var_project_gcp = os.environ.get("PROJECT_GCP", "")
env_var_path_sa = os.environ.get("PATH_SA", "")

# SET SERVICE ACCOUNT GCP AND PROJECT
PROJECT_ID = env_var_project_gcp
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_var_path_sa



# PARÁMETROS tablas bigquery
DATASET_ID_DS = '6_hello_world_refresh_observer'
TABLE_BQ_UPDATE_TRACKING = '_param_tracking_update'



# inicializar flask app
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})



# -------------------------------------------- MOSTRAR LA HORA ACTUAL EN LA APP WEB Y SE ACTUALIZE CADA SEGUNDO EN BASE A EVENTOS ( EventSource() )   --------------------------------------------
@app.route('/actual_time')
def events():
    def generate():
        while True:
            data = f'The time is {time.strftime("%H:%M:%S")}'
            yield f'data: {data}\n\n'
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')






# --------------------------------------------   ACTUALIZAR PÁGINA MIRANDO "OBSERVER" REVISAR SI UNA VARIABLE SE ACTUALIZA   --------------------------------------------
def get_last_update_bq_tracking_update():
    '''
    Obtener un dataframe desde una consulta SQL a la tabla de update tracking
    '''

    # leer tabla de bq
    query_sql = f'''SELECT * FROM `{PROJECT_ID_DS}.{DATASET_ID_DS}.{TABLE_BQ_UPDATE_TRACKING}`'''
    client = bigquery.Client(project = PROJECT_ID_DS)

    # Obtener ultima fecha de actualización. Hacer un try/except donde en el except hay un "indexerror" porque no hay datos y hacer un retry después de 30 segundos. 
    while True:
        try:
            df = client.query(query_sql).to_dataframe()
            latest_update = df['ultima_actualizacion'].values[0]
        except: #IndexError
            time.sleep(15)
        else:
            break
    return latest_update


@app.route('/events')
def observer():
    def generate_refresh_custom():
        while True:
            
            # leer tabla de bq y obtener fecha ultima actualización BQ
            latest_update_bq = get_last_update_bq_tracking_update()

            # inicializar cache (ultima fecha de actualizacion de bq)
            if cache.get('latest_update') == None:
                print('Inicializar cache con la última fecha de actualización de update tracking de BQ')
                cache.set('latest_update', latest_update_bq)
                print('CACHE_ULTIMA_ACTUALIZACION: ', latest_update_bq)

            # obtener ultima fecha actualizacion en el cache
            latest_update_cache = cache.get('latest_update')
            
            # comparar el cache app es distinto de la tabla de bq --> actualizar front
            if latest_update_cache != latest_update_bq:
                print('se ha actualizado el backend')
                
                # actualizar cache
                cache.delete('latest_update')
                cache.set('latest_update', latest_update_bq)
                print('CACHE_ULTIMA_ACTUALIZACION: ', latest_update_bq)
                
                # actualizar front
                yield 'data: refresh_page\n\n'
                print('observer: UPDATE')

            else:
                yield 'data: otro_mensaje\n\n'
                print('observer: NO update')

            time.sleep(60*2) #en segundos
    return Response(generate_refresh_custom(), mimetype='text/event-stream')





# -------------------------- CÓDIGO PARA APP: PÁGINA QUE SE MUESTRA LA HORA ACTUAL Y HACE UN GRÁFICO DE BARRAS CON LA HORA CADA VEZ QUE SE EJECUTA  --------------------------
def get_time_now():
    '''
    Obtener la hora actual
    '''
    # now
    now = datetime.datetime.now()
    
    # obtener valores individuales
    time_now = now.strftime("%H:%M:%S")
    hour_now = now.strftime("%H")
    minute_now = now.strftime("%M")
    second_now = now.strftime("%S")
    
    # trasnformar a numeros
    hour_now = int(hour_now)
    minute_now = int(minute_now)
    second_now = int(second_now)
    
    return time_now, hour_now, minute_now, second_now


def get_dataframe_time(hour_now, minute_now, second_now):
    '''
    transformar los valores a un dataframe para posteriormente ser ploteados
    '''

    df_time = pd.DataFrame([
        ['hora', hour_now],
        ['minuto', minute_now],
        ['segundo', second_now]
    ],
    columns = ['variable', 'value']
    )
    
    return df_time


def barplot(df, save_json = False):
    '''
    Hacer gráfico de barras
    '''

    # plot grafico de barras vertical
    fig = px.bar(df, y='value', x='variable' , orientation='v', text_auto = True)

    # agregar valores de las barras
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    # agregar título y tamaño gráfico
    fig.update_layout(
      #height = 800,
      width = 1000,
      title_text = 'Gráfico de barras',
      title_x = 0.5
    )

    # show plot
    #fig.show()
    
    # json to html
    if save_json == True:
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON


@app.route('/', methods=['GET', 'POST'])
def show_time_actual():
    '''
    Mostrar la hora actual y en un gráfico de barras de plotly de 3 barras donde se muestran en cada barra hora, minuto y segundo respectivamente (esto para poder validar
    que un gráfico de plotly se pueda refrescar y utilizar un gráfico de barras que muestra la hora actual es un buen ejemplo para representar un backend que se está actualizando
    constamente)
    '''

    # obtener la hora actual
    time, hour, minute, second = get_time_now()

    # transformar hora actual a dataframe para ser ploteado en un gráfico de barras
    df = get_dataframe_time(hour, minute, second)

    # obtener json con el gráfico para insertarlo en web page
    json_plot = barplot(df, save_json = True)


    return render_template('refresh.html', time_actual = time, json_plot_time = json_plot)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))