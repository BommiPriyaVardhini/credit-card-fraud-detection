# credit-card-fraud-detection
📖 Project Overview
This project is a full-stack web application designed to detect fraudulent credit card transactions. It is developed using Python Flask, and supports user authentication, fraud detection using a rule-based model, transaction logging, and a simple UI using HTML templates. The application also connects to SQLite databases to store user details and transaction history.
Key Features
*User Registration and Login system with session management.
*Fraud Detection Engine based on transaction rules and a machine learning model (model.pkl).
*Transaction Storage: Saves every prediction to the database.
*Transaction History: Users can view all past predictions on a separate page.
*Database Integration with SQLite using SQLAlchemy ORM.
*Web Interface using Flask templates (home, predict, login, register, transactions, etc.).

Technologies Used
Frontend: HTML (Jinja2 templating)
Backend: Python, Flask
Database: SQLite + SQLAlchemy ORM
Machine Learning: Scikit-learn (RandomForestClassifier)
Data Processing: Pandas, NumPy
file structure
structure:
├── app.py                               → Main Flask app
├── model.pkl or scalar.pkl              → Pre-trained ML model
├── database.db                          → Stores user login data
├── fix_db.py
├── fix_transactions.py                  → Stores transaction records
├── templates/                           → HTML templates
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── predict.html
│   ├── contactus.html
│   └── transactions.html
