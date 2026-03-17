import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.analyzer import analyze_text
from utils.alert_system import AlertSystem
from utils.risk_meter import RiskMeter

st.set_page_config(layout="wide")
st.title("🌍 JanVoice AI — Smart Governance Dashboard")

alert_system = AlertSystem()
risk_engine = RiskMeter()

data_log = []

df = pd.read_csv("data/sample_live_feed.csv")

feed = st.empty()
alert_box = st.empty()
issue_chart = st.empty()
sent_chart = st.empty()
risk_area = st.empty()
map_area = st.empty()

for i,row in df.iterrows():

    result = analyze_text(row["text"])

    result["lat"] = row["lat"]
    result["lon"] = row["lon"]

    data_log.append(result)

    alert_system.update(result["issue"], result["sentiment"])
    alert = alert_system.check_alert()

    feed.write(result)

    if alert:
        alert_box.error(alert)

    temp = pd.DataFrame(data_log)

    issue_chart.bar_chart(temp["issue"].value_counts())

    sent_chart.bar_chart(temp["sentiment"].value_counts())

    risk = risk_engine.calculate(data_log)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text':"Risk Index"},
        gauge={'axis':{'range':[0,100]}}
    ))

    risk_area.plotly_chart(gauge)

    map_area.map(temp[["lat","lon"]])

    time.sleep(2)