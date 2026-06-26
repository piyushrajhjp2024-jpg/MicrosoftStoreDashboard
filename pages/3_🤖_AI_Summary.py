import streamlit as st
import pandas as pd

df = pd.read_csv("data/all_combined.csv")

st.title("🤖 AI Review Summary")

app = st.selectbox("Select App", sorted(df["app"].unique()))

reviews = df[df["app"] == app].dropna().head(100)

st.subheader("Sample Reviews")
st.write(reviews["content"].tolist()[:5])

positive = (df[df["app"] == app]["score"] >= 4).mean() * 100

st.success(f"Positive Review Rate: {positive:.1f}%")

if positive > 75:
    st.write("✅ Customers are highly satisfied with this app.")
elif positive > 50:
    st.write("🙂 Customers have mixed opinions.")
else:
    st.write("⚠️ Customers are mostly dissatisfied.")

    st.markdown("---")
st.subheader("📊 AI Insights")

col1, col2 = st.columns(2)

with col1:
    st.metric("⭐ Average Rating", round(df["score"].mean(), 2))

with col2:
    st.metric("📝 Total Reviews", len(reviews))

    st.markdown("---")
st.subheader("☁️ Most Common Words")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = " ".join(reviews["content"].dropna().astype(str))

wc = WordCloud(width=800, height=400, background_color="white").generate(text)

fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)