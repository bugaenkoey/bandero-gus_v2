# Використовуємо базовий образ з Python 3.11.9 на базі Alpine Linux
FROM python:3.11.9-alpine

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Встановлюємо необхідні системні бібліотеки для компіляції Pygame
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    libc-dev \
    sdl2-dev \
    sdl2_image-dev \
    sdl2_mixer-dev \
    sdl2_ttf-dev \
    bash \
    make \
    musl-dev \
    freetype-dev \
    libpng-dev \
    jpeg-dev \
    pkgconfig \
    alpine-sdk

# Копіюємо файли з поточної локальної директорії до робочої директорії контейнера
COPY . .

# Встановлюємо залежності з файлу requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду, яка буде виконана при запуску контейнера
CMD ["python", "main.py"]
