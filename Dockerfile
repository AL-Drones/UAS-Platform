# Dockerfile
# Usamos Python 3.10 slim para ser leve, mas compatível
FROM python:3.10-slim

# Variáveis de ambiente para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalação de dependências do SISTEMA (GDAL e bibliotecas espaciais)
# Essencial para GeoDjango e manipulação de KML/Shapefiles
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        libproj-dev \
        gdal-bin \
        libgdal-dev \
        python3-gdal \
        gcc \
        g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Instala dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código do projeto para dentro do container
COPY . /app/

# O comando final será sobrescrito pelo docker-compose, mas deixamos um default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
