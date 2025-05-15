# Usa una imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias (si usas psycopg2 o alguna librería que las necesite)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto en el que la app escuchará
EXPOSE 8000

# Configurar las variables de entorno si no están definidas
ENV PORT 8000
ENV DATABASE_URL ${DATABASE_URL:-sqlite:///./database.db}

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
