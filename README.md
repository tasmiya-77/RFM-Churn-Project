# RFM-Churn-Project
This project performs a comprehensive RFM (Recency, Frequency, Monetary) Analysis and builds a Machine Learning model to predict customer churn. The goal is to identify high-value customers and detect those at risk of leaving based on their transaction history.
Key Implementation Steps
1. Data Cleaning & Preprocessing
Missing Data: Removed rows with missing CustomerID.

Deduplication: Dropped duplicate records to ensure data accuracy.

Type Conversion: Converted OrderDate to datetime objects for time-series calculations.

Feature Creation: Engineered a TotalSum column (Quantity * UnitPrice) to track monetary value.

2. RFM Calculation & Scoring
Aggregated data by CustomerID to calculate Recency, Frequency, and Monetary metrics.

Applied Quantile-based scoring (1-5) to rank customers across each metric.

Calculated an overall RFM Score to evaluate customer health.

3. Customer Segmentation
Mapped scores to specific business segments:

Champions: Most active and high-spending customers.

Loyal Customers: Regular shoppers with consistent spend.

Potential Loyalists: Recent spenders with growth potential.

At Risk / Lost: Customers who haven't purchased in a long time.

4. Data Visualization
Developed a Recency vs. Frequency Heatmap using Seaborn to show customer density.

Implemented a dark-themed visual style for professional data presentation.

5. Machine Learning (Predictive Modeling)
Algorithm: Trained a Random Forest Classifier to predict subscription_status (Churn).

Evaluation: Generated a classification report to measure model precision and recall.

Insight: Visualized Feature Importance to determine which RFM factor is the strongest predictor of churn.

Tech Stack
Python

Pandas (Data Manipulation)

Matplotlib & Seaborn (Data Visualization)

Scikit-Learn (Machine Learning)
