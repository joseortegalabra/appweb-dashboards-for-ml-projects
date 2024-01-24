import os
from flask import Flask, request, redirect, url_for, render_template, make_response
import pandas as pd
from ydata_profiling import ProfileReport

# flask app
app = Flask(__name__)


# ------------------------------------------------------------ Main Route. Index Page ------------------------------------------------------------
@app.route('/')
def index_links_pages():
    return render_template('index.html')



# ------------------------------------------------------------ Realizar perfilamiento a los datos ------------------------------------------------------------
def read_data(filename):
    """
    Función que trata de leer los datos. Acepta formato csv, pkl y excel. Si no funciona ninguno retorna un dataframe vació
    """
    try:
        df = pd.read_csv(filename)
        print('\n-------- data csv --------\n')
    except:
        try:
            df = pd.read_pickle(filename)
            print('\n-------- data pickle --------\n')
        except:
            try:
                df = pd.read_excel(filename)
                print('\n-------- data excel --------\n')
            except:
                print("\n-------- Error: no se pudo leer ningún archivo.--------\n")
                return pd.DataFrame()
    return df

@app.route('/generate_report')
def generate_report():
    return render_template('generate_report.html')


@app.route('/profiling_1', methods=['POST'])
def profiling_1():
    """
    Realizar profiling de un dataset
    """
    # leer dataframe
    filename = request.files['file']
    data = read_data(filename)

    # generar un report estandar de profiling (si el tamaño del dataset supera cierto límite el reporte generado es minimal generando solo los análisis con poco costo computacional)
    limit_minimal = 5000
    if data.shape[0]<limit_minimal:
        profile = ProfileReport(data, title = "Profiling Report")
    else:
        profile = ProfileReport(data, title = "Profiling Report", minimal=True)
    
    # generar respuesta con el reporte html y descargar automáticamente html generado (HTTP se configura como un archivo adjunto (attachment) con el nombre "report.html")
    profile_html = profile.to_html()
    response = make_response(profile_html)
    response.headers.set('Content-Disposition', 'attachment', filename='report.html')
    return response


@app.route('/profiling_2', methods=['POST'])
def profiling_2():
    """
    Realizar profiling de dos datasets comparándoselos (train vs test // antes vs después limpieza)
    """
    # leer dataframe
    filename_one = request.files['file_one']
    filename_two = request.files['file_two']
    data_one = read_data(filename_one)
    data_two = read_data(filename_two)


    # generar un report estandar de profiling (si el tamaño del dataset supera cierto límite el reporte generado es minimal generando solo los análisis con poco costo computacional)
    # generar reportes individuales para cada dataset y luego generar un reporte comparando ambos datasets
    limit_minimal = 5000
    if data_one.shape[0]<limit_minimal:
        data_one_report = ProfileReport(data_one, title = "Data One")
        data_two_report = ProfileReport(data_two, title = "Data Two")
    else:
        data_one_report = ProfileReport(data_one, title = "Data One", minimal=True)
        data_two_report = ProfileReport(data_two, title = "Data Two", minimal=True)
    
    comparison_report = data_one_report.compare(data_two_report)

    # generar respuesta con el reporte html y descargar automáticamente html generado (HTTP se configura como un archivo adjunto (attachment) con el nombre "report.html")
    comparison_report = comparison_report.to_html()
    response = make_response(comparison_report)
    response.headers.set('Content-Disposition', 'attachment', filename='report_comparison.html')
    return response

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))