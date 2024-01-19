FROM python:3.7.5-slim-buster
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn pandas numpy plotly google-cloud-bigquery db-dtypes Flask-Caching python-socketio==5.3.0

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
