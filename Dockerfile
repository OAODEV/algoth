FROM alpine
LABEL maintainer=yagermadden@gmail.com

RUN apk add --no-cache python3

RUN mkdir /app
WORKDIR /app
VOLUME /cache

ADD . /app
RUN pip3 install pipenv && pipenv install --system

EXPOSE 5007

CMD ["gunicorn", "-b", "0.0.0.0:5007", "algoth:app", "--log-file=-"]
