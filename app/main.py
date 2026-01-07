import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd

# Import modules
from auth import init_session_state, login_form, logout, require_auth, get_current_user_type
from ai_modules.resume_builder import show_resume_builder
from student_portal.video_interview import show_interview_simulator
from ai_modules.predictive_analytics import show_predictive_analytics
from college_portal.nep_compliance import show_nep_compliance
from college_portal.placement_dashboard import show_placement_dashboard
from company_portal.job_parser import show_job_parser
from company_portal.talent_heatmap import show_talent_heatmap

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
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Student Portal
@require_auth()
def student_portal():
    user_type = get_current_user_type()
    if user_type != "student":
        st.error("Access denied. This portal is for students only.")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title(f"👋 Welcome, Student")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Student Portal",
            options=["Dashboard", "AI Resume Builder", "Interview Simulator", 
                    "Career Analytics", "NEP Suggestions", "Credentials", "Job Search"],
            icons=["house", "file-text", "camera-video", "graph-up", "book", "shield-check", "search"],
            menu_icon="person",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"color": "#3B82F6", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#3B82F6", "color": "white"},
            }
        )
        
        # Quick stats
        st.divider()
        st.subheader("📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile Score", "85%", "+5")
        with col2:
            st.metric("Interviews", "3", "+1")
        
        # Logout button
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content based on selection
    if selected == "Dashboard":
        student_dashboard()
    elif selected == "AI Resume Builder":
        show_resume_builder()
    elif selected == "Interview Simulator":
        show_interview_simulator()
    elif selected == "Career Analytics":
        show_predictive_analytics()
    elif selected == "NEP Suggestions":
        show_nep_suggestions()
    elif selected == "Credentials":
        show_credentials()
    elif selected == "Job Search":
        show_job_search()

# College Portal
@require_auth()
def college_portal():
    user_type = get_current_user_type()
    if user_type != "college":
        st.error("Access denied. This portal is for college administrators only.")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/school.png", width=80)
        st.title(f"🏫 College Admin")
        
        # Navigation menu
        selected = option_menu(
            menu_title="College Portal",
            options=["Dashboard", "NEP Compliance", "Placement Analytics", 
                    "Student Management", "Company Relations", "Reports"],
            icons=["house", "check-circle", "bar-chart", "people", "building", "file-text"],
            menu_icon="building",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"color": "#3B82F6", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#3B82F6", "color": "white"},
            }
        )
        
        # College stats
        st.divider()
        st.subheader("🏫 College Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Students", "1250", "+5%")
        with col2:
            st.metric("Placement", "78%", "+3.2%")
        
        # Logout button
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content based on selection
    if selected == "Dashboard":
        college_dashboard()
    elif selected == "NEP Compliance":
        show_nep_compliance()
    elif selected == "Placement Analytics":
        show_placement_dashboard()
    elif selected == "Student Management":
        show_student_management()
    elif selected == "Company Relations":
        show_company_relations()
    elif selected == "Reports":
        show_reports()

# Company Portal
@require_auth()
def company_portal():
    user_type = get_current_user_type()
    if user_type != "company":
        st.error("Access denied. This portal is for company HR only.")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/business.png", width=80)
        st.title(f"🏢 HR Manager")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Company Portal",
            options=["Dashboard", "Job Parser", "Talent Heatmap", 
                    "Candidate Search", "Interview Management", "Analytics"],
            icons=["house", "search", "map", "people", "calendar", "graph-up"],
            menu_icon="briefcase",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"color": "#3B82F6", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#3B82F6", "color": "white"},
            }
        )
        
        # Company stats
        st.divider()
        st.subheader("🏢 Company Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Openings", "15", "-2")
        with col2:
            st.metric("Hires", "12", "+3")
        
        # Logout button
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content based on selection
    if selected == "Dashboard":
        company_dashboard()
    elif selected == "Job Parser":
        show_job_parser()
    elif selected == "Talent Heatmap":
        show_talent_heatmap()
    elif selected == "Candidate Search":
        show_candidate_search()
    elif selected == "Interview Management":
        show_interview_management()
    elif selected == "Analytics":
        show_company_analytics()

