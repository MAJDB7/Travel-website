
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from api.models import TravelPlace
import io
from PIL import Image
import os
from sklearn.metrics import mean_squared_error, accuracy_score
import matplotlib.pyplot as plt


model = VGG16(weights=None)  

model.load_weights('api/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')
photo='media/places_ph/eiffel-tower-975004_1920_Gr7XMpz.jpg'
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
    similarities = []
    for place in places:
        place_embedding = np.frombuffer(place.image_embedding, dtype=np.float32)
        similarity = cosine_similarity(embedding, [place_embedding])
        similarities.append((place, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_places = [place.name for place, similarity in similarities[:5]]  # Top 5 similar places
    return top_places



def preprocess_and_store_embeddings():
    places = TravelPlace.objects.exclude(photo__isnull=True)
    for place in places:
        img_path = place.photo.path
        if not os.path.exists(img_path):
            print(f"Image path does not exist: {img_path}")
            continue

        try:
            with open(img_path, 'rb') as img_file:
                embedding = get_image_embedding(img_file)
                place.image_embedding = embedding.tobytes()  # Store as binary
                place.save()
                print(f"Successfully processed and saved embedding for: {place.name}")
        except Exception as e:
            print(f"Error processing image for {place.name}: {e}")

embedding = get_image_embedding(photo) 
similar_places = find_similar_places(embedding)  
def calculate_metrics(ground_truth, predicted_values):
    # Assuming ground_truth and predicted_values are numpy arrays or lists
    mse = mean_squared_error(ground_truth, predicted_values)
    rmse = np.sqrt(mse)
    accuracy = accuracy_score(ground_truth, np.round(predicted_values))
    
    return rmse, accuracy

print(calculate_metrics())
def plot_metrics(rmse, accuracy):
    metrics = ['RMSE', 'Accuracy']
    values = [rmse, accuracy]
    
    plt.figure(figsize=(8, 6))
    plt.bar(metrics, values, color=['blue', 'green'])
    plt.title('Error Rate and Accuracy')
    plt.ylabel('Values')
    plt.ylim(0, 1)  # Assuming RMSE and Accuracy are normalized or comparable
    
    for index, value in enumerate(values):
        plt.text(index, value + 0.01, f'{value:.2f}', ha='center')
    
    plt.show()