import pickle
import pandas as pd
import os


# Loading the model
# model_path = r'D:\Nikss\Self Pracitce\Fast API (14-05-2025)\FastAPI with ML\Model/model.pkl'

# Inside docker, file paths changes so below code works locally and in docker both

# Get the folder of this file
current_dir = os.path.dirname(__file__)

# Path to model.pkl inside Docker
model_path = os.path.join(current_dir, "model.pkl")

with open(model_path, 'rb') as f:
    model = pickle.load(f)

model_version = '1.0.0'    # Model version comes automatically from MLFlow 
                                      # but here we are setting manually

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    
    input_df = pd.DataFrame([user_input])

    # Predicting the final class
    predicted_class = model.predict(input_df)[0]

    # Predicting probabilities for all classes
    probabilities = model.predict_proba(input_df)[0]

    # Confidence of the predicted class
    confidence = round(max(probabilities), 4)

    # Map probs to their class name and return in dict
    class_probabilities = {cls: round(prob, 4) for cls, prob in zip(class_labels, probabilities)}



    return {'Predicted Category': predicted_class,
            'Confidence for predicted category': confidence,
            "Class Probabilities": class_probabilities
            }