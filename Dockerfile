FROM python:3.11-slim
LABEL maintainer=thomas@yager-madden.com

ENV QUERY_PATH=/cache/queue.json

RUN mkdir /app
RUN mkdir /cache
WORKDIR /app
VOLUME /cache
RUN touch /cache/queue.json

ADD . /app
RUN pip3 install -r requirements.txt

EXPOSE 5007

CMD ["gunicorn", "-b", "0.0.0.0:5007", "algoth:app", "--log-file=-"]
