FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get install -y gunicorn
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/