####################################################################################
######################## Citi Bike Strategy Dashboard ##############################
####################################################################################
##################### by Andrew Miller for CareerFoundry ###########################
####################################################################################


######################### Importing Libraries######################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_plotly_events import plotly_events
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image


# Force dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


# Configure page
st.set_page_config(layout='wide')


################################ Side bar #########################################

# Define side bar
st.sidebar.title("Select a page:")
page = st.sidebar.selectbox(' ',
  ["1. Introduction",
   "2. Distribution of Stations Throughout NYC",
   "3. Most Popular Stations", 
   "4. Daily Trips and Temperature",
   "5. Daily Distribution: Weekday vs Weekend",
   "6. Imbalance of Arrivals vs Departures",
   "7. Most Popular Routes",
   "8. Recommendations"])


############################## Import data #########################################



df_daily = pd.read_csv('daily_trips_temp.csv', index_col = 0)
start_stations = pd.read_csv('start_stations.csv', index_col = 0)
df_avg_day = pd.read_csv('avg_day.csv', index_col = 0)
station_counts_to_graph = pd.read_csv('station_imbalance_to_graph.csv', index_col = 0)

####################################################################################
############################### 1. Introduction ####################################
####################################################################################


if page == "1. Introduction":
    st.markdown("# Citi Bike Strategy Dashboard")
    st.markdown("### Analysis by Andrew Miller for CareerFoundry")
    
    st.markdown("Citi Bike in New York City is a bicycle rental operation that sees huge ridership with almost 30 million trips taken in the year 2022 alone. Being one of the largest bike share systems in the world, there are distribution challenges that must be overcome to ensure that bikes are available where they are needed and that there are available docks for returns. The dashboard aims will examine how Citi Bikes are used and diagnose where rental bike distribution issues arise. Recommendations will then be made for Citi Bike management on possible solutions to alleviate these problems.")

    text_column, image_column = st.columns([2, 1]) # Create a two column layout

    with text_column:
        st.markdown("To uncover insights surrounding the usage of Citi Bikes, the analysis will focus on the following aspects:")
        st.markdown(" - Distribution of stations throughout NYC")
        st.markdown(" - Most popular stations")
        st.markdown(" - Daily Trips and Temperature")
        st.markdown(" - Daily distribution - weekday vs weekend")
        st.markdown(" - Imbalance of arrivals vs departures")
        st.markdown(" - Most popular cycle routes")
        

        st.markdown("Use the dropdown menu on the left to navigate to the required page.")

    with image_column:
        myImage = Image.open("girl-renting-city-bike-from-bike-stand-flipped.jpg")
        st.image(myImage, width=220)




####################################################################################    
############### 2. Distribution of Stations Throughout NYC #########################
####################################################################################


elif page == "2. Distribution of Stations Throughout NYC":
    
    st.markdown("## Distribution of stations throughout NYC")
    st.markdown("We start off by looking at how the stations are distributed throughout New York City across Manhattan as well as the outer boroughs.")
    st.markdown("The map has been rotated in order to see the full the distribution across the screen.  Each dot represents one of over 1700 Citi Bike stations in New York City with the color of each dot determined by the number of departures made from that station. Orange colours signify more departures from the station and the blue colours, fewer departures. Click on the legend to see details of the colour scale or manipulate the map using the controls.")

    path_to_html = "start_stations_v3.html"

    # Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    st.components.v1.html(html_data, height =450)

    st.markdown("The densist cluster of yellow/orange stations shows that Manhattan is extremely well-served with stations spread throughout, especially in Midtown and Lower Manhattan.  North of Central Park the usage begins to decrease and coverage starts to thin out through Harlem, Upper Manhatan and Washington Heights.  Over the Harlem river, the Bronx we also see usage but on a smaller scale with coverage coming to an end at Mosholu Parkway.")
    
    st.markdown("We also see good coverage in parts of Brooklyn with a strong presence in western Brooklyn around the Brooklyn Heights, DUMBO (Down Under the Manhattan Bridge Overpass) and Williamsburg areas.  In Queens, the coverage more limited, concentrated mainly around Astoria.")
    
    st.markdown("Throughout New York, we see that stations follow the urban core and waterfront areas with a clear drop-off as we move away from Manhattan.  The system is commuter-focused around transit hubs and dense employment centres such as Midtown Manhattan around Times Square, the Financial District in Lower Manhattan, downtown Brooklyn and well as the Hudson Yards on the west of Manhattan.") 
    
    st.markdown("Overall we see that the system is centred on Manhattan with a strong presence in Brooklyn but that it could benefit from expansion into public transport-accessible residential areas in the outer boroughs.")

    st.markdown("##### **Some possible areas for expansion:**")
    st.markdown("Expand further in central Brooklyn neighborhoods such as Bed-Stuy, Crown Heights and Prospect Heights")
    st.markdown("Extend the network deeper into Queens increasing density around Long Island City and add stations in Jackson Heights and areas near the subway lines.")
    st.markdown("Consider expansion into under-served residential areas by placing stations around neighborhoods and near subway or bus terminals to assist commuters with the beginning and end of their journeys.")
        

        



