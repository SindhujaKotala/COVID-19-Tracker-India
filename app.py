import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from PIL import Image
import plotly.graph_objects as go
import requests
from datetime import date
from datetime import datetime


url1 = 'https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/complete.csv'
url2 = 'https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/nation_level_daily.csv'

#image = Image.open("https://img.etimg.com/thumb/msid-74665367,width-643,imgsize-980841,resizemode-4/from-the-trumpet-shaped-protrusion-at-the-centre-of-a-daffodil-or-narcissus-to-a-part-of-a-cornice-with-a-vertical-face-to-the-most-popular-shape-of-chandeliers-corona-has-long-been-an-acceptable-part-of-society-.jpg")
#st.image(image)
st.header(' COVID-19 Tracker for India ')

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(url1) #, parse_dates=[['Date']])
    data.rename(columns={'Total Confirmed cases (Indian National)':'confirmed_cases_indian'}, inplace=True)
    data.rename(columns={'Total Confirmed cases ( Foreign National )':'confirmed_cases_foreign'}, inplace=True)
    data.rename(columns={'Cured/Discharged/Migrated':'recovered'}, inplace=True)
    data.rename(columns={'Name of State / UT':'name_of_state/ut'}, inplace=True)
    data.rename(columns={'Total Confirmed cases':'total_confirmed_cases'}, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date'] = pd.to_datetime(data['date'])
    return data

@st.cache(persist=True)
def load_cdata():
    cdata = pd.read_csv(url2)
    data.rename(columns={'Date':'date'}, inplace=True)
    cdata.rename(columns={'Daily Deceased':'dailydeceased'}, inplace=True)
    cdata.rename(columns={'Daily Confirmed':'dailyconfirmed'}, inplace=True)
    cdata.rename(columns={'Daily Recovered':'dailyrecovered'}, inplace=True)
    return cdata

data = load_data()
cdata = load_cdata()

dd = data.iloc[-1, data.columns.get_loc("date")]
st.write('Last Updated On ', dd)

if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)

d = st.date_input("Enter Date for date specific Data")

if d <= dd:
###    MAP AND CHART FOR DECEASED    ###

    st.header(" Areas where most people deceased due to COVID-19 in India ")
    data1=(data.query("date == @d")[["death"]].dropna(how='any'))
    f = data1['death'].max()
    deaths = st.slider("Number of Deaths", 0, int(f))
    st.write('As for,', d)
    st.write('areas with greater than %i no.of deaths are:' % deaths)
    data1=(data.query("death >= @deaths and date == @d")[["name_of_state/ut", "death","latitude", "longitude"]].dropna(how='any'))

    st.markdown('##### Hover for info!')
    fig1 = px.scatter_geo(data1, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "death")
    fig1.update_geos(
        lonaxis_range= [ 67.0, 97.6 ],
        lataxis_range= [ 5.5, 36.0 ],
        showcountries=True
    )
    st.write(fig1)

    #domain_pd = pd.to_datetime(['2020-03-10', date.today()], format='%m%d').astype(int) / 10 ** 6
    basic_chart1 = alt.Chart(cdata).mark_bar(size=4).encode(
            alt.X('date', title='Date', timeUnit='monthdate'#, scale=alt.Scale(domain=list(domain_pd))
        ),
        alt.Y('dailydeceased', title='No.of Deaths'),
        tooltip=[ 'dailydeceased']).interactive().properties( width=700, height=300).configure_axis(labelFontSize=7)
    st.altair_chart(basic_chart1)


    ###    MAP AND CHART FOR CONFIRMED_CASES  ###

    st.header("Areas of Positive Cases in India ")
    data2=(data.query("date == @d")[["total_confirmed_cases"]].dropna(how='any'))
    f2 = data2['total_confirmed_cases'].max()
    cases = st.slider("Number of Confirmed cases", 0, int(f2))
    st.write('As for,', d)
    st.write('areas with greater than %i no.of positive cases are:' % cases)
    data2 = ((data.query("total_confirmed_cases >= @cases and date == @d")[["name_of_state/ut", "total_confirmed_cases","latitude", "longitude"]].dropna(how='any')))
    #plot_data = data[data['date'].dt.date ==d]

    fig2 = px.scatter_geo(data2, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "total_confirmed_cases")

    fig2.update_geos(
        lonaxis_range= [ 67.0, 97.6 ],
        lataxis_range= [ 5.5, 36.0 ],
        showcountries=True
    )

    st.write(fig2)

    #domain_pd1 = pd.to_datetime(['2020-01-30', date.today()]).astype(int) / 10 ** 6
    basic_chart2 = alt.Chart(cdata).mark_bar(size=4).encode(
        alt.X('date', timeUnit='monthdate', title='Date'#, scale=alt.Scale(domain=list(domain_pd))
        ),
        alt.Y('dailyconfirmed', title='No.of Positive/Confirmed cases'),
        tooltip=[ 'dailyconfirmed']).interactive().properties( width=700, height=300).configure_axis(labelFontSize=7)
    st.altair_chart(basic_chart2)


    ###    MAP AND CHART FOR RECOVERED  ###

    st.header("Areas of Recovery in India")
    data3=(data.query("date == @d")[["recovered"]].dropna(how='any'))
    f3 = data3['recovered'].max()
    rcases = st.slider("Number of Recovered cases", 0, int(f3))
    st.write('As for,', d)
    st.write('areas with greather than %i no.of recovered cases are:' % cases)
    data3 = (data.query("recovered >= @rcases and date == @d")[["name_of_state/ut", "recovered","latitude", "longitude"]].dropna(how='any'))

    fig3 = px.scatter_geo(data3, lat="latitude", lon="longitude", hover_name="name_of_state/ut", size = "recovered")

    fig3.update_geos(
        lonaxis_range= [ 67.0, 97.6 ],
        lataxis_range= [ 5.5, 36.0 ],
        showcountries=True
    )

    st.write(fig3)


    #domain_pd2 = pd.to_datetime(['2020-03-01', date.today()]).astype(int) / 10 ** 6
    basic_chart3 = alt.Chart(cdata).mark_bar(size=4).encode(
        alt.X('date', timeUnit='monthdate', title='Date',#, scale=alt.Scale(domain=list(domain_pd))
        ),
        alt.Y('dailyrecovered', title='No.of Recovered cases'),
        tooltip=[ 'dailyrecovered']).interactive().properties( width=700, height=300).configure_axis(labelFontSize=7)

    st.altair_chart(basic_chart3)


    ###    MOST AFFECTED    ###
    dd = data.iloc[-1, data.columns.get_loc("date")]

    st.header(" States most affected by COVID-19")
    select = st.selectbox('With Respect To:', ['Total Deaths', 'Confirmed Cases', 'Recovered Cases'])

    if select == 'Total Deaths':
        st.write(data.query("date == @dd and death >= 1")[['name_of_state/ut', 'death']].sort_values(by = ['death'], ascending = False).dropna(how='any')[:5])
    elif select == 'Confirmed Cases':
        st.write(data.query("date == @dd and total_confirmed_cases >= 1")[['name_of_state/ut', 'total_confirmed_cases']].sort_values(by = ['total_confirmed_cases'], ascending = False).dropna(how='any')[:5])
    elif select == 'Recovered Cases':
        st.write(data.query("date == @dd and recovered >= 1")[['name_of_state/ut', 'recovered']].sort_values(by = ['recovered'], ascending = False).dropna(how='any')[:5])

else:
    st.write(" Data is updated till ", dd, " Please choose a date on or before it.")
