FROM python:3.8

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

WORKDIR /app