# Dashboard functions (simplified versions)
def student_dashboard():
    st.title("📈 Student Dashboard")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Placement Ready", "85%", "Ready")
    with col2:
        st.metric("Resume Score", "88/100", "+8")
    with col3:
        st.metric("Skill Match", "92%", "Excellent")
    with col4:
        st.metric("Companies Applied", "12", "+3")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    actions = [
        {"icon": "🤖", "title": "Build Resume", "desc": "Create AI-optimized resume"},
        {"icon": "🎥", "title": "Mock Interview", "desc": "Practice with AI feedback"},
        {"icon": "📊", "title": "Career Analysis", "desc": "Get personalized insights"},
        {"icon": "🎯", "title": "Job Match", "desc": "Find suitable positions"},
        {"icon": "📚", "title": "Skill Gap", "desc": "Identify skills to learn"},
        {"icon": "💼", "title": "Apply Now", "desc": "Browse opportunities"}
    ]
    
    cols = st.columns(3)
    for idx, action in enumerate(actions):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {action['icon']} {action['title']}")
                st.write(action['desc'])
                if st.button("Go →", key=f"action_{idx}", use_container_width=True):
                    st.info(f"Opening {action['title']}...")

def college_dashboard():
    st.title("🏫 College Admin Dashboard")
    
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
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    actions = [
        {"title": "NEP Compliance", "desc": "Check NEP 2020 alignment"},
        {"title": "Placement Dashboard", "desc": "Real-time analytics"},
        {"title": "Student Management", "desc": "Manage student profiles"},
        {"title": "Company Relations", "desc": "Partner with companies"},
        {"title": "Generate Reports", "desc": "Create detailed reports"},
        {"title": "AR Campus Tour", "desc": "Virtual campus experience"}
    ]
    
    cols = st.columns(3)
    for idx, action in enumerate(actions):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {action['title']}")
                st.write(action['desc'])
                if st.button("Manage", key=f"col_action_{idx}", use_container_width=True):
                    st.info(f"Opening {action['title']}...")

def company_dashboard():
    st.title("🏢 Company HR Dashboard")
    
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
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    actions = [
        {"title": "Post New Job", "desc": "Create job opening"},
        {"title": "Talent Search", "desc": "Find candidates"},
        {"title": "Schedule Interviews", "desc": "Manage interviews"},
        {"title": "Analytics", "desc": "View hiring metrics"},
        {"title": "Campus Drives", "desc": "Plan campus visits"},
        {"title": "Reports", "desc": "Generate reports"}
    ]
    
    cols = st.columns(3)
    for idx, action in enumerate(actions):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {action['title']}")
                st.write(action['desc'])
                if st.button("Go", key=f"comp_action_{idx}", use_container_width=True):
                    st.info(f"Opening {action['title']}...")

# Placeholder functions for other menu items
def show_nep_suggestions():
    st.title("📚 NEP 2020 Suggestions")
    st.info("NEP suggestions module will be implemented here")

def show_credentials():
    st.title("🔗 Blockchain Credentials")
    st.info("Blockchain credentials module will be implemented here")

def show_job_search():
    st.title("🔍 Job Search")
    st.info("Job search module will be implemented here")

def show_student_management():
    st.title("👥 Student Management")
    st.info("Student management module will be implemented here")

def show_company_relations():
    st.title("🤝 Company Relations")
    st.info("Company relations module will be implemented here")

def show_reports():
    st.title("📊 Reports")
    st.info("Reports module will be implemented here")

def show_candidate_search():
    st.title("👨‍🎓 Candidate Search")
    st.info("Candidate search module will be implemented here")

def show_interview_management():
    st.title("📅 Interview Management")
    st.info("Interview management module will be implemented here")

def show_company_analytics():
    st.title("📈 Company Analytics")
    st.info("Company analytics module will be implemented here")

# Main application
def main():
    if not st.session_state.authenticated:
        login_form()
    else:
        user_type = get_current_user_type()
        
        if user_type == "student":
            student_portal()
        elif user_type == "college":
            college_portal()
        elif user_type == "company":
            company_portal()
        else:
            st.error("Unknown user type. Please contact administrator.")

if __name__ == "__main__":
    main()
