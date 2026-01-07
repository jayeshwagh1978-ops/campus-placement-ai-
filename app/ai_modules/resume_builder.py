import streamlit as st
import pandas as pd
import json
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import os

class AIResumeBuilder:
    def __init__(self):
        self.setup_ai_models()
        
    def setup_ai_models(self):
        """Initialize AI models for resume building"""
        # Initialize OpenAI
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Initialize prompt templates
        self.resume_prompt = PromptTemplate(
            input_variables=["skills", "experience", "education", "target_role"],
            template="""
            Create an ATS-optimized resume for a {target_role} position.
            
            Skills: {skills}
            Experience: {experience}
            Education: {education}
            
            Format the resume with:
            1. Professional Summary tailored for the role
            2. Skills categorized by relevance
            3. Experience bullets with quantifiable achievements
            4. Education highlighting relevant coursework
            5. Keywords for ATS optimization
            6. Action verbs for impact
            
            Return in JSON format with sections.
            """
        )
    
    def analyze_resume_gap(self, current_resume, target_job_description):
        """Analyze gap between current resume and target job"""
        gap_prompt = f"""
        Compare current resume with target job description:
        
        Current Resume: {current_resume}
        Target Job: {target_job_description}
        
        Identify:
        1. Missing skills
        2. Experience gaps
        3. Keywords to add
        4. Suggested improvements
        5. ATS optimization tips
        
        Return analysis in structured format.
        """
        
        response = self.gemini_model.generate_content(gap_prompt)
        return response.text
    
    def generate_resume_sections(self, user_data):
        """Generate optimized resume sections"""
        sections = {
            "summary": self.generate_summary(user_data),
            "skills": self.categorize_skills(user_data['skills']),
            "experience": self.enhance_experience(user_data['experience']),
            "education": self.format_education(user_data['education']),
            "ats_score": self.calculate_ats_score(user_data)
        }
        return sections
    
    def calculate_ats_score(self, resume_data):
        """Calculate ATS compatibility score"""
        # Implement ATS scoring logic
        score = 85  # Placeholder
        feedback = [
            "✅ Strong keyword matching",
            "⚠️ Add more quantifiable achievements",
            "✅ Good section structure",
            "⚠️ Improve skills categorization"
        ]
        return {"score": score, "feedback": feedback}

def show_resume_builder():
    st.title("🤖 AI Resume Builder")
    
    with st.expander("📝 Enter Your Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            target_role = st.text_input("Target Role")
            
        with col2:
            current_role = st.text_input("Current Role")
            years_experience = st.number_input("Years of Experience", min_value=0, max_value=50)
            education_level = st.selectbox(
                "Education Level",
                ["High School", "Bachelor's", "Master's", "PhD", "Diploma"]
            )
        
        # Skills input
        st.subheader("Skills")
        skills = st.text_area(
            "Enter your skills (comma-separated)",
            placeholder="Python, Machine Learning, SQL, Communication, Team Leadership"
        )
        
        # Experience input
        st.subheader("Experience")
        experience = st.text_area(
            "Describe your experience",
            placeholder="Work experience, projects, internships..."
        )
        
        # Education details
        st.subheader("Education")
        education = st.text_area(
            "Education details",
            placeholder="Degree, University, Year, GPA, Relevant coursework..."
        )
        
        # Target job description
        st.subheader("Target Job Description")
        job_description = st.text_area(
            "Paste the job description",
            height=200
        )
    
    # Resume templates
    st.subheader("🎨 Choose Template")
    template_cols = st.columns(4)
    templates = ["Professional", "Modern", "Creative", "Minimalist"]
    
    with template_cols[0]:
        if st.button("Professional", use_container_width=True):
            st.session_state.selected_template = "professional"
    with template_cols[1]:
        if st.button("Modern", use_container_width=True):
            st.session_state.selected_template = "modern"
    with template_cols[2]:
        if st.button("Creative", use_container_width=True):
            st.session_state.selected_template = "creative"
    with template_cols[3]:
        if st.button("Minimalist", use_container_width=True):
            st.session_state.selected_template = "minimalist"
    
    # Generate Resume button
    if st.button("✨ Generate AI-Optimized Resume", type="primary", use_container_width=True):
        if all([name, skills, experience, education]):
            with st.spinner("Analyzing and optimizing your resume..."):
                builder = AIResumeBuilder()
                
                # Prepare data
                user_data = {
                    "name": name,
                    "skills": skills,
                    "experience": experience,
                    "education": education,
                    "target_role": target_role
                }
                
                # Generate resume
                resume_sections = builder.generate_resume_sections(user_data)
                
                # Display results
                st.success("✅ Resume generated successfully!")
                
                # Show ATS Score
                st.metric("ATS Compatibility Score", 
                         f"{resume_sections['ats_score']['score']}/100")
                
                # Show sections
                tabs = st.tabs(["Summary", "Skills", "Experience", "Education", "Feedback"])
                
                with tabs[0]:
                    st.write(resume_sections['summary'])
                
                with tabs[1]:
                    st.json(resume_sections['skills'])
                
                with tabs[2]:
                    st.write(resume_sections['experience'])
                
                with tabs[3]:
                    st.write(resume_sections['education'])
                
                with tabs[4]:
                    for feedback in resume_sections['ats_score']['feedback']:
                        st.write(feedback)
                
                # Download options
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📄 Download PDF",
                        data=json.dumps(resume_sections),
                        file_name="resume.json",
                        mime="application/json"
                    )
                with col2:
                    st.download_button(
                        "📝 Download Word",
                        data=json.dumps(resume_sections),
                        file_name="resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                with col3:
                    st.button("🔄 One-Click Apply", use_container_width=True)
        
        else:
            st.error("Please fill all required fields")
