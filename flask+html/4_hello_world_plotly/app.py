import os
import json
from flask import Flask, render_template

import pandas as pd
import numpy as np

from google.cloud import bigquery

import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


""" Read env variables """
env_var_project_gcp = os.environ.get("PROJECT_GCP", "")
env_var_path_sa = os.environ.get("PATH_SA", "")


# SET SERVICE ACCOUNT GCP AND PROJECT
PROJECT_ID = env_var_project_gcp
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_var_path_sa




# ------------------------------------------------------------ Main Route. Index Page ------------------------------------------------------------
# flask app
app = Flask(__name__)

@app.route('/')
def index_links_pages():
    return render_template('index.html')


# ------------------------------------------------------------ route: about ------------------------------------------------------------
########### Se pasa un template html y una variable para agregar al html
@app.route('/about')
def about():
    '''
    Para pruebas, enviar un string desde la API para ser mostrado en el front
    '''
    programming_languages = 'Python (Flask) y HTML'
    return render_template('about.html', message = programming_languages)



# ------------------------------------------------------------ route: tables ------------------------------------------------------------
########### Se crea un dataframe de pandas y este dataframe se muestra en el template html
def get_dataframe_from_bq():
    '''
    Obtener un dataframe desde una consulta SQL a una tabla de Bigquery
    Dataframe que va a ser mostrado en el front de una app web
    '''

    #query
    query_sql = '''
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.dataset_for_tests.table_1`
    ORDER BY date DESC
    '''

    # consultar
    client = bigquery.Client(project = PROJECT_ID)
    df = client.query(query_sql).to_dataframe()

    return df


@app.route('/tables')
def print_df_to_html():
    '''
    Dado un dataframe que se quiere mostrar en el front.
    Transformarlo a formato HTML
    Como la tabla está en formato HTML no puede ser insertado en otro archivo html, sino que se deben de concatenar (como si se estuvieran uniendo dos string)
    '''

    # obtener dataframe
    df = get_dataframe_from_bq()

    # transformar df a html
    df_html = df.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # tabla más ancha que ocupa toda la página

    return render_template('tables.html', table_html = df_html)



# ------------------------------------------------------------ route: plotly_1 ------------------------------------------------------------
def get_dataframe_barplot():
    '''
    Obtener dataframe de ejemplo con datos para hacer un gráfico de barras.
    Consultar los datos almacenados en una tabla de BQ
    '''
    #query
    query_sql = '''
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.dataset_for_tests.table_barplot`
    '''

    # consultar
    client = bigquery.Client(project = PROJECT_ID)
    df_bar_plot = client.query(query_sql).to_dataframe()

    return df_bar_plot

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


@app.route('/plotly_1')
def do_1_plot():
    '''
    Graficar 1 gráfico de plotly
    En este ejemplo se llaman las funciones que hacen un gráfico de barras
    '''
    # obtener datos
    df_bar_plot = get_dataframe_barplot()

    # obtener json del gráfico de barras
    json_bar_plot = barplot(df = df_bar_plot,
                            save_json = True)

    return render_template('plotly_1.html', json_plot = json_bar_plot)







# ------------------------------------------------------------ route: plotly_2 ------------------------------------------------------------
def read_dataframe_lineplot():
    '''
    Leer dataframe para gráfico de lineas
    - valor real
    - valor predicho
    - valor tag auxiliar ayuda a la predicción
    '''
    #query
    query_sql = '''
    SELECT * 
    FROM `cmpc-innovation-cd4ml-test.dataset_for_tests.table_forecast_data`
    '''

    # consultar
    client = bigquery.Client(project = PROJECT_ID)
    df = client.query(query_sql).to_dataframe()

    return df

def plot_forecast_with_auxiliar_variable(df, save_json = False):
    '''
    Graficar forecast de la forma tendencia del valor y luego continuar con la predicción.
    
    Se hace el formato de subplots para agregar la tendencia de un valor auxiliar en un subplot.
    '''
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # graficar eje primario - valores true
    fig.add_trace(
        go.Scatter(x = df['datetime'], 
                   y = df['true'], 
                   name = "True values"
                  ),
        secondary_y = False
    )

    # graficar eje primario - predicciones
    fig.add_trace(
        go.Scatter(x = df['datetime'], 
                   y = df['predicted'], 
                   name = "Predicted Values",
                   line = {'dash':'dot'},
                  ),
        secondary_y = False
    )

    # graficar eje secundario - valores auxiliares
    fig.add_trace(
        go.Scatter(x = df['datetime'], 
                   y = df['auxiliar'], 
                   name = "Auxiliar Values"
                  ),
        secondary_y = True
    )

    # agregar línea separación
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0 = 'viernes', x1 = 'viernes',
        yref='paper', # al setear paper puedo definir las posiciones en terminos relativos al tamaño del grafico. https://stackoverflow.com/questions/60907004/plotly-how-to-add-a-horizontal-line-to-a-line-graph
        y0 = 0, y1 = 1
    )

    # Titulo del gráfico
    fig.update_layout(
        title_text = "Gráfico de valor real y predicho (junto con graficar tag auxiliar)"
    )

    # Set x-axis title
    fig.update_xaxes(title_text = "Fecha")

    # Set y-axes titles
    fig.update_yaxes(title_text = "Eje Primario - Tag Principal", secondary_y=False)
    fig.update_yaxes(title_text="Eje Secundario - Tag Auxiliar", secondary_y=True)
    
    # show plot
    #fig.show()
    
    # json to html
    if save_json == True:
        graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
        return graphJSON



@app.route('/plotly_2')
def do_2_plot():
    '''
    Graficar 2 gráficos de plotly
    - Gráfico de barras (mismo del punto anterior)
    - Gráfico de scatter
    '''
    
    #################################### GRAFICO BAR PLOT ####################################
    # obtener datos
    df_bar_plot = get_dataframe_barplot()

    # obtener json del gráfico de barras
    json_bar_plot = barplot(df = df_bar_plot,
                            save_json = True)


    #################################### GRAFICO SCATTER PLOT ####################################
    # leer data
    df_scatter_plot = read_dataframe_lineplot()

    # para graficar la unión entre los valores reales y predicho - el valor previo al primer valor de la predicción 
    # se le debe asignar el valor real. HARCODEADO PARA FACILITAR EL EJEMPLO
    ultimo_valor_real = df_scatter_plot[df_scatter_plot['datetime'] == 'viernes']['true'].values[0]
    df_scatter_plot.loc[df_scatter_plot['datetime'] == 'viernes', 'predicted'] = ultimo_valor_real

    # obtener json del gráfico
    json_scatter_plot = plot_forecast_with_auxiliar_variable(df = df_scatter_plot,
                                                    save_json = True)

    return render_template('plotly_2.html', json_bar_plot = json_bar_plot, json_scatter_plot = json_scatter_plot)




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))