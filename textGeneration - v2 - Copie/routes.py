# app/routes.py

from flask import Flask, request, render_template, redirect, url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('data/trained_model.joblib')

# Load the vectorizer
vectorizer = CountVectorizer()
vectorizer.fit_transform([''])  # Dummy fit to avoid error in transform

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from JSON sent by Spring Boot microservice
    data = request.json

    job_profile = data.get('job_profile', '')
    product_name = data.get('product_name', '')

    # Preprocess input data
    input_data = vectorizer.transform([job_profile + " " + product_name])

    # Prediction
    prediction = model.predict(input_data)[0]

    # Render prediction result in JSON format
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(debug=True)
