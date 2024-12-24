import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import streamlit as st

def app():
    # Query the data
    csv_file_path_cleaned = os.path.join(os.path.dirname(__file__), 'xdr_data_cleaned.csv')
    data_cleaned = pd.read_csv(csv_file_path_cleaned)

    # Display the cleaned data
    st.title("User Satisfaction Analysis")
    st.subheader("Cleaned Data")
    st.write(data_cleaned.head())

    # Task 4 - Engagement and Experience Scores
    st.header("Task 4: Engagement and Experience Scores")

    # Task 4.1 - Engagement Score and Experience Score calculation
    def aggregate_metrics_per_customer(data_cleaned: pd.DataFrame) -> pd.DataFrame:
        aggregated = data_cleaned.groupby('MSISDN/Number').agg({
            'Bearer Id': 'count',
            'Dur. (ms)': 'sum',
            'Total DL (Bytes)': 'sum',
            'Total UL (Bytes)': 'sum'
        }).reset_index()

        aggregated['Total Traffic'] = aggregated['Total DL (Bytes)'] + aggregated['Total UL (Bytes)']
        aggregated.columns = ['MSISDN', 'Sessions', 'Duration', 'DL Traffic', 'UL Traffic', 'Total Traffic']

        top_10 = {
            'Sessions': aggregated.nlargest(10, 'Sessions'),
            'Duration': aggregated.nlargest(10, 'Duration'),
            'Total Traffic': aggregated.nlargest(10, 'Total Traffic')
        }

        return aggregated, top_10

    # Aggregate metrics
    aggregated_data, top_10_customers = aggregate_metrics_per_customer(data_cleaned)

    st.subheader("Aggregated Metrics per Customer")
    st.write(aggregated_data.head())

    # Task 4.2 - Calculate Satisfaction Scores
    def calculate_satisfaction_scores(scores_data):
        scores_data['Satisfaction Score'] = (scores_data['Engagement Score'] + scores_data['Experience Score']) / 2
        top_10_satisfied = scores_data.nlargest(10, 'Satisfaction Score')
        return scores_data, top_10_satisfied

    scores_data = aggregated_data.copy()  # Placeholder for scores data
    scores_data['Engagement Score'] = np.random.rand(len(scores_data))  # Replace with actual engagement scores
    scores_data['Experience Score'] = np.random.rand(len(scores_data))  # Replace with actual experience scores

    scores_data, top_10_satisfied = calculate_satisfaction_scores(scores_data)

    st.subheader("Top 10 Satisfied Customers")
    st.write(top_10_satisfied)

    # Task 4.3 - Build a Regression Model (Placeholder)
    # Note: You would need to implement the actual regression model function
    def build_regression_model(scores_data):
        # Placeholder for model building logic
        mse = np.random.rand()  # Replace with actual MSE
        r2 = np.random.rand()   # Replace with actual R2 score
        return None, mse, r2

    model, mse, r2 = build_regression_model(scores_data)
    st.write(f"Model MSE: {mse}")
    st.write(f"Model R2 Score: {r2}")

    # Clustering Satisfaction Scores
    def cluster_satisfaction(scores_data):
        kmeans = KMeans(n_clusters=3, random_state=42)
        scores_data['Cluster'] = kmeans.fit_predict(scores_data[['Engagement Score', 'Experience Score']])
        avg_satisfaction = scores_data.groupby('Cluster')['Satisfaction Score'].mean()
        avg_experience = scores_data.groupby('Cluster')['Experience Score'].mean()
        return scores_data, avg_satisfaction, avg_experience

    clustered_data, avg_satisfaction, avg_experience = cluster_satisfaction(scores_data)

    st.subheader("Average Satisfaction Scores per Cluster")
    st.write(avg_satisfaction)

    # Plotting the clusters
    fig, ax = plt.subplots()
    sns.scatterplot(data=clustered_data, x='Engagement Score', y='Experience Score', hue='Cluster', ax=ax, palette='viridis')
    plt.title("Engagement vs Experience Scores by Cluster")
    st.pyplot(fig)

# Note: Ensure to call this function in your main app script.