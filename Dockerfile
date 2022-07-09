FROM python:3.10-slim
WORKDIR /code
# Разделяем копирование requirements.txt от общего, так как он меняется гораздо реже, нежели основной код.
# Нет смысла пересобирать слой с зависимостями так же часто, как и основные слои.
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
ENTRYPOINT ["tail", "-f", "/dev/null"]

