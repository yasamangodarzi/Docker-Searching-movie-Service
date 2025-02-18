
FROM python:3.8.10

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["/bin/bash", "/app/run.sh"]
