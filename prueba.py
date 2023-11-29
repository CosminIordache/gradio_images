
import base64
import io
from PIL import Image
import gradio as gr
from db import db
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')


def convert_binary_image_to_pil_image(binary_image_data):
    image = Image.open(io.BytesIO(binary_image_data))
    return image

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
    print(images)
    return images


with gr.Blocks() as demo:
    images = get_uploaded_images()  # Assuming get_uploaded_images is a function that returns a list of images
    gr.Gallery(value=images, label="Generated images", show_label=False, elem_id="gallery", columns=[3], rows=[1], object_fit="contain", height="auto")

if __name__ == "__main__":
    demo.launch()

