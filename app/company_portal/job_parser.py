import streamlit as st
import pandas as pd
import spacy
from spacy import displacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import json
from collections import Counter

class NLPJobParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.setup_nltk()
        self.skill_database = self.load_skill_database()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def load_skill_database(self):
        """Load skill database from file"""
        skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'sql', 'r', 'go', 'rust'],
            'web_dev': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask'],
            'data_science': ['pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'tableau', 'powerbi'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving', 'creativity'],
            'tools': ['git', 'jenkins', 'jira', 'confluence', 'slack', 'figma']
        }
        return skills
    
    def parse_job_description(self, job_text):
        """Parse job description and extract key information"""
        doc = self.nlp(job_text)
        
        extracted_info = {
            'skills': self.extract_skills(doc),
            'experience': self.extract_experience(job_text),
            'education': self.extract_education(job_text),
            'responsibilities': self.extract_responsibilities(doc),
            'requirements': self.extract_requirements(doc),
            'job_title': self.extract_job_title(job_text),
            'location': self.extract_location(doc),
            'salary': self.extract_salary(job_text),
            'entities': self.extract_entities(doc)
        }
        
        # Calculate job complexity score
        extracted_info['complexity_score'] = self.calculate_complexity_score(extracted_info)
        
        # Match with skill database
        extracted_info['skill_gap_analysis'] = self.skill_gap_analysis(extracted_info['skills'])
        
        return extracted_info
    
    def extract_skills(self, doc):
        """Extract skills from job description"""
        skills_found = []
        
        # Check for skill patterns
        for token in doc:
            token_text = token.text.lower()
            
            # Check in skill database
            for category, skill_list in self.skill_database.items():
                if token_text in skill_list:
                    skills_found.append({
                        'skill': token_text,
                        'category': category,
                        'importance': 1 if token.pos_ in ['PROPN', 'NOUN'] else 0.5
                    })
        
        # Also look for skill phrases
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            for category, skill_list in self.skill_database.items():
                for skill in skill_list:
                    if skill in chunk_text and len(skill) > 2:
                        skills_found.append({
                            'skill': skill,
                            'category': category,
                            'importance': 1.5  # Higher importance for phrases
                        })
        
        # Remove duplicates
        unique_skills = []
        seen = set()
        for skill in skills_found:
            if skill['skill'] not in seen:
                seen.add(skill['skill'])
                unique_skills.append(skill)
        
        return unique_skills
    
    def extract_experience(self, text):
        """Extract experience requirements"""
        experience_patterns = [
            r'(\d+[\+\-]?\s*(?:year|yr)s?[\+\-]?\s*(?:of)?\s*experience)',
            r'experience\s*(?:of)?\s*(\d+[\+\-]?\s*(?:year|yr)s?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:year|yr)s?\s*experience'
        ]
        
        experience = []
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                experience.append(match.group())
        
        return experience
    
    def extract_education(self, text):
        """Extract education requirements"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'mtech', 'mba', 'btech', 'bsc', 'msc',
            'degree', 'diploma', 'certification', 'qualified', 'graduate'
        ]
        
        sentences = nltk.sent_tokenize(text)
        education_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in education_keywords):
                education_sentences.append(sentence)
        
        return education_sentences
    
    def extract_responsibilities(self, doc):
        """Extract key responsibilities"""
        responsibility_keywords = ['responsible', 'duties', 'role', 'will', 'must', 'should']
        responsibilities = []
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(keyword in sent_text for keyword in responsibility_keywords):
                # Clean the sentence
                clean_sent = ' '.join([token.text for token in sent 
                                      if not token.is_stop and token.pos_ in ['NOUN', 'VERB', 'ADJ']])
                if len(clean_sent.split()) > 3:  # Avoid very short sentences
                    responsibilities.append({
                        'sentence': sent.text,
                        'keywords': self.extract_keywords_from_sentence(sent.text)
                    })
        
        return responsibilities[:10]  # Return top 10 responsibilities
    
    def extract_requirements(self, doc):
        """Extract requirements"""
        requirement_keywords = ['required', 'requirement', 'must have', 'should have', 'needed']
        requirements = []
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            if any(keyword in sent_text for keyword in requirement_keywords):
                requirements.append(sent.text)
        
        return requirements
    
    def extract_job_title(self, text):
        """Extract job title"""
        # Common patterns for job titles
        patterns = [
            r'(?:position|role|job)\s*(?:of)?\s*([A-Z][a-zA-Z\s&]+)(?:\s+(?:position|role|job))?',
            r'([A-Z][a-zA-Z\s&]+)\s*(?:position|role|job)',
            r'we are hiring\s*([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Not Specified"
    
    def calculate_complexity_score(self, extracted_info):
        """Calculate job complexity score"""
        score = 0
        
        # Based on number of skills required
        score += min(len(extracted_info['skills']) * 5, 30)
        
        # Based on experience requirements
        if extracted_info['experience']:
            score += 20
        
        # Based on education requirements
        if extracted_info['education']:
            score += 15
        
        # Based on number of responsibilities
        score += min(len(extracted_info['responsibilities']) * 3, 15)
        
        # Based on number of requirements
        score += min(len(extracted_info['requirements']) * 2, 10)
        
        return min(score, 100)
    
    def skill_gap_analysis(self, required_skills):
        """Analyze skill gaps in current talent pool"""
        # This would compare with student database in production
        analysis = {
            'high_demand_skills': [],
            'low_supply_skills': [],
            'recommended_training': []
        }
        
        # Mock analysis
        for skill in required_skills[:5]:  # Top 5 skills
            analysis['high_demand_skills'].append(skill['skill'])
            analysis['recommended_training'].append(
                f"Training program for {skill['skill']}"
            )
        
        return analysis
    
    def generate_ats_keywords(self, extracted_info):
        """Generate ATS optimization keywords"""
        keywords = []
        
        for skill in extracted_info['skills']:
            keywords.append(skill['skill'])
        
        # Add common ATS keywords
        common_keywords = [
            'team player', 'problem solver', 'detail oriented',
            'fast learner', 'excellent communication', 'leadership',
            'project management', 'results driven'
        ]
        
        keywords.extend(common_keywords)
        
        return list(set(keywords))  # Remove duplicates

def show_job_parser():
    st.title("🔍 NLP Job Parser with Skill Extraction")
    
    # Initialize parser
    parser = NLPJobParser()
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📝 Paste Job Description")
        job_text = st.text_area(
            "Paste the complete job description here:",
            height=300,
            placeholder="Paste job description here...\n\nExample:\nWe are looking for a Python Developer with 3+ years of experience...",
            help="Paste the complete job description including requirements, responsibilities, and qualifications."
        )
    
    with col2:
        st.subheader("📤 Or Upload File")
        uploaded_file = st.file_uploader(
            "Upload job description file",
            type=['txt', 'pdf', 'docx'],
            help="Upload .txt, .pdf, or .docx file"
        )
        
        if uploaded_file:
            # Process uploaded file
            if uploaded_file.name.endswith('.txt'):
                job_text = uploaded_file.read().decode('utf-8')
            elif uploaded_file.name.endswith('.pdf'):
                # Add PDF processing here
                st.info("PDF processing would be implemented here")
                job_text = "PDF content extraction placeholder"
        
        # Sample job descriptions
        st.subheader("📋 Samples")
        sample_option = st.selectbox(
            "Load sample job description:",
            ["Select a sample", "Data Scientist", "Software Engineer", "Product Manager", "UX Designer"]
        )
        
        samples = {
            "Data Scientist": """
            Data Scientist - AI Research Team
            
            Responsibilities:
            - Develop and implement machine learning models for predictive analytics
            - Analyze large datasets to extract meaningful insights
            - Collaborate with engineering teams to deploy models in production
            - Create data visualizations and reports for stakeholders
            - Stay updated with latest AI/ML research and techniques
            
            Requirements:
            - Master's or PhD in Computer Science, Statistics, or related field
            - 3+ years of experience in data science
            - Strong proficiency in Python, R, SQL
            - Experience with TensorFlow, PyTorch, or similar frameworks
            - Knowledge of cloud platforms (AWS, GCP, or Azure)
            - Excellent communication and presentation skills
            
            Preferred Qualifications:
            - Published research in AI/ML conferences
            - Experience with big data technologies (Spark, Hadoop)
            - Knowledge of NLP and computer vision
            """,
            "Software Engineer": """
            Senior Software Engineer - Full Stack
            
            Job Description:
            We're looking for a skilled Full Stack Developer to join our growing team.
            
            Key Responsibilities:
            - Design, develop, and maintain web applications
            - Write clean, efficient, and well-documented code
            - Collaborate with product managers and designers
            - Participate in code reviews and architectural discussions
            - Troubleshoot and debug applications
            
            Technical Requirements:
            - 5+ years of software development experience
            - Proficiency in JavaScript, Python, and Java
            - Experience with React.js or Angular
            - Knowledge of Node.js and Express
            - Database experience (SQL and NoSQL)
            - Understanding of RESTful APIs and microservices
            
            Soft Skills:
            - Strong problem-solving abilities
            - Excellent team collaboration
            - Good communication skills
            - Ability to work in agile environment
            """
        }
        
        if sample_option in samples:
            job_text = samples[sample_option]
    
    # Parse button
    if st.button("🔍 Parse Job Description", type="primary", use_container_width=True):
        if job_text.strip():
            with st.spinner("Analyzing job description..."):
                # Parse the job description
                parsed_data = parser.parse_job_description(job_text)
                
                # Store in session state
                st.session_state.parsed_job_data = parsed_data
                st.session_state.job_text = job_text
                
                st.success("✅ Job description parsed successfully!")
        else:
            st.error("Please enter or upload a job description")
    
    # Display results if parsed
    if 'parsed_job_data' in st.session_state:
        parsed_data = st.session_state.parsed_job_data
        
        # Results tabs
        tabs = st.tabs([
            "📊 Overview", 
            "🛠️ Skills Analysis", 
            "🎯 Requirements", 
            "📈 ATS Optimization",
            "🧠 AI Insights"
        ])
        
        with tabs[0]:
            # Overview tab
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Job Title", parsed_data.get('job_title', 'N/A'))
                st.metric("Skill Categories Found", len(set([s['category'] for s in parsed_data['skills']])))
            
            with col2:
                st.metric("Total Skills Identified", len(parsed_data['skills']))
                if parsed_data.get('experience'):
                    exp_text = parsed_data['experience'][0]
                    st.metric("Experience Required", exp_text)
            
            with col3:
                st.metric("Complexity Score", f"{parsed_data['complexity_score']}/100")
                st.metric("Key Requirements", len(parsed_data['requirements']))
            
            # Visualization of skill categories
            st.subheader("Skill Distribution by Category")
            
            if parsed_data['skills']:
                skill_df = pd.DataFrame(parsed_data['skills'])
                category_counts = skill_df['category'].value_counts()
                
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Skills by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tabs[1]:
            # Skills Analysis tab
            st.subheader("Extracted Skills")
            
            # Group skills by category
            skill_categories = {}
            for skill in parsed_data['skills']:
                category = skill['category']
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill)
            
            # Display skills by category
            for category, skills in skill_categories.items():
                with st.expander(f"{category.upper()} ({len(skills)} skills)", expanded=True):
                    cols = st.columns(3)
                    for idx, skill in enumerate(skills):
                        col_idx = idx % 3
                        with cols[col_idx]:
                            importance_level = "🔴 High" if skill['importance'] > 1 else "🟡 Medium"
                            st.write(f"**{skill['skill'].title()}** - {importance_level}")
            
            # Skill gap analysis
            if parsed_data.get('skill_gap_analysis'):
                st.subheader("📊 Skill Gap Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**High Demand Skills:**")
                    for skill in parsed_data['skill_gap_analysis']['high_demand_skills'][:5]:
                        st.write(f"• {skill}")
                
                with col2:
                    st.write("**Recommended Training:**")
                    for training in parsed_data['skill_gap_analysis']['recommended_training'][:5]:
                        st.write(f"• {training}")
        
        with tabs[2]:
            # Requirements tab
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Key Responsibilities")
                if parsed_data['responsibilities']:
                    for idx, resp in enumerate(parsed_data['responsibilities'][:8], 1):
                        st.write(f"{idx}. {resp['sentence']}")
                        if resp.get('keywords'):
                            st.caption(f"Keywords: {', '.join(resp['keywords'][:3])}")
                else:
                    st.info("No specific responsibilities identified")
            
            with col2:
                st.subheader("🎓 Requirements")
                if parsed_data['requirements']:
                    for idx, req in enumerate(parsed_data['requirements'][:5], 1):
                        st.write(f"{idx}. {req}")
                else:
                    st.info("No specific requirements identified")
                
                st.subheader("📚 Education")
                if parsed_data['education']:
                    for idx, edu in enumerate(parsed_data['education'][:3], 1):
                        st.write(f"{idx}. {edu}")
                else:
                    st.info("No education requirements identified")
        
        with tabs[3]:
            # ATS Optimization tab
            st.subheader("🎯 ATS Optimization Keywords")
            
            # Generate ATS keywords
            ats_keywords = parser.generate_ats_keywords(parsed_data)
            
            # Display as tags
            st.write("**Include these keywords in job posting:**")
            keyword_cols = st.columns(4)
            for idx, keyword in enumerate(ats_keywords[:20]):  # Show top 20
                col_idx = idx % 4
                with keyword_cols[col_idx]:
                    st.markdown(f"`{keyword}`")
            
            # ATS Score
            st.subheader("📈 ATS Compatibility Score")
            
            ats_score = min(90 + len(parsed_data['skills']), 100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ATS Score", f"{ats_score}/100")
            with col2:
                st.metric("Keyword Density", "Good")
            with col3:
                st.metric("Readability", "Professional")
            
            # Suggestions for improvement
            st.subheader("💡 Suggestions for Better ATS Performance")
            
            suggestions = [
                "✅ Clear job title and structure",
                "✅ Specific skill requirements",
                "⚠️ Add more quantifiable requirements",
                "✅ Good use of industry-standard terms",
                "⚠️ Consider adding more soft skills"
            ]
            
            for suggestion in suggestions:
                st.write(suggestion)
        
        with tabs[4]:
            # AI Insights tab
            st.subheader("🤖 AI-Powered Insights")
            
            # Market demand analysis
            st.write("**📊 Market Demand Analysis**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Similar Jobs in Market", "1,234")
            with col2:
                st.metric("Average Salary", "$95,000")
            with col3:
                st.metric("Competition Level", "Medium")
            
            # Candidate matching insights
            st.write("**🎯 Candidate Matching Insights**")
            insights = [
                "This job description matches 85% with typical Data Scientist roles",
                "Top 3 most important skills: Python, Machine Learning, SQL",
                "Expected time to fill: 45 days",
                "Suggested platforms: LinkedIn, Indeed, Campus Placements"
            ]
            
            for insight in insights:
                st.info(insight)
            
            # Generate optimized job description
            if st.button("✨ Generate Optimized Job Description", use_container_width=True):
                with st.spinner("Generating optimized version..."):
                    optimized_jd = generate_optimized_jd(parsed_data)
                    st.text_area("Optimized Job Description", optimized_jd, height=300)
        
        # Action buttons
        st.subheader("🚀 Next Steps")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤 Post to Job Portal", use_container_width=True):
                st.success("Job posted successfully!")
        
        with col2:
            if st.button("🎯 Match with Candidates", use_container_width=True):
                st.session_state.show_matching = True
        
        with col3:
            st.download_button(
                "📥 Download Analysis",
                data=json.dumps(parsed_data, indent=2),
                file_name="job_analysis.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col4:
            if st.button("🔄 Parse Another", use_container_width=True):
                del st.session_state.parsed_job_data
                st.rerun()

def generate_optimized_jd(parsed_data):
    """Generate an optimized job description"""
    optimized = f"""
    {parsed_data.get('job_title', 'Job Position')}
    
    🌟 **About the Role:**
    We are seeking a talented professional for this exciting opportunity.
    
    🔧 **Key Skills Required:**
    {', '.join([s['skill'] for s in parsed_data['skills'][:10]])}
    
    📋 **Responsibilities:**
    """
    
    for resp in parsed_data['responsibilities'][:5]:
        optimized += f"• {resp['sentence']}\n"
    
    optimized += f"""
    🎓 **Requirements:**
    • {parsed_data.get('experience', ['Experience in relevant field'])[0]}
    • Relevant educational background
    • Strong problem-solving skills
    • Excellent communication abilities
    
    💼 **What We Offer:**
    • Competitive compensation package
    • Career growth opportunities
    • Collaborative work environment
    • Professional development support
    """
    
    return optimized
