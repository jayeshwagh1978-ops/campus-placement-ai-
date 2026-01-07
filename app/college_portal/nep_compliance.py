import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any

class NEPComplianceAnalyzer:
    def __init__(self):
        self.nep_guidelines = self.load_nep_guidelines()
        self.departments = ['CSE', 'ECE', 'ME', 'CE', 'IT', 'Physics', 'Chemistry', 'Mathematics']
    
    def load_nep_guidelines(self) -> Dict:
        """Load NEP 2020 guidelines"""
        return {
            "academic_flexibility": {
                "description": "Multiple entry/exit options",
                "weight": 20,
                "indicators": ["Credit transfer", "Multiple entry points", "Exit options with certificates"]
            },
            "multidisciplinary": {
                "description": "Interdisciplinary learning",
                "weight": 25,
                "indicators": ["Minor programs", "Elective courses", "Cross-department courses"]
            },
            "skill_development": {
                "description": "Vocational and skill-based education",
                "weight": 15,
                "indicators": ["Skill courses", "Industry internships", "Certification programs"]
            },
            "technology_integration": {
                "description": "Digital and online learning",
                "weight": 20,
                "indicators": ["Online courses", "Digital resources", "Blended learning"]
            },
            "research_innovation": {
                "description": "Research and innovation focus",
                "weight": 10,
                "indicators": ["Research projects", "Innovation cells", "Patent support"]
            },
            "internationalization": {
                "description": "Global exposure and collaboration",
                "weight": 10,
                "indicators": ["Foreign collaborations", "Student exchange", "Global curriculum"]
            }
        }
    
    def calculate_compliance_score(self, college_data: Dict) -> Dict[str, Any]:
        """Calculate NEP compliance score"""
        total_score = 0
        max_score = 100
        category_scores = {}
        
        for category, details in self.nep_guidelines.items():
            category_data = college_data.get(category, {})
            
            # Calculate category score based on implemented indicators
            implemented = category_data.get('implemented_indicators', [])
            total_indicators = len(details['indicators'])
            
            if total_indicators > 0:
                category_score = (len(implemented) / total_indicators) * details['weight']
                category_scores[category] = {
                    'score': round(category_score, 1),
                    'max_score': details['weight'],
                    'implemented': implemented,
                    'pending': [ind for ind in details['indicators'] if ind not in implemented]
                }
                total_score += category_score
        
        # Overall compliance level
        compliance_level = "Excellent" if total_score >= 85 else \
                          "Good" if total_score >= 70 else \
                          "Average" if total_score >= 50 else "Poor"
        
        return {
            'overall_score': round(total_score, 1),
            'max_score': max_score,
            'compliance_level': compliance_level,
            'category_scores': category_scores,
            'total_indicators': sum(len(details['indicators']) for details in self.nep_guidelines.values())
        }
    
    def generate_recommendations(self, compliance_result: Dict) -> List[Dict]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        for category, scores in compliance_result['category_scores'].items():
            if scores['score'] < scores['max_score'] * 0.8:  # Below 80% in category
                category_name = category.replace('_', ' ').title()
                priority = "High" if scores['score'] < scores['max_score'] * 0.5 else "Medium"
                
                recommendations.append({
                    'priority': priority,
                    'category': category_name,
                    'action': f"Implement: {', '.join(scores['pending'][:2])}",
                    'impact': f"Increase {category_name} score by {scores['max_score'] - scores['score']:.1f} points"
                })
        
        # Sort by priority
        recommendations.sort(key=lambda x: 0 if x['priority'] == 'High' else 1)
        
        return recommendations
    
    def generate_department_analysis(self) -> pd.DataFrame:
        """Generate department-wise NEP implementation analysis"""
        data = []
        
        for dept in self.departments:
            dept_data = {
                'Department': dept,
                'Multidisciplinary Courses': np.random.randint(5, 20),
                'Skill Courses': np.random.randint(3, 15),
                'Online Resources': np.random.randint(50, 200),
                'Research Projects': np.random.randint(2, 10),
                'International Collaborations': np.random.randint(0, 5)
            }
            data.append(dept_data)
        
        return pd.DataFrame(data)

