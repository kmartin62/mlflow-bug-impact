from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import altair as alt
from database.db import get_db
from sqlalchemy.orm import Session
from database.models import VwImprovements, VwSentimentAnalysis 

session: Session = next(get_db())

st.title("Model Improvements Visualization")

data = session.query(VwImprovements).all()

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

df = pd.DataFrame(data_list)

titles = df['title'].unique()

selected_title = st.selectbox("Select a Title", titles)

df_filtered = df[df['title'] == selected_title]

sentiment_data = session.query(VwSentimentAnalysis).filter(VwSentimentAnalysis.title == selected_title).first()

if sentiment_data:
    st.write(f"**Author**: {sentiment_data.author}")
    st.write(f"**Sentiment Label**: {sentiment_data.sentiment_label}")
    st.write(f"**Comments Count**: {sentiment_data.comments_count}")
else:
    st.write("No sentiment data available for this title.")

chart = (
    alt.Chart(df_filtered)
    .mark_bar()
    .encode(
        x=alt.X("metric:N", title="Metric"),
        y=alt.Y("value:Q", title="Percentage Change"),
        color="metric:N",
        tooltip=["title", "metric", "value"],
    )
    .properties(width=100, height=400)
)

st.altair_chart(chart, use_container_width=True)

session.close()
