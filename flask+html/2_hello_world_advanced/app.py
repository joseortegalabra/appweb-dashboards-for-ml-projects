import os
from flask import Flask, render_template
import pandas as pd



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
def create_dataframe_example():
    '''
    Crear un dataframe de ejemplo.
    Dataframe que va a ser mostrado en el front de una app web
    '''
    # crear tabla
    table = pd.DataFrame([
        ['alfa', 'Babilonia', 'Santiago'],
        ['beta', 'Egipto', 'Lima'],
        ['gamma', 'Sumeria', 'La Paz']
    ],
        columns = ['Letras griegas', 'Antiguas Civilizaciones', 'Capitales Latinoamérica']
    )
    return table

@app.route('/tables')
def print_df_to_html():
    '''
    Dado un dataframe que se quiere mostrar en el front.
    Transformarlo a formato HTML y utilizar bootstrap styling.

    Como la tabla está en formato HTML no puede ser insertado en otro archivo html, sino que se deben de concatenar (como si se estuvieran uniendo dos string)
    '''
    # obtener dataframe
    df = create_dataframe_example()

    # transformar df a html
    # df_html = df.to_html().replace('<table border="1" class="dataframe">','<table class="table table-striped">') # tabla más ancha que ocupa toda la página
    df_html = df.to_html()

    return render_template('tables.html', table_html = df_html)







# ------------------------------------------------------------ route: boxes_messages ------------------------------------------------------------
########### Se crea un conjunto de cajas para agregar mensajes en estas. Se utiliza el html template y además un css clásico

@app.route('/boxes_messages')
def boxes_messages():

    # crear diccionario con los mensajes
    msj1 = {'title':'TITULO PRUEBA 1',
            'content':'Contenido español'}
    
    msj2 = {'title':'TITLE TEST 2',
            'content':'Content english'}

    return render_template('boxes_messages.html', 
                           message1 = msj1, 
                           message2 = msj2
                           )





# ------------------------------------------------------------ route: boxes_kpis ------------------------------------------------------------
########### Se crea un conjunto de cajas para agregar valores en estas (principalmente kpis/métricas). Se utiliza el html template y además un css custom

def kpi1():
    '''
    Función que calcula kpi
    Retorna: nombre del kpi y su valor
    '''
    return {'name':'Nombre UNO', 'value': 10}

def kpi2():
    '''
    Función que calcula kpi
    Retorna: nombre del kpi y su valor
    '''
    return {'name':'Nombre DOS', 'value': 30}

def kpi3():
    '''
    Función que calcula kpi
    Retorna: nombre del kpi y su valor
    '''
    return {'name':'Nombre TRES', 'value': 5}

@app.route('/boxes_kpis')
def boxes_kpis():
    '''
    Toma los valores de los kpis y los deja en el formato para ser agregados al html
    '''
    dicc_kpi1 = kpi1()
    dicc_kpi2 = kpi2()
    dicc_kpi3 = kpi3()
    return render_template('boxes_kpis.html',
                           kpi1 = dicc_kpi1,
                           kpi2 = dicc_kpi2,
                           kpi3 = dicc_kpi3
                           )




# ------------------------------------------------------------ route: interaccion_usuario ------------------------------------------------------------
@app.route('/interactions_users')
def interacction_user():
    return "<h1>En construcción...</h1>"



# ------------------------------------------------------------ route: interaccion_usuario ------------------------------------------------------------
@app.route('/graph_plotly')
def graph_plotly():
    return "<h1>En construcción... Hay un ejemplo dedicado a crear gráficos de plotly</h1>"



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))