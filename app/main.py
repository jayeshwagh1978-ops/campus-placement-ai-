import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

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
    }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'username' not in st.session_state:
    st.session_state.username = None

# Login Page
def login_page():
    st.markdown('<h1 class="main-header">🎓 Campus Placement AI Platform</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔐 Login")
            user_type = st.selectbox(
                "Select User Type",
                ["Student", "College Admin", "Company HR"]
            )
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🚀 Login", use_container_width=True, type="primary"):
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
                    st.session_state.username = "demo_student"
                    st.rerun()
            
            st.divider()
            st.caption("For demo purposes, any credentials will work")

# Main App
def main():
    if st.session_state.user_type is None:
        login_page()
    else:
        if st.session_state.user_type == "Student":
            student_portal()
        elif st.session_state.user_type == "College Admin":
            college_portal()
        elif st.session_state.user_type == "Company HR":
            company_portal()

# Student Portal
def student_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=80)
        st.title(f"👋 {st.session_state.username}")
        
        # Navigation
        menu = st.radio(
            "Navigation",
            ["Dashboard", "AI Resume Builder", "Interview Simulator", 
             "Career Analytics", "Job Search", "Settings"],
            index=0
        )
        
        # Quick stats
        st.divider()
        st.subheader("📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile", "85%")
        with col2:
            st.metric("Interviews", "3")
        
        # Logout
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    # Main Content
    if menu == "Dashboard":
        student_dashboard()
    elif menu == "AI Resume Builder":
        ai_resume_builder()
    elif menu == "Interview Simulator":
        interview_simulator()
    elif menu == "Career Analytics":
        career_analytics()
    elif menu == "Job Search":
        job_search()
    elif menu == "Settings":
        settings_page()

def student_dashboard():
    st.title("📈 Student Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Placement Ready", "85%", "Ready")
    with col2:
        st.metric("Resume Score", "88/100", "+8")
    with col3:
        st.metric("Skill Match", "92%", "Excellent")
    with col4:
        st.metric("Applications", "12", "+3")
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    cols = st.columns(3)
    
    actions = [
        ("🤖", "Build Resume", "Create AI-optimized resume"),
        ("🎥", "Mock Interview", "Practice with AI feedback"),
        ("📊", "Career Analysis", "Get personalized insights"),
        ("🎯", "Job Match", "Find suitable positions"),
        ("📚", "Skill Gap", "Identify skills to learn"),
        ("💼", "Apply Now", "Browse opportunities")
    ]
    
    for idx, (icon, title, desc) in enumerate(actions):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.write(desc)
                if st.button("Go →", key=f"action_{idx}", use_container_width=True):
                    st.info(f"Opening {title}...")
    
    # Placement Trends
    st.subheader("📈 Placement Trends")
    
    # Sample data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    placements = [45, 52, 48, 60, 75, 82]
    
    fig = go.Figure(data=go.Scatter(x=months, y=placements, mode='lines+markers'))
    fig.update_layout(title="Monthly Placements", xaxis_title="Month", yaxis_title="Placements")
    st.plotly_chart(fig, use_container_width=True)

def ai_resume_builder():
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
            location = st.text_input("Location", "Bangalore, India")
        
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
        
        # Submit
        submitted = st.form_submit_button("✨ Generate AI Resume", type="primary")
    
    if submitted:
        if name and email and target_role:
            st.success("✅ Resume generated successfully!")
            
            # Display preview
            with st.container(border=True):
                st.subheader("📄 AI-Optimized Resume")
                st.write(f"**Name:** {name}")
                st.write(f"**Target Role:** {target_role}")
                st.write(f"**Experience:** {experience} years")
                st.write("\n**Skills:**")
                st.write(skills)
                st.write("\n**Experience Summary:**")
                st.write(experience_desc)
            
            # ATS Score
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ATS Score", "88/100")
            with col2:
                st.metric("Keyword Match", "92%")
            with col3:
                st.metric("Readability", "Excellent")
            
            # Download
            resume_text = f"""RESUME - {name}
            
Contact: {email} | {phone}
Target Role: {target_role}

SKILLS:
{skills}

EXPERIENCE:
{experience_desc}

--- Generated by Campus Placement AI Platform ---"""
            
            st.download_button(
                "📥 Download Resume",
                data=resume_text,
                file_name=f"{name}_Resume.txt",
                mime="text/plain"
            )
        else:
            st.error("Please fill required fields (*)")

