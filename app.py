import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="Orders Dashboard", layout="wide")
st.title("Orders Analytics Dashboard")

# ==========================
# LOAD DATA
# ==========================
df = pd.read_csv("orders_clean.csv")

# ==========================
# KEY METRICS
# ==========================
total_orders = len(df)
total_revenue = df["Value"].sum()
avg_order_value = df["Value"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

# ==========================
# TOP COMBOS
# ==========================
if "Ship_Mode" in df.columns and "Segment" in df.columns:
    st.subheader(" Top Ship Mode × Segment Combos")
    top_combos = df.groupby(["Ship_Mode","Segment"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False).head(10)
    st.table(top_combos)

# ==========================
# TOP 5 CUSTOMERS
# ==========================
if "Customer_ID" in df.columns:
    st.subheader(" Top 5 Customers")
    top_customers = df.groupby("Customer_ID").agg(
        Total_Orders=("Value", "count"),
        Total_Revenue=("Value", "sum")
    ).sort_values(by="Total_Revenue", ascending=False).head(5).reset_index()

    # Add preferred Ship Mode × Segment combo for each customer
    top_customers["Top_Combo"] = top_customers["Customer_ID"].apply(
        lambda x: df[df["Customer_ID"] == x].groupby(["Ship_Mode","Segment"]).size().idxmax()
    )
    st.table(top_customers)

# ==========================
# ORDERS BY SHIP MODE
# ==========================
if "Ship_Mode" in df.columns:
    st.subheader("Orders by Ship Mode")
    fig, ax = plt.subplots()
    df["Ship_Mode"].value_counts().plot(kind="bar", ax=ax, color="skyblue")
    ax.set_xlabel("Ship Mode")
    ax.set_ylabel("Number of Orders")
    st.pyplot(fig)

# ORDERS BY SEGMENT
if "Segment" in df.columns:
    st.subheader("Orders by Segment")
    fig2, ax2 = plt.subplots()
    df["Segment"].value_counts().plot(kind="bar", ax=ax2, color="lightgreen")
    ax2.set_xlabel("Segment")
    ax2.set_ylabel("Number of Orders")
    st.pyplot(fig2)

# ==========================
# FILTER
# ==========================
min_val, max_val = st.slider(
    "Filter Orders by Value",
    float(df["Value"].min()),
    float(df["Value"].max()),
    (float(df["Value"].min()), float(df["Value"].max()))
)
filtered_df = df[(df["Value"] >= min_val) & (df["Value"] <= max_val)]

# Histogram
st.subheader("Order Value Distribution")
fig3, ax3 = plt.subplots()
ax3.hist(filtered_df["Value"], bins=20, color="skyblue", edgecolor="black")
ax3.set_xlabel("Order Value")
ax3.set_ylabel("Number of Orders")
st.pyplot(fig3)


