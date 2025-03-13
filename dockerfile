FROM python:3.13-slim

# Install all required packages
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    git \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Bun
RUN curl -fsSL https://bun.sh/install | bash

# Добавление Bun в PATH (для пользователя root)
ENV PATH="/root/.bun/bin:${PATH}"

# Set the working directory
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8800
EXPOSE 3300

CMD ["sh", "-c", "cd /app && reflex run --env prod --backend-port 8800 --frontend-port 3300"]
