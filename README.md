# AI-Powered-Student-Mentoring-and-Risk-Analysis-System-Using-Machine-Learning
## Overview

The AI-Powered Student Mentoring and Risk Analysis System is an intelligent web-based application developed to provide personalized academic guidance, wellness support, and career counseling for students. The system leverages Machine Learning, Artificial Intelligence, and Data Analytics to identify at-risk students and recommend suitable mentors and improvement strategies.

## Problem Statement

Educational institutions often face challenges in monitoring student performance, identifying struggling students, and providing timely support. Traditional mentoring approaches are manual, time-consuming, and difficult to scale. This project addresses these issues through intelligent automation and predictive analytics.

## Objectives

* Predict student risk levels using Machine Learning.
* Generate a Student Risk Index (SRI).
* Provide personalized mentor recommendations.
* Offer academic, wellness, and career guidance.
* Enable real-time interaction through an AI-powered chatbot.
* Visualize student analytics through reports and dashboards.

## Features

### Student Risk Prediction

* Predicts student risk levels using Random Forest Classification.
* Calculates Student Risk Index (SRI).
* Categorizes students into different risk groups.

### AI Chatbot

* Provides real-time responses to student queries.
* Supports academic, career, and wellness guidance.
* Integrated with OpenAI API.

### Mentor Recommendation System

* Recommends mentors based on student requirements.
* Supports Academic, Wellness, and Career mentoring.
* Displays mentor expertise and availability.

### Dashboard and Analytics

* Student performance dashboard.
* Risk analysis reports.
* Data visualization and insights.

### Reports Generated

* Feature Importance Analysis
* Confusion Matrix
* Heatmap Visualization
* SRI Distribution Graph
* Category Distribution Charts
* Cluster Analysis

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Machine Learning & Data Processing

* Scikit-Learn
* Pandas
* NumPy

### Visualization

* Matplotlib
* Plotly

### AI Integration

* OpenAI API

### Development Tools

* Visual Studio Code
* Git
* GitHub

## Project Structure

AI Mentoring System

├── backend/

│ ├── app.py

│ ├── model.py

│ ├── mentor.py

│ ├── recommendation.py

│ ├── templates/

│ ├── static/

│ ├── model.pkl

│ └── scaler.pkl

├── data/

│ ├── students.csv

│ ├── mentors.csv

│ └── outputs/

├── requirements.txt

└── README.md

## Machine Learning Model

* Algorithm Used: Random Forest Classifier
* Purpose: Student Risk Prediction
* Input Features:

  * GPA
  * Attendance
  * Stress Level
  * Productivity Score
  * Engagement Score
  * Career Readiness
* Output:

  * Risk Category
  * Student Risk Index (SRI)

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Student-Mentoring-and-Risk-Analysis-System-Using-Machine-Learning.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python backend/app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

## Future Enhancements

* Database Integration (MySQL/MongoDB)
* Mobile Application Support
* Advanced AI Mentoring
* Real-Time Notifications
* Student Performance Forecasting
* Multi-Institution Support

## Academic Relevance

This project demonstrates the practical application of:

* Artificial Intelligence
* Machine Learning
* Educational Data Mining
* Data Analytics
* Web Application Development
* Recommendation Systems

## Author

MD Noore Jamal

Bachelor of Commerce (Accounts)

Project: AI-Powered Student Mentoring and Risk Analysis System

## License

This project is developed for educational and academic purposes.
