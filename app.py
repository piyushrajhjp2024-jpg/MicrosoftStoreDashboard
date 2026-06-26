
import streamlit as st
import pandas as pd
import plotly.express as px



from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv("data/all_combined.csv")
selected_app = st.selectbox(
    "📱 Select App",
    ["All"] + sorted(df["app"].unique().tolist())
)
if selected_app != "All":
    filtered_df = df[df["app"] == selected_app]
else:
    filtered_df = df

selected_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    1,
    5,
    1
)
search = st.text_input(
    "🔍 Search App or Review",
    placeholder="Type Facebook, WhatsApp, YouTube..."
)
if selected_app == "All":
    filtered_df = df
else:
    filtered_df = df[
        (df["app"] == selected_app) &
        (df["score"] >= selected_rating)
    ]

filtered_df = filtered_df[filtered_df["score"] >= selected_rating]

total_reviews = len(filtered_df)
total_apps = filtered_df["app"].nunique()
avg_rating = round(filtered_df["score"].mean(), 2)
positive = round((filtered_df["score"] >= 4).mean() * 100, 1)
# -----------------------
# PAGE CONFIG
# -----------------------

st.set_page_config(
    page_title="Microsoft Store Analytics",
    page_icon="🏪",
    layout="wide"
)
# ===========================
# SIDEBAR
# ===========================

st.sidebar.title("🏪 Microsoft Store")

st.sidebar.markdown("---")



st.sidebar.markdown("---")

st.sidebar.success("Version 1.0")
# ======================
# SIDEBAR
# ======================

st.sidebar.markdown("# 🏪Microsoft Store")

st.sidebar.title("Microsoft Store")

st.sidebar.markdown("---")



st.sidebar.markdown("---")

st.sidebar.success("Dashboard v1.0")
# ==========================
# SIDEBAR
# ==========================

st.sidebar.image("assets/logo.png", width=70)

st.sidebar.title("Microsoft Store")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Analytics",
        "😊 Sentiment",
        "📱 Apps",
        "🔍 Search",
        "⚙️ Settings"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write("Made with ❤️ using Streamlit")

# -----------------------
# HEADER
# -----------------------

col1,col2,col3=st.columns([1,7,1])

with col1:
    st.markdown("## 🏪")

with col2:
    st.text_input(
        "",
        placeholder="🔍 Search apps, reviews and more..."
    )

with col3:
    st.markdown("## 👤")

# -----------------------
# HERO IMAGE
# -----------------------

