import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Campus Placement AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🎓 Campus Placement AI")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Data Analysis", "Placement Predictor", "About"])

if page == "Home":
    st.header("Welcome to Campus Placement AI")
    st.write("""
    This AI-powered application helps predict campus placement outcomes 
    based on student academic performance and skills.
    
    ### Features:
    📊 **Data Analysis** - Explore placement trends and patterns
    🤖 **AI Predictor** - Predict placement chances using ML models
    📈 **Visualizations** - Interactive charts and graphs
    💼 **Insights** - Get actionable recommendations
    """)
    
    # Sample data display
    st.subheader("📋 Sample Student Data")
    sample_data = pd.DataFrame({
        'Student_ID': [101, 102, 103, 104, 105],
        'CGPA': [8.5, 7.2, 9.1, 6.8, 8.9],
        'Internships': [2, 1, 3, 0, 2],
        'Projects': [3, 2, 4, 1, 3],
        'Skills': ['Python,SQL', 'Java', 'Python,ML,SQL', 'C++', 'Python,Java,Cloud'],
        'Placement_Status': ['Placed', 'Not Placed', 'Placed', 'Not Placed', 'Placed']
    })
    st.dataframe(sample_data, use_container_width=True)
    
    st.success("✅ Application is running successfully!")

elif page == "Data Analysis":
    st.header("📊 Data Analysis Dashboard")
    
    # Create sample data for visualization
    np.random.seed(42)
    data_size = 200
    
    analysis_data = pd.DataFrame({
        'CGPA': np.round(np.random.normal(7.5, 1.2, data_size), 1),
        'Internships': np.random.randint(0, 4, data_size),
        'Projects': np.random.randint(1, 6, data_size),
        'Placement_Chance': np.random.uniform(0, 1, data_size)
    })
    analysis_data['CGPA'] = analysis_data['CGPA'].clip(5.0, 10.0)
    analysis_data['Placement_Status'] = analysis_data['Placement_Chance'].apply(lambda x: 'Placed' if x > 0.6 else 'Not Placed')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CGPA Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(data=analysis_data, x='CGPA', hue='Placement_Status', kde=True, ax=ax)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Placement by Internships")
        placement_rate = analysis_data.groupby('Internships')['Placement_Status'].apply(
            lambda x: (x == 'Placed').mean() * 100
        ).reset_index()
        st.bar_chart(placement_rate.set_index('Internships'))
    
    st.subheader("📈 Correlation Analysis")
    fig, ax = plt.subplots(figsize=(10, 6))
    corr_data = analysis_data[['CGPA', 'Internships', 'Projects', 'Placement_Chance']]
    sns.heatmap(corr_data.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

elif page == "Placement Predictor":
    st.header("🤖 Placement Predictor")
    
    # User input form
    with st.form("prediction_form"):
        st.subheader("Enter Student Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA Score", 5.0, 10.0, 7.5, 0.1)
            internships = st.selectbox("Number of Internships", [0, 1, 2, 3, 4])
            backlogs = st.selectbox("Number of Backlogs", [0, 1, 2, 3])
        
        with col2:
            projects = st.selectbox("Number of Projects", [1, 2, 3, 4, 5])
            skills = st.multiselect("Technical Skills", 
                                  ['Python', 'Java', 'SQL', 'Machine Learning', 
                                   'Web Development', 'Cloud Computing', 'Data Analysis'])
            communication = st.slider("Communication Skills (1-10)", 1, 10, 6)
        
        submitted = st.form_submit_button("Predict Placement")
    
    if submitted:
        # Simple prediction logic (can replace with actual ML model)
        score = 0
        
        # CGPA contribution (40%)
        if cgpa >= 9.0:
            score += 40
        elif cgpa >= 8.0:
            score += 30
        elif cgpa >= 7.0:
            score += 20
        else:
            score += 10
        
        # Internships contribution (20%)
        score += internships * 5
        
        # Projects contribution (15%)
        score += projects * 3
        
        # Skills contribution (15%)
        score += len(skills) * 3
        
        # Communication contribution (10%)
        score += communication
        
        # Determine placement
        placement_chance = min(score / 100, 1.0)
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Prediction Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Score", f"{score}/100")
        
        with col2:
            st.metric("Placement Chance", f"{placement_chance*100:.1f}%")
        
        with col3:
            status = "HIGH" if placement_chance >= 0.7 else "MEDIUM" if placement_chance >= 0.5 else "LOW"
            st.metric("Prediction", status)
        
        # Progress bar
        st.progress(placement_chance)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        if placement_chance >= 0.7:
            st.success("""
            ✅ **Excellent profile!** 
            - Continue current efforts
            - Prepare for interviews
            - Target top companies
            """)
        elif placement_chance >= 0.5:
            st.warning("""
            ⚠️ **Good profile, needs improvement**
            - Work on 1-2 more projects
            - Improve communication skills
            - Consider an internship
            """)
        else:
            st.error("""
            ❌ **Needs significant improvement**
            - Focus on improving CGPA
            - Complete at least 1 internship
            - Build technical skills portfolio
            - Work on communication skills
            """)

elif page == "About":
    st.header("ℹ️ About This Application")
    
    st.write("""
    ### Campus Placement AI
    
    **Version:** 1.0.0
    
    **Description:**
    This application uses Machine Learning to predict campus placement outcomes 
    based on various academic and extracurricular parameters.
    
    ### Features:
    - 📊 Data visualization and analysis
    - 🤖 AI-powered placement prediction
    - 📈 Interactive dashboards
    - 💼 Personalized recommendations
    
    ### Technology Stack:
    - **Frontend:** Streamlit
    - **Backend:** Python, Scikit-learn
    - **ML Models:** Random Forest, Logistic Regression
    - **Visualization:** Matplotlib, Seaborn
    
    ### Developed by:
    Campus Placement AI Team
    
    ### Contact:
    For support or queries, please contact the development team.
    """)
    
    st.info("""
    ⚠️ **Note:** This is a demonstration application. 
    For production use, train with actual placement data.
    """)

# Footer
st.markdown("---")
st.caption("© 2024 Campus Placement AI | Made with Streamlit")

print("App loaded successfully!")  # This helps in debugging
