FROM python:3.12.6-slim-bullseye

WORKDIR /app

ARG MODEL_NAME

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY download-model.py /app
RUN python3 /app/download-model.py

COPY app.py /app
COPY run.sh /app

ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HUB_OFFLINE=1
ENV DO_NOT_TRACK=1

CMD ["/app/run.sh"]
