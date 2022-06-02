# 2022-06-01 	v.1

FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade --disable-pip-version-check -r /app/requirements.txt

COPY app/ /app

# copiar crontabs para root (rever segurança)
COPY cronjob /etc/crontabs/root

CMD ( crond -f -d 8 & ) && uvicorn srvSpacefl:app --host 0.0.0.0 --port 8000
