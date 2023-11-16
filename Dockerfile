# Utilizamos la imagen de Python de Heroku, que es basada en Ubuntu.
FROM python:3.11.5-alpine

# Agregamos las dependencias de compilación necesarias
RUN apk add --no-cache g++ gcc libgcc libstdc++

RUN python3 -m ensurepip \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install openai

# Establecemos un directorio de trabajo en /app
WORKDIR /app

# Copiamos el contenido de la aplicación en el directorio de trabajo
COPY . /app

# Instalamos las dependencias de Python directamente desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutamos la aplicación cuando se inicie el contenedor
CMD ["python", "run.py"]