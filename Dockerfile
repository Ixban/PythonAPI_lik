
#FROM gcr.io/proy-vsp-sae-v15/gae-docker/py3/pyodbc:2020-06-03T1500
FROM gcr.io/proy-vsp-sae-v1-deploy-test-v1/gae-docker/py3/pyodbc:2020-06-03T1500

WORKDIR /app
ADD . /app
RUN python3 -m pip install -r requirements.txt

CMD gunicorn -t 600 -b :$PORT main:app 