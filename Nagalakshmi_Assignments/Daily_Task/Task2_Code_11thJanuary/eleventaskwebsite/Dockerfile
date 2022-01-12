From python:3

WORKDIR /app

ENV MYSQL_URL_PATTERN = mysql://admin:Pass_123@python-flask.cdzu1re08efv.ap-south-1.rds.amazonaws.com/flask
ENV ACCESS_KEY = AKIAQQXY2KBDFHCBWY4J
ENV SECRET_KEY = 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

copy ./requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . ./

cmd python app.py