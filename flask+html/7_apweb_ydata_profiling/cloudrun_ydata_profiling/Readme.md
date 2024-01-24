# Ydata-profiling en cloud run

En este repo se muestra como hacer una simple app web alojada en cloud run que permite hacer un perfilamiento/EDA básico de los datos utilizando ydata-profiling (antes llamado pandas profiling)


### Deploy en cloud run
Correr Notebook "deploy.ipynb"


### Prueba local
En este paso se procede a probar localmente la app web y verificar que funciona todo bien. 
Importante: cada vez que se hace un cambio hay que “cerrar el server” y volver a correr flask para poder visualizar en la UI el cambio hecho en los códigos
Para probar localmente utilizando anaconda se procede a hacer lo siguiente:
- Abrir terminal de anaconda
- Pararse en la carpeta donde está el script “app.py”.En mi caso
	- d:
	- cd [path]

- Correr líneas de códigos para ver la app en local (reemplazar export de linux por set de windows). En mis pruebas solo fue necesario correr la última línea para probar localmente “flask run”
        	- set FLASK_APP=app
        	- set FLASK_ENV=development
        	- flask run

- La app corre localmente en la URL. En la consola también indica esta url, solo basta con copiar (control + Y) y pegar en el navegador
http://127.0.0.1:5000/
