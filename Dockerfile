FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY pheye.py /app

CMD ["python3", "pheye.py"]
