
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from .models import TravelPlace,TravelPlaceImages
import io
from PIL import Image
import os
from sklearn.metrics import mean_squared_error, accuracy_score
import matplotlib.pyplot as plt

model = VGG16(weights=None)  

model.load_weights('api/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')

def get_image_embedding(img_file):
    # Convert InMemoryUploadedFile to BytesIO
    img = Image.open(io.BytesIO(img_file.read()))
    img = img.resize((224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    embedding = model.predict(img_data)
    
    return embedding

def find_similar_places(embedding):
    places = TravelPlace.objects.exclude(image_embedding__isnull=True)
    p_places = TravelPlaceImages.objects.exclude(image_embedding__isnull=True)

    similarities = []
    
    # for place in places:
    #     place_embedding = np.frombuffer(place.image_embedding, dtype=np.float32)
    #     similarity = cosine_similarity(embedding, [place_embedding])
    #     similarities.append((place, similarity))
    
    for p_place in p_places:
        place_embedding = np.frombuffer(p_place.image_embedding, dtype=np.float32)
        similarity = cosine_similarity(embedding, [place_embedding])
        similarities.append((p_place, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_places = [p_place.id for p_place, similarity in similarities[:5]]  # Top 5 similar places
    return top_places



def preprocess_and_store_embeddings():
    places = TravelPlace.objects.exclude(photo__isnull=True)
    p_images=TravelPlaceImages.objects.exclude(images__isnull=True)
    # for place in places:
    #     img_path = place.photo.path
    #     if not os.path.exists(img_path):
    #         print(f"Image path does not exist: {img_path}")
    #         continue

    #     try:
    #         with open(img_path, 'rb') as img_file:
    #             embedding = get_image_embedding(img_file)
    #             place.image_embedding = embedding.tobytes()  # Store as binary
    #             place.save()
    #             print(f"Successfully processed and saved embedding for: {place.name}")
    #     except Exception as e:
    #         print(f"Error processing image for {place.name}: {e}")

    for place in p_images:
        img_path = place.images.path
        if not os.path.exists(img_path):
            print(f"Image path does not exist: {img_path}")
            continue

        try:
            with open(img_path, 'rb') as img_file:
                embedding = get_image_embedding(img_file)
                place.image_embedding = embedding.tobytes()  # Store as binary
                place.save()
                print(f"Successfully processed and saved embedding for: {place.tp}")
        except Exception as e:
            print(f"Error processing image for {place.tp}: {e}")


