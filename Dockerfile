FROM ubuntu:latest
LABEL authors="maxim"

ENTRYPOINT ["top", "-b"]

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

RUN python3.11 --version && pip --version

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

