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


def get_data():
    url = f"http://{MONGO_ADDRESS}/showdata/"
    headers = {"accept": "application/json"}
    response = requests.get(url,headers=headers)
    return response.json()


if st.sidebar.button('Water now'):
    water_now()

start_date =  st.sidebar.date_input('start_date',datetime.datetime(2020,1,1))
end_date =  st.sidebar.date_input('end_date',datetime.datetime(2020,1,1))

df = pd.DataFrame(get_data())
#df = df.iloc[-1000:]
# df.date = np.arange(df.shape[0])
df.columns = ['sensor_name','sensor_value','date']
df['date'] = pd.to_datetime(df['date'],infer_datetime_format=True)

# st.write(type(start_date))
print(df.iloc[0].date,np.datetime64(start_date))
df = df[df['date'] >= np.datetime64(start_date)]
# df = df.groupby('sensor_name').agg()
df['sensor_value'] = df.sensor_value.apply(lambda x: x)
df['sensor_value'].ewm(span = 3600).mean()
st.write(df)
fig = plt.figure(figsize=(20,10))
ax = fig.add_axes([0.4, 0.4, 0.8, 0.8]) # main axes
df = df.sample(50)
for i in np.unique(df.sensor_name):
    ax.plot(np.arange(df[df.sensor_name==i].shape[0]),df[df.sensor_name==i]['sensor_value'])
ax.legend(np.unique(df.sensor_name))
ax.set_xticks(np.arange(df.shape[0]))
ax.set_xticklabels(df.date,rotation='vertical')
st.pyplot(fig)
