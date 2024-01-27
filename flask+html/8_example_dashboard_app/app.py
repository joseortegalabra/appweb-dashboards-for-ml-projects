import os
from flask import Flask, render_template, Response, request
import time

import pandas as pd
from google.cloud import bigquery
from datetime import datetime
import numpy as np
import json

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly




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






# -------------------------- GENERAR DATOS PARA SER ENVIADOS AL FRONT  --------------------------
""" funciones auxiliares consultar bq """
def GCPQuery2BigQuery(Project,InputQuery):
    """
    Función auxiliar para consultar una tabla de BQ y obtener un dataframe. Utiliza la función "query_bq_to_dataframe" donde existe un while infinito para hacer la consulta hasta que se obtenga un dataframe
    no vacio (tenga al menos una fila) o hasta que se obtenga un error por timeout en la ejeución del código en una cloud function

    Args:
        Project (string): proyect de GCP
        InputQuery (string): query SQL

    Returns:
        dataframe: dataframe resultante de la query
    """

    count_consultas_fallidas = 0
    delay = 5

    # -- do while --
    # ---> do: consultar data
    df_result = query_bq_to_dataframe(Project, InputQuery)
    
    # while: mientras data obtenida este vacia, seguir ejecutando consultar data
    while df_result.shape[0] == 0:
        time.sleep(delay)
        df_result = query_bq_to_dataframe(Project, InputQuery)
        count_consultas_fallidas += 1

    return df_result

def query_bq_to_dataframe(Project,InputQuery):
    """
    Ejecutar la query (string) pasada como input y retornar el resultado como un dataframe

    Args:
        Project (string): projecto de GCP
        InputQuery (string): string con la query

    Returns:
        dataframe: dataframe resultante de la query
    """
    client = bigquery.Client(project = Project)
    query_job = client.query(InputQuery)
    results = query_job.result()
    results = results.to_dataframe()
    return results


""" funciones auxiliares cálculos """
def get_color_alerta_prediction(alerta_prediction):
    """
    Dado el nivel de alerta de la predicción (bajo, medio, alto) obtener un color para ser mostrado en la app
    Mapeo de colores:
    - bajo: green
    - medio: orange
    - alto: red
    """
    if alerta_prediction == "bajo":
        return "green"
    if alerta_prediction == "medio":
        return "orange"
    if alerta_prediction == "alto":
        return "red"


""" funciones auxiliares feature 1.2 - semaforo alerta prediccion actual """
def identificar_alerta_actual_para_semaforo(nivel_alerta):
    """
    Identificar alerta actual (green, orange, red) y generar output para semáforo
    
    Output semáforo:
        colors = ['rgb(50, 50, 50)', 'orange', 'rgb(50, 50, 50)']
        sizes = [50, 75, 50]
        
    Cuando está apagado color toma los valores "rgb(50, 50, 50)" y el tamaño de la esfera es "50"
    Cuando está encendido color toma los valores "green" (nombre del color encendido) y el tamaño de la esfera es "75"
    """
    
    print('NIVEL DE ALERTA ACTUAL: ', nivel_alerta)

    # generar colors y size por defecto todo apagado. ORDEN: ['red', 'orange', 'green']
    colors = ['rgb(50, 50, 50)', 'rgb(50, 50, 50)', 'rgb(50, 50, 50)']
    sizes = [50, 50, 50]

    # encender (color y tamaño) del nivel de alerta actual
    if nivel_alerta == "green":
        colors[2] = "green"
        sizes[2] = 75

    if nivel_alerta == "orange":
        colors[1] = "orange"
        sizes[1] = 75

    if nivel_alerta == "red":
        colors[0] = "red"
        sizes[0] = 75
        
    return colors, sizes

def make_plot_semaforo(nivel_alerta, save_json = False):
    """
    Dado el nivel de alerta, hacer un semáforo que esté encendido de acuerdo al grado de alerta
    """
    
    #### OBTENER COLORS Y SIZES DEL SEMÁFORO - ESTA CONFIGURACIÓN VARIA DE ACUERDO AL COLOR DE ALERTA "green, orange, red"
    colors, sizes = identificar_alerta_actual_para_semaforo(nivel_alerta)

    
    # PARAMS
    x_coords = [0.5, 0.5, 0.5]
    y_coords = [0.8, 0.5, 0.2]
    values = [1, 2, 3]
    labels = ['Red', 'Yellow', 'Green']


    #HACER GRAFICO
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
    
    # show plot - desactivado porque sino abre el plot en otra pestaña
    # fig.show()
    
    # json to html
    if save_json == True:
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON


""" funciones auxiliares feature 2.1 - graficar tendencia numérica real vs predicho """
def tendencia_real_vs_predicho(df, save_json = False):
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


