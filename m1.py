import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sample_sales_dataset.csv", parse_dates=["Date"])
    return df

df = load_data()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔍 Filter Options")

selected_region = st.sidebar.multiselect(
    "Select Region(s)", options=df["Region"].unique(), default=df["Region"].unique()
)
selected_category = st.sidebar.multiselect(
    "Select Category(s)", options=df["Category"].unique(), default=df["Category"].unique()
)
selected_store = st.sidebar.multiselect(
    "Select Store(s)", options=df["Store_ID"].unique(), default=df["Store_ID"].unique()
)

# Apply filters
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Store_ID"].isin(selected_store))
]

# ---------------------------
# Dashboard Header
# ---------------------------
st.title("📈 Sales Analytics and Forecasting Dashboard")
st.markdown("This interactive dashboard provides insights from 5 years of sales data including revenue trends, product performance, and customer behavior.")

# ---------------------------
# Key Metrics
# ---------------------------
total_revenue = filtered_df["Revenue"].sum()
avg_units_sold = filtered_df["Units_Sold"].mean()
avg_rating = filtered_df["Customer_Rating"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Avg Units Sold", f"{avg_units_sold:,.0f}")
col3.metric("⭐ Avg Customer Rating", f"{avg_rating:.2f}")

st.markdown("---")

# ---------------------------
# Time Series Visualization
# ---------------------------
st.subheader("📅 Revenue Over Time")
revenue_over_time = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
fig_revenue = px.line(
    revenue_over_time, x="Date", y="Revenue",
    title="Monthly Revenue Trend (2018–2022)",
    markers=True, template="plotly_white"
)
st.plotly_chart(fig_revenue, use_container_width=True)

# ---------------------------
# Category-wise Analysis
# ---------------------------
st.subheader("🛍️ Revenue by Product Category")
category_revenue = filtered_df.groupby("Category")["Revenue"].sum().reset_index()
fig_category = px.bar(
    category_revenue, x="Category", y="Revenue",
    color="Category", title="Total Revenue by Category",
    text_auto=True, template="plotly_white"
)
st.plotly_chart(fig_category, use_container_width=True)

# ---------------------------
# Regional Performance
# ---------------------------
st.subheader("🌍 Regional Performance")
region_revenue = filtered_df.groupby("Region")["Revenue"].sum().reset_index()
fig_region = px.pie(
    region_revenue, names="Region", values="Revenue",
    title="Revenue Share by Region"
)
st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------
# Correlation Heatmap
# ---------------------------
st.subheader("📊 Correlation Heatmap")
numeric_cols = ["Units_Sold", "Unit_Price", "Discount", "Revenue", "Marketing_Spend", "Competitor_Price", "Customer_Rating"]
corr = filtered_df[numeric_cols].corr()

fig_corr = px.imshow(
    corr, text_auto=True, color_continuous_scale="RdBu_r",
    title="Feature Correlation Matrix"
)
st.plotly_chart(fig_corr, use_container_width=True)

# ---------------------------
# Data Table
# ---------------------------
st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered_df.head(20))

st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit and Plotly")
