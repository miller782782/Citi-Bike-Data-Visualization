# Importing libraries

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

# Configure page
st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout='wide')

# Add title
st.title("CitiBike Strategy Dashboard")

# Add markdown text
st.markdown("The dashboard aims to diagnose where rental bike distribution issues arise and to advise CitiBike management on possible solutions to alleviate these problems.")


st.markdown("Checking for automatic update.")

####################### Import data #########################################

df_daily = pd.read_csv('daily_trips_temp.csv', index_col = 0)
top20 = pd.read_csv('top20_start_stations.csv', index_col = 0)


############################## DEFINE THE CHARTS ############################

## Bar chart
fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Reds'}))

fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title = 'Sum of trips',
    plot_bgcolor="#2b2b2b",   # inside axes
    paper_bgcolor="#2b2b2b",  # outside axes
    font=dict(color="white"),
    margin = dict(b=120),
    width = 900, height = 600)

fig.update_xaxes(
    showgrid = True,
    gridcolor="#444",
    zerolinecolor="#444")

fig.update_yaxes(
    showgrid = True,
    gridcolor="#444",
    zerolinecolor="#444")

st.plotly_chart(fig, use_container_width = True)

## Dual-axis line graph


fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = df_daily['date'], 
           y = df_daily['no_of_trips'], 
           name = 'Daily bike rides',
           line=dict(color='palevioletred')),
    secondary_y = False, 
)

fig_2.add_trace(
go.Scatter(x=df_daily['date'], 
           y = df_daily['avgTemp'], 
           name = 'Daily temperature', 
           line=dict(color='orange')),
    secondary_y=True, 
)

# Now customize the graph to fit the chosen theme

fig.update_layout(
    title = 'Average Temperature and Number of Rides per Day',
    plot_bgcolor="#2b2b2b",   # inside axes
    paper_bgcolor="#2b2b2b",  # outside axes
    font=dict(color="white"),
    margin = dict(b=120), 
    height = 800,
    showlegend=False)

# x-axis
fig_2.update_xaxes(
    title_text = 'Date',
    showgrid = True,
    gridcolor="#444",
    zerolinecolor="#444")

# Left y-axis (no of trips)
fig_2.update_yaxes(
    title_text = 'No of trips',
    title_font=dict(color='palevioletred'),
    tickfont=dict(color='palevioletred'),
    showgrid = False,
    gridcolor="#444",
    zerolinecolor="#444",
    secondary_y = False)

# Right y-axis (Temperature)
fig_2.update_yaxes(
    title_text = 'Average Daily Temperature °C',
    title_font=dict(color='orange'),
    tickfont=dict(color='orange'),
    showgrid = True,
    gridcolor="#444",
    zerolinecolor="#444",
    secondary_y = True)

st.plotly_chart(fig_2, use_container_width=True)


## Add the KeplerGl map


path_to_html = "NY Bike Trips Aggregated_v2.html"

# Read file and keep in variable 
with open(path_to_html, 'r') as f:
    html_data = f.read()

## Show in web page 
st.header("Most popular bike trips in New York")
st.components.v1.html(html_data, height =1000)