FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    python3-pygame \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "Xvfb :99 -screen 0 1280x720x24 & DISPLAY=:99 python3 src/core/game.py"]