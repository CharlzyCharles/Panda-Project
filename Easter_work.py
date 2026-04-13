import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

st.title("Sales Dashboard")

df = pd.read_csv("Pandas Project.csv")

st.markdown("## ABOUT")
st.markdown("### This is a dashboard showing sales of products made by a firm."
            " It contains relevant KPIs and charts ")

# Clean data
df['Amount'] = pd.to_numeric(
    df['Amount'].str.replace(r'[\$,]', '', regex=True),
    errors='coerce'
)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# KPIs
top_salesperson = df.groupby('Sales Person')['Amount'].sum().idxmax()
top_revenue = df.groupby('Sales Person')['Amount'].sum().max()




df['Revenue_per_Box'] = df['Amount'] / df['Boxes Shipped']
avg_rev_box = df['Revenue_per_Box'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Top Salesperson", value=top_salesperson)
col2.metric("Highest Revenue", f"${top_revenue:,.2f}")
col3.metric("Avg Revenue/Box", f"${avg_rev_box:.2f}")

# Product boxes
st.subheader("Boxes per Product")
product_boxes = df.groupby('Product')['Boxes Shipped'].sum()
st.bar_chart(product_boxes)

# Monthly sales
df['Month'] = df['Date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('Month')['Amount'].sum()
st.subheader("Monthly Sales Trend")
st.line_chart(monthly_sales)

# Country revenue
country_rev = df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
st.subheader("Revenue by Country")
st.bar_chart(country_rev)

# Map (basic)

url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
world = gpd.read_file(url)

merged = world.merge(country_rev,
                     how="left",
                     left_on="name",
                     right_on="Country"

)

fig, ax = plt.subplots(figsize=(15,8))
# ax.set_facecolor("skyblue")
fig.patch.set_facecolor("skyblue") # sets the background of the map as royal_blue

# PLOT
merged.plot(
    column="Amount",
    cmap="coolwarm",
    #Color scheme: Orange -> Red-Light = low revenue-Dark = high revenue
    linewidth=0.5,
    #Border thickness of countries
    ax=ax,
    edgecolor="yellow",

    legend=True)

#CUSTOMIZE MAP
#Set ocean color

ax.set_title(label="country_revenue",fontsize=25)
ax.set_axis_off() # To Remove axes

# STREAMLIT SETUP
st.title("Revenue by Country")
st.pyplot(fig)





# Avg revenue per product
st.subheader("Avg Revenue per Product")
avg_product = df.groupby('Product')['Amount'].mean()
st.bar_chart(avg_product)

 # Preview
st.subheader("Dataset Preview")
st.dataframe(df.sample(15))

st.sidebar.header("Filter Dashboard")

# Country filter
country = st.sidebar.multiselect(
    "Select Country",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

# Month filter
month = st.sidebar.multiselect(
    "Select Month",
    options=df['Month'].unique(),
    default=df['Month'].unique()
)

# Product filter
product = st.sidebar.multiselect(
    "Select Product",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)


filtered_df = df[
    (df['Country'].isin(country)) &
    (df['Month'].isin(month)) &
    (df['Product'].isin(product))
]
revenue_country = filtered_df.groupby('Country')['Revenue'].sum()

st.subheader("Revenue by Country")
st.bar_chart(revenue_country)

monthly_revenue = filtered_df.groupby('Month')['Revenue'].sum()

# Optional: sort months correctly
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

monthly_revenue = monthly_revenue.reindex(month_order)

st.subheader("Monthly Revenue Trend")
st.line_chart(monthly_revenue)

revenue_product = filtered_df.groupby('Product')['Revenue'].sum()

st.subheader("Revenue per Product")
st.bar_chart(revenue_product)

st.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")

