🚖 NYC Taxi Trip Analytics Dashboard
📘 Overview

This fullstack application analyzes the New York City Taxi Trip dataset, enabling users to explore urban mobility patterns interactively.
The system performs data extraction, transformation, and loading (ETL), stores it in a relational database (PostgreSQL), and exposes Flask-based REST APIs for visualization of patterns such as fare trends, trip distance, and tip behavior.

🗂️ Project Structure
Team-5-Summative_Enterprise_Web_Development/
│
├── README.md
├── Team-5_Report_Documentation.pdf
│
├── backend/                               # Flask + PostgreSQL backend (ETL + APIs)
│   │
│   ├── data/
│   │   ├── raw/
│   │   │   └── train.csv
│   │   └── processed/
│   │       └── trips_cleaned.csv
│   │
│   ├── instance/
│   │   └── nyc_taxi.db
│   │
│   ├── logs/
│   │   └── etl.log
│   │
│   ├── migrations/
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── c41d9143fc57_initial.py
│   │
│   ├── scripts/
│   │   ├── run_etl.py
│   │   └── import_to_db.py
│   │
│   ├── src/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   │
│   │   ├── api/
│   │   │   └── trips.py
│   │   │
│   │   ├── etl_steps/
│   │   │   ├── cleaner.py
│   │   │   ├── feature_engineering.py
│   │   │   └── loader.py
│   │   │
│   │   ├── models/
│   │   │   └── trip.py
│   │   │
│   │   ├── services/
│   │   │   └── etl.py
│   │   │
│   │   ├── services_custom/
│   │   │   └── top_k_hotspots.py
│   │   │
│   │   └── utils/
│   │       └── logger.py
│   │
│   ├── .env.example
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
└── frontend/                              # Frontend (Vanilla HTML, CSS, JS)
    ├── index.html
    ├── styles.css
    └── app.js

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/AureleKarega/Team-5-Summative_Enterprise_Web_Development.git
cd Team-5-Summative_Enterprise_Web_Development

2️⃣ Backend Setup

Ensure Python 3.9+ is installed.

cd backend
pip install -r requirements.txt
python etl_pipeline.py      # Cleans and loads data into the database
python app.py               # Starts Flask API server


The backend will run at:
➡️ http://localhost:7070/api/trips

3️⃣ Frontend Setup

Open frontend/index.html directly in your browser
or use Live Server in VS Code for a smoother preview.

The frontend connects automatically to the backend API to display trip data and charts.

🌐 API Endpoints
Endpoint	Method	Description
/api/trips	GET	Returns all trips (paginated)
/api/stats	GET	Returns summary statistics (avg fare, distance, duration)
/api/filter	POST	Filters trips by date, fare, or distance
/api/top_zones	GET	Returns top 10 pickup/drop-off zones

Example Request

curl http://localhost:7070/api/stats

🧱 Database Schema

Table: trips

Column	Type	Description
id	INTEGER	Primary key
pickup_datetime	DATETIME	Trip start time
dropoff_datetime	DATETIME	Trip end time
pickup_longitude	FLOAT	Pickup location
dropoff_longitude	FLOAT	Dropoff location
distance_km	FLOAT	Distance in kilometers
fare_amount	FLOAT	Fare charged
tip_amount	FLOAT	Tip given
payment_type	TEXT	Payment method
speed_kmh	FLOAT	Derived feature (distance / duration)
✨ Features

🧹 Clean and normalize the NYC Taxi dataset (Python ETL)

🗄️ Relational database (SQLite/PostgreSQL) with indexing

🧩 RESTful API using Flask for trip data access

📊 Interactive dashboard built in HTML, CSS, and JavaScript

📈 Visual charts for fare, distance, and speed analysis (Chart.js)

🔍 Filtering & sorting by date, fare, and distance

🧠 Custom algorithm for top K pickup zone detection

🎥 Video Walkthrough

Video Walkthrough Link: [Insert your video link here]

The walkthrough covers:

Data cleaning and transformation

API testing and demonstration

Dashboard visualization

Key urban mobility insights

💻 Tech Stack
Layer	Technology
Backend	Python (Flask)
Database	SQLite / PostgreSQL
Frontend	HTML, CSS, JavaScript (Chart.js)
Data	NYC Taxi Trip Dataset
📊 Insights

Average fare increases with distance, but tips vary by payment type.

Peak taxi demand is observed between 6–9 PM in Manhattan.

Short trips (<2 km) dominate total rides, showing hyper-local movement.

👩‍💻 Team & Credits

Developed by Team 5:

Reine Ella Dusenayo

Nina Bwiza

Alain Christian Mugenga

Aurele Karega

📅 Date: October 16, 2025
