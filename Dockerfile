# Dockerfile
FROM python:3.11-slim

# Variables de entorno para evitar archivos .pyc y log buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Por defecto, no se especifica CMD (usamos docker-compose)
# Puedes dejarlo comentado o vacío
# CMD ["gunicorn", "starwars_api.wsgi:application", "--bind", "0.0.0.0:8000"]