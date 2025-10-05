import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="GalamseyWatch",
    page_icon="🛰️",
    layout="wide"
)

# Header
st.title("🛰️ GalamseyWatch")
st.markdown("**Satellite-based Detection of Illegal Mining in Ghana**")

# Sidebar
st.sidebar.header("Controls")
region = st.sidebar.selectbox(
    "Select Region",
    ["Western Region", "Ashanti Region", "Eastern Region", "All Regions"]
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=90), datetime.now()),
    max_value=datetime.now()
)

# Mock data for demonstration
@st.cache_data
def load_mock_data():
    # Ghana mining regions coordinates
    locations = [
        {"name": "Obuasi", "lat": 6.2027, "lon": -1.6640, "severity": 0.8, "region": "Ashanti"},
        {"name": "Tarkwa", "lat": 5.3006, "lon": -1.9959, "severity": 0.9, "region": "Western"},
        {"name": "Dunkwa", "lat": 5.9667, "lon": -1.7833, "severity": 0.7, "region": "Central"},
        {"name": "Prestea", "lat": 5.4333, "lon": -2.1333, "severity": 0.6, "region": "Western"},
    ]
    
    data = []
    for loc in locations:
        for i in range(30):
            date = datetime.now() - timedelta(days=i*3)
            data.append({
                "location": loc["name"],
                "lat": loc["lat"] + np.random.normal(0, 0.01),
                "lon": loc["lon"] + np.random.normal(0, 0.01),
                "severity": max(0, loc["severity"] + np.random.normal(0, 0.1)),
                "region": loc["region"],
                "date": date,
                "ndvi_change": np.random.uniform(-0.3, -0.1),
                "bsi_change": np.random.uniform(0.1, 0.4)
            })
    
    return pd.DataFrame(data)

df = load_mock_data()

# Main dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Galamsey Hotspots Map")
    
    # Create map centered on Ghana
    m = folium.Map(location=[7.9465, -1.0232], zoom_start=7)
    
    # Add markers for detected mining activities
    for _, row in df.iterrows():
        if row['severity'] > 0.5:
            color = 'red' if row['severity'] > 0.7 else 'orange'
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=row['severity'] * 10,
                popup=f"{row['location']}<br>Severity: {row['severity']:.2f}",
                color=color,
                fillColor=color,
                fillOpacity=0.6
            ).add_to(m)
    
    # Display map
    map_data = st_folium(m, width=700, height=500)

with col2:
    st.subheader("📊 Detection Summary")
    
    # Key metrics
    total_hotspots = len(df[df['severity'] > 0.5])
    high_severity = len(df[df['severity'] > 0.7])
    avg_severity = df['severity'].mean()
    
    st.metric("Total Hotspots", total_hotspots)
    st.metric("High Severity Sites", high_severity)
    st.metric("Average Severity", f"{avg_severity:.2f}")
    
    # Severity distribution
    fig_severity = px.histogram(
        df, x='severity', bins=20,
        title="Severity Distribution",
        labels={'severity': 'Severity Score', 'count': 'Frequency'}
    )
    st.plotly_chart(fig_severity, use_container_width=True)

# Time series analysis
st.subheader("📈 Environmental Impact Trends")

col3, col4 = st.columns(2)

with col3:
    # NDVI change over time
    daily_ndvi = df.groupby('date')['ndvi_change'].mean().reset_index()
    fig_ndvi = px.line(
        daily_ndvi, x='date', y='ndvi_change',
        title="Vegetation Loss (NDVI Change)",
        labels={'ndvi_change': 'NDVI Change', 'date': 'Date'}
    )
    st.plotly_chart(fig_ndvi, use_container_width=True)

with col4:
    # BSI change over time
    daily_bsi = df.groupby('date')['bsi_change'].mean().reset_index()
    fig_bsi = px.line(
        daily_bsi, x='date', y='bsi_change',
        title="Soil Exposure (BSI Change)",
        labels={'bsi_change': 'BSI Change', 'date': 'Date'}
    )
    st.plotly_chart(fig_bsi, use_container_width=True)

# Regional analysis
st.subheader("🏞️ Regional Impact Analysis")

regional_stats = df.groupby('region').agg({
    'severity': ['mean', 'count'],
    'ndvi_change': 'mean',
    'bsi_change': 'mean'
}).round(3)

regional_stats.columns = ['Avg Severity', 'Hotspot Count', 'Avg NDVI Change', 'Avg BSI Change']
st.dataframe(regional_stats, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Sources:** NASA Landsat 8/9, MODIS Terra/Aqua | **Powered by:** Google Earth Engine")
st.markdown("*This is a demonstration using simulated data for NASA Space Apps Challenge 2024*")