import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Campus Placement AI Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #3B82F6;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Authentication function (placeholder)
def authenticate_user(username, password, user_type):
    # Simple authentication for demo
    return username and password

# Login page
def login_page():
    st.markdown('<h1 class="main-header">🎓 Campus Placement AI Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("Login")
            user_type = st.selectbox(
                "Select User Type",
                ["Student", "College Admin", "Company HR", "Admin"]
            )
            username = st.text_input("Username/Email")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Login", use_container_width=True):
                    if authenticate_user(username, password, user_type):
                        st.session_state.user_type = user_type
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            with col_b:
                if st.button("Demo Login", use_container_width=True):
                    st.session_state.user_type = "Student"
                    st.session_state.username = "demo_user"
                    st.rerun()

# Student Dashboard
def student_dashboard():
    st.title("👨‍🎓 Student Portal")
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Placement Status", "Pending", "Ready")
    with col2:
        st.metric("Resume Score", "85/100", "+5")
    with col3:
        st.metric("Interviews", "3", "+1")
    with col4:
        st.metric("Skills", "12", "+3")
    
    # Features grid
    st.subheader("Available Features")
    
    features = [
        {"icon": "🤖", "title": "AI Resume Builder", "desc": "Build ATS-optimized resumes"},
        {"icon": "🎥", "title": "Interview Simulator", "desc": "Practice with AI feedback"},
        {"icon": "📊", "title": "Career Analytics", "desc": "Get personalized insights"},
        {"icon": "🎯", "title": "NEP Suggestions", "desc": "Major/Minor recommendations"},
        {"icon": "🔗", "title": "Credentials", "desc": "Blockchain verified certificates"},
        {"icon": "💬", "title": "AI Assistant", "desc": "24/7 career guidance"}
    ]
    
    cols = st.columns(3)
    for idx, feature in enumerate(features):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {feature['icon']} {feature['title']}")
                st.write(feature['desc'])
                if st.button(f"Explore →", key=f"btn_{idx}"):
                    st.info(f"Opening {feature['title']}...")
    
    # Sample data visualization
    st.subheader("📈 Placement Trends")
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Placements': [45, 52, 48, 60, 75, 82],
        'Average Salary': [500000, 520000, 510000, 550000, 580000, 600000]
    })
    
    fig = px.line(data, x='Month', y=['Placements', 'Average Salary'],
                  title="Monthly Placement Statistics",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

# College Admin Dashboard
def college_admin_dashboard():
    st.title("🏫 College Admin Portal")
    
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", "1250", "+5%")
    with col2:
        st.metric("Placement Rate", "78%", "+3.2%")
    with col3:
        st.metric("Avg Salary", "₹6.5L", "+12%")
    with col4:
        st.metric("Companies", "85", "+8")
    
    # College features
    st.subheader("College Management Features")
    
    college_features = [
        {"title": "NEP Compliance", "desc": "Check NEP 2020 alignment"},
        {"title": "Placement Dashboard", "desc": "Real-time analytics"},
        {"title": "Curriculum Mapping", "desc": "Subject alignment"},
        {"title": "Faculty Management", "desc": "Blockchain credentials"},
        {"title": "AR Campus Tour", "desc": "Virtual campus experience"},
        {"title": "Reports", "desc": "Generate detailed reports"}
    ]
    
    for feature in college_features:
        with st.expander(f"📋 {feature['title']}"):
            st.write(feature['desc'])
            if st.button(f"Manage {feature['title']}", key=f"col_{feature['title']}"):
                st.success(f"Opening {feature['title']} module")

# Company HR Dashboard
def company_hr_dashboard():
    st.title("🏢 Company HR Portal")
    
    # Company metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open Positions", "15", "-2")
    with col2:
        st.metric("Applications", "342", "+45")
    with col3:
        st.metric("Interviews", "28", "+8")
    with col4:
        st.metric("Hires", "12", "+3")
    
    # HR features
    st.subheader("HR Management Features")
    
    hr_features = [
        {"title": "Job Parser", "desc": "AI-powered job description analysis"},
        {"title": "Talent Heatmap", "desc": "Visual campus talent distribution"},
        {"title": "Hiring Analytics", "desc": "Data-driven insights"},
        {"title": "Interview Vault", "desc": "Secure feedback storage"},
        {"title": "Leaderboard", "desc": "National ranking"},
        {"title": "Internship Pipeline", "desc": "Streamlined hiring process"}
    ]
    
    cols = st.columns(2)
    for idx, feature in enumerate(hr_features):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### {feature['title']}")
                st.write(feature['desc'])
                if st.button("Use Tool", key=f"hr_{idx}"):
                    st.info(f"Launching {feature['title']}...")
    
    # Sample talent data
    st.subheader("🎯 Talent Distribution")
    talent_data = pd.DataFrame({
        'Skill': ['Python', 'ML', 'Java', 'React', 'SQL', 'Cloud'],
        'Students': [250, 180, 220, 150, 300, 120],
        'Demand': [95, 90, 85, 80, 95, 90]
    })
    
    fig = px.bar(talent_data, x='Skill', y=['Students', 'Demand'],
                 barmode='group', title="Skill Distribution vs Industry Demand")
    st.plotly_chart(fig, use_container_width=True)

# Main application
def main_app():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title(f"Welcome, {st.session_state.username}")
        st.write(f"Role: {st.session_state.user_type}")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
        
        st.divider()
        
        # Quick links based on user type
        st.subheader("Quick Links")
        if st.session_state.user_type == "Student":
            st.button("📄 My Resume", use_container_width=True)
            st.button("📅 My Interviews", use_container_width=True)
            st.button("📊 My Progress", use_container_width=True)
            st.button("🎯 Recommendations", use_container_width=True)
        elif st.session_state.user_type == "College Admin":
            st.button("📈 Placement Stats", use_container_width=True)
            st.button("👥 Student Management", use_container_width=True)
            st.button("🏢 Company Relations", use_container_width=True)
            st.button("📋 Reports", use_container_width=True)
        elif st.session_state.user_type == "Company HR":
            st.button("📢 Post Jobs", use_container_width=True)
            st.button("👨‍🎓 View Candidates", use_container_width=True)
            st.button("📅 Schedule Interviews", use_container_width=True)
            st.button("📊 Analytics", use_container_width=True)
    
    # Main content based on user type
    if st.session_state.user_type == "Student":
        student_dashboard()
    elif st.session_state.user_type == "College Admin":
        college_admin_dashboard()
    elif st.session_state.user_type == "Company HR":
        company_hr_dashboard()

# Run the app
if __name__ == "__main__":
    if st.session_state.user_type is None:
        login_page()
    else:
        main_app()
