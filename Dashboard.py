import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

sns.set(style="whitegrid")

def fraud_dashboard():
    st.set_page_config(layout="wide")
    st.sidebar.title("🛡️ SigFinance Fraud Monitor")
    st.sidebar.markdown("Real-time fraud analytics dashboard for monitoring transactions.")
    st.sidebar.markdown("---")
    st.sidebar.success("Status: Live ✅")
    st.sidebar.markdown("Built by Ibediogwu Promise Ekele")
    st.sidebar.markdown("Data Scientist | Machine Learning Engineer")

    st.title("💼 Fraud Detection Analytics Dashboard")

    try:
        df = pd.read_json("input/transaction_log.json")
    except Exception as e:
        st.warning("⚠️ No transaction log found or invalid format.")
        return

    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round('us')

    # === KPI Metrics ===
    st.markdown("## 📌 Key Performance Indicators")

    total_transactions = len(df)
    total_frauds = df['is_fraud'].sum()
    total_genuine = total_transactions - total_frauds
    total_amount = df['amount'].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="🔢 Total Transactions", value=f"{total_transactions:,}")
    with col2:
        st.metric(label="🚨 Fraudulent", value=f"{total_frauds:,}", delta_color="inverse")
    with col3:
        st.metric(label="✅ Genuine", value=f"{total_genuine:,}")
    with col4:
        st.metric(label="💰 Total Amount (NGN)", value=f"₦{total_amount:,.2f}")

    st.markdown("---")

    # === Fraud Distribution & Time Series Analysis (Same Row) ===
    st.markdown("## 📊 Fraud Overview & Activity Trend")
    col1, col2 = st.columns([1, 2])  # You can adjust ratios as needed


    # --- Column 1: Pie Chart (Plotly) ---
    with col1:
        st.markdown("#### 🧩 Fraud Distribution")
        pie_data = df['is_fraud'].value_counts().rename(index={0: 'Genuine', 1: 'Fraudulent'})
        fig_pie = go.Figure(
            data=[go.Pie(
                labels=pie_data.index,
                values=pie_data.values,
                hole=0.4,  # donut style
                marker_colors=['#2ecc71', '#e74c3c'],
                pull=[0.05] * len(pie_data),
                hoverinfo='label+percent+value'
            )]
        )
        fig_pie.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Column 2: Time Series Line Chart (Plotly) ---
    with col2:
        st.markdown("#### 📈 Hourly Transaction Trend")
        df['timestamp_hour'] = df['timestamp'].dt.floor('h')
        ts_data = df.groupby(['timestamp_hour', 'is_fraud']).size().unstack(fill_value=0)
        ts_data = ts_data.rename(columns={0: 'Genuine', 1: 'Fraudulent'})

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=ts_data.index,
            y=ts_data['Genuine'],
            mode='lines+markers',
            name='Genuine',
            line=dict(color='#2ecc71')
        ))
        fig_line.add_trace(go.Scatter(
            x=ts_data.index,
            y=ts_data['Fraudulent'],
            mode='lines+markers',
            name='Fraudulent',
            line=dict(color='#e74c3c')
        ))
        fig_line.update_layout(
            xaxis_title='Hour',
            yaxis_title='Number of Transactions',
            margin=dict(t=30, b=0, l=0, r=0),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            hovermode='x unified'
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # === Transactions Table ===
    st.markdown("## 🧾 Detailed Transaction Log")
    st.dataframe(df.sort_values(by='timestamp', ascending=False), use_container_width=True)

    st.markdown("---")

    # === PDF Export Note ===
    st.info("📥 To export this dashboard as a PDF, use your browser's print option (Ctrl+P or Cmd+P) and choose **Save as PDF**.")

fraud_dashboard()