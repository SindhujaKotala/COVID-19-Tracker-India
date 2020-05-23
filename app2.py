import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import altair as alt
from PIL import Image
import plotly.graph_objects as go

image = Image.open("C:/Project/corona.png")
st.image(image, width=700)
st.header(' COVID-19 Tracker for India 😷')
DATA_URL = ("C:\Project\complete.csv")

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL) #, parse_dates=[['Date']])
    data.rename(columns={'Total Confirmed cases(Indian National)':'confirmed_cases_indian)', 'Total Confirmed cases( Foreign National )':'confirmed_cases_Foreign'}, inplace=True)
    #3data.rename(columns={'Total Confirmed cases(Indian National)':'Confirmed Cases(Indian)'}, inplace=True)
    data.rename(columns={'cured_discharged_migrated':'recovered'}, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()
domain_pd = pd.to_datetime(['2020-03-10', '2020-05-17']).astype(int) / 10 ** 6
midpoint = (np.average(data['latitude']), np.average(data['longitude']))
domain_pd1 = pd.to_datetime(['2020-01-30', '2020-05-17']).astype(int) / 10 ** 6

df1 = pd.DataFrame
for i in pd.to_datetime(list(domain_pd1)):
    df=(data.query("date == @i")[["death","recovered", "total_confirmed_cases"]].dropna(how='any'))
    df1.append(df)
st.write(df1)

d = st.date_input("Enter Date if you need date specific Data")


st.header(" Areas where most people died due to COVID-19 in India ")
#data1=(data.query("date == @d")[["death"]].dropna(how='any'))
#f = np.argmax(data1['death'].values)
#f = data1.get_value(f)
deaths = st.slider("Number of Deaths", 0, 1135)#f)
st.write('As for,', d)
st.write('areas with greater than %i no.of deaths are:' % deaths)
data1=(data.query("death >= @deaths and date == @d")[["name_of_state/ut", "death","latitude", "longitude"]].dropna(how='any'))
fig1 = px.scatter_geo(data1, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "death")
#fig.update_layout(
#)
fig1.update_geos(
    showcountries=True,
    lonaxis_range= [ 65.0, 92.0 ],
    lataxis_range= [ 5.0, 35.0 ],
)
st.write(fig1)


basic_chart = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', timeUnit='yearmonthdate', title='Date', scale=alt.Scale(domain=list(domain_pd))
    ),
    alt.Y('death', title='No.of Deaths'),
    tooltip=['date', 'death']).interactive().properties( width=600, height=300)
st.altair_chart(basic_chart)

st.header("Areas where most cases were found positive in India ")
cases = st.slider("Number of Confirmed cases", 0, 30706)
st.write('As for,', d)
st.write('areas with greater than %i no.of positive cases are:' % cases)
data2=(data.query("total_confirmed_cases >= @cases and date == @d")[["name_of_state/ut", "total_confirmed_cases","latitude", "longitude"]].dropna(how='any'))

fig2 = px.scatter_geo(data2, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "total_confirmed_cases")
#fig.update_layout(
#)
fig2.update_geos(
    showcountries=True,
    lonaxis_range= [ 65.0, 92.0 ],
    lataxis_range= [ 5.0, 35.0 ],
)
st.write(fig2)

domain_pd1 = pd.to_datetime(['2020-01-30', '2020-05-17']).astype(int) / 10 ** 6
basic_chart1 = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', timeUnit='yearmonthdate', title='Date', scale=alt.Scale(domain=list(domain_pd))
    ),
    alt.Y('total_confirmed_cases', title='No.of Positive/Confirmed cases'),
    tooltip=['date', 'total_confirmed_cases']).interactive().properties( width=600, height=300)

st.altair_chart(basic_chart1)




st.header("Areas of Recovery ")
rcases = st.slider("Number of Recovered cases", 0, 30706)
st.write('As for,', d)
st.write('areas with greather than %i no.of recovered cases are:' % rcases)
data3=(data.query("recovered >= @rcases and date == @d")[["name_of_state/ut", "recovered", "latitude", "longitude"]].dropna(how='any'))

fig3 = px.scatter_geo(data3, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "recovered")
#fig.update_layout(
#)
fig3.update_geos(
    showcountries=True,
    lonaxis_range= [ 65.0, 92.0 ],
    lataxis_range= [ 5.0, 35.0 ],
)
st.write(fig3)

domain_pd2 = pd.to_datetime(['2020-03-01', '2019-05-17']).astype(int) / 10 ** 6
basic_chart2 = alt.Chart(data).mark_bar(size=6).encode(
    alt.X('date', timeUnit='yearmonthdate', title='Date', scale=alt.Scale(domain=list(domain_pd))
    ),
    alt.Y('recovered', title='No.of Recovered cases'),
    tooltip=['date', 'recovered']).interactive().properties( width=600, height=300)

st.altair_chart(basic_chart2)

if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
