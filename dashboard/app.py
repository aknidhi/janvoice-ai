import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

from src.analyzer import analyze_text
from utils.alert_system import AlertSystem
from utils.risk_meter import RiskMeter

st.set_page_config(
    page_title="JanVoice AI Control Room",
    layout="wide"
)

st.title("🌍 JanVoice AI — Smart Governance Control Room")

# ===================== SYSTEM OBJECTS =====================

alert_system = AlertSystem()
risk_engine = RiskMeter()

feed_col, alert_col = st.columns([3,1])

issue_chart = st.empty()
sentiment_chart = st.empty()
risk_meter_area = st.empty()
map_area = st.empty()

kpi_area = st.empty()

data_log = []

df = pd.read_csv("data/sample_live_feed.csv")

# ===================== LIVE STREAM =====================

for i, row in df.iterrows():

    result = analyze_text(row['text'])

    result['lat'] = row['lat']
    result['lon'] = row['lon']

    data_log.append(result)

    # ---------- ALERT SYSTEM ----------
    alert_system.update(result['issue'], result['sentiment'])
    alert = alert_system.check_alert()

    # ---------- KPI METRICS ----------
    temp_df = pd.DataFrame(data_log)

    total_msgs = len(temp_df)
    neg_msgs = temp_df[temp_df['sentiment'].astype(str).str.contains("1|2")].shape[0]
    top_issue = temp_df['issue'].value_counts().idxmax()

    with kpi_area.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("📨 Total Messages", total_msgs)
        c2.metric("⚠ Negative Messages", neg_msgs)
        c3.metric("🔥 Top Issue", top_issue)

    # ---------- LIVE FEED ----------
    with feed_col:
        st.subheader("📡 Live Public Feed")
        st.write(result)

    # ---------- ALERT BOX ----------
    with alert_col:
        st.subheader("🚨 Alerts")
        if alert:
            st.error(alert)
        else:
            st.success("No Critical Alert")

    # ---------- ISSUE DISTRIBUTION ----------
    issue_chart.subheader("📊 Issue Distribution")
    issue_chart.bar_chart(temp_df['issue'].value_counts())

    # ---------- SENTIMENT TREND ----------
    sentiment_chart.subheader("😊 Sentiment Trend")
    sentiment_chart.line_chart(
        temp_df['sentiment'].astype(str).str[0].astype(int)
    )

    # ---------- RISK METER ----------
    risk_score = risk_engine.calculate(data_log)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': "🚨 Public Risk Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}
            ]
        }
    ))

    risk_meter_area.plotly_chart(gauge, use_container_width=True)

    # ---------- MAP ----------
    map_area.subheader("🗺️ Complaint Hotspots")
    map_area.map(temp_df[['lat','lon']])

    time.sleep(2)