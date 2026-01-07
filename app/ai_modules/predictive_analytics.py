import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

class PredictiveAnalytics:
    def __init__(self):
        self.student_data = self.generate_sample_data()
    
    def generate_sample_data(self) -> pd.DataFrame:
        """Generate sample student data for demonstration"""
        np.random.seed(42)
        
        students = []
        for i in range(100):
            student = {
                'student_id': f'S{1000 + i}',
                'cgpa': round(np.random.uniform(6.0, 9.5), 2),
                'attendance': round(np.random.uniform(75, 100), 1),
                'projects': np.random.randint(1, 10),
                'internships': np.random.randint(0, 3),
                'skills': np.random.randint(5, 25),
                'coding_score': np.random.randint(500, 2000),
                'communication_score': np.random.randint(50, 100),
                'department': np.random.choice(['CSE', 'ECE', 'ME', 'CE', 'IT']),
                'year': np.random.choice([3, 4]),
                'placement_status': np.random.choice(['Placed', 'Not Placed'], p=[0.7, 0.3]),
                'package': round(np.random.uniform(3.5, 15.0), 2) if np.random.random() > 0.3 else 0
            }
            students.append(student)
        
        return pd.DataFrame(students)
    
    def calculate_placement_probability(self, student_features: dict) -> float:
        """Calculate placement probability based on features"""
        # Simplified model for demo
        score = 0
        
        # CGPA weight
        cgpa = student_features.get('cgpa', 0)
        score += min(cgpa * 10, 30)
        
        # Projects weight
        projects = student_features.get('projects', 0)
        score += min(projects * 3, 15)
        
        # Internships weight
        internships = student_features.get('internships', 0)
        score += internships * 8
        
        # Skills weight
        skills = student_features.get('skills', 0)
        score += min(skills * 2, 20)
        
        # Communication score weight
        comm_score = student_features.get('communication_score', 0)
        score += comm_score * 0.2
        
        # Normalize to 0-100
        probability = min(score, 95)
        
        return round(probability, 1)
    
    def predict_salary_range(self, student_features: dict) -> dict:
        """Predict salary range based on features"""
        base_salary = 4.0  # Base LPA
        
        # Adjust based on features
        adjustments = {
            'cgpa': (student_features.get('cgpa', 0) - 7.5) * 0.5,
            'projects': student_features.get('projects', 0) * 0.2,
            'internships': student_features.get('internships', 0) * 0.5,
            'coding_score': (student_features.get('coding_score', 0) - 1000) / 1000,
            'department': {'CSE': 1.0, 'IT': 0.8, 'ECE': 0.6, 'ME': 0.4, 'CE': 0.3}.get(
                student_features.get('department', 'CSE'), 0.5
            )
        }
        
        predicted = base_salary + sum(adjustments.values())
        
        # Add randomness for range
        lower = max(3.0, predicted * 0.8)
        upper = min(20.0, predicted * 1.2)
        
        return {
            'lower': round(lower, 1),
            'predicted': round(predicted, 1),
            'upper': round(upper, 1)
        }
    
    def get_recommendations(self, student_features: dict) -> list:
        """Get personalized recommendations"""
        recommendations = []
        
        cgpa = student_features.get('cgpa', 0)
        projects = student_features.get('projects', 0)
        internships = student_features.get('internships', 0)
        skills = student_features.get('skills', 0)
        comm_score = student_features.get('communication_score', 0)
        
        if cgpa < 7.5:
            recommendations.append({
                'priority': 'High',
                'area': 'Academic Performance',
                'action': 'Focus on improving CGPA to at least 7.5',
                'impact': 'Increase placement chances by 25%'
            })
        
        if projects < 3:
            recommendations.append({
                'priority': 'High',
                'area': 'Projects',
                'action': 'Complete at least 3 quality projects',
                'impact': 'Demonstrate practical skills to employers'
            })
        
        if internships == 0:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Internships',
                'action': 'Secure at least one internship',
                'impact': 'Gain industry experience and references'
            })
        
        if skills < 15:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Skills',
                'action': 'Learn 5 new technical skills',
                'impact': 'Meet minimum requirements for most jobs'
            })
        
        if comm_score < 70:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Communication',
                'action': 'Practice communication skills',
                'impact': 'Improve interview performance significantly'
            })
        
        # Always include these recommendations
        recommendations.extend([
            {
                'priority': 'Low',
                'area': 'Networking',
                'action': 'Attend career fairs and networking events',
                'impact': 'Increase job opportunities by 15%'
            },
            {
                'priority': 'Low',
                'area': 'Resume',
                'action': 'Get resume reviewed by career center',
                'impact': 'Improve ATS compatibility'
            }
        ])
        
        return recommendations
    
    def generate_trend_analysis(self) -> dict:
        """Generate placement trend analysis"""
        # Simulate monthly placement data
        months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS')
        
        trend_data = {
            'month': months.strftime('%b'),
            'placements': np.random.randint(30, 100, len(months)),
            'average_package': np.random.uniform(4.5, 8.5, len(months)),
            'top_companies': np.random.randint(10, 30, len(months))
        }
        
        # Add seasonal pattern
        trend_data['placements'] = trend_data['placements'] + [20, 30, 40, 50, 60, 70, 60, 50, 40, 30, 20, 10]
        
        return pd.DataFrame(trend_data)