def interview_simulator():
    st.title("🎥 AI Interview Simulator")
    
    # Interview Setup
    col1, col2, col3 = st.columns(3)
    with col1:
        interview_type = st.selectbox("Interview Type", ["Technical", "HR", "Managerial", "Mock"])
    with col2:
        difficulty = st.select_slider("Difficulty", ["Easy", "Medium", "Hard"])
    with col3:
        duration = st.selectbox("Duration", ["15 min", "30 min", "45 min", "60 min"])
    
    # Question Bank
    st.subheader("💬 Practice Questions")
    
    questions = {
        "Technical": [
            "Explain the difference between list and tuple in Python.",
            "What is the time complexity of binary search?",
            "How does REST API work?",
            "Explain SQL joins with examples."
        ],
        "HR": [
            "Tell me about yourself.",
            "Why do you want to work here?",
            "Describe a challenging project.",
            "Where do you see yourself in 5 years?"
        ],
        "Managerial": [
            "How do you handle team conflicts?",
            "Describe your leadership style.",
            "How do you prioritize tasks?",
            "How do you give feedback?"
        ]
    }
    
    selected_q = st.selectbox(
        "Select a question:",
        questions.get(interview_type, questions["Technical"])
    )
    
    st.write(f"**Question:** {selected_q}")
    
    # Answer Section
    answer = st.text_area("Your Answer:", height=200, placeholder="Type your answer here...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎤 Record Answer", use_container_width=True):
            st.info("Recording started... Speak clearly.")
    with col2:
        if st.button("📹 Start Video", use_container_width=True):
            st.info("Video recording started... Maintain eye contact.")
    
    # AI Analysis
    if st.button("🤖 Get AI Feedback", type="primary", use_container_width=True):
        if answer.strip():
            st.success("✅ Analysis complete!")
            
            with st.container(border=True):
                st.subheader("📊 AI Feedback Report")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Clarity", "85/100")
                    st.metric("Relevance", "92/100")
                    st.metric("Structure", "78/100")
                
                with col2:
                    st.write("**✅ Strengths:**")
                    st.success("• Good structure and flow")
                    st.success("• Relevant examples provided")
                    
                    st.write("**⚠️ Improvements:**")
                    st.warning("• Add more specific metrics")
                    st.warning("• Include more technical details")
            
            # Tips
            st.subheader("💡 Improvement Tips")
            tips = [
                "Use STAR method (Situation, Task, Action, Result)",
                "Include specific numbers and achievements",
                "Practice maintaining eye contact",
                "Keep answers concise (1-2 minutes)",
                "Show enthusiasm and confidence"
            ]
            
            for tip in tips:
                st.write(f"• {tip}")
        else:
            st.error("Please provide an answer before analysis")

