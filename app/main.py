import streamlit as st

st.title("🎓 Campus Placement AI")
st.success("✅ App deployed successfully!")

# Simple test
st.write("### Student Data")
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "CGPA": [8.5, 7.2, 9.1],
    "Placement": ["Placed", "Not Placed", "Placed"]
}

st.table(data)

# Simple button
if st.button("Test Button"):
    st.balloons()
    st.write("🎉 Everything works!")