st.markdown("""
<div style="
background:linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB);
padding:50px;
border-radius:20px;
margin-top:20px;
margin-bottom:20px;
">

<h1 style="color:white;font-size:45px;">
📊 Customer Review Analytics Dashboard
</h1>

<p style="color:white;font-size:20px;">
Analyze 200,000+ App Reviews using Python, SQL, Power BI, Tableau & AI
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("## 📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    ">
    <h2>⭐ {avg_rating}</h2>
    <p>Average Rating</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    ">
    <h2>💬 {total_reviews}</h2>
    <p>Total Reviews</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    ">
    <h2>📱 {total_apps}</h2>
    <p>Total Apps</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    ">
    <h2>😊 {positive}%</h2>
    <p>Positive Reviews</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 🔥 Trending Apps")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    ">
    <h2>📘 Facebook</h2>
    <h3>⭐ 4.6</h3>
    <p>12,450 Reviews</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    ">
    <h2>📸 Instagram</h2>
    <h3>⭐ 4.4</h3>
    <p>9,850 Reviews</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    ">
    <h2>💬 WhatsApp</h2>
    <h3>⭐ 4.3</h3>
    <p>8,540 Reviews</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style="
    background:#1E293B;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    ">
    <h2>📺 YouTube</h2>
    <h3>⭐ 4.5</h3>
    <p>7,620 Reviews</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("## 📊 Rating Distribution")

fig = px.histogram(
    filtered_df,
    x="score",
    color="score",
    title="Rating Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.markdown("## 😊 Sentiment Analysis")

sentiment = pd.DataFrame({
    "Sentiment": ["Positive", "Neutral", "Negative"],
    "Count": [76, 18, 6]
})

fig2 = px.pie(
    sentiment,
    names="Sentiment",
    values="Count",
    hole=0.6,
    title="Customer Sentiment"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
st.markdown("---")
st.markdown("## 📱 Top Apps by Reviews")
top_apps = filtered_df["app"].value_counts().reset_index()
top_apps.columns = ["App", "Reviews"]
fig3 = px.bar(
    top_apps.head(10),
    x="App",
    y="Reviews",
    color="Reviews",
    title="Top 10 Apps by Number of Reviews",
    text_auto=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
st.markdown("---")
st.markdown("## 🔍 Search Reviews")
search_app = st.text_input(
    "Search by App Name",
    placeholder="Example: Facebook"
)
if search_app:

    filtered = filtered_df[
        filtered_df["app"].str.contains(
            search_app,
            case=False,
            na=False
        )
    ]

    st.dataframe(
    filtered[
        ["app", "score", "content"]
    ]
)
st.markdown("---")
st.markdown("## 😊 Top Positive Reviews")

positive = filtered_df[
    filtered_df["score"] >= 4
]

st.dataframe(
    positive[
        ["app", "score", "content"]
    ].head(10)
)
st.markdown("---")
st.markdown("## 😞 Worst Reviews")

negative = df[
    df["score"] <= 2
]

st.dataframe(
    negative[
        ["app", "score", "content"]
    ].head(10)
)
st.markdown("---")
st.markdown("## ☁️ Most Used Words in Reviews")

sample_df = df.sample(5000, random_state=42)
text = " ".join(sample_df["content"].dropna().astype(str))
wc = WordCloud(
    width=1000,
    height=500,
    background_color="black",
    colormap="viridis"
).generate(text)

fig, ax = plt.subplots(figsize=(14,6))
ax.imshow(wc)
ax.axis("off")

st.pyplot(fig)
st.markdown("---")
st.markdown("## ⭐ Featured Apps")

c1, c2, c3 = st.columns(3)

with c1:
    st.image("assets/logo.png", width=80)
    st.write("### Facebook")
    st.write("⭐ 4.6")

with c2:
    st.image("assets/logo.png", width=80)
    st.write("### Instagram")
    st.write("⭐ 4.5")

with c3:
    st.image("assets/logo.png", width=80)
    st.write("### WhatsApp")
    st.write("⭐ 4.4")
    st.markdown("---")
st.markdown("## 📝 Latest Reviews")

st.dataframe(
    filtered_df[["app", "score", "content"]].head(20),
    use_container_width=True
)

st.download_button(
    label="📥 Download Reviews CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_reviews.csv",
    mime="text/csv"
)


st.markdown("---")
st.markdown("## 🤖 AI Review Summary")

positive = (filtered_df["score"] >= 4).sum()
negative = (filtered_df["score"] <= 2).sum()
neutral = len(filtered_df) - positive - negative

if positive > negative:
    st.success(
        f"Most users are satisfied with this app.\n\n"
        f"✅ Positive Reviews: {positive}\n"
        f"😐 Neutral Reviews: {neutral}\n"
        f"❌ Negative Reviews: {negative}"
    )
else:
    st.warning(
        f"Users have mixed opinions.\n\n"
        f"✅ Positive Reviews: {positive}\n"
        f"😐 Neutral Reviews: {neutral}\n"
        f"❌ Negative Reviews: {negative}"
    )


st.markdown("---")
st.markdown("## 📊 Rating Distribution")
fig = px.histogram(
    filtered_df,
    x="score",
    color="score",
    title="Distribution of Ratings"
)

st.plotly_chart(fig, use_container_width=True)




st.markdown("---")
st.markdown("## 🥧 Positive vs Negative Reviews")

positive = len(df[df["score"] >= 4])
negative = len(df[df["score"] < 4])

pie = px.pie(
    names=["Positive", "Negative"],
    values=[positive, negative],
    title="Review Sentiment"
)

st.plotly_chart(pie, use_container_width=True)


st.markdown("---")
st.markdown("## 📊 Top Apps by Reviews")

top_apps = (
    filtered_df["app"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_apps.columns = ["App", "Reviews"]

bar = px.bar(
    top_apps,
    x="App",
    y="Reviews",
    color="App",
    title="Top 10 Apps by Number of Reviews"
)
bar.update_layout(
    plot_bgcolor="#0F172A",
    paper_bgcolor="#0F172A",
    font=dict(
        color="white",
        size=14
    ),
    title_font=dict(
        color="white",
        size=22
    ),
    xaxis=dict(
        title="App",
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    yaxis=dict(
        title="Reviews",
        title_font=dict(color="white"),
        tickfont=dict(color="white")
    ),
    legend=dict(
        font=dict(color="white")
    )
)
bar.update_traces(textfont_color="white")

st.plotly_chart(bar, use_container_width=True)


st.markdown("---")
st.markdown("## 📥 Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="filtered_reviews.csv",
    mime="text/csv"
)

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:gray;
font-size:16px;
">
© 2025 Microsoft Store Analytics Dashboard<br>
Built with ❤️ using Python, SQL, Streamlit, Power BI & Tableau
</div>
""", unsafe_allow_html=True)