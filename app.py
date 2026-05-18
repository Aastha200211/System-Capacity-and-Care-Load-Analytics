import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="System Capacity and Care Load Analytics Dashboard for Unaccompanied Children",
    page_icon="📊",
    layout="wide"
)

# =========================
# CUSTOM STYLE
# =========================
st.markdown("""
<style>

/* =========================
   MAIN BACKGROUND IMAGE
========================= */
.stApp {
    background: url("https://images.unsplash.com/photo-1516321318423-f06f85e504b3") no-repeat center center fixed;
    background-size: cover;
}


/* LIGHT OVERLAY */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.72);
    z-index: -1;
}

/* =========================
   BIG TITLE STYLE
========================= */
.big-title {
    font-size: 60px;
    font-weight: 900;
    text-align: center;
    color: yellow !important;
    text-shadow: 2px 2px 8px rgba(255,255,255,0.4);
    margin-bottom: 20px;
}

/* =========================
   TOP HEADER
========================= */
header[data-testid="stHeader"] {
    background: transparent !important;
    box-shadow: none !important;
}

/* REMOVE TOOLBAR */
div[data-testid="stToolbar"] {
    background: transparent !important;
}

/* =========================
   SIDEBAR STYLE
========================= */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.88) !important;
    backdrop-filter: blur(8px);
    border-right: 2px solid #d6e4f0 !important;
}

/* REMOVE INNER BLOCK */
section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: #2c3e50 !important;
    font-weight: 500;
}

/* =========================
   SIDEBAR INPUT BOX
========================= */
section[data-testid="stSidebar"] .stDateInput {
    background: rgba(255,255,255,0.95) !important;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #dce6f2;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

/* INPUT FIELD */
section[data-testid="stSidebar"] input {
    background: transparent !important;
    color: #2c3e50 !important;
    border: none !important;
}

/* =========================
   KPI CARD STYLE
========================= */
.card {
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

/* =========================
   TABS STYLE
========================= */
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.85);
    color: #2c3e50;
    border-radius: 10px;
    padding: 10px 20px;
    margin-right: 5px;
    font-weight: 600;
}

/* ACTIVE TAB */
.stTabs [aria-selected="true"] {
    background-color: #dbeafe;
    color: #1d4ed8;
}

/* =========================
   DATAFRAME STYLE
========================= */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.9);
    border-radius: 12px;
    padding: 10px;
}
/* TOP RIGHT DEPLOY + MENU */
button[kind="header"],
button[data-testid="baseButton-headerNoPadding"] {
    color: white !important;
}

/* SIDEBAR ARROW */
button[kind="header"] svg {
    fill: white !important;
    color: white !important;
}

/* THREE DOT MENU */
[data-testid="stToolbar"] {
    color: white !important;
}

/* DEPLOY TEXT */
.st-emotion-cache-18ni7ap {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MAIN TITLE
# =========================
st.markdown("""
<h1 class="big-title">
📊 System Capacity and Care Load Analytics Dashboard for Unaccompanied Children
</h1>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'])

# Fix HHS column
df['Children in HHS Care'] = df['Children in HHS Care'].astype(str).str.replace(',', '')
df['Children in HHS Care'] = pd.to_numeric(df['Children in HHS Care'], errors='coerce')
df['Children in HHS Care'] = df['Children in HHS Care'].ffill()

# =========================
# CREATE METRICS
# =========================
df['Total_Load'] = df['Children in CBP custody'] + df['Children in HHS Care']
df['Net_Intake'] = df['Children transferred out of CBP custody'] - df['Children discharged from HHS Care']
df['Backlog'] = df['Net_Intake'].rolling(7).mean()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

start = st.sidebar.date_input("Start Date", df['Date'].min())
end = st.sidebar.date_input("End Date", df['Date'].max())

filtered = df[(df['Date'] >= pd.to_datetime(start)) & (df['Date'] <= pd.to_datetime(end))]

# =========================
# KPI SECTION
# =========================
st.markdown("""
<h2 style="
color: #7c3aed;
font-weight: 700;
">
📌 Key Metrics
</h2>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div style="
    background: linear-gradient(135deg, #1abc9c, #16a085);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <h3>📊 Max Load</h3>
    <h2>{int(filtered['Total_Load'].max())}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f39c12, #e67e22);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <h3>⚖️ Avg Net Intake</h3>
    <h2>{round(filtered['Net_Intake'].mean(), 2)}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    padding: 25px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <h3>🚨 Max Backlog</h3>
    <h2>{round(filtered['Backlog'].max(), 2)}</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🧠 Insights"])

# =========================
# TAB 1 - OVERVIEW
# =========================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(filtered, x='Date', y='Total_Load',
                       title="Total System Load",
                       color_discrete_sequence=["#2E86C1"])
        fig1.update_layout(template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(filtered, x='Date',
                       y=['Children in CBP custody', 'Children in HHS Care'],
                       title="CBP vs HHS",
                       color_discrete_sequence=["#e74c3c", "#2ecc71"])
        fig2.update_layout(template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 2 - TRENDS
# =========================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        fig3 = px.line(filtered, x='Date', y='Net_Intake',
                       title="Net Intake Trend",
                       color_discrete_sequence=["#f39c12"])
        fig3.update_layout(template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        fig4 = px.line(filtered, x='Date', y='Backlog',
                       title="Backlog Trend",
                       color_discrete_sequence=["#8e44ad"])
        fig4.update_layout(template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True)

# =========================
# TAB 3 - INSIGHTS
# =========================
with tab3:
    st.subheader("🧠 Key Insights")

    st.markdown("""
<div style="
background: rgba(255,255,255,0.85);
padding: 20px;
border-radius: 15px;
color: #000000;
font-size: 20px;
font-weight: 600;
box-shadow: 0 4px 12px rgba(0,0,0,0.2);
margin-bottom: 20px;
">

🧠 <span style="color:#7c3aed; font-size:32px;"><b>Key Insights</b></span><br><br>

✔ System load has decreased significantly over time <br>
✔ Net intake has stabilized near zero <br>
✔ Backlog shows temporary stress but stabilizes later

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background: rgba(255,255,255,0.85);
padding: 18px;
border-radius: 15px;
color: #000000;
font-size: 20px;
font-weight: 600;
box-shadow: 0 4px 12px rgba(0,0,0,0.2);
">

📊 <span style="color:#2563eb;"><b>Forecast Insight:</b></span><br><br>

The system is currently stable with no immediate overload risk.

</div>
""", unsafe_allow_html=True)

st.write("### Data Summary")
st.dataframe(filtered.describe())