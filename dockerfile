# Use a imagem base oficial do Python
FROM python:3.12

LABEL maintainer="cristian.hennequin1@gmail.com"

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Atualiza o sistema e instala as dependências necessárias
RUN apt-get update && apt-get install -y \
    weasyprint \
    python3-pip \
    libffi-dev \
    gcc \
    musl-dev \
    python3-dev \
    zlib1g-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    g++ \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    libharfbuzz-dev \
    libxml2-dev \
    libxslt1-dev \
    netcat-openbsd && \
    apt-get clean


# Cria diretórios e define permissões
RUN mkdir -p /app /base_static /base_templates /scripts /app/static /app/media && \
    chmod -R 755 /app /base_static /base_templates /scripts /app/static /app/media && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /app /base_static /base_templates /scripts /app/static /app/media

# Verifica e corrige permissões no ponto de montagem
RUN mkdir -p /var/lib/postgresql/data && \
    chmod -R 0700 /var/lib/postgresql/data && \
    chown -R duser:duser /var/lib/postgresql/data

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos para o contêiner
COPY --chown=duser:duser requirements.txt /app/
COPY --chown=duser:duser . /app/
COPY --chown=duser:duser scripts/commands.sh /scripts/commands.sh

# Instala o virtualenv e as dependências do Python
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt

# Define o PATH para incluir o ambiente virtual e scripts
ENV PATH="/scripts:/venv/bin:$PATH"

# Define o usuário como duser
USER duser

# Expõe a porta 8000
EXPOSE 8000

# Comando de inicialização
CMD ["/scripts/commands.sh"]
