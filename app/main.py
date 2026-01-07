import streamlit as st

st.set_page_config(page_title="Campus Placement AI", layout="wide")
st.title("🎯 Campus Placement AI")
st.success("✅ App is running successfully!")

# Simple test
st.write("### Test Section")
st.write("All dependencies are installed correctly.")
st.write("You can now add your actual placement prediction code.")

# Add a button
if st.button("Click to test"):
    st.balloons()
    st.write("🎈 Everything works!")
