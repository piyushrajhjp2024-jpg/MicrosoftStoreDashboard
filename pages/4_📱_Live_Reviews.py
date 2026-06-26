import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
import plotly.express as px
from google_play_scraper import reviews
from transformers import pipeline
from streamlit_autorefresh import st_autorefresh
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Review Analytics Dashboard",
    page_icon="📱",
    layout="wide"
)

st_autorefresh(
    interval=30000,
    key="refresh"
)

# =========================
# TITLE
# =========================

st.title("📱 AI-Powered Real-Time App Review Analytics Dashboard")

st.markdown("---")

# =========================
# APP SELECTOR
# =========================

apps = {
    "WhatsApp": "com.whatsapp",
    "Instagram": "com.instagram.android",
    "Facebook": "com.facebook.katana",
    "Telegram": "org.telegram.messenger",
    "Spotify": "com.spotify.music"
}

selected_app = st.selectbox(
    "Select Application",
    list(apps.keys())
)

app_id = apps[selected_app]

# =========================
# BUTTON
# =========================

if st.button("🚀 Fetch Reviews"):

    with st.spinner("Fetching reviews and analyzing sentiment..."):

        sentiment_model = pipeline(
            "sentiment-analysis"
        )

        result, _ = reviews(
            app_id,
            count=100
        )

        seen = set()

        sentiments = []
        ratings = []

        positive_reviews = []
        negative_reviews = []

        review_data = []

        # =========================
        # REVIEW PROCESSING
        # =========================

        for r in result:

            review_text = str(
                r["content"]
            ).strip()

            if len(review_text) < 20:
                continue

            if review_text in seen:
                continue

            seen.add(review_text)

            rating = r["score"]

            ratings.append(rating)

            sentiment_result = sentiment_model(
                review_text[:512]
            )

            label = sentiment_result[0]["label"]

            confidence = round(
                sentiment_result[0]["score"],
                3
            )

            sentiments.append(label)

            if label == "POSITIVE":
                positive_reviews.append(
                    review_text
                )
            else:
                negative_reviews.append(
                    review_text
                )

            review_data.append(
                {
                    "Rating": rating,
                    "Sentiment": label,
                    "Confidence": confidence,
                    "Review": review_text
                }
            )

        # =========================
        # DATAFRAME
        # =========================

        review_df = pd.DataFrame(
            review_data
        )

        if review_df.empty:
            st.error(
                "No reviews found."
            )
            st.stop()

        total_reviews = len(
            review_df
        )

        positive_count = len(
            review_df[
                review_df["Sentiment"]
                == "POSITIVE"
            ]
        )

        negative_count = len(
            review_df[
                review_df["Sentiment"]
                == "NEGATIVE"
            ]
        )

        avg_rating = round(
            review_df["Rating"].mean(),
            2
        )

        positive_pct = round(
            positive_count
            / total_reviews
            * 100,
            1
        )

        negative_pct = round(
            negative_count
            / total_reviews
            * 100,
            1
        )

        # =========================
        # KPI CARDS
        # =========================

        st.header(
            "📊 Dashboard Overview"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📄 Reviews",
                total_reviews
            )

        with col2:
            st.metric(
                "⭐ Avg Rating",
                avg_rating
            )

        with col3:
            st.metric(
                "😊 Positive %",
                positive_pct
            )

        with col4:
            st.metric(
                "😡 Negative %",
                negative_pct
            )

        # =========================
        # PIE CHART
        # =========================

        pie = px.pie(
            review_df,
            names="Sentiment",
            title="Sentiment Distribution"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

        # =========================
        # TREND CHART
        # =========================

        trend_df = pd.DataFrame(
            {
                "Review Number": range(
                    1,
                    len(sentiments) + 1
                ),
                "Positive Reviews": [
                    sentiments[:i].count(
                        "POSITIVE"
                    )
                    for i in range(
                        1,
                        len(sentiments) + 1
                    )
                ]
            }
        )

        st.subheader(
            "📈 Sentiment Trend"
        )

        st.line_chart(
            trend_df.set_index(
                "Review Number"
            )
        )

        # =========================
        # AI SUMMARY
        # =========================

        st.subheader(
            "🤖 AI Review Summary"
        )

        if positive_pct >= 70:

            st.success(
                f"""
Customers are highly satisfied.

Average Rating: {avg_rating}

Positive Reviews: {positive_pct}%

Negative Reviews: {negative_pct}%
"""
            )

        elif positive_pct >= 50:

            st.warning(
                f"""
Customer feedback is mixed.

Average Rating: {avg_rating}

Positive Reviews: {positive_pct}%

Negative Reviews: {negative_pct}%
"""
            )

        else:

            st.error(
                f"""
Customer satisfaction is low.

Average Rating: {avg_rating}

Positive Reviews: {positive_pct}%

Negative Reviews: {negative_pct}%
"""
            )

        # =========================
        # WORD CLOUD
        # =========================

        st.subheader(
            "☁️ Review Word Cloud"
        )

        all_text = " ".join(
            positive_reviews
            + negative_reviews
        )

        if len(all_text) > 0:

            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color="white"
            ).generate(
                all_text
            )

            fig, ax = plt.subplots(
                figsize=(10, 5)
            )

            ax.imshow(
                wordcloud
            )

            ax.axis("off")

            st.pyplot(fig)

        # =========================
        # BEST REVIEWS
        # =========================

        st.subheader(
            "🏆 Best Reviews"
        )

        for review in positive_reviews[:5]:
            st.success(review)

        # =========================
        # COMPLAINTS
        # =========================

        st.subheader(
            "⚠️ Customer Complaints"
        )

        for review in negative_reviews[:5]:
            st.error(review)
    st.subheader("🔍 Top Issues Detection")

    issue_keywords = [
        "login",
        "otp",
        "call",
        "message",
        "verification",
        "payment",
        "crash",
        "slow",
        "account",
        "update"
    ]

    issue_counts = {}

    all_reviews_text = " ".join(
        negative_reviews
    ).lower()

    for keyword in issue_keywords:

        issue_counts[keyword] = (
            all_reviews_text.count(keyword)
        )

    issues_df = pd.DataFrame(
        issue_counts.items(),
        columns=[
            "Issue",
            "Count"
        ]
    )

    issues_df = issues_df.sort_values(
        by="Count",
        ascending=False
    )

    st.dataframe(
        issues_df,
        use_container_width=True
    )

        # =========================
        # RAW DATA
        # =========================

    st.subheader(
            "📋 Review Dataset"
        )

    st.dataframe(
            review_df,
            use_container_width=True
    )
    fig = px.bar(
    issues_df.head(10),
    x="Issue",
    y="Count",
    title="Top Customer Issues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



    pdf_file = "review_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(
            100,
            800,
            "AI Review Analytics Report"
        )

    c.drawString(
            100,
            770,
            f"Total Reviews: {total_reviews}"
        )

    c.drawString(
            100,
            740,
            f"Average Rating: {avg_rating}"
        )

    c.save()

    with open(pdf_file, "rb") as pdf:
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name="review_report.pdf",
                mime="application/pdf"
            )