####################################################################################
############################## 3. Most Popular Stations ############################
####################################################################################


elif page == "3. Most Popular Stations":

    st.markdown("## Most popular stations")

    st.markdown("With over 1700 stations distributed throughout the city and possibilities for future expansion, we now turn our attention to the busiest of these stations.  The figure below shows the top 20 most-used stations in New York City and their locations. Hover over the chart or graph for specific departure counts.")


##### Map and bar chart together using subplots

    top20_stations = start_stations.head(20)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'bar'}, {'type': 'scattermapbox'}]],
        column_widths=[0.5, 0.5],
        subplot_titles=('Top 20 Most-Used Citi Bike Stations in New York City', 'Station Locations'),
        horizontal_spacing=0.1
    )
    fig.update_annotations(yshift=10)    


    ## Bar chart
    fig.add_trace(
        go.Bar(x = top20_stations['station_name'],
               y = start_stations['total_departures'],
               marker=dict(
                   color=top20_stations['total_departures'],
                   colorscale=['#2c7bb6', '#fdae61']),
                hovertemplate='<b>%{x}</b><br>Departures: %{y}<extra></extra>'),
        row=1, col=1)



     # Add map with station markers
    fig.add_trace(
        go.Scattermapbox(
            lat=top20_stations['latitude'],
            lon=top20_stations['longitude'],
            mode='markers+text',
            marker=dict(
                size=10,
                color=top20_stations['total_departures'],
                colorscale=['#2c7bb6', '#fdae61'],
                showscale=False,
            ),
            text=top20_stations['station_name'],
            textposition='middle right',
            textfont=dict(size=9, color='white'),
            hovertemplate='<b>%{text}</b><br>Departures: %{marker.color}<extra></extra>',
            name=''
        ),
        row=1, col=2)



    fig.update_layout(
        #title = 'Top 20 most-used Citi Bike stations in New York',
        xaxis_title = 'Start Stations',
        yaxis_title = 'Number of Trips',
        plot_bgcolor='#2b2b2b',   # inside axes
        paper_bgcolor='#2b2b2b',  # outside axes
        font=dict(color='white'),
        margin = dict(b=120),
        width = 900, height = 600)



    fig.update_xaxes(
        title_text='Station',
        showgrid = True,
        gridcolor='#444',
        row=1, col=1)
            

    fig.update_yaxes(
        title_text='Number of Departures',
        showgrid = True,
        gridcolor='#444',
        row=1, col=1)
            

    fig.update_mapboxes(
        style='carto-darkmatter',  
        center=dict(
            lat=top20_stations['latitude'].mean(),
            lon=top20_stations['longitude'].mean()
        ),
        zoom=11,
        row=1, col=2
    )


    fig.update_layout(
        height=600,
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=100, b=150)
    )
          
    st.plotly_chart(fig, use_container_width = True)

    st.markdown("Perhaps unsurprisingly given the distribution of stations on the previous page, the top 20 most-used stations all lie in Manhattan with clusters in Midtown and Lower Manhattan.  These are the core business and commercial districts with of these stations lying on or near major north-south avenues for commuter routes. The most popular station for starting journeys with over 128,000 departures is at W 21st & 6th Ave near the Chelsea/Flatiron district.  This area is a major transit hub and destination sitting near offices, residential areas and attractions, acting as a gateway to and from the Flatiron district, Madison Square Park, Union Square and numerous tech and office buildings.")

    st.markdown("Located in the Lower Manhattan, the station at West St & Chambers St was the next most-used with 123,000 departures. Providing access to the financial district and Tribeca, this station serves daily commuters heading to/from work in Manhattan as well as being great for visitors wanting to visit downtown's waterfront areas and attractions.  This is a busy and mixed use area making the station a crucial node for both residents and visitors using Citi Bike.")

    st.markdown("The station at Broadway & W 58th Street is adjacent to Central Park, a major attraction for both tourists and local residents for recreational bike rides.  With 114,000 departures,  this station also serves the nearby theatre district and with the surrounding neighborhood consisting of residential buildings, hotels and office spaces, there is a constant flow of people in the area day and night.")

    st.markdown("There is some consistency in the usage of the rest of the top 20 with these stations scattered throughout Manhattan with a clear drop-off after the top 3 stations.  The top station has 40% more departures than the 20th station showing concentrated demand.  A possible implication of this could be that heavy reliance on a few key stations creates the potential for overcrowding.")
    

 

