# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer variables de entorno para evitar que Python escriba archivos pyc y bufferice la salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos y instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto en el que la aplicación correrá
EXPOSE 5000

# Definir la variable de entorno para Flask
ENV FLASK_APP=app.py

# Comando para ejecutar la aplicación
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn"  , "-b", "0.0.0.0:8888", "wsgi:app"]