def show_predictive_analytics():
    st.title("📊 Predictive Analytics Dashboard")
    
    # Initialize analytics
    analytics = PredictiveAnalytics()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Student Analysis", "📈 College Trends", "🏢 Company Insights", "🤖 AI Predictions"])
    
    with tab1:
        st.subheader("Student Placement Probability Analysis")
        
        # Student input form
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA", 6.0, 10.0, 8.0, 0.1)
            attendance = st.slider("Attendance %", 60.0, 100.0, 85.0, 0.1)
            projects = st.number_input("Number of Projects", 0, 20, 3)
        
        with col2:
            internships = st.number_input("Internships Completed", 0, 5, 1)
            skills = st.slider("Technical Skills Count", 5, 50, 15)
            department = st.selectbox("Department", ["CSE", "ECE", "ME", "CE", "IT"])
        
        # Additional metrics
        col3, col4 = st.columns(2)
        
        with col3:
            coding_score = st.slider("Coding Test Score", 500, 2000, 1200, 50)
        
        with col4:
            comm_score = st.slider("Communication Score", 50, 100, 75)
        
        # Analyze button
        if st.button("🔍 Analyze Placement Probability", type="primary", use_container_width=True):
            # Prepare student features
            student_features = {
                'cgpa': cgpa,
                'attendance': attendance,
                'projects': projects,
                'internships': internships,
                'skills': skills,
                'coding_score': coding_score,
                'communication_score': comm_score,
                'department': department
            }
            
            # Calculate probabilities
            placement_prob = analytics.calculate_placement_probability(student_features)
            salary_range = analytics.predict_salary_range(student_features)
            recommendations = analytics.get_recommendations(student_features)
            
            # Display results
            st.subheader("Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Placement Probability", f"{placement_prob}%")
                
                # Probability gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=placement_prob,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Probability"},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 40], 'color': "lightgray"},
                            {'range': [40, 70], 'color': "gray"},
                            {'range': [70, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Expected Salary", f"₹{salary_range['predicted']}L PA")
                st.write(f"**Range:** ₹{salary_range['lower']}L - ₹{salary_range['upper']}L PA")
                
                # Salary distribution visualization
                departments = ['CSE', 'ECE', 'ME', 'CE', 'IT']
                avg_salaries = [8.5, 6.8, 5.5, 5.2, 7.2]  # Example data
                
                fig = go.Figure(data=[
                    go.Bar(x=departments, y=avg_salaries, marker_color='lightblue')
                ])
                
                fig.update_layout(
                    title="Average Salary by Department",
                    yaxis_title="LPA",
                    height=200
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.metric("Competitiveness", 
                         "High" if placement_prob >= 80 else "Medium" if placement_prob >= 60 else "Low")
                
                # Skills radar chart
                categories = ['Technical', 'Projects', 'Internships', 'Academic', 'Communication']
                values = [skills/50*100, projects/10*100, internships/3*100, cgpa/10*100, comm_score]
                
                fig = go.Figure(data=[
                    go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Student Profile'
                    )
                ])
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=False,
                    height=250
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.subheader("🎯 Personalized Recommendations")
            
            # Group by priority
            high_priority = [r for r in recommendations if r['priority'] == 'High']
            medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
            low_priority = [r for r in recommendations if r['priority'] == 'Low']
            
            if high_priority:
                st.warning("### ⚠️ High Priority Actions")
                for rec in high_priority:
                    with st.expander(f"{rec['area']}: {rec['action']}", expanded=True):
                        st.write(f"**Impact:** {rec['impact']}")
            
            if medium_priority:
                st.info("### 📋 Medium Priority Actions")
                cols = st.columns(2)
                for idx, rec in enumerate(medium_priority):
                    with cols[idx % 2]:
                        with st.container(border=True):
                            st.write(f"**{rec['area']}**")
                            st.write(rec['action'])
                            st.caption(f"Impact: {rec['impact']}")
            
            if low_priority:
                st.success("### 💡 General Recommendations")
                for rec in low_priority:
                    st.write(f"• **{rec['area']}:** {rec['action']} ({rec['impact']})")
    
    with tab2:
        st.subheader("College-wide Placement Analytics")
        
        # Generate trend data
        trend_data = analytics.generate_trend_analysis()
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_placements = trend_data['placements'].sum()
            st.metric("Total Placements", f"{total_placements}")
        
        with col2:
            avg_package = trend_data['average_package'].mean()
            st.metric("Avg Package", f"₹{avg_package:.1f}L")
        
        with col3:
            peak_month = trend_data.loc[trend_data['placements'].idxmax(), 'month']
            st.metric("Peak Month", peak_month)
        
        with col4:
            companies = trend_data['top_companies'].sum()
            st.metric("Companies Visited", companies)
        
        # Trend visualization
        st.subheader("📈 Monthly Placement Trends")
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Placements by Month', 'Average Package Trend',
                           'Company Participation', 'Placement Efficiency'),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                   [{'type': 'bar'}, {'type': 'pie'}]]
        )
        
        # Plot 1: Placements by month
        fig.add_trace(
            go.Bar(x=trend_data['month'], y=trend_data['placements'],
                   name='Placements', marker_color='blue'),
            row=1, col=1
        )
        
        # Plot 2: Average package trend
        fig.add_trace(
            go.Scatter(x=trend_data['month'], y=trend_data['average_package'],
                       mode='lines+markers', name='Avg Package',
                       line=dict(color='green', width=3)),
            row=1, col=2
        )
        
        # Plot 3: Company participation
        fig.add_trace(
            go.Bar(x=trend_data['month'], y=trend_data['top_companies'],
                   name='Companies', marker_color='orange'),
            row=2, col=1
        )
        
        # Plot 4: Department-wise placements (sample data)
        departments = ['CSE', 'ECE', 'ME', 'CE', 'IT']
        dept_placements = [85, 65, 45, 40, 60]
        fig.add_trace(
            go.Pie(labels=departments, values=dept_placements,
                   name='Department Split'),
            row=2, col=2
        )
        
        fig.update_layout(height=700, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Department comparison
        st.subheader("🏫 Department Comparison")
        
        dept_data = pd.DataFrame({
            'Department': departments,
            'Placements': dept_placements,
            'Avg Package': [9.5, 6.8, 5.5, 5.2, 7.2],
            'Placement %': [92, 78, 65, 60, 85]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(dept_data, x='Department', y='Placements',
                         title='Placements by Department',
                         color='Placements', color_continuous_scale='viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(dept_data, x='Placement %', y='Avg Package',
                             size='Placements', color='Department',
                             title='Package vs Placement Rate',
                             size_max=60)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🏢 Company Hiring Insights")
        
        # Sample company data
        companies = [
            {'name': 'Google', 'visits': 8, 'offers': 25, 'avg_package': 18.5, 'domain': 'Tech'},
            {'name': 'Microsoft', 'visits': 10, 'offers': 30, 'avg_package': 16.8, 'domain': 'Tech'},
            {'name': 'Amazon', 'visits': 12, 'offers': 45, 'avg_package': 15.5, 'domain': 'Tech'},
            {'name': 'TCS', 'visits': 15, 'offers': 80, 'avg_package': 6.5, 'domain': 'IT Services'},
            {'name': 'Infosys', 'visits': 14, 'offers': 75, 'avg_package': 6.2, 'domain': 'IT Services'},
            {'name': 'Wipro', 'visits': 12, 'offers': 60, 'avg_package': 5.8, 'domain': 'IT Services'},
            {'name': 'Goldman Sachs', 'visits': 4, 'offers': 12, 'avg_package': 14.5, 'domain': 'Finance'},
            {'name': 'Morgan Stanley', 'visits': 3, 'offers': 10, 'avg_package': 13.8, 'domain': 'Finance'},
            {'name': 'Bosch', 'visits': 6, 'offers': 25, 'avg_package': 8.5, 'domain': 'Engineering'},
            {'name': 'Siemens', 'visits': 5, 'offers': 20, 'avg_package': 8.2, 'domain': 'Engineering'}
        ]
        
        company_df = pd.DataFrame(companies)
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            domain_filter = st.multiselect(
                "Filter by Domain",
                options=company_df['domain'].unique(),
                default=company_df['domain'].unique()
            )
        
        with col2:
            min_offers = st.slider("Minimum Offers", 0, 100, 0)
        
        # Filter data
        filtered_df = company_df[
            (company_df['domain'].isin(domain_filter)) &
            (company_df['offers'] >= min_offers)
        ]
        
        # Visualization
        fig = px.treemap(filtered_df, path=['domain', 'name'],
                         values='offers',
                         color='avg_package',
                         color_continuous_scale='RdYlGn',
                         title='Company Hiring Distribution',
                         hover_data=['visits', 'offers', 'avg_package'])
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Company Hiring Details")
        
        # Sort options
        sort_by = st.selectbox("Sort by", ['offers', 'avg_package', 'visits'])
        sort_order = st.radio("Order", ['Descending', 'Ascending'])
        
        sorted_df = filtered_df.sort_values(
            by=sort_by,
            ascending=(sort_order == 'Ascending')
        )
        
        # Display metrics for selected companies
        st.dataframe(
            sorted_df.style.background_gradient(subset=['offers', 'avg_package'], cmap='YlOrRd'),
            use_container_width=True
        )
        
        # Hiring pattern analysis
        st.subheader("📈 Hiring Pattern Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(filtered_df, x='visits', y='offers',
                             size='avg_package', color='domain',
                             hover_name='name',
                             title='Visits vs Offers',
                             size_max=30)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(filtered_df, x='domain', y='avg_package',
                         title='Package Distribution by Domain')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🤖 AI-Powered Predictions")
        
        st.info("""
        This section uses machine learning models to predict:
        - Future placement trends
        - Student success probability
        - Market demand for skills
        - Optimal interview timing
        """)
        
        # Prediction parameters
        col1, col2 = st.columns(2)
        
        with col1:
            prediction_period = st.selectbox(
                "Prediction Period",
                ["Next 3 months", "Next 6 months", "Next 1 year", "Next 2 years"]
            )
            
            confidence_level = st.slider("Confidence Level", 80, 99, 90)
        
        with col2:
            include_factors = st.multiselect(
                "Include Factors",
                ["Economic Trends", "Industry Growth", "Skill Demand", "Previous Patterns", "Seasonality"],
                default=["Previous Patterns", "Seasonality"]
            )
            
            if st.button("🚀 Generate Predictions", use_container_width=True):
                with st.spinner("Running AI models..."):
                    # Simulate prediction generation
                    time.sleep(2)
                    
                    # Generate predictions
                    predictions = {
                        'next_3_months': {
                            'placements': 245,
                            'avg_package': 7.8,
                            'top_domains': ['AI/ML', 'Cloud Computing', 'Cybersecurity'],
                            'high_demand_skills': ['Python', 'AWS', 'React', 'Data Analysis']
                        },
                        'next_6_months': {
                            'placements': 520,
                            'avg_package': 8.2,
                            'top_domains': ['FinTech', 'HealthTech', 'EdTech'],
                            'high_demand_skills': ['Machine Learning', 'DevOps', 'Full Stack', 'UI/UX']
                        }
                    }
                    
                    st.success("✅ Predictions generated successfully!")
                    
                    # Display predictions
                    period_key = 'next_3_months' if '3 months' in prediction_period else 'next_6_months'
                    pred = predictions[period_key]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Predicted Placements", pred['placements'])
                    
                    with col2:
                        st.metric("Expected Avg Package", f"₹{pred['avg_package']}L")
                    
                    with col3:
                        st.metric("Confidence", f"{confidence_level}%")
                    
                    # Domain predictions
                    st.subheader("🌐 Emerging Domains")
                    
                    cols = st.columns(len(pred['top_domains']))
                    for idx, domain in enumerate(pred['top_domains']):
                        with cols[idx]:
                            with st.container(border=True):
                                st.markdown(f"### {domain}")
                                growth = random.randint(15, 40)
                                st.metric("Growth", f"+{growth}%")
                    
                    # Skill predictions
                    st.subheader("🛠️ High-Demand Skills")
                    
                    skill_data = pd.DataFrame({
                        'Skill': pred['high_demand_skills'],
                        'Demand Score': [random.randint(80, 100) for _ in pred['high_demand_skills']],
                        'Salary Impact': [random.uniform(1.2, 2.0) for _ in pred['high_demand_skills']]
                    })
                    
                    fig = px.bar(skill_data, x='Skill', y='Demand Score',
                                 color='Salary Impact',
                                 title='Skill Demand & Salary Impact',
                                 color_continuous_scale='viridis')
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Actionable insights
                    st.subheader("🎯 Actionable Insights")
                    
                    insights = [
                        "Focus curriculum updates on AI/ML and Cloud Computing",
                        "Schedule placement drives in October-November for maximum impact",
                        "Partner with FinTech companies for specialized hiring",
                        "Offer certification programs in high-demand skills"
                    ]
                    
                    for insight in insights:
                        st.info(f"💡 {insight}")
