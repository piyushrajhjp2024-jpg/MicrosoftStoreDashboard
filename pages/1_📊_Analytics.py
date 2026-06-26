import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Analytics Dashboard")

df = pd.read_csv("data/all_combined.csv")

fig = px.histogram(
    df,
    x="score",
    color="score",
    title="Rating Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Top Apps
st.subheader("📱 Top Apps by Reviews")

top_apps = df["app"].value_counts().reset_index()
top_apps.columns = ["App", "Reviews"]

fig2 = px.bar(
    top_apps.head(10),
    x="App",
    y="Reviews",
    color="App"
)

st.plotly_chart(fig2, use_container_width=True)