""" funciones auxiliares feature 2.2 - graficar tendencia alertas generadas """
def tendencia_alertas_predichas(df, save_json = False):
    """
    Hacer un gráfico de barras para representar la tendencia de las diferentes predicciones de alertas: bajo, medio, alto
    """

    """ definir params """

    # parámetros mapeo colores (bajo, medio, alto) (green, orange, red), (1,2,3)
    colors = {'bajo': 'green', 'medio': 'orange', 'alto': 'red'}
    number = {'bajo': 1, 'medio': 2, 'alto': 3}


    # obtener los valores únicos de las predicciones (por ejemplo que solo hallan prediciones bajo y no medio ni alto)
    alertas_unicas_generadas = df['Alert_prediction'].unique()

    # filtrar los parámetros de mapeo de acuerdo a los valors únicos predichos
    # por ejemplo si en las predicciones solo hay valores "bajo" y "alto", el valor "medio debe de borrarse de los params"
    colors = {clave: valor for clave, valor in colors.items() if clave in alertas_unicas_generadas}
    number = {clave: valor for clave, valor in number.items() if clave in alertas_unicas_generadas}
    cat_order = list(colors.keys())


    """ transformaciones a los datos - de acuerdo a los params """

    # Convertir la columna "Alert_prediction" en tipo categórico con un orden específico
    df['Alert_prediction'] = pd.Categorical(df['Alert_prediction'], categories=cat_order, ordered=True)

    ## Crear la columna "Bar_size" con el tamaño de las barras
    df['Bar_size'] = df['Alert_prediction'].map(number)



    ########################################################################################################################
    # Crear el gráfico de barras
    fig = px.bar(df, x='datetime', y='Bar_size', color='Alert_prediction', barmode='stack', color_discrete_map=colors)

    # Establecer el orden deseado en el eje y
    fig.update_layout(title='Tendencia de Alertas Generadas',
                      xaxis_title='Fecha y hora',
                      yaxis_title='Frecuencia',
                      yaxis=dict(categoryorder='array', categoryarray=cat_order, tickvals=list(range(1, len(cat_order)+1)), ticktext=cat_order),
                      title_x=0.5
                     )

    # show plot - desactivado porque sino abre el plot en otra pestaña
    #fig.show()


    # json to html
    if save_json == True:
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON





""" ENVIAR INFORMACION A FRONT """
@app.route('/', methods=['GET', 'POST'])  # https://stackoverflow.com/questions/61058754/method-not-allowed-for-requested-url
def generate_data_to_front():
    """
    Generar todos los datos que son enviados al front. El front es el template html "principal.html" y se tienen que definir todas las variables 
    que deben de ser enviadas al front.
    """

    """ FEATURE 1 - INFO PREDICCIÓN ACTUAL """

    # consultar tabla instance_predictions
    query_instance_prediction = f"""
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.template_research_and_development_mvp_stacking.front_instance_predictions` 
    """
    table_instance_predictions = GCPQuery2BigQuery('cmpc-innovation-cd4ml-test', query_instance_prediction)

    # feature 1.1 info predicción actual
    FECHA_ULTIMA_ACTUALIZACION = table_instance_predictions['datetime'][0].strftime('%Y-%m-%d %H:%M:%S')
    FECHA_PREDICCION = table_instance_predictions['datetime_forecast'][0].strftime('%Y-%m-%d %H:%M:%S')
    VALOR_PREDICCION = np.round(table_instance_predictions['Value_prediction'].values[0], 2)
    ALERTA_PREDICCION = table_instance_predictions['Alert_prediction'].values[0]
    COLOR_ALERTA_PREDICCION = get_color_alerta_prediction(ALERTA_PREDICCION)

    # feature 1.2 semáforo alerta predicción actual
    JSON_SEMAFORO_ALERTA = make_plot_semaforo(nivel_alerta = COLOR_ALERTA_PREDICCION, 
                                            save_json = True)


    """ FEATURE 2 - TENDENCIAS """
    # consultar tabla tendency_predictions
    query_tendency_predictions = f"""
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.template_research_and_development_mvp_stacking.front_tendency_predictions`
    order by datetime asc
    """
    table_tendency_predictions = GCPQuery2BigQuery('cmpc-innovation-cd4ml-test', query_tendency_predictions)

    # feature 2.1 graficar tendencia numérica real vs predicho
    JSON_TENDENCIA_REAL_PREDICHO = tendencia_real_vs_predicho(df = table_tendency_predictions,
                                                            save_json = True)
    
    # feature 2.2 graficar tendencia alertas generadas
    JSON_TENDENCIA_ALERTAS = tendencia_alertas_predichas(df = table_tendency_predictions,
                                                    save_json = True)


    return render_template('principal.html',
                           FECHA_ULTIMA_ACTUALIZACION = FECHA_ULTIMA_ACTUALIZACION, 
                           FECHA_PREDICCION = FECHA_PREDICCION,
                           VALOR_PREDICCION = VALOR_PREDICCION,
                           ALERTA_PREDICCION = ALERTA_PREDICCION,
                           JSON_SEMAFORO_ALERTA = JSON_SEMAFORO_ALERTA,
                           JSON_TENDENCIA_REAL_PREDICHO = JSON_TENDENCIA_REAL_PREDICHO,
                           JSON_TENDENCIA_ALERTAS = JSON_TENDENCIA_ALERTAS
                           )





if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))