import streamlit as st
from datetime import time, datetime

st.header("st.slider")

# example 1 
st.subheader("Slider")

age = st.slider("How old are you?" , 0,100)
st.write("I'm", age, "years old")

#example 2
st.subheader("Range slider")

range = st.slider("Select a range of values" , 0.00, 100.00, value = (25.00,75.00))
st.write("Value :", range)

#example 3
st.subheader("Range time slider")

appointment = st.slider(label = "Schedule your appointment:" , min_value = time(0,59) , max_value= time(23,59), value = (time(8, 40), time(12, 45)))
st.write("You're scheduled for:", appointment)

#example 4
st.subheader("Datetime slider")

start_time = st.slider(label= "when do you start?" , format="MMMM Do YYYY" , min_value=datetime(1995,11,23) , max_value=datetime(2022,11,23))
st.write("Start time: ", start_time)
