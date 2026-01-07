import streamlit as st
import pandas as pd
import numpy as np
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

def main():
    if st.session_state.user_type is None:
        login_page()
    else:
        if st.session_state.user_type == "Student":
            student_portal()
        elif st.session_state.user_type == "College":
            college_portal()
        elif st.session_state.user_type == "Company":
            company_portal()

def login_page():
    st.markdown('<h1 class="main-header">🎓 Campus Placement AI Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔐 Login")
            user_type = st.selectbox(
                "Select User Type",
                ["Student", "College", "Company"]
            )
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🚀 Login", use_container_width=True, type="primary"):
                    # Simple demo authentication
                    if username and password:
                        st.session_state.user_type = user_type
                        st.session_state.username = username
                        st.success(f"Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("Please enter username and password")
            
            with col_b:
                if st.button("👁️ Demo Login", use_container_width=True):
                    st.session_state.user_type = "Student"
                    st.session_state.username = "demo_user"
                    st.rerun()
            
            st.divider()
            st.caption("Demo Credentials: Any username/password will work")

def student_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title(f"👋 Welcome, {st.session_state.username}")
        
        # Navigation
        page = st.selectbox(
            "Navigation",
            ["Dashboard", "Resume Builder", "Interview Practice", "Career Analytics", "Settings"]
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
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    # Main content
    if page == "Dashboard":
        show_student_dashboard()
    elif page == "Resume Builder":
        show_resume_builder()
    elif page == "Interview Practice":
        show_interview_practice()
    elif page == "Career Analytics":
        show_career_analytics()
    elif page == "Settings":
        show_settings()

def show_student_dashboard():
    st.title("📈 Student Dashboard")
    
    # KPI metrics
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
                if st.button(f"Go →", key=f"action_{idx}", use_container_width=True):
                    st.info(f"Opening {action['title']}...")
    
    # Sample data visualization
    st.subheader("📈 Placement Trends")
    
    # Create sample data
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Placements': [45, 52, 48, 60, 75, 82],
        'Average Salary': [500, 520, 510, 550, 580, 600]
    })
    
    # Display as chart
    chart_data = pd.DataFrame({
        'Month': data['Month'],
        'Placements': data['Placements']
    })
    
    st.bar_chart(chart_data.set_index('Month'))
    
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

def show_resume_builder():
    st.title("🤖 AI Resume Builder")
    
    with st.form("resume_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", "John Doe")
            email = st.text_input("Email*", "john.doe@example.com")
            phone = st.text_input("Phone", "+91 9876543210")
        
        with col2:
            target_role = st.text_input("Target Role*", "Software Engineer")
            experience = st.number_input("Years of Experience", 0, 50, 3)
            current_role = st.text_input("Current Role", "Junior Developer")
        
        # Skills
        st.subheader("Skills")
        skills = st.text_area(
            "Enter your skills (comma-separated)",
            "Python, Java, SQL, React, AWS, Communication, Team Leadership"
        )
        
        # Experience
        st.subheader("Work Experience")
        experience_desc = st.text_area(
            "Describe your work experience",
            "• Developed and maintained web applications using React and Node.js\n• Led a team of 5 developers...",
            height=150
        )
        
        # Education
        st.subheader("Education")
        education = st.text_area(
            "Education details",
            "Bachelor of Technology in Computer Science\nUniversity Name, 2022\nGPA: 3.8/4.0"
        )
        
        # Submit button
        submitted = st.form_submit_button("✨ Generate AI-Optimized Resume", type="primary")
    
    if submitted:
        if name and email and target_role:
            st.success("✅ Resume generated successfully!")
            
            # Display resume preview
            with st.container(border=True):
                st.subheader("📄 Resume Preview")
                st.write(f"**Name:** {name}")
                st.write(f"**Email:** {email}")
                st.write(f"**Phone:** {phone}")
                st.write(f"**Target Role:** {target_role}")
                st.write("\n**Skills:**")
                st.write(skills)
                st.write("\n**Experience:**")
                st.write(experience_desc)
                st.write("\n**Education:**")
                st.write(education)
            
            # Download button
            resume_text = f"""
            RESUME - {name}
            
            Contact:
            Email: {email}
            Phone: {phone}
            
            Target Role: {target_role}
            
            Skills:
            {skills}
            
            Experience:
            {experience_desc}
            
            Education:
            {education}
            """
            
            st.download_button(
                "📥 Download Resume",
                data=resume_text,
                file_name=f"{name}_Resume.txt",
                mime="text/plain"
            )
        else:
            st.error("Please fill all required fields (*)")

def show_interview_practice():
    st.title("🎥 Interview Practice")
    
    st.info("Practice your interview skills with AI-powered feedback")
    
    # Question categories
    categories = st.multiselect(
        "Select question categories:",
        ["Technical", "Behavioral", "Scenario-based", "Problem Solving", "Leadership"],
        default=["Technical", "Behavioral"]
    )
    
    # Question display
    if categories:
        st.subheader("💬 Practice Questions")
        
        questions = [
            "Tell me about yourself and your background.",
            "Why are you interested in this role?",
            "Describe a challenging project you worked on.",
            "How do you handle tight deadlines?",
            "What are your strengths and weaknesses?"
        ]
        
        selected_q = st.selectbox("Select a question:", questions)
        
        st.write(f"**Question:** {selected_q}")
        
        # Answer input
        answer = st.text_area("Your Answer:", height=200)
        
        # Recording buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Record Audio Answer", use_container_width=True):
                st.info("Audio recording started...")
        
        with col2:
            if st.button("📹 Record Video Answer", use_container_width=True):
                st.info("Video recording started...")
        
        # Submit for feedback
        if st.button("📊 Get AI Feedback", type="primary"):
            if answer.strip():
                st.success("✅ Analysis complete!")
                
                # Display feedback
                with st.container(border=True):
                    st.subheader("🤖 AI Feedback")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Clarity Score", "85/100")
                        st.metric("Content Relevance", "90/100")
                        st.metric("Confidence Level", "78/100")
                    
                    with col2:
                        st.write("**Strengths:**")
                        st.success("✓ Good structure and organization")
                        st.success("✓ Relevant examples provided")
                        
                        st.write("**Areas for Improvement:**")
                        st.warning("⚠️ Could use more specific metrics")
                        st.warning("⚠️ Consider adding more technical details")
                
                # Tips
                st.subheader("💡 Tips for Improvement")
                tips = [
                    "Use the STAR method (Situation, Task, Action, Result)",
                    "Include specific numbers and metrics",
                    "Practice maintaining eye contact",
                    "Keep answers concise (1-2 minutes)",
                    "Show enthusiasm for the role"
                ]
                
                for tip in tips:
                    st.write(f"• {tip}")
            else:
                st.error("Please provide an answer before getting feedback")

def show_career_analytics():
    st.title("📊 Career Analytics")
    
    st.info("AI-powered insights for your career growth")
    
    # Student profile
    col1, col2 = st.columns(2)
    
    with col1:
        cgpa = st.slider("CGPA", 6.0, 10.0, 8.5, 0.1)
        projects = st.number_input("Number of Projects", 0, 20, 5)
    
    with col2:
        internships = st.number_input("Internships", 0, 5, 2)
        skills = st.slider("Technical Skills Count", 5, 50, 15)
    
    # Analyze button
    if st.button("🔍 Analyze Career Prospects", type="primary"):
        # Calculate scores
        base_score = 50
        cgpa_score = (cgpa - 6.0) * 10
        projects_score = projects * 5
        internships_score = internships * 15
        skills_score = skills * 2
        
        total_score = min(base_score + cgpa_score + projects_score + internships_score + skills_score, 95)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Placement Probability", f"{total_score}%")
        
        with col2:
            expected_salary = round(4.0 + (cgpa - 6.0) * 1.5 + internships * 0.8, 1)
            st.metric("Expected Salary", f"₹{expected_salary}L PA")
        
        with col3:
            readiness = "High" if total_score >= 80 else "Medium" if total_score >= 60 else "Low"
            st.metric("Readiness Level", readiness)
        
        # Recommendations
        st.subheader("🎯 Personalized Recommendations")
        
        recommendations = []
        
        if cgpa < 7.5:
            recommendations.append("Improve CGPA to at least 7.5")
        
        if projects < 3:
            recommendations.append("Complete at least 3 quality projects")
        
        if internships == 0:
            recommendations.append("Secure at least one internship")
        
        if skills < 10:
            recommendations.append("Learn 5 additional technical skills")
        
        if recommendations:
            for rec in recommendations:
                st.warning(f"⚠️ {rec}")
        else:
            st.success("✅ Your profile is strong for placements!")
        
        # Skill demand visualization
        st.subheader("📈 In-Demand Skills")
        
        skill_data = pd.DataFrame({
            'Skill': ['Python', 'Java', 'React', 'AWS', 'SQL', 'Machine Learning'],
            'Demand': [95, 85, 90, 88, 92, 96],
            'Salary Impact': [1.5, 1.2, 1.4, 1.6, 1.3, 1.8]
        })
        
        st.bar_chart(skill_data.set_index('Skill')['Demand'])

def show_settings():
    st.title("⚙️ Settings")
    
    with st.form("settings_form"):
        st.subheader("Profile Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            display_name = st.text_input("Display Name", st.session_state.username)
            email = st.text_input("Email", "student@example.com")
        
        with col2:
            phone = st.text_input("Phone", "+91 9876543210")
            department = st.selectbox("Department", ["CSE", "ECE", "ME", "CE", "IT"])
        
        st.subheader("Notification Preferences")
        
        col3, col4 = st.columns(2)
        
        with col3:
            email_notifications = st.checkbox("Email Notifications", True)
            job_alerts = st.checkbox("Job Alerts", True)
        
        with col4:
            interview_updates = st.checkbox("Interview Updates", True)
            newsletter = st.checkbox("Newsletter", False)
        
        # Save button
        if st.form_submit_button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")

def college_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/school.png", width=80)
        st.title(f"🏫 College Admin")
        
        page = st.selectbox(
            "Navigation",
            ["Dashboard", "Placement Analytics", "Student Management", "Company Relations", "Reports"]
        )
        
        st.divider()
        st.subheader("🏫 College Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Students", "1250", "+5%")
        with col2:
            st.metric("Placement", "78%", "+3.2%")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if page == "Dashboard":
        show_college_dashboard()
    else:
        st.title(f"🏫 {page}")
        st.info(f"{page} module will be implemented in Phase 2")

def show_college_dashboard():
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
    
    # Placement trend
    st.subheader("📈 Placement Trend")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    placements = [45, 52, 48, 60, 75, 82, 65, 70, 85, 90, 95, 100]
    
    trend_data = pd.DataFrame({
        'Month': months,
        'Placements': placements
    })
    
    st.line_chart(trend_data.set_index('Month'))
    
    # Department-wise performance
    st.subheader("📊 Department Performance")
    
    dept_data = pd.DataFrame({
        'Department': ['CSE', 'ECE', 'ME', 'CE', 'IT'],
        'Placements': [85, 65, 45, 40, 60],
        'Avg Salary': [9.5, 6.8, 5.5, 5.2, 7.2]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(dept_data.set_index('Department')['Placements'])
    
    with col2:
        st.bar_chart(dept_data.set_index('Department')['Avg Salary'])

def company_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/business.png", width=80)
        st.title(f"🏢 HR Manager")
        
        page = st.selectbox(
            "Navigation",
            ["Dashboard", "Job Postings", "Candidate Search", "Interview Schedule", "Analytics"]
        )
        
        st.divider()
        st.subheader("🏢 Company Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Openings", "15", "-2")
        with col2:
            st.metric("Hires", "12", "+3")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if page == "Dashboard":
        show_company_dashboard()
    else:
        st.title(f"🏢 {page}")
        st.info(f"{page} module will be implemented in Phase 3")

def show_company_dashboard():
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
    
    # Application trend
    st.subheader("📈 Application Trend")
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    applications = [45, 52, 48, 60, 75, 30, 12]
    
    app_data = pd.DataFrame({
        'Day': days,
        'Applications': applications
    })
    
    st.area_chart(app_data.set_index('Day'))
    
    # Top skills in applications
    st.subheader("🛠️ Top Skills in Applications")
    
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'Java', 'React', 'AWS', 'SQL'],
        'Count': [250, 180, 220, 150, 300]
    })
    
    st.bar_chart(skills_data.set_index('Skill'))

if __name__ == "__main__":
    main()