####################################################################################
######################### 4. Daily Trips and Temperature  ##########################
####################################################################################

elif page == "4. Daily Trips and Temperature":


    st.markdown("## Daily Trips and Temperature")

    st.markdown("Looking at the general usage of Citi Bike in New York throughout the year, we can see on the graph below how the daily number of trips (in orange) varied in 2022. Using a second y-axis we can also see the average daily temperature (in blue). Hover over the graph for details or use the controls to zoom in on specific sections.") 

    # Dual axis plot of trips and temperature.
    
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
        go.Scatter(
            x = df_daily['date'], 
            y = df_daily['no_of_trips'], 
            name = 'Daily bike rides',
            line=dict(color='#fdae61')
        ),
        secondary_y=False
    )

    fig_2.add_trace(
        go.Scatter(
            x = df_daily['date'],
            y = df_daily['avgTemp'], 
            name = 'Daily temperature', 
            line=dict(color='#2c7bb6')
        ),
        secondary_y=True 
    )

    fig_2.update_layout(
        title = 'Average Temperature and Number of Rides per Day',
        plot_bgcolor="#2b2b2b",   # inside axes
        paper_bgcolor="#2b2b2b",  # outside axes
        font=dict(color="white"),
        margin = dict(b=100), 
        height = 500,
        showlegend=True)

    # x-axis
    fig_2.update_xaxes(
        title_text = 'Date',
        showgrid = True,
        gridcolor="#444",
        zerolinecolor="#444")

    # Left y-axis (no of trips)
    fig_2.update_yaxes(
        title_text = 'No of trips',
        title_font=dict(color='#fdae61'),
        tickfont=dict(color='#fdae61'),
        showgrid = False,
        gridcolor="#444",
        zerolinecolor="#444",
        secondary_y = False)

    # Right y-axis (Temperature)
    fig_2.update_yaxes(
        title_text = 'Average Daily Temperature °C',
        title_font=dict(color='#2c7bb6'),
        tickfont=dict(color='#2c7bb6'),
        showgrid = True,
        gridcolor="#444",
        zerolinecolor="#444",
        secondary_y = True)

    st.plotly_chart(fig_2, use_container_width=True)

    st.markdown("We can see the ridership is clearly higher during the summer months compared to the winter and temperature does appear to be a factor with a general trend showing more rides when the temperature is warmer.  We must be careful not to infer too much though from this graph as the differently scaled axes can make a correlation look stronger than it actually is.  Even within warm months we see high variability with significant day-to-day fluctuations with spikes from the two graphs not always aligning.  This suggests that other aspects such as rain, holidays or events may also play a role in the usage of Citi Bikes. Additionally, we would expect there to be differences between weekday and weekend use, which we investigate next!")



