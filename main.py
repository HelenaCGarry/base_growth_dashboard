import streamlit as st
import pandas as pd
import os
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px

#page config
st.set_page_config(layout="wide")

#graphs config
palette = ['#aae03e','#bed626', '#d1cb09','#e2c000','#f1b300','#ffa600']
pio.templates["palette"] = go.layout.Template(
    layout = {
        'title':
            {'font': {'color': '#fbfbfb'}
            },
        'font': {'color': '#fbfbfb'},
        'colorway': palette,
    }
)
pio.templates.default = "palette"

#load data
revenue_data = pd.read_csv('data/revenue.csv')
energy_delivery_data = pd.read_csv('data/energy_delivery.csv')
texas_counties_data = pd.read_csv('data/Texas_counties_consumers.csv')

st.markdown("<h6 style='text-align: center'>Helena C. Garry take-home assessment 01/20/2025 </h4>", unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center'>Base Power Company</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center'>Growth Analysis</h2>", unsafe_allow_html=True)


#generate graphs
fig_1 = go.Figure()

# Add Monthly Revenue
fig_1.add_trace(
    go.Scatter(
        x=revenue_data['Month'],
        y=revenue_data['Monthly_Revenue_USD'],
        mode='lines+markers',
        name='Monthly Revenue (USD)',
        line=dict(color='#aae03e', width=2),
        marker=dict(size=6)
    )
)

# Add Revenue Growth Percentage
fig_1.add_trace(
    go.Scatter(
        x=revenue_data['Month'],
        y=revenue_data['Revenue_Growth_%'],
        mode='lines+markers',
        name='Revenue Growth (%)',
        line=dict(color='green', dash='dash', width=2),
        marker=dict(size=6),
        yaxis='y2'  # Assign to second y-axis
    )
)

fig_1.update_layout(
    title='2024 Revenue',
    xaxis_title='',
    yaxis=dict(
        title='Revenue (USD)',
        #titlefont=dict(color='blue'),
        #tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='Revenue Growth (%)',
        #titlefont=dict(color='green'),
        #tickfont=dict(color='green'),
        overlaying='y',  # Overlay second axis on the first
        side='right'
    ),
    legend_title='Metrics',
    #template='plotly_white',
    xaxis=dict(tickangle=-45)
)


fig_1.update_layout(
    title_x=0.5,
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))
fig_1.update_xaxes(type='category')

st.plotly_chart(fig_1, use_container_width=True)    



energy_col , costumer_col = st.columns(2)

with energy_col:
    fig_2 = go.Figure()

    # Add Energy Delivered
    fig_2.add_trace(
        go.Scatter(
            x=energy_delivery_data['Month'],
            y=energy_delivery_data['Energy_Delivered_kWh'],
            mode='lines+markers',
            name='Energy Delivered (kWh)',
            line=dict(color='#ffa600', width=2),
            marker=dict(size=6)
        )
    )
    # Update layout
    fig_2.update_layout(
        title='Energy Delivered Over Time',
        xaxis_title='',
        yaxis_title='Energy Delivered (kWh)',
        legend_title='Metrics',
        xaxis=dict(tickangle=-45),
        yaxis=dict(titlefont=dict(size=12)),
    )
    fig_2.update_xaxes(type='category')
    fig_2.update_layout(width=500, height=500)
    st.plotly_chart(fig_2, use_container_width=True)


    

with costumer_col:

    # Calculate Consumer Growth Percentage
    texas_counties_data['Customer Growth %'] = (
        (texas_counties_data['2024_Consumers'] - texas_counties_data['2023_Consumers']) /
        texas_counties_data['2023_Consumers'] * 100
    )


    custom_colorscale = [
    [0, '#aae03e'], 
    [0.5, '#d9c600'],  
    [1, '#ffa600']  
]
    # Create the choropleth map
    fig_3 = px.choropleth(
        texas_counties_data,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations='FIPS',
        color='Customer Growth %',
        hover_name='County',
        hover_data={'FIPS': False, 'Customer Growth %': ':.2f'},
        title='Customer Growth Percentage by County in Texas (2023-2024)',
        color_continuous_scale=custom_colorscale,
    )

    fig_3.update_layout(coloraxis_colorbar=dict(
    title=dict(text="%")
    ))

    fig_3.update_geos(
        visible=False,
        resolution=50,
        scope="usa",  # Focus on the United States
        #center={"lat": 31.0, "lon": -99.9018},  # Centered on Texas
        projection=dict(
            type="albers usa",  # Albers projection fits well for US
        ),
        projection_scale=6,  # Adjust zoom level to fit better
        fitbounds="locations"  # This automatically fits based on the visible locations
    )
    fig_3.update_layout(height=300,width=300, margin={"r":0,"t":100,"l":0,"b":0})

    st.plotly_chart(fig_3, use_container_width=True)


st.markdown("""

## Key growth metrics overview            
### Revenue Growth

**Why:**  
Captures the financial growth of the company, indicating success in monetizing services.

**Growth Indicator:**  
A consistent increase shows expanding customer base and/or higher revenue per customer.

### Total Energy Delivered to Customers

**Why:**  
Reflects the company's operational scale and ability to meet demand, as well as its ability to power customer homes.

**Growth Indicator:**  
An upward trend indicates expansion of the customer base and the production capacity of Base Power .

### Geographic Expansion

**Why:**  
Tracking which areas of Texas have seen higher customer base growth can help Base Power identify key factors driving customer growth and leverage them in regions where growth has been slower.  
If Base Power is expanding beyond its initial areas of operation, tracking new service regions or market entries is also critical.

**Growth Indicator:**  
Increased number of customer households per county shows growing market presence."""
    )

