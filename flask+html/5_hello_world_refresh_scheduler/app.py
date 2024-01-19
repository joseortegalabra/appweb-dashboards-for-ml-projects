import os
import json
import time

from flask import Flask, render_template, Response, request

import pandas as pd
import numpy as np


import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime



# flask app
app = Flask(__name__)



# -------------------------- MOSTRAR LA HORA ACTUAL EN LA APP WEB Y SE ACTUALIZE CADA SEGUNDO EN BASE A EVENTOS ( EventSource() )   --------------------------
@app.route('/actual_time')
def events():
    def generate():
        while True:
            data = f'The time is {time.strftime("%H:%M:%S")}'
            yield f'data: {data}\n\n'
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')






# -------------------------- PÁGINA QUE SE MUESTRA LA HORA ACTUAL Y HACE UN GRÁFICO DE BARRAS CON LA HORA CADA VEZ QUE SE EJECUTA  --------------------------
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



@app.route('/', methods=['GET', 'POST'])  # https://stackoverflow.com/questions/61058754/method-not-allowed-for-requested-url
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