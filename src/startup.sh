#!/bin/bash

# Start the first process
streamlit run app.py --server.address 0.0.0.0 &

uvicorn server:app --host 0.0.0.0