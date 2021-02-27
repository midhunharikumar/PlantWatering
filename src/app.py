import requests
import json
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib
import numpy as np
def get_data():
    url = "http://10.0.0.102:8000/showdata/"

    headers = {"accept": "application/json"}

    response = requests.get(url,headers=headers)
    return response.json()


df = pd.DataFrame(get_data())
df.columns = ['sensor_name','sensor_value','date']
plt.plot(df.sensor_value.to_list()[:10])
