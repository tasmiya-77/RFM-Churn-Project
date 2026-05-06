import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Professional Page Setup
st.set_page_config(page_title="AI Customer Insights", layout="wide")

st.title("📊 Customer Churn & RFM Analysis Dashboard")
st.markdown("### Identifying at-risk customers and high-value segments.")

@st.cache_data
def load_data():
    # Load the specific file from your repository
    data = pd.read_csv('E Commerce Customer Insights and Churn Dataset.csv')
    # Clean column names (removes hidden spaces)
    data.columns = data.columns.str.strip()
    return data

try:
    df = load_data()
    
    # 1. KPIs / Metrics Row
    st.subheader("Business Overview")
    col1, col2, col3 = st.columns(3)
    
    # Using your confirmed column name 'customer_id'
    total_customers = df['customer_id'].nunique()
    total_revenue = (df['Quantity'] * df['UnitPrice']).sum()
    avg_price = df['UnitPrice'].mean()

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Avg Unit Price", f"${avg_price:.2f}")

    # 2. Data Preview Section
    with st.expander("🔍 View Raw Customer Data"):
        st.dataframe(df.head(20), use_container_width=True)

    # 3. Simple Visual for the Portfolio
    st.subheader("Unit Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df['UnitPrice'], bins=30, kde=True, color='skyblue')
    plt.xlabel("Price")
    plt.title("Range of Product Prices")
    st.pyplot(fig)

    st.success("✅ Dashboard is live and connected to GitHub!")

except Exception as e:
    st.error(f"⚠️ Error Loading Dashboard: {e}")
    st.info("Double-check that the file 'E Commerce Customer Insights and Churn Dataset.csv' is in your GitHub main folder.")
