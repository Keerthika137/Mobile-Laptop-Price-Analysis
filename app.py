import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Mobile & Laptop Price Analysis",
    page_icon="💻",
    layout="wide"
)

st.title("📱 Mobile & Laptop Price Comparison Dashboard")
st.write("Explore product prices, brands, and marketplace differences.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("mobile_laptop_prices_cleaned.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Products")

product_types = st.sidebar.multiselect(
    "Product Type",
    options=sorted(df["product_type"].dropna().unique()),
    default=sorted(df["product_type"].dropna().unique())
)

brands = st.sidebar.multiselect(
    "Brand",
    options=sorted(df["brand"].dropna().unique()),
    default=sorted(df["brand"].dropna().unique())
)

marketplaces = st.sidebar.multiselect(
    "Marketplace",
    options=sorted(df["marketplace"].dropna().unique()),
    default=sorted(df["marketplace"].dropna().unique())
)

filtered_df = df[
    df["product_type"].isin(product_types)
    & df["brand"].isin(brands)
    & df["marketplace"].isin(marketplaces)
]

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Listings", len(filtered_df))

if not filtered_df.empty:
    col2.metric(
        "Average Price",
        f"₹{filtered_df['price'].mean():,.0f}"
    )
    col3.metric(
        "Lowest Price",
        f"₹{filtered_df['price'].min():,.0f}"
    )
else:
    col2.metric("Average Price", "—")
    col3.metric("Lowest Price", "—")

st.divider()

# Product table
st.subheader("Product Listings")
st.dataframe(filtered_df, use_container_width=True)

# Price chart
if not filtered_df.empty:
    st.subheader("Price Comparison by Product")

    chart_data = filtered_df.copy()
    chart_data["Product Label"] = (
        chart_data["product_name"]
        + " ("
        + chart_data["marketplace"]
        + ")"
    )

    chart_data = chart_data.sort_values("price")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        data=chart_data,
        x="price",
        y="Product Label",
        ax=ax
    )
    ax.set_xlabel("Price (₹)")
    ax.set_ylabel("Product")
    ax.set_title("Listed Prices")
    fig.tight_layout()

    st.pyplot(fig)

    st.subheader("Average Price by Brand")
    brand_avg = (
        filtered_df.groupby("brand", as_index=False)["price"]
        .mean()
        .sort_values("price")
    )

    st.bar_chart(brand_avg, x="brand", y="price")

    st.subheader("Marketplace Summary")
    marketplace_avg = (
        filtered_df.groupby("marketplace", as_index=False)["price"]
        .mean()
    )

    st.bar_chart(marketplace_avg, x="marketplace", y="price")
else:
    st.warning("No products match your selected filters.")

st.caption(
    "Prices are based on the dataset provided. "
    "Verify current listings before making purchasing decisions."
)