####################################################################################
################## 5. Daily Distribution - Weekday vs Weekend ######################
####################################################################################

# blue: '#2c7bb6', orange: '#fdae61'

elif page == "5. Daily Distribution: Weekday vs Weekend":

    st.markdown("## Daily Distribution: Weekday vs Weekend")
    
    st.markdown("If we look at the average number of trips per hour on weekdays and at weekends throughout the year, we see two distict usage distributions.")


    # Two subplots showing average Weekday and Weekend use by aggregated by hour.
    
    # Define colours
    colors = {
        'Weekday': '#2c7bb6',
        'Weekend': '#fdae61'
    }
    
    # Create subplots
    fig_3 = make_subplots(
        cols=2,
        shared_xaxes=True,
        shared_yaxes=True,
        subplot_titles=['Weekday', 'Weekend']
    )
    
    # Add bars for each day type
    for i, day_type in enumerate(['Weekday', 'Weekend'], start=1):
        df_subset = df_avg_day[df_avg_day['day_type'] == day_type]
    
        fig_3.add_trace(
            go.Bar(
                x=df_subset['start_hour'],
                y=df_subset['trip_count'],
                name=day_type,
                marker=dict(
                    color=colors[day_type],
                    line=dict(color='black', width=0.5)),
                showlegend=False),
            row=1,
            col=i)
    
    # Customise layout
    fig_3.update_layout(
        title='Average Number of Trips by Hour: Weekday vs Weekend',
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font=dict(color='white'),
        height=350,
        margin=dict(t=100))
    
    # Axis formatting
    fig_3.update_xaxes(
        title_text='Hour of Day',
        tickmode='array',
        tickvals=list(range(0, 24, 2)),
        range=[-0.5, 23.5],
        gridcolor='#444')
    
    fig_3.update_yaxes(
        title_text='Average Number of Trips',
        gridcolor='#444')
     
    st.plotly_chart(fig_3, use_container_width=True)

    st.markdown("Looking first at the weekday distribution we see the classic rush hour pattern with clear usage spikes at 8am with around 6000 rides and between 5-7pm with 8000 rides per hour.  Clearly commuter-driven, these are people using Citi Bike to get to and from work. Outside of these peak times, the demand grows throughout the day from 10am to 4pm and then drops off throughout the evening and night. ")

    st.markdown("At the weekend we do not see the rush hour spikes but a instead there is a steady growth from around 5am rising to over 6000 rides per hour between 2pm and 5pm. The rate of usage then drops off in the evening but usage remains higher longer into the evening than on weekdays.  The demand is very much recreation-driven, these are people out enjoying their day.")

    st.markdown("These demand distributions can be used to inform bike redistribution strategies.  Stations near offices or transit hubs need more capacity during weekday rush hours while weekend capacity should focus on popular recreational areas during the afternoon.  Bike redistribution needs different strategies for weekdays compared to weekends. In the next section, we will look at the redistribution of bikes to the most imbalanced stations.")




####################################################################################
############### 6. Imbalance of Arrivals vs Departures #############################
####################################################################################

