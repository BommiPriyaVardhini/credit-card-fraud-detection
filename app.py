import numpy as np
import pandas as pd
import pickle
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from datetime import timedelta
from flask import Flask, request, jsonify
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Flask App
app = Flask(__name__)
app.secret_key = "secret"
app.permanent_session_lifetime = timedelta(minutes=30)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))  # Redirect to login after successful registration
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="Username already exists.")

    return render_template('register.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:  # If user exists
            session['user'] = username
            session['user_id'] = user[0]  # Store user ID in session
            return redirect(url_for('predict'))  # Redirect to prediction page
        else:
            return render_template('login.html', error="Invalid Credentials. Please try again.")

    return render_template('login.html', error=None)

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy



# Use SQLite (or replace with MySQL connection string)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Database Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_card_number = db.Column(db.String(20), nullable=False)
    validity = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.String(10), nullable=False)
    transaction_time = db.Column(db.String(10), nullable=False)
    prediction = db.Column(db.String(20), nullable=False)

# Create database tables before first request
with app.app_context():
    db.create_all()


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html', prediction=None)

    # Print received form data
    print("🔹 Received Form Data:")
    print(request.form)  # Debugging: Check what data Flask is getting

    # Get form data
    card_number = request.form.get("credit_card_number")
    validity = request.form.get("validity")
    amount = request.form.get("amount")
    transaction_date = request.form.get("transaction_date")
    transaction_time = request.form.get("transaction_time")

    if not all([card_number, validity, amount, transaction_date, transaction_time]):
        print("❌ Missing input data!")
        return render_template("predict.html", prediction="Missing input data", error=True)

    # Updated Fraud Detection Logic
    if (5000 <= int(amount) <= 5500) or (15000 <= int(amount) <= 16000):
        prediction = "Fraud"
    else:
        prediction = "Not Fraud"

    
    new_transaction = Transaction(
            credit_card_number=card_number,
            validity=validity,
            amount=amount,
            transaction_date=transaction_date,
            transaction_time=transaction_time,
            prediction=prediction
    )
    db.session.add(new_transaction)
    db.session.commit()

    return render_template(
        "predict.html",
        prediction=prediction,
        error=False,
        card_number=card_number,
        validity=validity,
        amount=amount,
        transaction_date=transaction_date,
        transaction_time=transaction_time
    )


@app.route('/transactions')
def transactions():
    # Fetch all stored transactions
    all_transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=all_transactions)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove session data
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
