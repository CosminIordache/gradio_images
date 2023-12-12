import io
from PIL import Image
import gradio as gr
from db import db
import psycopg2
from dotenv import load_dotenv
import os
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests


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

def category_image(image_data):
    img_url = image_data
    image = Image.open(img_url)

    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    # model predicts one of the 1000 ImageNet classes
    predicted_class_idx = logits.argmax(-1).item()
    
    return model.config.id2label[predicted_class_idx]

def upload_image(name, image_file):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()

    category = category_image(image_file)

    with open(image_file, "rb") as f:
        image_bytes = f.read()

    cur.execute("""
        INSERT INTO images (image_name, image_data, image_category) VALUES (%s, %s, %s) RETURNING image_data;
    """, (name, image_bytes, category))

    inserted_image_data = cur.fetchone()[0]

    conn.commit()
    conn.close()

    inserted_image_pil = convert_binary_image_to_pil_image(inserted_image_data)

    
    return inserted_image_pil



def get_uploaded_images():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()
    cur.execute("""
        SELECT image_name, image_data, image_category FROM images;
    """)
    images = []
    for image_name, image_data, image_category in cur:
        image_conv = convert_binary_image_to_pil_image(image_data)
        images.append(image_conv)

    conn.close()
    return images

def get_category_images():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()
    cur.execute("""
        SELECT image_name, image_data, image_category FROM images;
    """)
    category = []
    for image_name, image_data, image_category in cur:
        category.append(image_category)

    unique_category = list(set(category))

    conn.close()
    return unique_category


with gr.Blocks() as demo:
    categories = get_category_images()
    uploaded_images = get_uploaded_images()
    
    with gr.Column():
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
            btn1 = gr.Button("Update category", scale=0)
        
        gallery = gr.Gallery(value=uploaded_images, columns=[3], show_download_button=True)
        text = gr.Text(f"{categories}")
        
        btn.click(get_uploaded_images, None, gallery)
        btn1.click(get_category_images, None, text)

if __name__ == "__main__":
    demo.title = "Images"
    demo.launch()
    