def career_analytics():
    st.title("📊 Career Analytics Dashboard")
    
    # Student Profile Input
    st.subheader("📋 Your Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        cgpa = st.slider("CGPA", 6.0, 10.0, 8.5, 0.1)
        projects = st.number_input("Number of Projects", 0, 20, 5)
    
    with col2:
        internships = st.number_input("Internships Completed", 0, 5, 2)
        skills = st.slider("Technical Skills", 5, 50, 15)
    
    # Analyze Button
    if st.button("🔍 Analyze Career Prospects", type="primary", use_container_width=True):
        # Calculate scores
        placement_prob = min(50 + (cgpa - 6) * 10 + projects * 3 + internships * 8 + skills * 2, 95)
        expected_salary = round(4.0 + (cgpa - 6.0) * 1.5 + internships * 0.8, 1)
        
        # Display Results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Placement Probability", f"{placement_prob}%")
        with col2:
            st.metric("Expected Salary", f"₹{expected_salary}L PA")
        with col3:
            readiness = "High" if placement_prob >= 80 else "Medium" if placement_prob >= 60 else "Low"
            st.metric("Readiness", readiness)
        
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
        
        # Skill Demand Visualization
        st.subheader("📈 In-Demand Skills")
        
        skill_data = pd.DataFrame({
            'Skill': ['Python', 'Java', 'React', 'AWS', 'SQL', 'ML'],
            'Demand': [95, 85, 90, 88, 92, 96]
        })
        
        fig = px.bar(skill_data, x='Skill', y='Demand', 
                     title="Skill Demand in Market",
                     color='Demand',
                     color_continuous_scale='viridis')
        st.plotly_chart(fig, use_container_width=True)

def job_search():
    st.title("🔍 Job Search")
    
    # Search Filters
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("Keywords", "software engineer")
        location = st.text_input("Location", "Bangalore")
    with col2:
        experience = st.selectbox("Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
        job_type = st.selectbox("Job Type", ["Full-time", "Internship", "Contract"])
    
    # Search Button
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        # Sample Job Data
        jobs = [
            {"Company": "Google", "Role": "Software Engineer", "Location": "Bangalore", "Exp": "1-3 years", "Salary": "₹15-25L"},
            {"Company": "Microsoft", "Role": "Data Scientist", "Location": "Hyderabad", "Exp": "3-5 years", "Salary": "₹18-30L"},
            {"Company": "Amazon", "Role": "ML Engineer", "Location": "Bangalore", "Exp": "2-4 years", "Salary": "₹16-28L"},
            {"Company": "TCS", "Role": "Full Stack Developer", "Location": "Mumbai", "Exp": "0-2 years", "Salary": "₹6-12L"},
            {"Company": "Infosys", "Role": "DevOps Engineer", "Location": "Pune", "Exp": "1-3 years", "Salary": "₹8-15L"},
            {"Company": "Wipro", "Role": "Cloud Architect", "Location": "Chennai", "Exp": "4-6 years", "Salary": "₹20-35L"}
        ]
        
        st.success(f"Found {len(jobs)} matching jobs")
        
        # Display Jobs
        for job in jobs:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"### {job['Role']}")
                    st.write(f"**{job['Company']}** - {job['Location']}")
                with col2:
                    st.write(f"**Experience:** {job['Exp']}")
                    st.write(f"**Salary:** {job['Salary']}")
                with col3:
                    if st.button("Apply", key=f"apply_{job['Company']}"):
                        st.success(f"Applied to {job['Role']} at {job['Company']}")

def settings_page():
    st.title("⚙️ Settings")
    
    with st.form("settings_form"):
        st.subheader("Profile Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", "John Doe")
            email = st.text_input("Email", "john.doe@example.com")
        with col2:
            phone = st.text_input("Phone", "+91 9876543210")
            department = st.selectbox("Department", ["CSE", "ECE", "ME", "CE", "IT"])
        
        st.subheader("Preferences")
        notifications = st.checkbox("Enable Notifications", True)
        newsletter = st.checkbox("Subscribe to Newsletter", False)
        
        if st.form_submit_button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")

# College Portal
def college_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/school.png", width=80)
        st.title(f"🏫 College Admin")
        
        menu = st.radio(
            "Navigation",
            ["Dashboard", "Placement Analytics", "Student Management", "Reports", "Settings"],
            index=0
        )
        
        st.divider()
        st.subheader("College Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Students", "1250")
        with col2:
            st.metric("Placement", "78%")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if menu == "Dashboard":
        college_dashboard()
    elif menu == "Placement Analytics":
        placement_analytics()
    elif menu == "Student Management":
        student_management()
    elif menu == "Reports":
        reports_page()
    elif menu == "Settings":
        college_settings()

def college_dashboard():
    st.title("🏫 College Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", "1250", "+5%")
    with col2:
        st.metric("Placement Rate", "78%", "+3.2%")
    with col3:
        st.metric("Avg Salary", "₹6.5L", "+12%")
    with col4:
        st.metric("Companies", "85", "+8")
    
    # Placement Trend
    st.subheader("📈 Placement Trend")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    placements = [45, 52, 48, 60, 75, 82, 65, 70, 85, 90, 95, 100]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=placements, mode='lines+markers', name='Placements'))
    fig.update_layout(title="Monthly Placements 2024", xaxis_title="Month", yaxis_title="Number of Placements")
    st.plotly_chart(fig, use_container_width=True)
    
    # Department Performance
    st.subheader("📊 Department Performance")
    
    dept_data = pd.DataFrame({
        'Department': ['CSE', 'ECE', 'ME', 'CE', 'IT'],
        'Placements': [85, 65, 45, 40, 60],
        'Avg Salary': [9.5, 6.8, 5.5, 5.2, 7.2]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(dept_data, x='Department', y='Placements',
                      title='Placements by Department',
                      color='Placements')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(dept_data, x='Department', y='Avg Salary',
                      title='Average Salary by Department',
                      color='Avg Salary')
        st.plotly_chart(fig2, use_container_width=True)

def placement_analytics():
    st.title("📊 Placement Analytics")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("Year", [2024, 2023, 2022, 2021])
    with col2:
        department = st.selectbox("Department", ["All", "CSE", "ECE", "ME", "CE", "IT"])
    with col3:
        company = st.selectbox("Company", ["All", "Google", "Microsoft", "Amazon", "TCS", "Infosys"])
    
    # Analytics Metrics
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Placements", "245")
    with col2:
        st.metric("Placement Rate", "78.5%")
    with col3:
        st.metric("Avg Package", "₹6.8L")
    with col4:
        st.metric("Top Recruiter", "Google")
    
    # Company-wise Analysis
    st.subheader("🏢 Company-wise Placements")
    
    company_data = pd.DataFrame({
        'Company': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys', 'Wipro'],
        'Placements': [25, 20, 18, 45, 40, 35],
        'Avg Package': [18.5, 16.8, 15.5, 6.5, 6.2, 5.8]
    })
    
    fig = px.bar(company_data, x='Company', y='Placements',
                 title='Number of Placements by Company',
                 color='Avg Package',
                 color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)

def student_management():
    st.title("👥 Student Management")
    
    # Search and Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search Students")
    with col2:
        dept_filter = st.selectbox("Department", ["All", "CSE", "ECE", "ME", "CE", "IT"])
    with col3:
        status_filter = st.selectbox("Placement Status", ["All", "Placed", "Not Placed", "Internship"])
    
    # Student Data
    students = [
        {"Name": "John Doe", "Roll No": "S1001", "Department": "CSE", "CGPA": 8.5, "Status": "Placed", "Company": "Google"},
        {"Name": "Jane Smith", "Roll No": "S1002", "Department": "ECE", "CGPA": 8.2, "Status": "Placed", "Company": "Microsoft"},
        {"Name": "Bob Johnson", "Roll No": "S1003", "Department": "CSE", "CGPA": 7.8, "Status": "Not Placed", "Company": "-"},
        {"Name": "Alice Brown", "Roll No": "S1004", "Department": "ME", "CGPA": 8.0, "Status": "Internship", "Company": "Bosch"},
        {"Name": "Charlie Wilson", "Roll No": "S1005", "Department": "IT", "CGPA": 8.7, "Status": "Placed", "Company": "Amazon"},
    ]
    
    # Display Students
    for student in students:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{student['Name']}** ({student['Roll No']})")
                st.write(f"{student['Department']} | CGPA: {student['CGPA']}")
            with col2:
                st.write(f"**Status:** {student['Status']}")
            with col3:
                st.write(f"**Company:** {student['Company']}")
            with col4:
                if st.button("View", key=f"view_{student['Roll No']}"):
                    st.info(f"Viewing details for {student['Name']}")

def reports_page():
    st.title("📋 Reports")
    
    # Report Types
    report_type = st.selectbox(
        "Select Report Type",
        ["Placement Report", "Student Performance", "Company Engagement", "Department Analysis"]
    )
    
    # Report Parameters
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    # Generate Report
    if st.button("📄 Generate Report", type="primary", use_container_width=True):
        st.success("✅ Report generated successfully!")
        
        # Sample Report Data
        report_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Placements': [45, 52, 48, 60, 75, 82],
            'Avg Salary': [5.0, 5.2, 5.1, 5.5, 5.8, 6.0],
            'Companies': [12, 15, 14, 18, 20, 22]
        })
        
        st.dataframe(report_data, use_container_width=True)
        
        # Download
        csv = report_data.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name=f"{report_type.replace(' ', '_')}.csv",
            mime="text/csv"
        )

