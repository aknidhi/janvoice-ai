import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

from src.analyzer import analyze_text
from utils.alert_system import AlertSystem
from utils.risk_meter import RiskMeter

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="JanVoice AI Control Room",
    layout="wide"
)

# ---------- DARK THEME STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
.block-container {
    padding-top: 1rem;
}
.kpi-card {
    background-color: #161B22;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #30363D;
}
.alert-box {
    background-color: #2b0000;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid red;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🌍 JanVoice AI — Smart Governance Control Room")

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Control Panel")
speed = st.sidebar.slider("Simulation Speed", 1, 5, 2)
issue_filter = st.sidebar.selectbox(
    "Filter Issue",
    ["All","Traffic","Water","Electricity","Road","General"]
)

# ---------- SYSTEM OBJECTS ----------
alert_system = AlertSystem()
risk_engine = RiskMeter()

data_log = []

df = pd.read_csv("data/sample_live_feed.csv")

# ---------- KPI PLACEHOLDER ----------
kpi_area = st.empty()

# ---------- GRID LAYOUT ----------
col1, col2 = st.columns([2,1])
chart_col, map_col = st.columns([2,1])

feed_area = col1.empty()
alert_area = col2.empty()
issue_chart = chart_col.empty()
sent_chart = chart_col.empty()
risk_meter = map_col.empty()
map_area = map_col.empty()

# ---------- LIVE LOOP ----------
for i,row in df.iterrows():

    result = analyze_text(row["text"])
    result["lat"] = row["lat"]
    result["lon"] = row["lon"]

    data_log.append(result)

    alert_system.update(result["issue"], result["sentiment"])
    alert = alert_system.check_alert()

    temp = pd.DataFrame(data_log)

    # ---------- FILTER ----------
    if issue_filter != "All":
        temp = temp[temp["issue"] == issue_filter]

    # ---------- KPI ----------
    total = len(temp)
    negative = len(temp[temp["sentiment"]=="Negative"])
    top_issue = temp["issue"].value_counts().idxmax()

    with kpi_area.container():
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='kpi-card'><h3>{total}</h3>Total Messages</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='kpi-card'><h3>{negative}</h3>Negative</div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='kpi-card'><h3>{top_issue}</h3>Top Issue</div>", unsafe_allow_html=True)

    # ---------- ANIMATED LIVE FEED ----------
    feed_area.subheader("📡 Live Public Feed")

    feed_html = """
    <div style="
    height:220px;
    overflow:hidden;
    background:#161B22;
    padding:10px;
    border-radius:10px;
    border:1px solid #30363D;
    ">
    <marquee direction="up" scrollamount="2">
    """

    for item in data_log[-8:]:
        feed_html += f"""
        <p style='color:#58a6ff'>
        {item['text']} → <b>{item['issue']}</b> ({item['sentiment']})
        </p>
        """

    feed_html += "</marquee></div>"

    feed_area.markdown(feed_html, unsafe_allow_html=True)

        # ---------- ALERT ----------
    alert_area.subheader("🚨 Alerts")
    if alert:
        alert_area.markdown(f"<div class='alert-box'>{alert}</div>", unsafe_allow_html=True)
    else:
        alert_area.success("No critical alert")

    # ---------- ISSUE CHART ----------
    import plotly.express as px

    issue_chart.subheader("📊 Issue Distribution")

    issue_counts = temp["issue"].value_counts().reset_index()
    issue_counts.columns = ["Issue","Count"]

    fig_issue = px.bar(
        issue_counts,
        x="Issue",
        y="Count",
        color="Count",
        color_continuous_scale="Turbo"
)

    fig_issue.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white"
)

    issue_chart.plotly_chart(fig_issue, use_container_width=True)

    # ---------- SENTIMENT CHART ----------
    sent_chart.subheader("😊 Sentiment Analysis")

    sent_counts = temp["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment","Count"]

    fig_sent = px.pie(
        sent_counts,
        values="Count",
        names="Sentiment",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    fig_sent.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white"
    )

    sent_chart.plotly_chart(fig_sent, use_container_width=True)

    # ---------- RISK METER ----------
    risk = risk_engine.calculate(data_log)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text':"🚨 Public Risk Index"},
        gauge={
            'axis':{'range':[0,100]},
            'steps':[
                {'range':[0,30],'color':"green"},
                {'range':[30,70],'color':"orange"},
                {'range':[70,100],'color':"red"}
            ]
        }
    ))

    risk_meter.plotly_chart(gauge, key=f"risk_gauge_{time.time()}", use_container_width=True)

    # ---------- MAP ----------
    map_area.subheader("🗺️ Complaint Hotspots")
    map_area.map(temp[["lat","lon"]])

    time.sleep(speed)