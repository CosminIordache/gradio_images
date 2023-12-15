# Procesamiento y Categorización de Imágenes con PostgreSQL

Este repositorio contiene un script en Python para el procesamiento y categorización de imágenes utilizando una base de datos PostgreSQL. El proyecto utiliza Docker para configurar una instancia de PostgreSQL. Las imágenes se cargan, se procesan utilizando el modelo Vision Transformer (ViT) y se almacenan en la base de datos PostgreSQL.

## Configuración
#### Instala Docker en tu máquina
```bash
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04
```
#### Clona el repositorio:
```bash
git clone https://github.com/CosminIordache/gradio_images.git
```

Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables de entorno:
```bash
DB_NAME=images
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
```

### Docker Compose

Docker Compose es una herramienta que permite definir y ejecutar aplicaciones Docker de manera multi-contenedor. El archivo docker-compose.yml en este proyecto define la configuración de los servicios, redes y volúmenes necesarios para ejecutar la aplicación de procesamiento de imágenes con PostgreSQL.

#### Iniciar docker
```bash
docker compose up -d
```

#### Parar docker
```bash
docker compose down
```

### Inicialización de la Base de Datos

El script db/db.py inicializa la base de datos PostgreSQL creando una tabla llamada images. Utiliza la biblioteca psycopg2 para interactuar con la base de datos.
La base de datos se puede ver en dbeaver, haciendo una conexion de postgresql. Desde dbeaver se controla las tablas y los datos de forma visual, tambien se puede hacer desde el archivo db.py mediante consultas.

### Procesamiento y Categorización de Imágenes

La funcionalidad principal del proyecto se implementa en main.py. El script utiliza la biblioteca gradio para crear una interfaz web simple para cargar imágenes, procesarlas con el modelo ViT y mostrar los resultados.

### Uso

Ejecuta el script main.py para lanzar la interfaz web de Gradio:
```bash
python main.py
```

Abre tu navegador web y accede a http://localhost:7860 para acceder a la interfaz de procesamiento de imágenes.
