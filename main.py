from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import altair as alt
from database.db import get_db
from sqlalchemy.orm import Session
from database.models import VwImprovements

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

df['title'] = df['title'].astype(str)

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("title:N", title="Pull Request Title"),
        y=alt.Y("value:Q", title="Percentage Change"),
        color="metric:N",
        tooltip=["title", "metric", "value"],
    )
    .properties(width=800, height=400)
)

st.altair_chart(chart, use_container_width=True)

session.close()
