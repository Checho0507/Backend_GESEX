FROM python:3.11-slim

WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Puerto que escuchará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

