import streamlit as st
import pandas as pd
import plotly.express as px

# Custom Styles
st.markdown(
    '''
    <style>
    .css-1d391kg { background-color: #1e293b; } /* Dark sidebar */
    .css-18e3th9 { background-color: #f4f7fb; } /* Light main background */
    .stSlider > div > div > div > div { background: linear-gradient(90deg, #4A90E2, #50E3C2); } /* Custom slider color */
    .stSelectbox > div > div > div > div { color: #4A90E2; } /* Custom selectbox color */
    .stMultiSelect > div > div > div > div { color: #99105188; } /* Custom multiselect color */
    .stPlot > div > div { width: 100%; height: 500px; } /* Increased plot size */
    </style>
    ''',
    unsafe_allow_html=True
)

# Color palette for charts
COLOR_PALETTE = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA",
    "#FFA15A", "#19D3F3", "#FF6692", "#B6E880",
    "#FF97FF", "#FECB52"
]

# Series mapping
SERIES_ID_NAME_MAP = {
    "CES0000000001": "Total Nonfarm Employment",
    "CES0500000001": "Total Private Employment",
    "CES2000000001": "Construction Employment",
    "CES3000000001": "Manufacturing Employment",
    "CES4000000001": "Trade, Transportation, and Utilities Employment",
    "CES6000000001": "Professional and Business Services Employment",
    "CES7000000001": "Education and Health Services Employment",
    "CES8000000001": "Leisure and Hospitality Employment",
    "LNS14000000": "Unemployment Rate",
    "LNS11300000": "Labor Force Participation Rate",
    "LNS12300000": "Civilian Employment-Population Ratio",
    "LNS13023621": "Part-Time for Economic Reasons",
    "LNS12032194": "Women Labor Force Participation",
    "LNS12500000": "Median Duration of Unemployment",
    "LNS12600000": "Average Hourly Earnings"
}
NAME_TO_SERIES_ID = {v: k for k, v in SERIES_ID_NAME_MAP.items()}

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/labor_stats.csv")

df = load_data()

# Sidebar
st.sidebar.title("Interactive Filters")
st.sidebar.markdown("Select options to filter the data.")

# Year Range Slider
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (2010, 2023)
)

# Metric Dropdown (sorted alphabetically)
metric_name = st.sidebar.selectbox("Select Metric", sorted(SERIES_ID_NAME_MAP.values()))
metric = NAME_TO_SERIES_ID[metric_name]

# Period Filter
periods = st.sidebar.multiselect(
    "Select Periods (Months)",
    df["period_name"].unique(),
    df["period_name"].unique()
)

# Filter Data
filtered_data = df[
    (df["series_id"] == metric) &
    (df["year"].between(year_range[0], year_range[1])) &
    (df["period_name"].isin(periods))
]

# Main Layout
st.title("Interactive US Labor Statistics Dashboard")
st.markdown("Analyze trends and key metrics with dynamic visualizations.")

# Two-Column Layout
col1, col2 = st.columns(2)

# Column 1: Key Metrics and Filters
with col1:
    st.subheader("Key Insights")
    if not filtered_data.empty:
        avg_value = filtered_data["value"].mean()
        st.metric("Average Value", f"{avg_value:.2f}")
        max_value = filtered_data["value"].max()
        st.metric("Maximum Value", f"{max_value:.2f}")
    else:
        st.warning("No data available for the selected filters.")

# Column 2: Main Chart
with col2:
    st.subheader(f"Trend: {metric_name}")
    if not filtered_data.empty:
        line_chart = px.line(
            filtered_data,
            x="year",
            y="value",
            color="period_name",
            title=f"{metric_name} Over Time",
            labels={"value": metric_name, "year": "Year"},
            color_discrete_sequence=COLOR_PALETTE
        )
        st.plotly_chart(line_chart, use_container_width=True)
    else:
        st.error("No data available to display.")

# Additional Chart Options
st.header("Additional Visualizations")
if not filtered_data.empty:
    chart_type = st.selectbox("Choose Chart Type", ["Bar Chart", "Pie Chart", "Table"])
    if chart_type == "Bar Chart":
        bar_chart = px.bar(
            filtered_data,
            x="year",
            y="value",
            color="period_name",
            barmode="group",
            title=f"{metric_name} (Bar Chart)",
            color_discrete_sequence=COLOR_PALETTE
        )
        st.plotly_chart(bar_chart, use_container_width=True)
    elif chart_type == "Pie Chart":
        pie_chart = px.pie(
            filtered_data,
            values="value",
            names="period_name",
            title=f"{metric_name} Distribution",
            color_discrete_sequence=COLOR_PALETTE
        )
        st.plotly_chart(pie_chart, use_container_width=True)
    elif chart_type == "Table":
        st.write(filtered_data)
else:
    st.error("No data available for additional visualizations.")