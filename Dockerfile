FROM python:3.10-slim
WORKDIR /healthcheckbot/

RUN apt update
RUN apt install -y iputils-ping

COPY requirements.txt .
RUN pip3 install -r requirements.txt


COPY . .
COPY config/settings.yaml config/settings.yaml

ENTRYPOINT ["python3", "__init__.py"]
