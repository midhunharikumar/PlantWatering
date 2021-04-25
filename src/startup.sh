#!/bin/bash

# Start the first process
streamlit run app.py &

uvicorn server:app