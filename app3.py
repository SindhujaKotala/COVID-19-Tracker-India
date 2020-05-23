import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import altair as alt
from PIL import Image


st.header(' COVID-19 Tracker for India ')
DATA_URL = ("C:/Users/admin/Desktop/Coursera/Projects/CovidProject/complete.csv")

image = Image.open("C:/Users/admin/Desktop/Coursera/Projects/CovidProject/corona.png")
st.image(image, width=700)

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL) #, parse_dates=[['Date']])
    #data.rename(columns={'Total Confirmed cases(Indian National)':'Confirmed Cases(Indian)', 'Total Confirmed cases( Foreign National )':'Confirmed Cases(Foreign)'}, inplace=True)
    #3data.rename(columns={'Total Confirmed cases(Indian National)':'Confirmed Cases(Indian)'}, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()

#original_data = data

d = st.date_input("Enter Date if you need date specific Data")

st.header(" Areas where most people died due to COVID-19 in India ")
deaths = st.slider("Number of Deaths", 0, 1135)
st.write('As for,', d)
st.write('areas with greater than %i no.of deaths are:' % deaths)
st.map(data.query("death >= @deaths and date == @d ")[["latitude", "longitude"]].dropna(how='any'))
#original_data = data[data['date']==d]

basic_chart = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', title='Date', #scale=alt.Scale(domain=('Mar 15', 'May 17'))
    ),
    alt.Y('death', title='No.of Deaths'),
    tooltip=['date', 'death']).interactive().properties( width=600, height=300)

st.altair_chart(basic_chart)

#if st.checkbox("Show Raw Data?", False):
#    st.subheader('Raw Data')
#    st.write(original_data)


st.header("Areas where most cases were found positive in India ")
cases = st.slider("Number of Confirmed cases", 0, 30706)
st.write('As for,', d)
st.write('areas with %i no.of corona cases are:' % cases)
st.map(data.query("total_confirmed_cases >= @cases and date == @d")[["latitude", "longitude"]].dropna(how='any'))
#plot_data = data[data['date'].dt.date ==d]

basic_chart1 = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', title='Date', #scale=alt.Scale(domain=('Mar 15', 'May 17'))
    ),
    alt.Y('total_confirmed_cases', title='No.of Positive/Confirmed cases'),
    tooltip=['date', 'total_confirmed_cases']).interactive().properties( width=600, height=300)

st.altair_chart(basic_chart1)

st.header("Areas of Recovery ")
reccases = st.slider("Number of recovered cases", 0, 7088)
st.write('As for,', d)
st.write('areas with %i no.of recovered corona cases are:' % reccases)
st.map(data.query("cured/discharged/migrated >= @reccases and date == @d")[["latitude", "longitude"]].dropna(how='any'))


basic_chart2 = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', title='Date', #scale=alt.Scale(domain=('Mar 15', 'May 17'))
    ),
    alt.Y('cured/discharged/migrated', title='No.of Recovered cases'),
    tooltip=['date', 'cured/discharged/migrated']).interactive().properties( width=600, height=300)

st.altair_chart(basic_chart2)


#'''hist = np.histogram(data['date'].dt.day)[0]
#chart_data = pd.DataFrame({'Date': range(0,10), 'cases': hist})
#fig = px.bar(chart_data, x='Date', y='cases', hover_data=['Date', 'cases'], height=400)
#st.write(fig)'''


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
