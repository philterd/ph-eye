FROM python:3.12.6-slim-bullseye AS model
RUN apt-get update && apt-get install -y git git-lfs
RUN git lfs install
RUN git clone https://huggingface.co/almanach/camembert-bio-gliner-v0.1 /tmp/model
RUN rm -rf /tmp/model/.git

FROM python:3.12.6-slim-bullseye

WORKDIR /app

ARG MODEL_NAME

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY --from=model /tmp/model /app/model

COPY app.py /app
COPY run.sh /app

ENV HF_HUB_DISABLE_TELEMETRY=1
ENV HF_HUB_OFFLINE=1
ENV DO_NOT_TRACK=1

CMD ["/app/run.sh"]
