import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Executive Customer Analytics", layout="wide")

# Premium Gold & Black CSS Injection
st.markdown("""
    <style>
        .main {
            background-color: #0b0d10;
            color: #e0e0e0;
        }
        h1, h2, h3 {
            color: #D4AF37 ! inportant;
        }
        .stMetric label {
            color: #D4AF37 !important;
            font-weight: bold;
        }
        .stMetric div[data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
        .stDataFrame {
            border: 1px solid #D4AF37;
        }
        hr {
            border-top: 1px solid #D4AF37;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Executive Customer Intelligence Dashboard")
st.markdown("Automated RFM Segmentation and Churn Prediction")

@st.cache_data
def process_executive_data():
    # Loading the dataset from the repository
    df = pd.read_csv('E Commerce Customer Insights and Churn Dataset.csv')
    df.columns = df.columns.str.strip().str.lower()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['transaction_total'] = df['quantity'] * df['unit_price']
    
    # Logic for RFM Analysis
    reference_date = df['order_date'].max()
    rfm = df.groupby('customer_id').agg({
        'order_date': lambda x: (reference_date - x.max()).days,
        'customer_id': 'count',
        'transaction_total': 'sum'
    }).rename(columns={'order_date': 'recency', 'customer_id': 'frequency', 'transaction_total': 'monetary'})

    # Dynamic Scoring Logic
    rfm['r_rank'] = pd.qcut(rfm['recency'], 3, labels=[3, 2, 1])
    rfm['f_rank'] = pd.qcut(rfm['frequency'].rank(method='first'), 3, labels=[1, 2, 3])
    rfm['m_rank'] = pd.qcut(rfm['monetary'], 3, labels=[1, 2, 3])
    
    def define_segment(row):
        total_score = int(row['r_rank']) + int(row['f_rank']) + int(row['m_rank'])
        if total_score >= 8: return 'Platinum Champion'
        if total_score >= 5: return 'Gold Loyalists'
        return 'At Risk'
        
    rfm['customer_segment'] = rfm.apply(define_segment, axis=1)
    return rfm

try:
    data_engine = process_executive_data()

    # Executive Summary Metrics
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Client Base", f"{len(data_engine):,}")
    m2.metric("Gross Revenue Contribution", f"${data_engine['monetary'].sum():,.2f}")
    m3.metric("Average Lifetime Value", f"${data_engine['monetary'].mean():,.2f}")

    # Strategic Analysis Section
    st.markdown("---")
    left, right = st.columns([6, 4])

    with left:
        st.subheader("Market Segment Distribution")
        # Gold and Black themed Chart
        fig = px.pie(data_engine, names='customer_segment', 
                     color='customer_segment',
                     color_discrete_map={
                         'Platinum Champion': '#D4AF37', 
                         'Gold Loyalists': '#996515', 
                         'At Risk': '#43464B'
                     },
                     hole=0.4)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Top Priority Accounts")
        top_tier = data_engine.sort_values('monetary', ascending=False).head(10)
        st.dataframe(top_tier[['monetary', 'customer_segment']], use_container_width=True)

    # Customer Intelligence Search
    st.markdown("---")
    st.subheader("Individual Account Lookup")
    target_id = st.selectbox("Select Account ID for Detailed Analysis", data_engine.index)
    
    selected_client = data_engine.loc[target_id]
    st.write(f"The account **{target_id}** is classified as: **{selected_client['customer_segment']}**")
    st.info(f"Last Transaction: {selected_client['recency']} days ago | Total Orders: {selected_client['frequency']}")

except Exception as error:
    st.error(f"System Error: {error}")
