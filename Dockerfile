FROM python:3.12-slim

# Esse é o diretório de trabalho no Docker
WORKDIR /app

# Copia apenas os requisitos para otimizar o cache
COPY requirements.txt .

# Instalação das dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para o contêiner
COPY ./app ./app

ENV PYTHONUNBUFFERED=1
