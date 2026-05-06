import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AI Customer Insights", layout="wide")
st.title("📊 Customer Churn & RFM Analysis Dashboard")

@st.cache_data
def load_data():
    # Loading your dataset
    data = pd.read_csv('E Commerce Customer Insights and Churn Dataset.csv')
    # Cleaning spaces just in case
    data.columns = data.columns.str.strip()
    return data

try:
    df = load_data()
    
    st.subheader("Business Overview")
    col1, col2, col3 = st.columns(3)
    
    # Matching your exact column names
    total_customers = df['customer_id'].nunique()
    total_revenue = (df['quantity'] * df['unit_price']).sum()
    avg_price = df['unit_price'].mean()

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Avg Unit Price", f"${avg_price:.2f}")

    # Data Table
    with st.expander("🔍 View Raw Customer Data"):
        st.dataframe(df.head(20), use_container_width=True)

    # Visualization
    st.subheader("Unit Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df['unit_price'], bins=30, kde=True, color='skyblue')
    plt.title("Product Pricing Insights")
    st.pyplot(fig)

    st.success("✅ Dashboard Fully Operational!")

except Exception as e:
    st.error(f"⚠️ Error: {e}")
    st.info("Check that your CSV column names match exactly: customer_id, quantity, unit_price, order_date")
