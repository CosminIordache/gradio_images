from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image


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