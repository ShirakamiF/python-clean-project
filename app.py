"""
Sales Dashboard - Streamlit App
Built for: cleaned_sales_data.xlsx (Order_ID, City, Product, Category, Total_Amount, etc.)

HOW TO RUN:
1. Open terminal / command prompt
2. cd into the folder where this file is saved
3. Run:  streamlit run app.py
4. Your browser will open automatically at http://localhost:8501
5. Upload your cleaned_sales_data.xlsx file using the uploader in the sidebar
"""

import streamlit as st
import pandas as pd

# ----------------------------------------------------
# PAGE CONFIG (must be the first Streamlit command)
# ----------------------------------------------------
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 Sales Data Dashboard")
st.caption("Upload your cleaned sales file to explore sales performance interactively.")

# ----------------------------------------------------
# STEP 1: FILE UPLOAD
# ----------------------------------------------------
FILE_NAME = "cleaned_sales_data.xlsx" # <-- must match your actual file name

@st.cache_data
def load_data(FILE_NAME):
    if FILE_NAME.endswith(".csv"):
        df = pd.read_csv(FILE_NAME)
    else:
        df = pd.read_excel(FILE_NAME)
    return df

try:
	df = load_data(FILE_NAME)

except FileNotFoundError:
	st.error(f"⚠️ Could not find '{FILE_NAME}'. Make sure it's in the same folder as app.py.")
	st.stop()



# Make sure Order_Date is a proper datetime (in case it wasn't saved as one)
if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# ----------------------------------------------------
# STEP 2: SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.header("Filters")

def multiselect_filter(column_name, label):
    if column_name in df.columns:
        options = sorted(df[column_name].dropna().unique().tolist())
        selected = st.sidebar.multiselect(label, options, default=options)
        return selected
    return None

city_filter = multiselect_filter("City", "City")
category_filter = multiselect_filter("Category", "Category")
status_filter = multiselect_filter("Order_Status", "Order Status")
payment_filter = multiselect_filter("Payment_Method", "Payment Method")

filtered_df = df.copy()

if city_filter is not None:
    filtered_df = filtered_df[filtered_df["City"].isin(city_filter)]
if category_filter is not None:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]
if status_filter is not None:
    filtered_df = filtered_df[filtered_df["Order_Status"].isin(status_filter)]
if payment_filter is not None:
    filtered_df = filtered_df[filtered_df["Payment_Method"].isin(payment_filter)]

# ----------------------------------------------------
# STEP 3: KPI METRIC CARDS
# ----------------------------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Total_Amount"].sum() if "Total_Amount" in filtered_df.columns else 0
total_orders = len(filtered_df)
avg_order_value = filtered_df["Total_Amount"].mean() if "Total_Amount" in filtered_df.columns else 0
avg_rating = filtered_df["Customer_Rating"].mean() if "Customer_Rating" in filtered_df.columns else 0

col1.metric("Total Sales", f"RM {total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Order Value", f"RM {avg_order_value:,.2f}")
col4.metric("Avg Rating", f"{avg_rating:.1f} / 5" if pd.notna(avg_rating) else "N/A")

st.divider()

# ----------------------------------------------------
# STEP 4: CHARTS
# ----------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales by City")
    if "City" in filtered_df.columns and "Total_Amount" in filtered_df.columns:
        city_sales = filtered_df.groupby("City")["Total_Amount"].sum().sort_values(ascending=False)
        st.bar_chart(city_sales)
    else:
        st.warning("City or Total_Amount column not found.")

with chart_col2:
    st.subheader("Sales by Category")
    if "Category" in filtered_df.columns and "Total_Amount" in filtered_df.columns:
        cat_sales = filtered_df.groupby("Category")["Total_Amount"].sum().sort_values(ascending=False)
        st.bar_chart(cat_sales)
    else:
        st.warning("Category or Total_Amount column not found.")

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("Orders by Status")
    if "Order_Status" in filtered_df.columns:
        status_counts = filtered_df["Order_Status"].value_counts()
        st.bar_chart(status_counts)
    else:
        st.warning("Order_Status column not found.")

with chart_col4:
    st.subheader("Monthly Sales Trend")
    if "Order_Month" in filtered_df.columns and "Total_Amount" in filtered_df.columns:
        monthly_sales = (
            filtered_df[filtered_df["Order_Month"] != "Missing Date"]
            .groupby("Order_Month")["Total_Amount"]
            .sum()
            .sort_index()
        )
        st.line_chart(monthly_sales)
    else:
        st.warning("Order_Month or Total_Amount column not found.")

st.divider()

# ----------------------------------------------------
# STEP 5: DATA QUALITY OVERVIEW (uses your cleaning flags!)
# ----------------------------------------------------
if "Data_Quality_Flag" in filtered_df.columns:
    st.subheader("Data Quality Overview")
    dq_col1, dq_col2 = st.columns([1, 2])

    with dq_col1:
        dq_counts = filtered_df["Data_Quality_Flag"].value_counts()
        st.write(dq_counts)

    with dq_col2:
        st.bar_chart(dq_counts)

st.divider()

# ----------------------------------------------------
# STEP 6: RAW DATA TABLE
# ----------------------------------------------------
st.subheader(f"Raw Data ({len(filtered_df)} rows)")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# STEP 7: DOWNLOAD FILTERED DATA
# ----------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
