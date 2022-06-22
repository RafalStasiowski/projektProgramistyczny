#FROM python:3.8-slim-buster
#
#WORKDIR /app
#
#
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#
#COPY . .
#ENV FLASK_APP='app.py'
##CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#EXPOSE 5000
#CMD gunicorn main:app
FROM python:3.8


WORKDIR /

COPY . .

RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:app