def college_settings():
    st.title("⚙️ College Settings")
    
    with st.form("college_settings"):
        st.subheader("College Information")
        
        col1, col2 = st.columns(2)
        with col1:
            college_name = st.text_input("College Name", "ABC College of Engineering")
            location = st.text_input("Location", "Bangalore, Karnataka")
        with col2:
            contact_person = st.text_input("Contact Person", "Dr. John Smith")
            contact_email = st.text_input("Contact Email", "placement@abccollege.edu")
        
        st.subheader("Placement Settings")
        enable_ai = st.checkbox("Enable AI Features", True)
        auto_notifications = st.checkbox("Auto Notifications", True)
        
        if st.form_submit_button("💾 Save Settings", type="primary"):
            st.success("College settings saved successfully!")

# Company Portal
def company_portal():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/business.png", width=80)
        st.title(f"🏢 HR Manager")
        
        menu = st.radio(
            "Navigation",
            ["Dashboard", "Job Postings", "Candidate Search", "Interviews", "Analytics", "Settings"],
            index=0
        )
        
        st.divider()
        st.subheader("Company Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Openings", "15")
        with col2:
            st.metric("Hires", "12")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_type = None
            st.session_state.username = None
            st.rerun()
    
    if menu == "Dashboard":
        company_dashboard()
    elif menu == "Job Postings":
        job_postings()
    elif menu == "Candidate Search":
        candidate_search()
    elif menu == "Interviews":
        interviews_page()
    elif menu == "Analytics":
        company_analytics()
    elif menu == "Settings":
        company_settings()

