import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="km_hospital"
)

cursor = conn.cursor()
print("Database connected successfully!")

# added patients
import bcrypt

def add_patient(name, dob, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO Patients (name, dob, email, password) VALUES (%s, %s, %s, %s)", 
                   (name, dob, email, hashed_password.decode('utf-8')))
    conn.commit()
    print("Patient added successfully!")

# view patients
def view_patients():
    cursor.execute("SELECT * FROM Patients")
    for patient in cursor.fetchall():
        print(patient)

# schedule appointment
def schedule_appointment(patient_id, provider_id, date, status="Scheduled"):
    cursor.execute("INSERT INTO Appointments (patient_id, provider_id, date, status) VALUES (%s, %s, %s, %s)", 
                   (patient_id, provider_id, date, status))
    conn.commit()
    print("Appointment scheduled!")

# user interface
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to K&M Hospital App!"

@app.route('/patients', methods=['GET'])
def get_patients():
    cursor.execute("SELECT * FROM Patients")
    patients = cursor.fetchall()
    return jsonify(patients)

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    schedule_appointment(data['patient_id'], data['provider_id'], data['date'])
    return jsonify({"message": "Appointment created!"})

if __name__ == "__main__":
    app.run(debug=True)

# testing the project
def test_connection():
    assert conn.is_connected(), "Database connection failed!"

# 
