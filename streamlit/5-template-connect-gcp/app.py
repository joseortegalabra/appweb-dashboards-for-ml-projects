import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os
from dotenv import load_dotenv



# READ ENV VARIABLES - CREDENTIALS TO CONNECT TO BQ
load_dotenv()
env_var_project_gcp = os.environ.get("PROJECT_GCP", "")
env_var_path_sa = os.environ.get("PATH_SA", "")

PROJECT_ID = env_var_project_gcp
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env_var_path_sa



########### read table from bq
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


########### show table
st.write("#### SHOW TABLE BIG QUERY")
df_table_to_show = get_dataframe_from_bq()
st.dataframe(df_table_to_show)