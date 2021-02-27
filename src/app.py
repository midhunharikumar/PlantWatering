import requests
import json
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


def get_data():
    url = "http://10.0.0.102:8000/showdata/"

    headers = {"accept: application/json"}

    response = requests.get(url,headers=headers)
    return response.text()


st.write(get_data())
