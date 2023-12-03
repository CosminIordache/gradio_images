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

    inserted_image_data = cur.fetchone()[0]

    conn.commit()
    conn.close()

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
        images.append(image_conv)

    conn.close()
    return images


with gr.Blocks() as demo:
    with gr.Column():
        images_update = get_uploaded_images() 
        interface = gr.Interface(
            fn=upload_image,
            inputs=[
                gr.Textbox(label="Name"),
                gr.File(label="Image"),
            ],
            outputs=[
                gr.Image()
            ],
            title="Filter Sports Images"
        )
        with gr.Row():
            btn = gr.Button("Update images", scale=0)
            filter = gr.Dropdown(choices=["todos","americano", "basket", "baisball", "boxeo", "ciclismo", "f1", "futbol", "golf", "natacion", "tenis"])
            
        gallery = gr.Gallery(value=images_update, columns=[3], show_download_button=True)
        btn.click(get_uploaded_images, None, gallery)


if __name__ == "__main__":
    demo.title = "Sports Images"
    demo.launch()
    