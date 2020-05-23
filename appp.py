import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

st.header(' COVID-19 Tracker for India 😷')
DATA_URL = ("C:\Project\complete.csv")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows) #, parse_dates=[['Date']])
    #data.rename(columns={'Total Confirmed cases(Indian National)':'Confirmed Cases(Indian)', 'Total Confirmed cases( Foreign National )':'Confirmed Cases(Foreign)'}, inplace=True)
    #3data.rename(columns={'Total Confirmed cases(Indian National)':'Confirmed Cases(Indian)'}, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data = load_data(2020)
original_data = data

d = st.date_input("Enter Date if need date specific Data")

st.header("Where are the most people located, who died due to COVID-19 in India? ")
deaths = st.slider("Number of Deaths", 0, 1135)
st.write('As for,', d)
st.write('areas with %i no.of deaths are:' % deaths)
st.map(data.query("death >= @deaths and date == @d")[["latitude", "longitude"]])

st.header("Where are the most people located, who died due to COVID-19 in India? ")
deaths = st.slider("Number of Confirmed cases", 0, 1135)
st.write('As for,', d)
st.write('areas with %i no.of deaths are:' % deaths)
st.map(data.query("total_confirmed_cases >= @deaths and date == @d")[["latitude", "longitude"]].dropna(how='any'))

midpoint = (np.average(data['latitude']), np.average(data['longitude']))

'''
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data =data[['Date', 'Latitude', 'Longitude']],
        get_position=['longitude', 'latitude'],
        radius=400,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 1000],
        ),
    ],
))
'''
'''
hist = np.histogram(data['Date'].dt.day)[0]
chart_data = pd.DataFrame({'Date': data['Date'], 'cases': hist})
fig = px.bar(chart_data, x='Date', y='confirmed cases', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

'''






if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
