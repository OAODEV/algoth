FROM alpine:latest
MAINTAINER yagermadden@gmail.com

RUN apk update && apk add \
    python3 \
    python3-dev

RUN mkdir /app
WORKDIR /app
VOLUME /cache

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN rm -rf /var/cache/apk/* \
    && rm -rf /tmp/*

ADD cut-rate.py /app/
ADD templates/ /app/templates
ADD entry.sh /tmp/entry.sh

EXPOSE 5007

ENTRYPOINT ["/tmp/entry.sh"]

CMD ["gunicorn", "-b", "0.0.0.0:5007", "cut-rate:app", "--log-file=-"]
