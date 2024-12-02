# Dockerfile for Backend
FROM python:3.9-slim

RUN apt-get update && apt-get install -y locales apt-utils

RUN sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG fr_FR.UTF-8  
ENV LANGUAGE fr_FR:en  
ENV LC_ALL fr_FR.UTF-8   

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "frontend.py"]
