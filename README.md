###Procesamiento y Categorización de Imágenes con PostgreSQL

Este repositorio contiene un script en Python para el procesamiento y categorización de imágenes utilizando una base de datos PostgreSQL. El proyecto utiliza Docker para configurar una instancia de PostgreSQL. Las imágenes se cargan, se procesan utilizando el modelo Vision Transformer (ViT) y se almacenan en la base de datos PostgreSQL.
Configuración

    Instala Docker en tu máquina.

    Clona el repositorio:

    bash

git clone https://github.com/tu-nombre/procesamiento-de-imagenes.git

Navega al directorio del proyecto:

bash```
cd procesamiento-de-imagenes
```

Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables de entorno:

bash```
    DB_NAME=images
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
```

Docker Compose

Utiliza la siguiente configuración de Docker Compose para configurar el contenedor PostgreSQL:

yaml

version: '3.9'

services:
  postgres:
    image: postgres
    ports:
      - 5432:5432
    volumes:
      - ~/apps/postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=images

Inicialización de la Base de Datos

El script db_init.py inicializa la base de datos PostgreSQL creando una tabla llamada images. Utiliza la biblioteca psycopg2 para interactuar con la base de datos.

python

# db_init.py

# (Código omitido por brevedad)

Procesamiento y Categorización de Imágenes

La funcionalidad principal del proyecto se implementa en main.py. El script utiliza la biblioteca gradio para crear una interfaz web simple para cargar imágenes, procesarlas con el modelo ViT y mostrar los resultados.

python

# main.py

# (Código omitido por brevedad)

Uso

    Ejecuta el script db_init.py para inicializar la base de datos:

    bash

python db_init.py

Ejecuta el script main.py para lanzar la interfaz web de Gradio:

bash

    python main.py

    Abre tu navegador web y accede a http://localhost:7860 para acceder a la interfaz de procesamiento de imágenes.

Funcionalidades Adicionales

    El proyecto incluye funcionalidades para recuperar imágenes cargadas, sus categorías y actualizar las imágenes y categorías mostradas.

Dependencias

    psycopg2
    gradio
    Pillow
    transformers

Instala las dependencias utilizando:

bash

pip install -r requirements.txt
