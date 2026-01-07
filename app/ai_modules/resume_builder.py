import streamlit as st
import pandas as pd
import json
import re
from typing import Dict, List, Any
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class ResumeBuilder:
    def __init__(self):
        self.setup_nltk()
        self.skill_database = self.load_skill_database()
        self.templates = self.load_templates()
    
    def setup_nltk(self):
        """Setup NLTK resources"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def load_skill_database(self) -> Dict[str, List[str]]:
        """Load skill database"""
        return {
            'Programming': ['Python', 'Java', 'JavaScript', 'C++', 'SQL', 'R', 'Go', 'Rust', 'TypeScript'],
            'Web Development': ['HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring'],
            'Data Science': ['Pandas', 'NumPy', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Tableau', 'Power BI'],
            'Cloud & DevOps': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins'],
            'Databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'Cassandra'],
            'Soft Skills': ['Communication', 'Leadership', 'Teamwork', 'Problem-solving', 'Creativity', 'Time Management'],
            'Tools': ['Git', 'JIRA', 'Confluence', 'Slack', 'Figma', 'VS Code', 'Postman']
        }
    
    def load_templates(self) -> Dict[str, Dict]:
        """Load resume templates"""
        return {
            'Professional': {
                'style': 'modern',
                'sections': ['Contact', 'Summary', 'Experience', 'Education', 'Skills', 'Projects'],
                'colors': ['#2c3e50', '#3498db', '#ffffff']
            },
            'Modern': {
                'style': 'contemporary',
                'sections': ['Header', 'Profile', 'Work Experience', 'Education', 'Technical Skills', 'Certifications'],
                'colors': ['#1a5276', '#3498db', '#f8f9fa']
            },
            'Academic': {
                'style': 'formal',
                'sections': ['Personal Info', 'Academic Background', 'Research Experience', 'Publications', 'Skills', 'References'],
                'colors': ['#2c3e50', '#7f8c8d', '#ffffff']
            }
        }
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        found_skills = {}
        
        for category, skills in self.skill_database.items():
            category_skills = []
            for skill in skills:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text.lower()):
                    category_skills.append(skill)
            
            if category_skills:
                found_skills[category] = category_skills
        
        return found_skills
    
    def calculate_ats_score(self, resume_data: Dict) -> Dict[str, Any]:
        """Calculate ATS compatibility score"""
        score = 0
        feedback = []
        
        # Check for key sections
        required_sections = ['experience', 'education', 'skills']
        for section in required_sections:
            if resume_data.get(section):
                score += 20
            else:
                feedback.append(f"Missing {section} section")
        
        # Check for keywords
        if resume_data.get('skills'):
            skill_count = len(resume_data['skills'].split(',')) if isinstance(resume_data['skills'], str) else len(resume_data['skills'])
            score += min(skill_count * 2, 30)
        
        # Check for quantifiable achievements
        if resume_data.get('experience'):
            if any(word in resume_data['experience'].lower() for word in ['increased', 'reduced', 'improved', 'achieved', 'developed']):
                score += 20
                feedback.append("✅ Good use of action verbs and quantifiable results")
            else:
                feedback.append("⚠️ Add more quantifiable achievements")
        
        # Format check
        if len(resume_data.get('summary', '')) > 50 and len(resume_data.get('summary', '')) < 200:
            score += 10
        else:
            feedback.append("⚠️ Summary should be 50-200 characters")
        
        return {
            'score': min(score, 100),
            'feedback': feedback,
            'level': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs Improvement'
        }
    
    def generate_resume_text(self, user_data: Dict, template: str = 'Professional') -> str:
        """Generate resume text based on template"""
        template_config = self.templates.get(template, self.templates['Professional'])
        
        resume = f"""
        # {user_data.get('name', 'Your Name')}
        
        ## Contact Information
        📧 {user_data.get('email', 'email@example.com')}
        📱 {user_data.get('phone', '+91 XXXXXXXXXX')}
        📍 {user_data.get('location', 'City, Country')}
        🔗 {user_data.get('linkedin', 'linkedin.com/in/username')}
        
        ## Professional Summary
        {user_data.get('summary', 'Experienced professional seeking new opportunities.')}
        
        ## Work Experience
        {user_data.get('experience', 'Add your work experience here.')}
        
        ## Education
        {user_data.get('education', 'Add your education details here.')}
        
        ## Skills
        {user_data.get('skills', 'Add your skills here.')}
        
        ## Projects
        {user_data.get('projects', 'Add your projects here.')}
        
        ## Certifications
        {user_data.get('certifications', 'Add your certifications here.')}
        """
        
        return resume
    
    def analyze_job_fit(self, resume_data: Dict, job_description: str) -> Dict:
        """Analyze fit between resume and job description"""
        resume_skills = self.extract_skills(json.dumps(resume_data))
        job_skills = self.extract_skills(job_description)
        
        # Calculate match score
        matched_skills = []
        missing_skills = []
        
        for category, skills in job_skills.items():
            for skill in skills:
                if skill in resume_skills.get(category, []):
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)
        
        match_score = len(matched_skills) / (len(matched_skills) + len(missing_skills)) * 100 if (len(matched_skills) + len(missing_skills)) > 0 else 0
        
        return {
            'match_score': round(match_score, 1),
            'matched_skills': matched_skills[:10],
            'missing_skills': missing_skills[:10],
            'suggestions': [
                f"Add these skills: {', '.join(missing_skills[:5])}" if missing_skills else "Good skill match!",
                "Use more quantifiable achievements",
                "Tailor your summary to the job role"
            ]
        }

def show_resume_builder():
    st.title("🤖 AI Resume Builder")
    
    # Initialize builder
    builder = ResumeBuilder()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Build Resume", "🎯 ATS Analysis", "🔍 Job Match", "📊 Templates"])
    
    with tab1:
        st.subheader("Create Your Resume")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")
            linkedin = st.text_input("LinkedIn Profile")
            location = st.text_input("Location")
        
        with col2:
            target_role = st.text_input("Target Role*")
            years_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=0)
            current_role = st.text_input("Current Role")
            education_level = st.selectbox("Highest Education", 
                                         ["Select", "High School", "Bachelor's", "Master's", "PhD"])
        
        # Professional Summary
        st.subheader("Professional Summary")
        summary = st.text_area("Write a brief professional summary (2-3 sentences)", 
                              height=100,
                              placeholder="Experienced software developer with 5+ years in full-stack development...")
        
        # Skills
        st.subheader("Skills")
        skills_input = st.text_area("Enter your skills (comma-separated)",
                                   height=100,
                                   placeholder="Python, Machine Learning, SQL, React, AWS, Communication...")
        
        # Experience
        st.subheader("Work Experience")
        experience = st.text_area("Describe your work experience",
                                 height=150,
                                 placeholder="• Developed and maintained web applications using React and Node.js\n• Led a team of 5 developers...")
        
        # Education
        st.subheader("Education")
        education = st.text_area("Education details",
                                height=100,
                                placeholder="Bachelor of Technology in Computer Science\nUniversity Name, Year\nGPA: 3.8/4.0")
        
        # Generate Resume Button
        if st.button("✨ Generate AI-Optimized Resume", type="primary", use_container_width=True):
            if name and email and target_role:
                with st.spinner("Building your resume..."):
                    # Prepare data
                    user_data = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'linkedin': linkedin,
                        'location': location,
                        'target_role': target_role,
                        'summary': summary,
                        'skills': skills_input,
                        'experience': experience,
                        'education': education,
                        'years_experience': years_experience
                    }
                    
                    # Calculate ATS score
                    ats_result = builder.calculate_ats_score(user_data)
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ATS Score", f"{ats_result['score']}/100")
                    with col2:
                        st.metric("Skill Count", len(skills_input.split(',')) if skills_input else 0)
                    with col3:
                        st.metric("Experience Level", 
                                 f"{'Entry' if years_experience < 3 else 'Mid' if years_experience < 7 else 'Senior'}")
                    
                    # Show feedback
                    with st.expander("📋 AI Feedback & Suggestions", expanded=True):
                        for fb in ats_result['feedback']:
                            if fb.startswith('✅'):
                                st.success(fb)
                            elif fb.startswith('⚠️'):
                                st.warning(fb)
                            else:
                                st.info(fb)
                    
                    # Generate and display resume
                    st.subheader("📄 Generated Resume Preview")
                    resume_text = builder.generate_resume_text(user_data)
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.text_area("Resume Content", resume_text, height=400)
                    
                    with col2:
                        st.download_button(
                            "📥 Download as PDF",
                            data=resume_text,
                            file_name=f"{name.replace(' ', '_')}_Resume.txt",
                            mime="text/plain"
                        )
                        
                        st.download_button(
                            "📝 Download as JSON",
                            data=json.dumps(user_data, indent=2),
                            file_name=f"{name.replace(' ', '_')}_Resume.json",
                            mime="application/json"
                        )
                        
                        # Share options
                        st.button("📤 Share with Career Center", use_container_width=True)
                        st.button("🎯 Match with Jobs", use_container_width=True)
            else:
                st.error("Please fill all required fields (marked with *)")
    
    with tab2:
        st.subheader("📊 ATS Compatibility Analysis")
        
        # Upload or paste resume
        analysis_option = st.radio("Choose analysis method:", 
                                  ["Paste Resume Text", "Upload Resume File"])
        
        if analysis_option == "Paste Resume Text":
            resume_text = st.text_area("Paste your resume content:", height=200)
        else:
            uploaded_file = st.file_uploader("Upload resume (TXT or PDF)", type=['txt', 'pdf'])
            if uploaded_file:
                resume_text = uploaded_file.read().decode('utf-8')
        
        if st.button("Analyze ATS Compatibility", use_container_width=True) and resume_text:
            # Extract skills
            skills = builder.extract_skills(resume_text)
            
            # Calculate scores
            score_data = builder.calculate_ats_score({'skills': resume_text, 'experience': resume_text})
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall ATS Score", f"{score_data['score']}/100", score_data['level'])
                
                # Skill categories
                st.subheader("🛠️ Detected Skills")
                for category, skill_list in skills.items():
                    with st.expander(f"{category} ({len(skill_list)})"):
                        st.write(", ".join(skill_list))
            
            with col2:
                # Visualization
                import plotly.graph_objects as go
                
                categories = ['Format', 'Keywords', 'Experience', 'Education', 'Customization']
                scores = [85, 78, 92, 88, 75]  # Example scores
                
                fig = go.Figure(data=[
                    go.Bar(x=categories, y=scores, marker_color='lightblue')
                ])
                
                fig.update_layout(
                    title="Score by Category",
                    yaxis=dict(range=[0, 100]),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Improvement suggestions
            st.subheader("💡 Improvement Suggestions")
            
            suggestions = [
                "✅ Use standard section headers (Experience, Education, Skills)",
                "⚠️ Add more quantifiable achievements (increased X by Y%)",
                "✅ Include relevant keywords from job descriptions",
                "⚠️ Keep resume length to 1-2 pages",
                "✅ Use bullet points for readability",
                "⚠️ Remove personal pronouns (I, me, my)"
            ]
            
            for suggestion in suggestions:
                st.write(suggestion)
    
    with tab3:
        st.subheader("🔍 Job Description Matching")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Your Resume**")
            resume_for_match = st.text_area("Paste your resume content", height=150)
        
        with col2:
            st.write("**Target Job Description**")
            job_description = st.text_area("Paste the job description", height=150)
        
        if st.button("Analyze Job Fit", use_container_width=True) and resume_for_match and job_description:
            with st.spinner("Analyzing fit..."):
                # Prepare data
                resume_data = {'skills': resume_for_match, 'experience': resume_for_match}
                
                # Analyze fit
                fit_result = builder.analyze_job_fit(resume_data, job_description)
                
                # Display results
                st.subheader("🎯 Match Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Match Score", f"{fit_result['match_score']}%")
                
                with col2:
                    st.metric("Skills Matched", len(fit_result['matched_skills']))
                
                with col3:
                    st.metric("Skills Missing", len(fit_result['missing_skills']))
                
                # Show matched skills
                st.subheader("✅ Skills You Have")
                if fit_result['matched_skills']:
                    cols = st.columns(4)
                    for idx, skill in enumerate(fit_result['matched_skills']):
                        with cols[idx % 4]:
                            st.success(f"✓ {skill}")
                else:
                    st.info("No matching skills detected")
                
                # Show missing skills
                st.subheader("⚠️ Skills to Develop")
                if fit_result['missing_skills']:
                    cols = st.columns(4)
                    for idx, skill in enumerate(fit_result['missing_skills']):
                        with cols[idx % 4]:
                            st.warning(f"📚 {skill}")
                else:
                    st.success("Great! You have all the required skills")
                
                # Suggestions
                st.subheader("🎯 Customized Recommendations")
                for suggestion in fit_result['suggestions']:
                    st.info(suggestion)
    
    with tab4:
        st.subheader("🎨 Resume Templates")
        
        templates = [
            {"name": "Professional", "desc": "Clean, corporate style", "best_for": "Corporate jobs, consulting"},
            {"name": "Modern", "desc": "Contemporary design", "best_for": "Tech, startups, creative roles"},
            {"name": "Academic", "desc": "Formal, detailed", "best_for": "Research, academia, PhD applications"},
            {"name": "Creative", "desc": "Design-focused", "best_for": "Design, marketing, creative fields"},
            {"name": "Minimalist", "desc": "Simple and elegant", "best_for": "All industries, ATS-friendly"},
            {"name": "Executive", "desc": "Leadership-focused", "best_for": "Senior roles, management positions"}
        ]
        
        cols = st.columns(3)
        for idx, template in enumerate(templates):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"### {template['name']}")
                    st.write(template['desc'])
                    st.caption(f"Best for: {template['best_for']}")
                    
                    if st.button(f"Use {template['name']}", key=f"template_{idx}", use_container_width=True):
                        st.session_state.selected_template = template['name']
                        st.success(f"Selected {template['name']} template!")
                        st.rerun()
        
        # Template customization
        if 'selected_template' in st.session_state:
            st.divider()
            st.subheader(f"Customize {st.session_state.selected_template} Template")
            
            col1, col2 = st.columns(2)
            
            with col1:
                primary_color = st.color_picker("Primary Color", "#2c3e50")
                secondary_color = st.color_picker("Secondary Color", "#3498db")
                font_family = st.selectbox("Font Family", ["Arial", "Calibri", "Times New Roman", "Helvetica", "Georgia"])
            
            with col2:
                font_size = st.slider("Font Size", 10, 16, 12)
                spacing = st.slider("Line Spacing", 1.0, 2.0, 1.5)
                columns = st.radio("Layout", ["Single Column", "Two Columns"])
            
            # Preview
            st.subheader("Template Preview")
            with st.container(border=True):
                st.markdown(f"""
                <div style="font-family: {font_family}; font-size: {font_size}px; line-height: {spacing};">
                <h2 style="color: {primary_color};">John Doe</h2>
                <p style="color: {secondary_color};">Software Developer</p>
                <p>📧 john.doe@email.com | 📱 +1 (123) 456-7890</p>
                <hr>
                <h3 style="color: {primary_color};">Professional Summary</h3>
                <p>Experienced software developer with 5+ years in full-stack development...</p>
                </div>
                """, unsafe_allow_html=True)
