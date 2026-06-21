FROM python:3.12.6-slim-bullseye

WORKDIR /app

ARG PHEYE_MODEL=pii_en_small
ENV PHEYE_MODEL=${PHEYE_MODEL}

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY models/ /app/models/
COPY download_model.py /app
RUN python3 /app/download_model.py

COPY app.py /app
COPY run.sh /app

ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HUB_OFFLINE=1
ENV DO_NOT_TRACK=1

CMD ["/app/run.sh"]
