FROM python:3.10-slim
WORKDIR /healthcheckbot/

VOLUME config

RUN apt update
RUN apt install -y iputils-ping

COPY requirements.txt .
RUN pip3 install -r requirements.txt


COPY . .

ENTRYPOINT ["python3", "__init__.py"]
