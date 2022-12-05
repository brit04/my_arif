import streamlit as st 

st.header("st.button")

if st.button("say hello"):
    st.write("why helo there")
else :  
    st.write("goodbye")
