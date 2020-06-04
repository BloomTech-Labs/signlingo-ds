FROM ubuntu:16.04
FROM python:3.7-slim

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libglib2.0 libsm6 libxext6 libxrender-dev


COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

EXPOSE 5000
CMD [ "app.py", "run" ]
