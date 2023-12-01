FROM ubuntu:latest
LABEL authors="pavelnezdara"

RUN apt-get update -y
RUN apt-get install python3-pip -y

COPY dependency/pip3-dependecy /requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR "/"
COPY ../TRASK_uberserver-main%20 /uberserver_src

CMD ["uvicorn", "uberserver_src.app:app", "--host", "0.0.0.0", "--port", "8000"]