def show_nep_compliance():
    st.title("📚 NEP 2020 Compliance Analyzer")
    
    # Initialize analyzer
    analyzer = NEPComplianceAnalyzer()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏫 College Analysis", "🎯 Recommendations", "📊 Department View", "📈 Progress Tracking"])
    
    with tab1:
        st.subheader("College-wide NEP Compliance Assessment")
        
        # Input form for college data
        with st.form("college_assessment"):
            st.write("### 📋 College Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                college_name = st.text_input("College Name", "ABC College of Engineering")
                accreditation = st.selectbox("Accreditation", ["NAAC A++", "NAAC A+", "NAAC A", "NAAC B", "None"])
                student_strength = st.number_input("Total Students", 1000, 20000, 5000)
            
            with col2:
                established_year = st.number_input("Established Year", 1950, 2024, 1995)
                location = st.text_input("Location", "Mumbai, Maharashtra")
                departments = st.multiselect("Departments", analyzer.departments, default=["CSE", "ECE", "ME"])
            
            st.divider()
            st.write("### 🎯 NEP Implementation Status")
            
            # Dynamic form for each NEP category
            college_data = {}
            
            for category, details in analyzer.nep_guidelines.items():
                category_name = category.replace('_', ' ').title()
                
                with st.expander(f"{category_name} ({details['weight']} points)", expanded=False):
                    st.write(details['description'])
                    
                    # Indicators for this category
                    implemented = st.multiselect(
                        f"Implemented indicators for {category_name}",
                        details['indicators'],
                        key=f"ind_{category}"
                    )
                    
                    # Additional notes
                    notes = st.text_area(
                        f"Additional notes for {category_name}",
                        placeholder="Describe implementation details...",
                        key=f"notes_{category}"
                    )
                    
                    college_data[category] = {
                        'implemented_indicators': implemented,
                        'notes': notes
                    }
            
            # Submit button
            submitted = st.form_submit_button("📊 Calculate Compliance Score", type="primary")
        
        if submitted:
            with st.spinner("Analyzing NEP compliance..."):
                # Calculate compliance score
                result = analyzer.calculate_compliance_score(college_data)
                
                # Display results
                st.success(f"✅ Analysis Complete! Overall Score: {result['overall_score']}/{result['max_score']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Score", f"{result['overall_score']}/{result['max_score']}")
                
                with col2:
                    st.metric("Compliance Level", result['compliance_level'])
                
                with col3:
                    implemented_total = sum(len(scores['implemented']) for scores in result['category_scores'].values())
                    st.metric("Indicators Implemented", f"{implemented_total}/{result['total_indicators']}")
                
                # Radar chart for category scores
                st.subheader("📈 Category-wise Analysis")
                
                categories = list(result['category_scores'].keys())
                scores = [result['category_scores'][cat]['score'] for cat in categories]
                max_scores = [result['category_scores'][cat]['max_score'] for cat in categories]
                
                # Create radar chart
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=scores,
                    theta=[cat.replace('_', ' ').title() for cat in categories],
                    fill='toself',
                    name='Current Score',
                    line_color='blue'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=max_scores,
                    theta=[cat.replace('_', ' ').title() for cat in categories],
                    fill='toself',
                    name='Maximum Score',
                    line_color='red',
                    opacity=0.3
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(max_scores) + 5]
                        )
                    ),
                    showlegend=True,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed category breakdown
                st.subheader("📋 Detailed Category Breakdown")
                
                for category, scores in result['category_scores'].items():
                    with st.expander(f"{category.replace('_', ' ').title()} - {scores['score']}/{scores['max_score']} points", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("✅ **Implemented:**")
                            for indicator in scores['implemented']:
                                st.success(f"• {indicator}")
                        
                        with col2:
                            if scores['pending']:
                                st.write("⚠️ **Pending:**")
                                for indicator in scores['pending']:
                                    st.warning(f"• {indicator}")
                            else:
                                st.success("All indicators implemented!")
    
    with tab2:
        st.subheader("🎯 Improvement Recommendations")
        
        if 'result' in locals():
            recommendations = analyzer.generate_recommendations(result)
            
            if recommendations:
                # High priority recommendations
                high_priority = [r for r in recommendations if r['priority'] == 'High']
                if high_priority:
                    st.error("### ⚠️ High Priority Actions")
                    for rec in high_priority:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([1, 2, 1])
                            with col1:
                                st.markdown(f"**{rec['category']}**")
                            with col2:
                                st.write(rec['action'])
                            with col3:
                                st.info(rec['impact'])
                
                # Medium priority recommendations
                medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
                if medium_priority:
                    st.warning("### 📋 Medium Priority Actions")
                    cols = st.columns(2)
                    for idx, rec in enumerate(medium_priority):
                        with cols[idx % 2]:
                            with st.container(border=True):
                                st.markdown(f"**{rec['category']}**")
                                st.write(rec['action'])
                                st.caption(rec['impact'])
                
                # Action plan
                st.subheader("📅 6-Month Action Plan")
                
                action_plan = [
                    {"Month": "Month 1", "Action": "Form NEP Implementation Committee", "Responsibility": "Principal"},
                    {"Month": "Month 2", "Action": "Curriculum review and gap analysis", "Responsibility": "Academic Council"},
                    {"Month": "Month 3", "Action": "Faculty training on NEP guidelines", "Responsibility": "HR Department"},
                    {"Month": "Month 4", "Action": "Implement multidisciplinary courses", "Responsibility": "Department Heads"},
                    {"Month": "Month 5", "Action": "Set up skill development center", "Responsibility": "Placement Cell"},
                    {"Month": "Month 6", "Action": "Establish international collaborations", "Responsibility": "International Office"}
                ]
                
                for action in action_plan:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col1:
                            st.write(f"**{action['Month']}**")
                        with col2:
                            st.write(action['Action'])
                        with col3:
                            st.caption(action['Responsibility'])
            else:
                st.success("🎉 Excellent! All NEP guidelines are well implemented.")
        else:
            st.info("Please complete the college assessment in the 'College Analysis' tab first.")
    
    with tab3:
        st.subheader("📊 Department-wise NEP Implementation")
        
        # Generate department analysis
        dept_data = analyzer.generate_department_analysis()
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            selected_departments = st.multiselect(
                "Select Departments",
                analyzer.departments,
                default=analyzer.departments[:5]
            )
        
        with col2:
            metric = st.selectbox(
                "View Metric",
                ["Multidisciplinary Courses", "Skill Courses", "Online Resources", "Research Projects", "International Collaborations"]
            )
        
        # Filter data
        filtered_data = dept_data[dept_data['Department'].isin(selected_departments)]
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(filtered_data, x='Department', y=metric,
                        title=f"{metric} by Department",
                        color=metric,
                        color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Department comparison radar chart
            metrics = ['Multidisciplinary Courses', 'Skill Courses', 'Online Resources']
            
            fig = go.Figure()
            
            for dept in selected_departments[:3]:  # Limit to 3 departments for clarity
                dept_values = filtered_data[filtered_data['Department'] == dept][metrics].values[0]
                fig.add_trace(go.Scatterpolar(
                    r=dept_values,
                    theta=metrics,
                    fill='toself',
                    name=dept
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(filtered_data[metrics].max())]
                    )
                ),
                showlegend=True,
                title="Department Comparison",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Department recommendations
        st.subheader("🎯 Department-specific Recommendations")
        
        for dept in selected_departments:
            with st.expander(f"Recommendations for {dept}", expanded=False):
                dept_row = filtered_data[filtered_data['Department'] == dept].iloc[0]
                
                recommendations = []
                
                if dept_row['Multidisciplinary Courses'] < 10:
                    recommendations.append("Increase multidisciplinary course offerings")
                
                if dept_row['Skill Courses'] < 5:
                    recommendations.append("Add more skill-based vocational courses")
                
                if dept_row['Research Projects'] < 3:
                    recommendations.append("Encourage more research projects")
                
                if dept_row['International Collaborations'] == 0:
                    recommendations.append("Establish international collaborations")
                
                if recommendations:
                    for rec in recommendations:
                        st.write(f"• {rec}")
                else:
                    st.success("Department is well-aligned with NEP guidelines!")
    
    with tab4:
        st.subheader("📈 Progress Tracking")
        
        # Simulated progress data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        progress_data = pd.DataFrame({
            'Month': months,
            'Overall Score': [45, 48, 52, 58, 62, 65, 68, 72, 75, 78, 82, 85],
            'Multidisciplinary': [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85],
            'Skill Development': [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
            'Technology Integration': [50, 55, 60, 65, 70, 75, 80, 85, 90, 92, 95, 98]
        })
        
        # Progress chart
        fig = px.line(progress_data, x='Month', y=['Overall Score', 'Multidisciplinary', 'Skill Development', 'Technology Integration'],
                      title="Monthly NEP Implementation Progress",
                      markers=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Milestones
        st.subheader("🏆 Implementation Milestones")
        
        milestones = [
            {"date": "2024-01-15", "milestone": "NEP Implementation Committee formed", "status": "Completed"},
            {"date": "2024-02-28", "milestone": "Curriculum review completed", "status": "Completed"},
            {"date": "2024-03-31", "milestone": "Faculty training program launched", "status": "In Progress"},
            {"date": "2024-04-30", "milestone": "Multidisciplinary courses introduced", "status": "Pending"},
            {"date": "2024-06-30", "milestone": "Skill development center operational", "status": "Pending"},
            {"date": "2024-09-30", "milestone": "100% NEP compliance target", "status": "Pending"}
        ]
        
        for milestone in milestones:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(milestone['date'])
            with col2:
                st.write(milestone['milestone'])
            with col3:
                if milestone['status'] == 'Completed':
                    st.success("✅ Completed")
                elif milestone['status'] == 'In Progress':
                    st.info("🔄 In Progress")
                else:
                    st.warning("⏳ Pending")
            
            st.divider()
        
        # Export options
        st.subheader("📥 Reports & Exports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "📄 Download Compliance Report",
                data=progress_data.to_csv(),
                file_name="nep_compliance_report.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                "📊 Download Dashboard",
                data=progress_data.to_json(),
                file_name="nep_dashboard.json",
                mime="application/json"
            )
        
        with col3:
            if st.button("📧 Share with UGC", use_container_width=True):
                st.success("Report shared successfully!")
