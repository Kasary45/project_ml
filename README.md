Rent Prediction Project
Overview
The Rent Prediction Project aims to forecast rental prices for properties based on various features, helping tenants find affordable housing and assisting investors in making informed decisions. This project utilizes machine learning techniques to analyze data collected from rental listings and predict future rental prices.

Table of Contents
Features
Technologies Used
Data Collection
Data Preprocessing
Model Building
Evaluation
Deployment
Getting Started
License
Features
Predicts rental prices based on property features such as location, size, and amenities.
Provides insights into rental trends across major cities.
Utilizes various machine learning algorithms for model training and evaluation.
Technologies Used
Python
Pandas
NumPy
Scikit-learn
Selenium
Flask
AWS EC2
XGBoost, CatBoost, and other ML libraries
Data Collection
Data was collected by scraping rental listings from Makan.com using Selenium. The dataset includes information on rental prices, property features, and location details.

Data Preprocessing
Data Cleaning: Removed duplicates and irrelevant entries.
Outlier Detection: Identified and handled outliers to improve model accuracy.
Encoding Categorical Variables: Used LabelEncoder from scikit-learn to encode categorical features such as city, class, and furnished status.
Feature Engineering: Created new features to enhance model performance, including rent per area.
Model Building
The project employed multiple machine learning models, including:

Linear Regression
Decision Trees
Random Forest
XGBoost
CatBoost
The Decision Tree Regressor was selected as the final model based on its performance metrics.

Evaluation
The model was evaluated using metrics such as:

Mean Absolute Error (MAE)
Mean Squared Error (MSE)
R-squared score
Deployment
The model is deployed using Flask on an AWS EC2 instance, enabling real-time predictions through a web application.

Getting Started
To run this project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone [repository-url]
cd rent-prediction-project
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Flask application:

bash
Copy code
python app.py
Access the web application in your browser at http://localhost:5000.
