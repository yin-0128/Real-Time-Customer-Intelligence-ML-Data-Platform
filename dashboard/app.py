import streamlit as st
import requests

# Point to the internal Docker network name for the API
API_URL = "http://api:8000/predict"

st.title("Customer Churn Prediction Dashboard")
st.markdown("Enter customer metrics to predict churn probability.")

days_active = st.number_input("Days Active", min_value=1, value=100)
total_events = st.number_input("Total Events", min_value=0, value=50)
avg_event_value = st.number_input("Average Event Value", min_value=0.0, value=25.0)

if st.button("Predict Churn"):
    payload = {
        "days_active": days_active,
        "total_events": total_events,
        "avg_event_value": avg_event_value
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            churn_pred = "Yes" if result["churn_prediction"] == 1 else "No"
            prob = result["probability"]
            
            st.success("Prediction complete!")
            st.metric(label="Will Churn?", value=churn_pred)
            st.metric(label="Churn Probability", value=f"{prob:.2%}")
        else:
            st.error(f"Error from API: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the API. Make sure the backend is running.")
