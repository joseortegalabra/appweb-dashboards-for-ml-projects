import os
from flask import Flask, render_template
import pandas as pd
from google.cloud import bigquery

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



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))