import base64
import io
from PIL import Image
import gradio as gr
from db import db
import psycopg2
from dotenv import load_dotenv
import os

#Create database
db

load_dotenv()
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')


def convert_binary_image_to_pil_image(binary_image_data):
    image = Image.open(io.BytesIO(binary_image_data))
    return image

def upload_image(name, image_file):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()

    with open(image_file, "rb") as f:
        image_bytes = f.read()

    cur.execute("""
        INSERT INTO images (image_name, image_data) VALUES (%s, %s) RETURNING image_data;
    """, (name, image_bytes))

    # Recuperar la imagen recién insertada
    inserted_image_data = cur.fetchone()[0]

    conn.commit()
    conn.close()

    # Convertir la imagen a formato PIL antes de devolverla
    inserted_image_pil = convert_binary_image_to_pil_image(inserted_image_data)

    return inserted_image_pil

def get_uploaded_images():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()
    cur.execute("""
        SELECT image_name, image_data FROM images;
    """)
    images = []
    for image_name, image_data in cur:
        image_conv = convert_binary_image_to_pil_image(image_data)
        # Add image dictionary to list of images
        images.append(image_conv)

    conn.close()
    return images




with gr.Blocks() as demo:
    with gr.Column():
        images = get_uploaded_images() 
        interface = gr.Interface(
            fn=upload_image,
            inputs=[
                gr.Textbox(label="Name"),
                gr.File(label="Image"),
            ],
            outputs=[
                gr.Image()
            ],
            title="Upload Image to PostgreSQL"
        )
        gr.Gallery(value=images, label="Generated images", show_label=False, elem_id="gallery", columns=[3], rows=[1], object_fit="contain")

if __name__ == "__main__":
    demo.launch()