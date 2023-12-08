# Utilizamos una imagen de Python estándar
FROM python:3.11.6

# Establecemos un directorio de trabajo en /app
WORKDIR /app

# Copiamos el contenido de la aplicación en el directorio de trabajo
COPY . /app

# Instalamos las dependencias de Python directamente desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutamos la aplicación cuando se inicie el contenedor
CMD ["python", "run.py"]