elif page == "6. Imbalance of Arrivals vs Departures":

    st.markdown("## Imbalance of Arrivals vs Departures")
    st.markdown("In order for bikes to be available for customers and for there to be empty docks in which to return bikes, it will be necessary to redistribute bikes manually.  The figure below shows the 20 most unbalanced stations in the network.")

    st.markdown("The metric used here is 'Number of Arrivals' - 'Number of Departures' so a positive result (shown in orange) indicates stations likely to have problems with docks being unavailable, meaning that bikes must be removed in order to accept returning bikes. Conversely, a negative result (shown in blue) means that the station is likely to experience a shortage of bikes. This requires bikes to be transferred to these stations to keep up with demand.")
    
    # blue: '#2c7bb6', orange: '#fdae61'
    
    # Bar chart showing imbalaces with map showing locations

    # Create subplots with bar chart and map side by side
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "bar"}, {"type": "scattermapbox"}]],
        column_widths=[0.5, 0.5],
        subplot_titles=("Station Arrival/Departure Difference", "Station Locations"),
        horizontal_spacing=0.1
    )
    
    fig.update_annotations(yshift=20)
    
    # Add bar chart
    fig.add_trace(
        go.Bar(
            y=station_counts_to_graph.index,
            x=station_counts_to_graph['difference'],
            orientation='h',
            marker=dict(
                color=station_counts_to_graph['difference'],
                colorscale=['#2c7bb6','white','#fdae61'],
                cmid=0,
            ),
            text=station_counts_to_graph['difference'],
            textposition='outside',
            textfont=dict(size=12),
            name='',
            hovertemplate='<b>%{y}</b><br>Difference: %{x}<extra></extra>'
        ),
        row=1, col=1
        
    )
 
    # Add map with station markers
    fig.add_trace(
        go.Scattermapbox(
            lat=station_counts_to_graph['latitude'],
            lon=station_counts_to_graph['longitude'],
            mode='markers+text',
            marker=dict(
                size=12,
                color=station_counts_to_graph['difference'],
                colorscale=['#2c7bb6','white','#fdae61'],
                cmid=0,
                showscale=False,
            ),
            text=station_counts_to_graph.index,
            textposition='top right',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{text}</b><br>Difference: %{marker.color}<extra></extra>',
            name=''
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_xaxes(
        title=dict(
            text="Difference (Arrivals - Departures)"),
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='white',
        row=1, col=1,
        range=[-8000,6000],
        tickmode="array",
        tickvals=list(range(-5000, 6000, 2500)),
        showgrid=True,
        gridcolor="#444"
    
    )
    
    fig.update_yaxes(
        autorange='reversed',
        row=1, col=1,
        title_standoff=20,
        gridcolor="#444"
    )
    
    # Configure the map
    fig.update_mapboxes(
        style="carto-darkmatter",  
        center=dict(
            lat=40.729518,
            lon= -73.975746
        ),
        zoom=11,
        row=1, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        hovermode='closest',
        plot_bgcolor="#2b2b2b",   # inside axes
        paper_bgcolor="#2b2b2b",  # outside axes
        font=dict(color="white"),
        margin=dict(l=40, r=40, t=70, b=100)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("")
    
    st.markdown("By combining the bar chart and map, we see that northern stations have more bikes leaving than arriving while southern stations have more bikes arriving than leaving. This pattern is consistent with commuter travel and indicates a stong need for manual bike distribution. Looking at the top 10 stations at each extreme, it is clear that considerable rebalancing is essential.  The magnitude of these differences suggests that a significant truck or van operation is needed to redistribute bikes.")
    
    st. markdown("Further temporal analysis into the imbalances at these stations would be required to work out efficient schedules for redistribution of bikes.  A possible idea to encourage users to return the bikes to net departure stations would be to offer dynamic pricing or incentives for these trips.")

    st.markdown("We have seen that many journeys do not begin and end at the same station, so where do people go?  This will be the next aspect of the analysis.")

####################################################################################    
########################## 7. Most Popular Routes ##################################
####################################################################################


elif page == "7. Most Popular Routes":

    st.markdown("## Most Popular Routes")
    st.markdown("Where are people actually going on Citi Bikes? Some of the most popular routes are round trips starting and ending at the same station, others are one way trips throughout the city.  The map below shows routes that were taken more than 3500 times in 2022. The orange end of the arcs represent the departure and the blue ends represent the arrival of the trip. A round trip is shown as just a point on the map.")


    
    path_to_html = "Most popular trips_v3.html"

    # Read file and keep in variable 
    with open(path_to_html, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    
    st.components.v1.html(html_data, height =500)

    st.markdown("Immediately we can see how busy it is at the southern end of Central Park. In fact, the top 2 trips are round trips starting from Central Park South & 6th Ave (12041 rides) and 7th Ave & Central Park South (8541 rides). This suggests that the most popular use of CitiBiki may be to ride around Central Park. Other trips starting and ending at stations around the edges of the park are also very popular routes. The route from the south of the park to the north is also popular. This makes sense as riding in Central Park is definitely one of the more relaxing ways to ride a bike in New York City!")

    st.markdown("There are also several popular leisure routes on Roosevelt Island near the Tramway, a cable car joining the Island to Manhattan's Upper East Side.")

    st.markdown("On the west of Manhattan we see frequently-traveled routes following 10th Ave and 12th Ave along the Hudson River.  These routes travel along the scenic Hudson River Greenway which is said to offer stunning views of the Hudson River all the way from Battery Park in the south to the Upper West Side.  There are dedicated cycle paths here which is consistent with the number of trips we see on the map.")

    st.markdown("W 21st street has many popular routes due to dedicated crosstown bike lanes here that connect to major north-south routes such as the Hudson River Greenway.  This area in the Flatiron neighborhood is said to be a good starting point for various urban and scenic rides.")
                



####################################################################################    
########################### 8. Recommendations #####################################
####################################################################################

    
else:
    
    st.markdown("## Recommendations")
    st.markdown("Having examined various aspects of the usage and distribution of the Citi Bike network, the following recommendations can be made:")
    
    
    text_column, image_column = st.columns([2, 1]) # Two column layout

    with text_column:
        st.markdown("#### **Expansion of Network**")
        st.markdown("Expand service into the under-served areas of the outer boroughs such as central Brooklyn and deeper into Queens.")
        st.markdown("Focus expansion near subway and bus terminals to assist in the first and last mile of commuters' journeys." )
        st.markdown("Prioritise residential neighbourhoods with good public transport access to capture more demand from commuters.  ")

        st.markdown("#### **Optimisation of Bike Redistribution**")
        st.markdown("Implement different rebalancing schedules for weekdays vs weekends based on the usage patterns identified.")
        st.markdown("During the week, have focused rebalancing operations both in the afternoon ahead of the 5pm peak, and in the evening ready for the following day's morning rush hour.")
        st.markdown("On weekends, morning rebalancing would reset the stations before the afternoon surge.")
        st.markdown("Consider seasonal variations and plan for reduced winter operations but increase capacity during the peak summer months.  ")


        st.markdown("#### **Dynamic Pricing and Incentives**")
        st.markdown("Introduce pricing incentives or discounts for rides ending at known deficit stations to encourage trips that help to naturally rebalance the system.")
        st.markdown("It follows that surge pricing at times or high demand could be introduced to manage capacity and encourage off-peak use, however pricing strategies like this may prove to be very unpopular.  ")


        st.markdown("#### **Capacity Management**")
        st.markdown("Increase number of bikes and docks at high deficit stations to handle peak time surges.")
        st.markdown("Increase number of docks at high surplus stations to ensure that customers can return bikes.")
        st.markdown("Ensure that the top 20 stations have adequate capacity to meet demand since considerable revenue is generated by these stations.  ")

        
        st.markdown("#### **Recreational Routes**")
        st.markdown("Maintain and promote popular recreational routes such as the Hudson River Greenway, Central Park loops and Roosevelt Island.")
        st.markdown("Consider adding more stations along these scenic routes.")
        st.markdown("Invest in marketing of weekend leisure routes since these have proved themselves to be very popular and a significant source of revenue for Citi Bike.  ")
            

        st.markdown("#### **Areas for Future Analysis**")
        st.markdown("Conduct further temporal analysis of station imbalances with the goal of creating efficient redistribution schedules.")
        st.markdown("Investigate the relationship between rain and ridership, not just temperature, for better operational planning")
        st.markdown("Analyse weekday vs weekend usage patterns for individual stations to further optimize capacity at a more local level.")

        st.markdown("If you have further questions, please feel to contact me at andrewalexander.data@gmail.com")
            

    with image_column:
        myImage = Image.open("bicycle-row-with-blurred-background.jpg")
        st.image(myImage, width=220)
        myImage_2 = Image.open("mechanic-repairing-bicycle.jpg")
        st.image(myImage_2, width=220)
        myImage_3 = Image.open("row-parked-vintage-bicycles-bikes-rent-sidewalk.jpg")
        st.image(myImage_3, width=220)
        myImage_4 = Image.open("close-up-bicycle-gear.jpg")
        st.image(myImage_4, width=220)



