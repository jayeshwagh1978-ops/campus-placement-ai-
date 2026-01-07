import streamlit as st
import pandas as pd
import numpy as np
import re
import json
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px

class JobParser:
    def __init__(self):
        self.skill_database = self.load_skill_database()
        self.job_templates = self.load_job_templates()
    
    def load_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skill database"""
        return {
            "programming": ["Python", "Java", "JavaScript", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "TypeScript"],
            "web_dev": ["HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "Spring"],
            "mobile": ["React Native", "Flutter", "Android", "iOS", "Xamarin"],
            "databases": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Oracle", "SQLite"],
            "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "CI/CD"],
            "data_science": ["Python", "R", "SQL", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Tableau", "Power BI"],
            "ai_ml": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Reinforcement Learning", "MLOps"],
            "devops": ["Linux", "Bash", "Git", "Docker", "Kubernetes", "AWS", "Azure", "Jenkins", "Terraform"],
            "soft_skills": ["Communication", "Leadership", "Teamwork", "Problem-solving", "Critical Thinking", "Time Management"],
            "tools": ["Git", "JIRA", "Confluence", "Slack", "Figma", "VS Code", "IntelliJ", "Postman"]
        }
    
    def load_job_templates(self) -> Dict[str, Dict]:
        """Load job description templates"""
        return {
            "Software Engineer": {
                "required_skills": ["Python", "Java", "SQL", "Git", "Problem-solving"],
                "experience": "2+ years",
                "responsibilities": [
                    "Design, develop and maintain software applications",
                    "Write clean, efficient, and well-documented code",
                    "Collaborate with cross-functional teams",
                    "Participate in code reviews"
                ]
            },
            "Data Scientist": {
                "required_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
                "experience": "3+ years",
                "responsibilities": [
                    "Analyze large datasets to extract insights",
                    "Build and deploy machine learning models",
                    "Create data visualizations and reports",
                    "Collaborate with business teams"
                ]
            },
            "DevOps Engineer": {
                "required_skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux"],
                "experience": "2+ years",
                "responsibilities": [
                    "Design and implement CI/CD pipelines",
                    "Manage cloud infrastructure",
                    "Ensure system reliability and scalability",
                    "Implement monitoring and logging"
                ]
            }
        }
    
    def parse_job_description(self, job_text: str) -> Dict[str, Any]:
        """Parse job description and extract key information"""
        extracted = {
            "skills": self.extract_skills(job_text),
            "experience": self.extract_experience(job_text),
            "education": self.extract_education(job_text),
            "responsibilities": self.extract_responsibilities(job_text),
            "requirements": self.extract_requirements(job_text),
            "job_title": self.extract_job_title(job_text),
            "location": self.extract_location(job_text),
            "salary": self.extract_salary(job_text),
            "company": self.extract_company(job_text)
        }
        
        # Calculate job complexity
        extracted["complexity_score"] = self.calculate_complexity(extracted)
        
        # Generate ATS keywords
        extracted["ats_keywords"] = self.generate_ats_keywords(extracted)
        
        return extracted
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        found_skills = {}
        text_lower = text.lower()
        
        for category, skills in self.skill_database.items():
            category_skills = []
            for skill in skills:
                skill_lower = skill.lower()
                # Check for skill mentions
                if re.search(r'\b' + re.escape(skill_lower) + r'\b', text_lower):
                    category_skills.append(skill)
            
            if category_skills:
                found_skills[category] = category_skills
        
        return found_skills
    
    def extract_experience(self, text: str) -> List[str]:
        """Extract experience requirements"""
        patterns = [
            r'(\d+\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience)',
            r'experience\s*(?:of)?\s*(\d+\+?\s*(?:years?|yrs?))',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)\s*experience'
        ]
        
        experience = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                experience.append(match.group())
        
        return list(set(experience))  # Remove duplicates
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education requirements"""
        education_keywords = [
            'bachelor', 'b\.?tech', 'b\.?e', 'b\.?sc',
            'master', 'm\.?tech', 'm\.?e', 'm\.?sc', 'mba',
            'phd', 'doctorate', 'degree', 'diploma',
            'graduat', 'qualif', 'certif'
        ]
        
        sentences = re.split(r'[.!?]+', text)
        education_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in education_keywords):
                education_sentences.append(sentence.strip())
        
        return education_sentences[:5]  # Return top 5
    
    def extract_responsibilities(self, text: str) -> List[str]:
        """Extract responsibilities"""
        responsibility_keywords = [
            'responsible', 'responsibilit', 'duties', 'role',
            'will', 'must', 'should', 'requires to'
        ]
        
        sentences = re.split(r'[.!?]+', text)
        responsibilities = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in responsibility_keywords):
                # Clean the sentence
                clean_sentence = ' '.join(sentence.split())
                if len(clean_sentence.split()) > 4:  # Avoid very short sentences
                    responsibilities.append(clean_sentence)
        
        return responsibilities[:10]
    
    def extract_requirements(self, text: str) -> List[str]:
        """Extract requirements"""
        requirement_keywords = [
            'requirement', 'required', 'must have', 'should have',
            'need to have', 'essential', 'preferred', 'qualif'
        ]
        
        sentences = re.split(r'[.!?]+', text)
        requirements = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in requirement_keywords):
                requirements.append(sentence.strip())
        
        return requirements[:10]
    
    def extract_job_title(self, text: str) -> str:
        """Extract job title"""
        # Look for common patterns
        patterns = [
            r'(?:position|role|job)\s*(?:of)?\s*([A-Z][a-zA-Z\s&]+)(?:\s+(?:position|role|job))?',
            r'([A-Z][a-zA-Z\s&]+)\s*(?:position|role|job|opening)',
            r'we are hiring\s*([A-Z][a-zA-Z\s&]+)',
            r'looking for\s*([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not Specified"
    
    def extract_location(self, text: str) -> str:
        """Extract job location"""
        location_patterns = [
            r'location[:\s]+([A-Z][a-zA-Z\s,]+)',
            r'based in\s+([A-Z][a-zA-Z\s,]+)',
            r'work from\s+([A-Z][a-zA-Z\s,]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not Specified"
    
    def extract_salary(self, text: str) -> Dict[str, str]:
        """Extract salary information"""
        salary_patterns = [
            r'salary[:\s]+([$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?\s*(?:-|\s+to\s+)\s*[$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?)',
            r'compensation[:\s]+([$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?\s*(?:-|\s+to\s+)\s*[$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?)',
            r'pay[:\s]+([$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?\s*(?:-|\s+to\s+)\s*[$₹€]?\s*\d+[,\d]*(?:\.\d+)?\s*[kK]?)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return {"range": match.group(1)}
        
        return {"range": "Not Specified"}
    
    def extract_company(self, text: str) -> str:
        """Extract company name"""
        # Simple extraction - in reality would use more sophisticated methods
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            if line.strip() and len(line.strip().split()) <= 5:
                return line.strip()
        
        return "Not Specified"
    
    def calculate_complexity(self, extracted_data: Dict) -> int:
        """Calculate job complexity score"""
        score = 0
        
        # Based on number of skill categories
        score += len(extracted_data.get('skills', {})) * 5
        
        # Based on experience requirements
        if extracted_data.get('experience'):
            score += 20
        
        # Based on education requirements
        if extracted_data.get('education'):
            score += 15
        
        # Based on number of responsibilities
        score += min(len(extracted_data.get('responsibilities', [])) * 3, 15)
        
        # Based on number of requirements
        score += min(len(extracted_data.get('requirements', [])) * 2, 10)
        
        return min(score, 100)
    
    def generate_ats_keywords(self, extracted_data: Dict) -> List[str]:
        """Generate ATS optimization keywords"""
        keywords = []
        
        # Add skills
        for category, skills in extracted_data.get('skills', {}).items():
            keywords.extend(skills)
        
        # Add common ATS keywords
        common_keywords = [
            "team player", "problem solver", "detail oriented",
            "fast learner", "excellent communication", "leadership",
            "project management", "results driven", "self motivated",
            "critical thinking", "analytical skills", "creative",
            "adaptable", "reliable", "professional"
        ]
        
        keywords.extend(common_keywords)
        
        # Remove duplicates and limit to top 20
        unique_keywords = list(set(keywords))
        return unique_keywords[:20]
    
    def generate_optimized_jd(self, parsed_data: Dict, template: str = "standard") -> str:
        """Generate optimized job description"""
        job_title = parsed_data.get('job_title', 'Position')
        skills = parsed_data.get('skills', {})
        
        # Flatten skills
        all_skills = []
        for category_skills in skills.values():
            all_skills.extend(category_skills)
        
        optimized = f"""
        {job_title}
        
        🌟 **About the Role:**
        We are looking for a talented {job_title} to join our dynamic team. 
        This is an exciting opportunity to work on cutting-edge projects and 
        make a significant impact.
        
        🔧 **Key Responsibilities:**
        """
        
        # Add responsibilities
        for resp in parsed_data.get('responsibilities', [])[:5]:
            optimized += f"• {resp}\n"
        
        optimized += f"""
        🎓 **Requirements:**
        • {parsed_data.get('experience', ['Experience in relevant field'])[0]}
        • Relevant educational background
        • Strong skills in: {', '.join(all_skills[:8])}
        • Excellent problem-solving abilities
        • Good communication skills
        
        💼 **What We Offer:**
        • Competitive salary package
        • Comprehensive health benefits
        • Professional development opportunities
        • Flexible work arrangements
        • Collaborative work environment
        
        📍 **Location:** {parsed_data.get('location', 'Multiple locations available')}
        
        📅 **Apply by:** {pd.Timestamp.now() + pd.Timedelta(days=30):%Y-%m-%d}
        """
        
        return optimized

def show_job_parser():
    st.title("🔍 AI Job Description Parser")
    
    # Initialize parser
    parser = JobParser()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Parse JD", "🎯 Optimize JD", "📊 Analytics"])
    
    with tab1:
        st.subheader("Parse Job Description")
        
        # Input methods
        input_method = st.radio(
            "Input Method",
            ["Paste Text", "Upload File", "Use Template"]
        )
        
        job_text = ""
        
        if input_method == "Paste Text":
            job_text = st.text_area(
                "Paste Job Description",
                height=300,
                placeholder="Paste the complete job description here..."
            )
        
        elif input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload Job Description",
                type=['txt', 'pdf', 'docx'],
                help="Upload .txt, .pdf, or .docx file"
            )
            
            if uploaded_file:
                if uploaded_file.name.endswith('.txt'):
                    job_text = uploaded_file.read().decode('utf-8')
                else:
                    st.info("PDF/DOCX processing would be implemented here")
                    job_text = "Sample job description content for demonstration"
        
        elif input_method == "Use Template":
            template = st.selectbox(
                "Select Template",
                list(parser.job_templates.keys())
            )
            
            if template:
                template_data = parser.job_templates[template]
                
                st.write("**Template Preview:**")
                st.write(f"**Role:** {template}")
                st.write(f"**Experience:** {template_data['experience']}")
                st.write("**Key Skills:**")
                for skill in template_data['required_skills']:
                    st.write(f"- {skill}")
                
                if st.button("Use This Template", use_container_width=True):
                    job_text = f"""
                    {template}
                    
                    We are looking for an experienced {template} to join our team.
                    
                    Responsibilities:
                    {' '.join(template_data['responsibilities'])}
                    
                    Requirements:
                    • {template_data['experience']} of experience
                    • Strong skills in {', '.join(template_data['required_skills'][:3])}
                    """
        
        # Parse button
        if st.button("🔍 Parse Job Description", type="primary", use_container_width=True) and job_text:
            with st.spinner("Analyzing job description..."):
                # Parse the job description
                parsed_data = parser.parse_job_description(job_text)
                
                # Display results
                st.success("✅ Job description parsed successfully!")
                
                # Overview
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Job Title", parsed_data.get('job_title', 'N/A'))
                
                with col2:
                    st.metric("Complexity Score", f"{parsed_data.get('complexity_score', 0)}/100")
                
                with col3:
                    skill_categories = len(parsed_data.get('skills', {}))
                    st.metric("Skill Categories", skill_categories)
                
                # Detailed analysis
                st.subheader("📋 Extracted Information")
                
                # Skills breakdown
                if parsed_data.get('skills'):
                    st.write("**🛠️ Skills Identified:**")
                    
                    for category, skills in parsed_data['skills'].items():
                        with st.expander(f"{category} ({len(skills)} skills)"):
                            cols = st.columns(3)
                            for idx, skill in enumerate(skills):
                                with cols[idx % 3]:
                                    st.info(f"• {skill}")
                
                # Requirements
                if parsed_data.get('requirements'):
                    st.write("**📝 Requirements:**")
                    for req in parsed_data['requirements'][:5]:
                        st.write(f"- {req}")
                
                # Experience & Education
                col1, col2 = st.columns(2)
                
                with col1:
                    if parsed_data.get('experience'):
                        st.write("**📅 Experience Required:**")
                        for exp in parsed_data['experience']:
                            st.info(f"• {exp}")
                
                with col2:
                    if parsed_data.get('education'):
                        st.write("**🎓 Education Requirements:**")
                        for edu in parsed_data['education'][:3]:
                            st.info(f"• {edu}")
                
                # ATS Keywords
                if parsed_data.get('ats_keywords'):
                    st.write("**🎯 ATS Optimization Keywords:**")
                    
                    # Display as tags
                    keyword_cols = st.columns(4)
                    for idx, keyword in enumerate(parsed_data['ats_keywords'][:16]):
                        with keyword_cols[idx % 4]:
                            st.markdown(f"`{keyword}`")
    
    with tab2:
        st.subheader("Optimize Job Description")
        
        st.info("""
        Generate an ATS-optimized, engaging job description that attracts top talent.
        """)
        
        # Job details form
        with st.form("optimize_jd"):
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input("Job Title*", "Software Engineer")
                department = st.selectbox("Department", ["Engineering", "Product", "Design", "Marketing", "Sales", "Operations"])
                experience = st.selectbox("Experience Level", ["Entry Level", "1-3 years", "3-5 years", "5-8 years", "8+ years"])
                location = st.text_input("Location", "Bangalore, India")
            
            with col2:
                employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Internship", "Remote"])
                salary_range = st.text_input("Salary Range", "₹10-20 LPA")
                application_deadline = st.date_input("Application Deadline")
            
            # Skills selection
            st.subheader("Required Skills")
            
            skill_categories = st.multiselect(
                "Select Skill Categories",
                list(parser.skill_database.keys()),
                default=["programming", "web_dev", "databases"]
            )
            
            selected_skills = []
            for category in skill_categories:
                skills = st.multiselect(
                    f"{category.replace('_', ' ').title()} Skills",
                    parser.skill_database[category],
                    default=parser.skill_database[category][:2]
                )
                selected_skills.extend(skills)
            
            # Responsibilities
            st.subheader("Key Responsibilities")
            responsibilities = []
            
            for i in range(5):
                resp = st.text_input(f"Responsibility {i+1}", 
                                   key=f"resp_{i}",
                                   placeholder="e.g., Design and develop scalable software solutions")
                if resp:
                    responsibilities.append(resp)
            
            # Submit button
            submitted = st.form_submit_button("✨ Generate Optimized JD", type="primary")
        
        if submitted:
            if job_title and selected_skills:
                with st.spinner("Generating optimized job description..."):
                    # Prepare data
                    job_data = {
                        'job_title': job_title,
                        'skills': {'custom': selected_skills},
                        'experience': [experience],
                        'location': location,
                        'responsibilities': responsibilities
                    }
                    
                    # Generate optimized JD
                    optimized_jd = parser.generate_optimized_jd(job_data)
                    
                    # Display result
                    st.success("✅ Optimized job description generated!")
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.text_area("Optimized Job Description", optimized_jd, height=400)
                    
                    with col2:
                        st.download_button(
                            "📥 Download as TXT",
                            data=optimized_jd,
                            file_name=f"{job_title.replace(' ', '_')}_JD.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                        
                        st.download_button(
                            "📄 Download as PDF",
                            data=optimized_jd,
                            file_name=f"{job_title.replace(' ', '_')}_JD.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.button("📤 Post to Job Portals", use_container_width=True)
                        
                        # ATS Score
                        ats_score = min(85 + len(selected_skills) * 2, 100)
                        st.metric("ATS Score", f"{ats_score}/100")
            else:
                st.error("Please fill required fields (Job Title and Skills)")
    
    with tab3:
        st.subheader("Job Market Analytics")
        
        # Generate sample data
        np.random.seed(42)
        
        # Skill demand analysis
        skills = ['Python', 'Java', 'JavaScript', 'React', 'AWS', 'Docker', 'SQL', 'Machine Learning']
        demand = np.random.randint(50, 100, len(skills))
        salary_impact = np.random.uniform(1.1, 2.0, len(skills))
        
        skill_data = pd.DataFrame({
            'Skill': skills,
            'Demand Score': demand,
            'Salary Impact': salary_impact
        })
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(skill_data, x='Skill', y='Demand Score',
                        title='Skill Demand in Market',
                        color='Demand Score',
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(skill_data, x='Demand Score', y='Salary Impact',
                            size='Demand Score', color='Skill',
                            title='Demand vs Salary Impact',
                            size_max=40)
            st.plotly_chart(fig, use_container_width=True)
        
        # Location analysis
        st.subheader("📍 Location-wise Analysis")
        
        locations = ['Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Delhi', 'Mumbai']
        openings = np.random.randint(100, 500, len(locations))
        avg_salary = np.random.uniform(8.0, 15.0, len(locations))
        
        location_data = pd.DataFrame({
            'Location': locations,
            'Job Openings': openings,
            'Avg Salary (LPA)': avg_salary
        })
        
        fig = px.scatter(location_data, x='Job Openings', y='Avg Salary (LPA)',
                        size='Job Openings', color='Location',
                        title='Location-wise Job Market',
                        size_max=40)
        st.plotly_chart(fig, use_container_width=True)
        
        # Trends over time
        st.subheader("📈 Market Trends")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        tech_openings = np.random.randint(1000, 2000, len(months))
        non_tech_openings = np.random.randint(500, 1500, len(months))
        
        trend_data = pd.DataFrame({
            'Month': months,
            'Tech Jobs': tech_openings,
            'Non-Tech Jobs': non_tech_openings
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=tech_openings,
            mode='lines+markers',
            name='Tech Jobs',
            line=dict(color='blue', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=months, y=non_tech_openings,
            mode='lines+markers',
            name='Non-Tech Jobs',
            line=dict(color='green', width=3)
        ))
        
        fig.update_layout(
            title='Monthly Job Openings Trend',
            xaxis_title='Month',
            yaxis_title='Number of Openings',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
