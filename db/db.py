import psycopg2 as db
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')

table_name = 'images'

# Establece una conexión a la base de datos con las variables de entorno
try:
    connection = db.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = connection.cursor()

    # Crear una tabla para almacenar imágenes
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            image_name VARCHAR(255) NOT NULL,
            image_data BYTEA NOT NULL,
            image_category VARCHAR(255) NOT NULL
        );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    print(f'Table "{table_name}" created successfully.')
    print("Connection established")
except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar conexión a la base de datos
    if cursor:
        cursor.close()
    if connection:
        connection.close()

