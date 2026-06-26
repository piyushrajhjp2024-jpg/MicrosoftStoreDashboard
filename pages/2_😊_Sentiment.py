import streamlit as st
import pandas as pd
import plotly.express as px

st.title("😊 Sentiment Analysis")

df = pd.read_csv("data/all_combined.csv")

positive = len(df[df["score"] >= 4])
negative = len(df[df["score"] < 4])

fig = px.pie(
    names=["Positive", "Negative"],
    values=[positive, negative],
    hole=0.5,
    title="Review Sentiment"
)

st.plotly_chart(fig, use_container_width=True)