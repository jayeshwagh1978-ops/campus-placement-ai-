import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from student_portal import student_profile, video_interview
from college_portal import nep_compliance, placement_dashboard
from company_portal import job_parser, talent_heatmap
from ai_modules import chatbot, resume_builder

# Page configuration
st.set_page_config(
    page_title="Campus Placement AI Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('app/static/css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Session state initialization
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'chatbot_open' not in st.session_state:
    st.session_state.chatbot_open = False

# Authentication function
def authenticate_user(username, password, user_type):
    # Implement authentication logic
    # Connect to database and verify credentials
    return True  # Placeholder

# Login page
def login_page():
    st.title("🎓 Campus Placement AI Platform")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.container(border=True):
            st.subheader("Login")
            user_type = st.selectbox(
                "Select User Type",
                ["Student", "College Admin", "Company HR", "Admin"]
            )
            username = st.text_input("Username/Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if authenticate_user(username, password, user_type):
                    st.session_state.user_type = user_type
                    st.session_state.user_id = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# Main application
def main_app():
    # Sidebar navigation
    with st.sidebar:
        st.image("app/static/images/logo.png", width=200)
        st.title(f"Welcome, {st.session_state.user_id}")
        
        # Different menus based on user type
        if st.session_state.user_type == "Student":
            menu_options = [
                "Dashboard",
                "AI Resume Builder",
                "Video Interview Simulator",
                "Career Advisor",
                "NEP Suggestions",
                "Predictive Analytics",
                "Blockchain Credentials",
                "Internship Portal"
            ]
            selected = option_menu(
                menu_title="Student Portal",
                options=menu_options,
                icons=["house", "file-text", "camera-video", "compass", "book", "graph-up", "shield-check", "briefcase"],
                menu_icon="person",
                default_index=0
            )
        elif st.session_state.user_type == "College Admin":
            menu_options = [
                "College Dashboard",
                "NEP Compliance Score",
                "Placement Analytics",
                "Curriculum Mapping",
                "AR/VR Campus Tour",
                "Faculty Credentials",
                "Student Management"
            ]
            selected = option_menu(
                menu_title="College Portal",
                options=menu_options,
                icons=["building", "check-circle", "bar-chart", "diagram-3", "vr", "person-badge", "people"],
                menu_icon="building",
                default_index=0
            )
        elif st.session_state.user_type == "Company HR":
            menu_options = [
                "Company Dashboard",
                "Job Parser & Posting",
                "Talent Heatmap",
                "Hiring Analytics",
                "Interview Feedback",
                "National Leaderboard",
                "Internship Pipeline",
                "Campus Notifications"
            ]
            selected = option_menu(
                menu_title="Company Portal",
                options=menu_options,
                icons=["building", "search", "map", "graph-up-arrow", "chat", "trophy", "lightning", "bell"],
                menu_icon="briefcase",
                default_index=0
            )
        
        # Floating chatbot button
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.chatbot_open = not st.session_state.chatbot_open
    
    # Main content based on selection
    if st.session_state.user_type == "Student":
        if selected == "Dashboard":
            student_profile.show_dashboard()
        elif selected == "AI Resume Builder":
            resume_builder.show_resume_builder()
        elif selected == "Video Interview Simulator":
            video_interview.show_interview_simulator()
        # ... other student modules
    
    elif st.session_state.user_type == "College Admin":
        if selected == "College Dashboard":
            placement_dashboard.show_college_dashboard()
        elif selected == "NEP Compliance Score":
            nep_compliance.show_nep_compliance()
        # ... other college modules
    
    elif st.session_state.user_type == "Company HR":
        if selected == "Company Dashboard":
            talent_heatmap.show_company_dashboard()
        elif selected == "Job Parser & Posting":
            job_parser.show_job_parser()
        # ... other company modules
    
    # Floating chatbot
    if st.session_state.chatbot_open:
        chatbot.show_chatbot()

# Run the app
if __name__ == "__main__":
    if st.session_state.user_type is None:
        login_page()
    else:
        main_app()
