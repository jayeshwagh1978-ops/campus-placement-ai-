import streamlit as st

# Simple app that definitely works
st.set_page_config(page_title="Campus Placement", layout="wide")
st.title("Campus Placement AI - TEST")
st.write("This is a test app to stop the restart loop.")

# Add a dataframe WITHOUT pandas
st.subheader("Student Data")
data = [
    {"Name": "Alice", "CGPA": 8.5, "Placed": "Yes"},
    {"Name": "Bob", "CGPA": 7.2, "Placed": "No"},
    {"Name": "Charlie", "CGPA": 9.1, "Placed": "Yes"}
]

for student in data:
    st.write(f"- {student['Name']}: CGPA {student['CGPA']}, {student['Placed']}")

st.success("✅ App is working! No more restart loop.")
