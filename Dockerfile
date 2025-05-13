# Imagen base oficial de Python
# FROM python:3.11-slim
 FROM python:3.11

# Variables de entorno necesarias para Playwright
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar edge de Playwright
RUN playwright install msedge

# Copiar el script
COPY scraper_playwright.py .

# Comando por defecto
CMD ["python", "scraper_playwright.py"]
