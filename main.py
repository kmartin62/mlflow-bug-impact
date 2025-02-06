from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import altair as alt
from database.db import get_db
from sqlalchemy.orm import Session
from database.models import VwImprovements, VwSentimentAnalysis  # Make sure VwSentimentAnalysis is imported

session: Session = next(get_db())

st.title("Model Improvements Visualization")

# Get all data from the database
data = session.query(VwImprovements).all()

# Prepare data for visualization
data_list = []
for row in data:
    data_list.append({
        "title": row.title,
        "metric": "Accuracy",
        "value": row.percentage_change_accuracy
    })
    data_list.append({
        "title": row.title,
        "metric": "Recall",
        "value": row.percentage_change_recall
    })
    data_list.append({
        "title": row.title,
        "metric": "Precision",
        "value": row.percentage_change_precision
    })
    data_list.append({
        "title": row.title,
        "metric": "F1 Score",
        "value": row.percentage_change_f1
    })
    data_list.append({
        "title": row.title,
        "metric": "Log Loss",
        "value": row.percentage_change_log_loss
    })

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data_list)

# Get unique titles for the dropdown
titles = df['title'].unique()

# Add a dropdown to select the title
selected_title = st.selectbox("Select a Title", titles)

# Filter the data for the selected title
df_filtered = df[df['title'] == selected_title]

# Query the sentiment analysis data for the selected title
sentiment_data = session.query(VwSentimentAnalysis).filter(VwSentimentAnalysis.title == selected_title).first()

# Display sentiment, author, and comments count if sentiment data exists
if sentiment_data:
    st.write(f"**Author**: {sentiment_data.author}")
    st.write(f"**Sentiment Label**: {sentiment_data.sentiment_label}")
    st.write(f"**Comments Count**: {sentiment_data.comments_count}")
else:
    st.write("No sentiment data available for this title.")

# Create a bar chart for the selected title
chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("metric:N", title="Metric"),
        y=alt.Y("value:Q", title="Percentage Change"),
        color="metric:N",
        tooltip=["title", "metric", "value"],
    )
    .properties(width=100, height=400)  # Set width and height for better display
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

session.close()
