from flask import Flask, request, jsonify, redirect, url_for, g
import pandas as pd
import joblib
import os
import sqlite3
import threading
from kafka import KafkaProducer

app = Flask(__name__)

# Function to load the trained model
def load_model():
    return joblib.load('data/trained_model.joblib')

# Function to load the fitted CountVectorizer
def load_vectorizer():
    return joblib.load('data/fitted_vectorizer.joblib')

# Function to load the employee dataset
def load_employee_data():
    csv_file_path = os.path.join('data', 'emps.csv')
    return pd.read_csv(csv_file_path, sep=';')

# Load the initial model, vectorizer, and employee data
model = load_model()
vectorizer = load_vectorizer()
employee_data = load_employee_data()

# Initialize Kafka producer
kafka_producer = KafkaProducer(bootstrap_servers='localhost:29092')
#kafka_producer2 = KafkaProducer(bootstrap_servers='localhost:9092')

# Function to interact with SQLite database
def interact_with_database():
    # Create SQLite connection within the function
    conn = sqlite3.connect('suggestions.db')
    c = conn.cursor()

    # Now you can use the connection and cursor objects within this function
    c.execute("SELECT * FROM suggestions")
    rows = c.fetchall()
    for row in rows:
        #print(row)
        pass

    # Close the connection when done
    conn.close()

# Create a new thread and run the function within that thread
db_thread = threading.Thread(target=interact_with_database)
db_thread.start()
db_thread.join()  # Wait for the thread to finish execution

# Function to get the SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('suggestions.db')
    return db

# Function to close the SQLite connection
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Close connection when the app exits
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route('/')
def index():
    return redirect(url_for('predict'))

def predict(profile_words, product_name, start_date, finish_date,id):
    # Preprocess input data using the fitted CountVectorizer
    input_data = vectorizer.transform([profile_words + " " + product_name])

    # Prediction
    prediction = model.predict(input_data)[0]
    
     

    # Retrieve employees matching the predicted job profile
    matched_employees = employee_data[(employee_data['Technologyidentified'] == prediction)]

    matched_employees['DMmpmaaal'] = matched_employees['DMmpmaaal'].astype(str)
   
    # Split email addresses to extract first and last names
    matched_employees['First_Name'] = matched_employees['DMmpmaaal'].apply(lambda x: x.split('@')[0].split('.')[0] if '@' in x else None)
    matched_employees['Last_Name'] = matched_employees['DMmpmaaal'].apply(lambda x: x.split('@')[0].split('.')[1] if '@' in x else None)

    # Drop unnecessary columns
    matched_employees.drop(columns=['DMmpmaaal', 'Technologyidentified', 'JobProfile',"ProductName"], inplace=True)

    # Remove rows with missing names
    matched_employees = matched_employees.dropna(subset=['First_Name', 'Last_Name'])

    # Drop duplicate first and last names combinations to avoid repetitions
    matched_employees_unique_names = matched_employees.drop_duplicates(subset=['First_Name', 'Last_Name'])

    # Join the unique first and last names into a single string
    matched_employees_names = matched_employees_unique_names.apply(lambda row: f"{row['First_Name']} {row['Last_Name']}", axis=1)
    
    # Send each matched employee name to Kafka topic
    for employee_name in matched_employees_names:
        Ms=employee_name+"#"+start_date+"#"+finish_date
        send_to_kafka(Ms)
    send_id_to_kafka(id)

    # Insert the suggestions into the database
    db = get_db()
    cursor = db.cursor()
    for employee_name in matched_employees_names:
        cursor.execute("INSERT INTO suggestions (predicted_profile, employee_name) VALUES (?, ?)", (prediction, employee_name))
    
    # Commit changes
    db.commit()
    prediction=prediction
    return (prediction)
    #return jsonify({'prediction': prediction})
@app.route('/predict', methods=['GET'])
def predict_endpoint():
    # Get parameters from the request
    profile_words = request.args.get('profileWords')
    product_name = request.args.get('productName')
    start_date = request.args.get('startDate')
    finish_date = request.args.get('finishDate')
    id=request.args.get('demandid')
    # Perform prediction
    prediction_result = predict(profile_words, product_name,start_date,finish_date,id)
    prediction_result= prediction_result+ "#"+start_date+"#"+finish_date+"#"
    #send_to_kafka(prediction_result)
    # Return prediction result
    return jsonify({"prediction": prediction_result})
def send_to_kafka(prediction):
    try:
        kafka_producer.send('prediction_names', prediction.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send prediction to Kafka: {e}")
def send_id_to_kafka(id):
    try:
        kafka_producer.send('prediction_id', id.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send id to Kafka: {e}")

if __name__ == '__main__':
    app.run(debug=True)
