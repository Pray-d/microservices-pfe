import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# File path to the CSV file
csv_file_path = os.path.join('data', 'r.csv')

# Read CSV data
data = pd.read_csv(csv_file_path, sep=';')

# Preprocessing
data.dropna(subset=['JobProfile', 'Technologyidentified'], inplace=True)
X = data['JobProfile'] + " " + data['ProductName'].fillna("")  
y = data['Technologyidentified']

# Feature Engineering
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

# Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the fitted CountVectorizer
vectorizer_file_path = os.path.join('data', 'fitted_vectorizer.joblib')
joblib.dump(vectorizer, vectorizer_file_path)

# Save the trained model
model_file_path = os.path.join('data', 'trained_model.joblib')
joblib.dump(model, model_file_path)

# Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
