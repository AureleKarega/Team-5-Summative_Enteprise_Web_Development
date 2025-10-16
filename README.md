
# NYC Taxi Trip Analytics Dashboard 

## Overview
This fullstack application analyzes the **New York City Taxi Trip dataset**, enabling users to explore urban mobility patterns interactively.  
The system performs data **extraction, transformation, and loading (ETL)**, stores it in a **relational database**, and exposes APIs to visualize patterns like fare, trip distance, and tip trends.

---


---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/nyc-taxi-dashboard.git
cd nyc-taxi-dashboard
```

### 2. Backend Setup
Ensure Python 3.9+ is installed.

```bash
cd backend
pip install -r requirements.txt
python etl_pipeline.py   # Cleans and loads data into database
python app.py            # Starts Flask API server
```

The backend will run at:  
➡️ `http://localhost:7070

### 3. Frontend Setup
Open `frontend/index.html` in your browser or use Live Server in VS Code.  
It will automatically connect to the backend API to fetch trip insights.

---

## 🧠 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/trips` | GET | Returns all trips (paginated) |
| `/api/stats` | GET | Returns summary statistics (avg fare, distance, duration) |
| `/api/filter` | POST | Filters trips by date, fare, or distance |
| `/api/top_zones` | GET | Returns top 10 pickup/drop-off zones |

Example Request:
```bash
curl http://localhost:5000/api/stats
```

---

## 🗄️ Database Schema

**Table:** `trips`
| Column | Type | Description |
|---------|------|-------------|
| id | INTEGER | Primary key |
| pickup_datetime | DATETIME | Trip start time |
| dropoff_datetime | DATETIME | Trip end time |
| pickup_longitude | FLOAT | Pickup location |
| dropoff_longitude | FLOAT | Dropoff location |
| distance_km | FLOAT | Distance in kilometers |
| fare_amount | FLOAT | Fare charged |
| tip_amount | FLOAT | Tip given |
| payment_type | TEXT | Payment method |
| speed_kmh | FLOAT | Derived feature (distance / duration) |

---

## 📊 Features

- Clean and normalized NYC Taxi dataset using Python (ETL)
- Relational database (SQLite/PostgreSQL) with indexes for fast queries
- REST API with Flask for data access
- Interactive dashboard built with HTML, CSS, and JavaScript
- Visual charts (using Chart.js) for fare and trip analysis
- Filtering and sorting options for better insights

---

## 📹 Video Walkthrough
🎥 [Video Walkthrough Link](https://youtu.be/Hs07qs53w-A)  
The walkthrough covers:
- Data cleaning and transformation
- API demonstration
- Dashboard interactivity
- Key insights on urban mobility

---

## 🧩 Tech Stack
**Backend:** Python (Flask)  
**Database:** SQLite / PostgreSQL  
**Frontend:** HTML, CSS, JavaScript (Chart.js)  
**Data:** NYC Taxi Trip Dataset  

---

## ✨ Insights
- Average fare increases with distance, but tips vary strongly by payment type.  
- Peak taxi demand observed between **6–9 PM** in Manhattan zones.  
- Short trips (<2 km) dominate total rides, showing hyper-local movement patterns.  

---

## 👥 Team & Credits
Developed by: **Your Name / Team Name**  
Date: October 16, 2025  

---

## 🧾 License
This project is for educational purposes only.
