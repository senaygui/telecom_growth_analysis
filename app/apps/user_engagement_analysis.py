import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import streamlit as st

def app():
    # Query the data
    csv_file_path = os.path.join(os.path.dirname(__file__), 'xdr_data.csv')
    data = pd.read_csv(csv_file_path)

    # Title of the section
    st.title("User Engagement Analysis")

    # Aggregate Metrics per Customer ID (MSISDN)
    dl_columns = [
        'Social Media DL (Bytes)', 
        'Google DL (Bytes)', 
        'Email DL (Bytes)', 
        'Youtube DL (Bytes)', 
        'Netflix DL (Bytes)', 
        'Gaming DL (Bytes)', 
        'Other DL (Bytes)'
    ]

    ul_columns = [
        'Social Media UL (Bytes)', 
        'Google UL (Bytes)', 
        'Email UL (Bytes)', 
        'Youtube UL (Bytes)', 
        'Netflix UL (Bytes)', 
        'Gaming UL (Bytes)', 
        'Other UL (Bytes)'
    ]

    agg_data = data.groupby('MSISDN/Number').agg(
        sessions_frequency=('Bearer Id', 'count'),
        total_duration=('Dur. (ms)', 'sum'),
        **{col: (col, 'sum') for col in dl_columns},
        **{col: (col, 'sum') for col in ul_columns}
    )

    # Calculate total data volume
    agg_data['total_traffic'] = agg_data[dl_columns].sum(axis=1) + agg_data[ul_columns].sum(axis=1)

    # Drop the intermediary columns
    agg_data = agg_data.drop(columns=dl_columns + ul_columns)

    # Display top 10 customers per engagement metric
    st.subheader("Top 10 Customers by Engagement Metrics")
    top_sessions = agg_data.nlargest(10, 'sessions_frequency')
    st.write("Top by Sessions Frequency:")
    st.write(top_sessions)

    top_duration = agg_data.nlargest(10, 'total_duration')
    st.write("Top by Total Duration:")
    st.write(top_duration)

    top_traffic = agg_data.nlargest(10, 'total_traffic')
    st.write("Top by Total Traffic:")
    st.write(top_traffic)

    # Clustering Analysis
    st.subheader("Clustering and Analysis")
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(agg_data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    agg_data['cluster'] = kmeans.fit_predict(normalized_data)

    # Compute Metrics for Each Cluster
    cluster_metrics = agg_data.groupby('cluster').agg(
        min_sessions=('sessions_frequency', 'min'),
        max_sessions=('sessions_frequency', 'max'),
        avg_sessions=('sessions_frequency', 'mean'),
        total_sessions=('sessions_frequency', 'sum'),
        min_duration=('total_duration', 'min'),
        max_duration=('total_duration', 'max'),
        avg_duration=('total_duration', 'mean'),
        total_duration=('total_duration', 'sum'),
        min_traffic=('total_traffic', 'min'),
        max_traffic=('total_traffic', 'max'),
        avg_traffic=('total_traffic', 'mean'),
        total_traffic=('total_traffic', 'sum')
    )

    st.write("Cluster Metrics:")
    st.write(cluster_metrics)

    # Visualize Results
    st.subheader("Average Sessions per Cluster")
    sns.barplot(x=cluster_metrics.index, y=cluster_metrics['avg_sessions'])
    plt.title('Average Sessions per Cluster')
    st.pyplot()

    # Elbow Method to Optimize k
    st.subheader("Elbow Method to Optimize k")
    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(normalized_data)
        inertia.append(kmeans.inertia_)

    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    st.pyplot()

    # Aggregate User Total Traffic per Application
    app_traffic = data.groupby('MSISDN/Number').agg({
        'Social Media DL (Bytes)': 'sum',
        'Youtube DL (Bytes)': 'sum',
        'Netflix DL (Bytes)': 'sum',
        'Google DL (Bytes)': 'sum',
        'Email DL (Bytes)': 'sum',
        'Gaming DL (Bytes)': 'sum',
        'Other DL (Bytes)': 'sum'
    })

    top_social_media = app_traffic.nlargest(10, 'Social Media DL (Bytes)')
    top_youtube = app_traffic.nlargest(10, 'Youtube DL (Bytes)')
    top_netflix = app_traffic.nlargest(10, 'Netflix DL (Bytes)')

    st.subheader("Top 10 Most Engaged Users per Application")
    st.write("Top by Social Media Traffic:")
    st.write(top_social_media)
    st.write("Top by YouTube Traffic:")
    st.write(top_youtube)
    st.write("Top by Netflix Traffic:")
    st.write(top_netflix)

    # Plot Top 3 Applications
    st.subheader("Top 3 Most Used Applications")
    top_apps = app_traffic.sum().nlargest(3)
    top_apps.plot(kind='bar')
    plt.title('Top 3 Most Used Applications')
    plt.ylabel('Total Traffic (Bytes)')
    st.pyplot()

# Note: Ensure to call this function in your main app script.