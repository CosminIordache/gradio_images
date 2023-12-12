### Categorizacion de imagenes con GRADIO

La base de datos esta echa en docker-compose mediante un .yaml

Para acceder a ella tenemos que encender el contenedor de la base de datos postgres.

Este programa sube imagenes a la base de datos y mediante un modelo de inteligencia artifical,
se categoriza automaticamente la imagen que esta subida a la base de datos.

La base de datos se puede visualizar desde DBEAVER-CE. (Haciendo una conexion a postgres)

```bash
 docker compose up -d
```

```bash
python3 main.py
```
