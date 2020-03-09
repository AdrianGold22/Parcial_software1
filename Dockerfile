FROM python:3.6-buster 

RUN pip3 install Flask
RUN pip3 install flask_mysqldb
RUN pip3 install redis
RUN pip3 install pytz


RUN mkdir templates
RUN mkdir static
RUN apt update 

COPY app.py /
COPY templates/* /templates/
COPY static/* /static/

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0 