def company_dashboard():
    st.title("🏢 Company Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open Positions", "15", "-2")
    with col2:
        st.metric("Applications", "342", "+45")
    with col3:
        st.metric("Interviews", "28", "+8")
    with col4:
        st.metric("Hires", "12", "+3")
    
    # Application Trend
    st.subheader("📈 Application Trend")
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    applications = [45, 52, 48, 60, 75, 30, 12]
    
    fig = go.Figure(data=go.Scatter(x=days, y=applications, mode='lines+markers', fill='tozeroy'))
    fig.update_layout(title="Weekly Applications", xaxis_title="Day", yaxis_title="Applications")
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Skills
    st.subheader("🛠️ Top Skills in Applications")
    
    skills_data = pd.DataFrame({
        'Skill': ['Python', 'Java', 'React', 'AWS', 'SQL', 'Docker'],
        'Count': [250, 180, 220, 150, 300, 120]
    })
    
    fig = px.bar(skills_data, x='Skill', y='Count',
                 title="Skill Distribution",
                 color='Count',
                 color_continuous_scale='blues')
    st.plotly_chart(fig, use_container_width=True)

def job_postings():
    st.title("📢 Job Postings")
    
    # Create New Job
    with st.expander("➕ Create New Job Posting", expanded=False):
        with st.form("new_job"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Job Title*", "Software Engineer")
                location = st.text_input("Location*", "Bangalore")
                job_type = st.selectbox("Job Type", ["Full-time", "Contract", "Internship"])
            with col2:
                experience = st.selectbox("Experience", ["Fresher", "1-3 years", "3-5 years", "5+ years"])
                salary = st.text_input("Salary Range", "₹10-20 LPA")
                deadline = st.date_input("Application Deadline")
            
            # Requirements
            st.subheader("Requirements")
            skills = st.text_area("Required Skills (comma-separated)", 
                                 "Python, Java, SQL, React, AWS")
            description = st.text_area("Job Description", 
                                      "We are looking for a talented software engineer...", 
                                      height=150)
            
            if st.form_submit_button("📤 Post Job", type="primary"):
                st.success("✅ Job posted successfully!")
    
    # Existing Job Postings
    st.subheader("📋 Active Job Postings")
    
    jobs = [
        {"Title": "Software Engineer", "Location": "Bangalore", "Type": "Full-time", "Applications": 45, "Status": "Active"},
        {"Title": "Data Scientist", "Location": "Hyderabad", "Type": "Full-time", "Applications": 32, "Status": "Active"},
        {"Title": "DevOps Engineer", "Location": "Pune", "Type": "Contract", "Applications": 28, "Status": "Active"},
        {"Title": "ML Intern", "Location": "Remote", "Type": "Internship", "Applications": 65, "Status": "Active"},
    ]
    
    for job in jobs:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{job['Title']}**")
                st.write(f"{job['Location']} | {job['Type']}")
            with col2:
                st.write(f"**Applications:** {job['Applications']}")
            with col3:
                st.write(f"**Status:** {job['Status']}")
            with col4:
                if st.button("Manage", key=f"manage_{job['Title']}"):
                    st.info(f"Managing {job['Title']}")

def candidate_search():
    st.title("👨‍🎓 Candidate Search")
    
    # Search Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        skills = st.text_input("Skills", "Python, SQL")
        cgpa = st.slider("Minimum CGPA", 6.0, 10.0, 7.5, 0.1)
    with col2:
        location = st.text_input("Preferred Location", "Bangalore")
        experience = st.selectbox("Experience Level", ["Any", "Fresher", "1+ years", "2+ years"])
    with col3:
        department = st.selectbox("Department", ["Any", "CSE", "ECE", "ME", "IT"])
        availability = st.selectbox("Availability", ["Immediate", "1 month", "3 months"])
    
    # Search Button
    if st.button("🔍 Search Candidates", type="primary", use_container_width=True):
        # Sample Candidates
        candidates = [
            {"Name": "John Doe", "College": "IIT Bombay", "CGPA": 8.5, "Skills": "Python, Java, AWS", "Experience": "2 years"},
            {"Name": "Jane Smith", "College": "NIT Trichy", "CGPA": 8.2, "Skills": "React, Node.js, SQL", "Experience": "1 year"},
            {"Name": "Bob Johnson", "College": "BITS Pilani", "CGPA": 8.7, "Skills": "ML, Python, TensorFlow", "Experience": "Fresher"},
            {"Name": "Alice Brown", "College": "IIIT Hyderabad", "CGPA": 8.9, "Skills": "Java, Spring, Microservices", "Experience": "3 years"},
        ]
        
        st.success(f"Found {len(candidates)} matching candidates")
        
        # Display Candidates
        for candidate in candidates:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{candidate['Name']}**")
                    st.write(f"{candidate['College']} | CGPA: {candidate['CGPA']}")
                    st.write(f"Skills: {candidate['Skills']}")
                with col2:
                    st.write(f"**Experience:** {candidate['Experience']}")
                with col3:
                    match_score = np.random.randint(85, 96)
                    st.metric("Match", f"{match_score}%")
                with col4:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("👁️", key=f"view_{candidate['Name']}"):
                            st.info(f"Viewing {candidate['Name']}'s profile")
                    with col_b:
                        if st.button("💬", key=f"contact_{candidate['Name']}"):
                            st.success(f"Contact request sent to {candidate['Name']}")

def interviews_page():
    st.title("📅 Interview Management")
    
    # Tabs for different interview stages
    tab1, tab2, tab3 = st.tabs(["📋 Scheduled", "🎯 Completed", "📊 Analysis"])
    
    with tab1:
        st.subheader("Upcoming Interviews")
        
        interviews = [
            {"Candidate": "John Doe", "Role": "Software Engineer", "Date": "2024-01-15", "Time": "10:00 AM", "Type": "Technical"},
            {"Candidate": "Jane Smith", "Role": "Data Scientist", "Date": "2024-01-16", "Time": "2:00 PM", "Type": "HR"},
            {"Candidate": "Bob Johnson", "Role": "ML Engineer", "Date": "2024-01-17", "Time": "11:00 AM", "Type": "Managerial"},
        ]
        
        for interview in interviews:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**{interview['Candidate']}**")
                    st.write(f"Role: {interview['Role']}")
                with col2:
                    st.write(f"**Date:** {interview['Date']}")
                    st.write(f"**Time:** {interview['Time']}")
                with col3:
                    st.write(f"**Type:** {interview['Type']}")
                with col4:
                    if st.button("Start", key=f"start_{interview['Candidate']}"):
                        st.info(f"Starting interview with {interview['Candidate']}")
    
    with tab2:
        st.subheader("Completed Interviews")
        st.info("Completed interviews will appear here")
    
    with tab3:
        st.subheader("Interview Analytics")
        
        # Interview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Interviews", "28")
        with col2:
            st.metric("Completion Rate", "92%")
        with col3:
            st.metric("Avg Duration", "45 min")
        with col4:
            st.metric("Success Rate", "65%")

def company_analytics():
    st.title("📈 Company Analytics")
    
    # Hiring Metrics
    st.subheader("📊 Hiring Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Time to Hire", "32 days", "-5")
    with col2:
        st.metric("Cost per Hire", "₹85K", "-8%")
    with col3:
        st.metric("Offer Acceptance", "78%", "+5%")
    with col4:
        st.metric("Quality of Hire", "4.2/5", "+0.3")
    
    # Source Analysis
    st.subheader("📋 Source Analysis")
    
    source_data = pd.DataFrame({
        'Source': ['Campus', 'Referral', 'LinkedIn', 'Job Portal', 'Agency'],
        'Candidates': [45, 32, 28, 65, 12],
        'Hires': [12, 8, 6, 4, 2]
    })
    
    fig = px.pie(source_data, values='Candidates', names='Source', 
                 title='Candidate Sources')
    st.plotly_chart(fig, use_container_width=True)
    
    # Skill Gap Analysis
    st.subheader("🔍 Skill Gap Analysis")
    
    gap_data = pd.DataFrame({
        'Skill': ['Python', 'AWS', 'React', 'ML', 'DevOps'],
        'Required': [95, 90, 85, 80, 75],
        'Available': [85, 75, 80, 65, 70],
        'Gap': [10, 15, 5, 15, 5]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=gap_data['Skill'], y=gap_data['Required'], name='Required'))
    fig.add_trace(go.Bar(x=gap_data['Skill'], y=gap_data['Available'], name='Available'))
    fig.update_layout(title="Skill Requirement vs Availability", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def company_settings():
    st.title("⚙️ Company Settings")
    
    with st.form("company_settings"):
        st.subheader("Company Information")
        
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name", "TechCorp Solutions")
            industry = st.selectbox("Industry", ["IT", "Finance", "Healthcare", "E-commerce", "Manufacturing"])
        with col2:
            hr_contact = st.text_input("HR Contact", "Sarah Johnson")
            hr_email = st.text_input("HR Email", "hr@techcorp.com")
        
        st.subheader("Hiring Preferences")
        enable_ai_matching = st.checkbox("Enable AI Candidate Matching", True)
        auto_scheduling = st.checkbox("Auto Interview Scheduling", True)
        notification_prefs = st.multiselect(
            "Notifications",
            ["New Applications", "Interview Reminders", "Report Generation", "System Updates"],
            default=["New Applications", "Interview Reminders"]
        )
        
        if st.form_submit_button("💾 Save Settings", type="primary"):
            st.success("Company settings saved successfully!")

if __name__ == "__main__":
    main()
