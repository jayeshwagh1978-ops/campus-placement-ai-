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
    
    fig = px.line(progress_data, x='Week', y=['Resume Score', 'Interview Score', 'Skill Count'],
                  title="Weekly Progress Tracking",
                  markers=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    
    activities = [
        {"date": "2024-01-10", "activity": "Resume reviewed by AI", "status": "✅ Completed"},
        {"date": "2024-01-09", "activity": "Mock interview completed", "status": "✅ Score: 85%"},
        {"date": "2024-01-08", "activity": "Applied to Google", "status": "⏳ Under Review"},
        {"date": "2024-01-07", "activity": "Skill assessment test", "status": "✅ Passed"},
        {"date": "2024-01-06", "activity": "Career counseling session", "status": "✅ Completed"}
    ]
    
    for act in activities:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(act['date'])
        with col2:
            st.write(act['activity'])
        with col3:
            st.write(act['status'])
        st.divider()

def show_nep_suggestions():
    st.title("📚 NEP 2020 Aligned Suggestions")
    
    st.info("""
    Based on NEP 2020 guidelines, here are personalized recommendations for your academic and career path.
    """)
    
    # Student profile
    col1, col2 = st.columns(2)
    
    with col1:
        current_major = st.selectbox("Current Major", 
                                    ["Computer Science", "Electronics", "Mechanical", "Civil", "Information Technology"])
        current_year = st.selectbox("Current Year", [1, 2, 3, 4])
        interests = st.multiselect("Your Interests",
                                  ["AI/ML", "Web Development", "Data Science", "Cybersecurity", 
                                   "IoT", "Robotics", "Cloud Computing", "Business Analytics"])
    
    with col2:
        skills = st.multiselect("Your Skills",
                               ["Python", "Java", "JavaScript", "SQL", "React", "AWS", "Docker", "Git"])
        career_goal = st.selectbox("Career Goal",
                                  ["Software Developer", "Data Scientist", "ML Engineer", 
                                   "DevOps Engineer", "Product Manager", "Research"])
    
    if st.button("🎯 Get NEP Recommendations", type="primary"):
        # Generate recommendations
        recommendations = {
            "major_minor": [
                {"major": "Computer Science", "minor": "Business Analytics", "reason": "Aligns with your interest in business applications"},
                {"major": "Computer Science", "minor": "Mathematics", "reason": "Strong foundation for AI/ML career"},
                {"major": "Computer Science", "minor": "Psychology", "reason": "Good for UX/Product Management roles"}
            ],
            "courses": [
                {"course": "AI Ethics", "type": "Multidisciplinary", "credits": 3},
                {"course": "Entrepreneurship", "type": "Vocational", "credits": 2},
                {"course": "Research Methodology", "type": "Research", "credits": 4}
            ],
            "internships": [
                {"type": "Research Intern", "domain": "AI/ML", "duration": "3 months"},
                {"type": "Industry Intern", "domain": "Software Development", "duration": "6 months"}
            ]
        }
        
        st.success("✅ Recommendations generated based on NEP 2020 guidelines!")
        
        # Display recommendations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🎓 Major/Minor Combinations")
            for rec in recommendations['major_minor']:
                with st.container(border=True):
                    st.write(f"**{rec['major']} + {rec['minor']}**")
                    st.caption(rec['reason'])
        
        with col2:
            st.subheader("📚 Recommended Courses")
            for rec in recommendations['courses']:
                with st.container(border=True):
                    st.write(f"**{rec['course']}**")
                    st.caption(f"{rec['type']} • {rec['credits']} credits")
        
        with col3:
            st.subheader("💼 Internship Pathways")
            for rec in recommendations['internships']:
                with st.container(border=True):
                    st.write(f"**{rec['type']}**")
                    st.caption(f"{rec['domain']} • {rec['duration']}")

def show_credentials():
    st.title("🔗 Blockchain Verified Credentials")
    
    st.info("""
    Your certificates and achievements stored securely on blockchain.
    Immutable and verifiable anywhere.
    """)
    
    # Sample credentials
    credentials = [
        {"name": "Bachelor of Technology", "issuer": "University", "date": "2024-05-15", "hash": "0x1234...", "verified": True},
        {"name": "Google Cloud Certified", "issuer": "Google", "date": "2024-03-20", "hash": "0x5678...", "verified": True},
        {"name": "AWS Solutions Architect", "issuer": "Amazon", "date": "2024-02-10", "hash": "0x9abc...", "verified": True},
        {"name": "Python Programming", "issuer": "Coursera", "date": "2023-12-05", "hash": "0xdef0...", "verified": True},
        {"name": "Machine Learning Specialization", "issuer": "Stanford", "date": "2023-10-15", "hash": "0x1235...", "verified": True}
    ]
    
    # Display credentials
    for cred in credentials:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.write(f"**{cred['name']}**")
                st.caption(f"Issued by: {cred['issuer']}")
            
            with col2:
                st.write(f"📅 {cred['date']}")
            
            with col3:
                if cred['verified']:
                    st.success("✅ Verified")
                else:
                    st.warning("⏳ Pending")
            
            with col4:
                if st.button("🔗 View", key=f"view_{cred['hash']}"):
                    st.code(f"Blockchain Hash: {cred['hash']}")
                    st.info("This certificate is permanently stored on the blockchain.")
    
    # Add new credential
    st.subheader("➕ Add New Certificate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cert_name = st.text_input("Certificate Name")
        issuer = st.text_input("Issuing Organization")
    
    with col2:
        issue_date = st.date_input("Issue Date")
        cert_file = st.file_uploader("Upload Certificate", type=['pdf', 'png', 'jpg'])
    
    if st.button("📤 Upload to Blockchain", type="primary"):
        if cert_name and issuer and cert_file:
            st.success("✅ Certificate uploaded to blockchain successfully!")
            st.info("Transaction Hash: 0x9876... (Store this for verification)")
        else:
            st.error("Please fill all fields and upload certificate")

# College and Company Portals (simplified for now)
def college_portal():
    st.title("🏫 College Admin Portal")
    st.info("College portal features will be implemented in Phase 2")

def company_portal():
    st.title("🏢 Company HR Portal")
    st.info("Company portal features will be implemented in Phase 3")

# Main application
def main_app():
    # Route based on user type
    if st.session_state.user_type == "Student":
        student_portal()
    elif st.session_state.user_type == "College Admin":
        college_portal()
    elif st.session_state.user_type == "Company HR":
        company_portal()
    else:
        st.error("Invalid user type")

# Run the app
if __name__ == "__main__":
    if st.session_state.user_type is None:
        login_page()
    else:
        main_app()
