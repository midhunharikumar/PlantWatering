import requests
import json
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import datetime
import matplotlib
import numpy as np
import pendulum
import os
# import pywemo


MONGO_ADDRESS = os.environ['MONGO_ADDRESS']

def water_now():
    url = f"http://{MONGO_ADDRESS}/run_motor/"
    headers = {"accept": "application/json"}

    response = requests.post(url,headers=headers)
    
    return response.json()

@st.cache
def get_data():
    url = f"http://{MONGO_ADDRESS}/showdata/"
    headers = {"accept": "application/json"}
    response = requests.get(url,headers=headers)
    return response.json()


if st.sidebar.button('Water now'):
    water_now()


sampling_rate = st.slider('Sampling rate',0,100,50,10)

start_date =  st.sidebar.date_input('start_date',datetime.datetime.now()-datetime.timedelta(hours=1))
end_date =  st.sidebar.date_input('end_date',datetime.datetime.now())

df = pd.DataFrame(get_data())
#df = df.iloc[-1000:]
# df.date = np.arange(df.shape[0])
df.columns = ['sensor_name','sensor_value','date']

sensor_checkboxes = {}
for i in np.unique(df.sensor_name):
    sensor_checkboxes[i]= st.sidebar.checkbox(i,value=True)

df['date'] = pd.to_datetime(df['date'],infer_datetime_format=True)

selected = [key for key,value in sensor_checkboxes.items() if value]
st.write(selected)

df = df[df['sensor_name'].apply(lambda x: x in selected)]

# st.write(type(start_date))

df = df[df['date'] >= pd.Timestamp(start_date)]
# df = df.groupby('sensor_name').agg()
df['sensor_value'] = df.sensor_value.apply(lambda x: x)
#df['sensor_value'].ewm(span = 3600).mean()
st.write(df)
fig = plt.figure(figsize=(20,10))
ax = fig.add_axes([0.4, 0.4, 0.8, 0.8]) # main axes
df = df.sample(sampling_rate)
for i in np.unique(df.sensor_name):
    ax.plot(np.arange(df[df.sensor_name==i].shape[0]),df[df.sensor_name==i]['sensor_value'])
ax.legend(np.unique(df.sensor_name))
ax.set_xticks(np.arange(df.shape[0]))
ax.set_xticklabels(df.date,rotation='vertical')
st.pyplot(fig)
