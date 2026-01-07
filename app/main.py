import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Import modules
from ai_modules.resume_builder import show_resume_builder
from student_portal.video_interview import show_interview_simulator
from ai_modules.predictive_analytics import show_predictive_analytics

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
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Authentication function
def authenticate_user(username, password, user_type):
    # Simple authentication for demo
    return username and password

# Login page
def login_page():
    st.markdown('<h1 class="main-header">🎓 Campus Placement AI Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔐 Login")
            user_type = st.selectbox(
                "Select User Type",
                ["Student", "College Admin", "Company HR", "Admin"]
            )
            username = st.text_input("Username/Email")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🚀 Login", use_container_width=True, type="primary"):
                    if authenticate_user(username, password, user_type):
                        st.session_state.user_type = user_type
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            
            with col_b:
                if st.button("👁️ Demo Login", use_container_width=True):
                    st.session_state.user_type = "Student"
                    st.session_state.username = "demo_user"
                    st.rerun()
            
            st.divider()
            st.caption("Don't have an account? Contact your institution administrator.")

# Student Portal
def student_portal():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title(f"👋 Welcome, {st.session_state.username}")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Student Portal",
            options=["Dashboard", "AI Resume Builder", "Interview Simulator", 
                    "Career Analytics", "NEP Suggestions", "Credentials"],
            icons=["house", "file-text", "camera-video", "graph-up", "book", "shield-check"],
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
        
        # AI Assistant
        st.divider()
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.show_chatbot = True
    
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
        {"icon": "🤖", "title": "Build Resume", "desc": "Create AI-optimized resume", "action": "resume"},
        {"icon": "🎥", "title": "Mock Interview", "desc": "Practice with AI feedback", "action": "interview"},
        {"icon": "📊", "title": "Career Analysis", "desc": "Get personalized insights", "action": "analytics"},
        {"icon": "🎯", "title": "Job Match", "desc": "Find suitable positions", "action": "jobs"},
        {"icon": "📚", "title": "Skill Gap", "desc": "Identify skills to learn", "action": "skills"},
        {"icon": "💼", "title": "Apply Now", "desc": "Browse opportunities", "action": "apply"}
    ]
    
    cols = st.columns(3)
    for idx, action in enumerate(actions):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {action['icon']} {action['title']}")
                st.write(action['desc'])
                if st.button(f"Go →", key=f"action_{idx}", use_container_width=True):
                    if action['action'] == 'resume':
                        st.session_state.menu_option = "AI Resume Builder"
                        st.rerun()
    
    # Progress tracking
    st.subheader("📈 Your Progress")
    
    progress_data = pd.DataFrame({
        'Week': ['W1', 'W2', 'W3', 'W4', 'W5', 'W6'],
        'Resume Score': [65, 70, 75, 80, 85, 88],
        'Interview Score': [60, 65, 70, 75, 80, 82],
        'Skill Count': [8, 10, 12, 14, 16, 18]
    })
    
    fig =
