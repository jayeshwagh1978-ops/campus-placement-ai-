import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class PlacementDashboard:
    def __init__(self):
        self.data = self.generate_sample_data()
        self.departments = ['CSE', 'ECE', 'ME', 'CE', 'IT', 'Physics', 'Chemistry', 'Mathematics']
    
    def generate_sample_data(self) -> pd.DataFrame:
        """Generate sample placement data"""
        np.random.seed(42)
        
        # Generate data for multiple years
        years = [2021, 2022, 2023, 2024]
        data = []
        
        for year in years:
            for dept in self.departments:
                for _ in range(np.random.randint(50, 150)):
                    student = {
                        'year': year,
                        'department': dept,
                        'student_id': f'S{np.random.randint(1000, 9999)}',
                        'cgpa': round(np.random.uniform(6.0, 9.5), 2),
                        'placed': np.random.choice([True, False], p=[0.7, 0.3]),
                        'package': round(np.random.uniform(3.0, 15.0), 2) if np.random.random() > 0.3 else 0,
                        'company': np.random.choice(['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys', 'Wipro', 'Accenture', None]),
                        'offer_date': f'{year}-{np.random.randint(1, 12):02d}-{np.random.randint(1, 28):02d}',
                        'internship': np.random.choice([True, False], p=[0.6, 0.4])
                    }
                    data.append(student)
        
        return pd.DataFrame(data)
    
    def calculate_metrics(self, year: int = None) -> Dict[str, Any]:
        """Calculate placement metrics"""
        if year:
            data = self.data[self.data['year'] == year]
        else:
            data = self.data
            year = "All Years"
        
        total_students = len(data)
        placed_students = data['placed'].sum()
        placement_rate = (placed_students / total_students * 100) if total_students > 0 else 0
        
        avg_package = data[data['placed']]['package'].mean()
        max_package = data[data['placed']]['package'].max()
        min_package = data[data['placed']]['package'].min()
        
        top_companies = data[data['placed']]['company'].value_counts().head(5).to_dict()
        
        return {
            'year': year,
            'total_students': total_students,
            'placed_students': placed_students,
            'placement_rate': round(placement_rate, 1),
            'avg_package': round(avg_package, 2),
            'max_package': round(max_package, 2),
            'min_package': round(min_package, 2),
            'top_companies': top_companies
        }
    
    def generate_forecast(self) -> pd.DataFrame:
        """Generate placement forecast for next year"""
        current_year = datetime.now().year
        months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        
        # Generate forecast based on historical trends
        base_placements = 80
        trend_increase = 0.15  # 15% year-over-year growth
        
        forecast_data = []
        for i, month in enumerate(months):
            # Simulate seasonal pattern
            seasonal_factor = 1 + 0.3 * np.sin(i * np.pi / 6)  # Sinusoidal pattern
            
            placements = int(base_placements * seasonal_factor * (1 + trend_increase))
            avg_package = round(6.5 * (1 + 0.1 * i/12), 2)
            
            forecast_data.append({
                'month': month,
                'predicted_placements': placements,
                'predicted_package': avg_package,
                'confidence_lower': int(placements * 0.8),
                'confidence_upper': int(placements * 1.2)
            })
        
        return pd.DataFrame(forecast_data)
    
    def get_department_performance(self) -> pd.DataFrame:
        """Get department-wise performance"""
        dept_stats = []
        
        for dept in self.departments:
            dept_data = self.data[self.data['department'] == dept]
            
            if len(dept_data) > 0:
                placed = dept_data['placed'].sum()
                total = len(dept_data)
                rate = (placed / total * 100) if total > 0 else 0
                avg_pkg = dept_data[dept_data['placed']]['package'].mean()
                
                dept_stats.append({
                    'Department': dept,
                    'Total Students': total,
                    'Placed': placed,
                    'Placement Rate %': round(rate, 1),
                    'Avg Package (LPA)': round(avg_pkg, 2) if not pd.isna(avg_pkg) else 0,
                    'Trend': '📈' if rate > 70 else '📉' if rate < 50 else '➡️'
                })
        
        return pd.DataFrame(dept_stats)
    
    def generate_insights(self) -> List[Dict]:
        """Generate AI-powered insights"""
        metrics = self.calculate_metrics(2024)
        dept_stats = self.get_department_performance()
        
        insights = []
        
        # Overall insights
        if metrics['placement_rate'] > 80:
            insights.append({
                'type': 'positive',
                'title': 'Excellent Placement Performance',
                'description': f"Placement rate of {metrics['placement_rate']}% exceeds industry standards"
            })
        elif metrics['placement_rate'] < 60:
            insights.append({
                'type': 'warning',
                'title': 'Placement Rate Needs Improvement',
                'description': f"Current rate of {metrics['placement_rate']}% is below target of 75%"
            })
        
        # Department insights
        worst_dept = dept_stats.loc[dept_stats['Placement Rate %'].idxmin()]
        best_dept = dept_stats.loc[dept_stats['Placement Rate %'].idxmax()]
        
        insights.extend([
            {
                'type': 'info',
                'title': f"Best Performing: {best_dept['Department']}",
                'description': f"{best_dept['Placement Rate %']}% placement rate with avg package ₹{best_dept['Avg Package (LPA)']}L"
            },
            {
                'type': 'warning',
                'title': f"Needs Attention: {worst_dept['Department']}",
                'description': f"Only {worst_dept['Placement Rate %']}% placement rate. Consider intervention strategies."
            }
        ])
        
        # Company insights
        if metrics['top_companies']:
            top_company = max(metrics['top_companies'], key=metrics['top_companies'].get)
            insights.append({
                'type': 'positive',
                'title': f"Top Recruiter: {top_company}",
                'description': f"Hired {metrics['top_companies'][top_company]} students this year"
            })
        
        # Trend insights
        current_rate = self.calculate_metrics(2024)['placement_rate']
        last_year_rate = self.calculate_metrics(2023)['placement_rate']
        
        if current_rate > last_year_rate:
            insights.append({
                'type': 'positive',
                'title': 'Positive Growth Trend',
                'description': f"Placement rate increased by {current_rate - last_year_rate:.1f}% compared to last year"
            })
        
        return insights

def show_placement_dashboard():
    st.title("📊 Placement Analytics Dashboard")
    
    # Initialize dashboard
    dashboard = PlacementDashboard()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏫 Department Analysis", "🎯 Forecast", "🤖 AI Insights"])
    
    with tab1:
        st.subheader("College-wide Placement Overview")
        
        # Year selector
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_year = st.selectbox(
                "Select Year",
                ["All Years", 2024, 2023, 2022, 2021],
                index=0
            )
        
        with col2:
            comparison = st.checkbox("Compare with Previous Year")
        
        # Calculate metrics
        if selected_year == "All Years":
            metrics = dashboard.calculate_metrics()
        else:
            metrics = dashboard.calculate_metrics(selected_year)
        
        # Display KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Students",
                f"{metrics['total_students']:,}",
                "All Programs" if selected_year == "All Years" else f"Year {selected_year}"
            )
        
        with col2:
            st.metric(
                "Placement Rate",
                f"{metrics['placement_rate']}%",
                f"{metrics['placed_students']:,} placed"
            )
        
        with col3:
            st.metric(
                "Average Package",
                f"₹{metrics['avg_package']}L",
                f"Max: ₹{metrics['max_package']}L"
            )
        
        with col4:
            internship_rate = round((dashboard.data['internship'].sum() / len(dashboard.data)) * 100, 1)
            st.metric(
                "Internship Conversion",
                f"{internship_rate}%",
                "To Placement"
            )
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Placement trend over years
            years = [2021, 2022, 2023, 2024]
            rates = [dashboard.calculate_metrics(year)['placement_rate'] for year in years]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years, y=rates,
                mode='lines+markers',
                name='Placement Rate',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title='Placement Rate Trend (2021-2024)',
                xaxis_title='Year',
                yaxis_title='Placement Rate (%)',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Package distribution
            placed_data = dashboard.data[dashboard.data['placed']]
            
            if len(placed_data) > 0:
                fig = px.histogram(placed_data, x='package',
                                  title='Salary Package Distribution',
                                  nbins=20,
                                  color_discrete_sequence=['green'])
                
                fig.update_layout(
                    xaxis_title='Package (LPA)',
                    yaxis_title='Number of Students',
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Top companies
        st.subheader("🏢 Top Recruiting Companies")
        
        if metrics['top_companies']:
            companies = list(metrics['top_companies'].keys())
            hires = list(metrics['top_companies'].values())
            
            fig = px.bar(x=companies, y=hires,
                        title='Number of Hires by Company',
                        labels={'x': 'Company', 'y': 'Number of Students'},
                        color=hires,
                        color_continuous_scale='viridis')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No placement data available for selected year")
    
    with tab2:
        st.subheader("Department-wise Performance Analysis")
        
        # Get department statistics
        dept_stats = dashboard.get_department_performance()
        
        # Display department metrics
        st.dataframe(
            dept_stats.style.background_gradient(subset=['Placement Rate %', 'Avg Package (LPA)'], cmap='YlOrRd'),
            use_container_width=True
        )
        
        # Department comparison
        st.subheader("📊 Department Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(dept_stats, x='Department', y='Placement Rate %',
                        title='Placement Rate by Department',
                        color='Placement Rate %',
                        color_continuous_scale='RdYlGn')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(dept_stats, x='Placement Rate %', y='Avg Package (LPA)',
                            size='Total Students', color='Department',
                            title='Package vs Placement Rate',
                            size_max=40)
            st.plotly_chart(fig, use_container_width=True)
        
        # Department details
        st.subheader("📋 Department Details")
        
        selected_dept = st.selectbox("Select Department for Details", dashboard.departments)
        
        if selected_dept:
            dept_data = dashboard.data[dashboard.data['department'] == selected_dept]
            
            if len(dept_data) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total = len(dept_data)
                    st.metric("Total Students", total)
                
                with col2:
                    placed = dept_data['placed'].sum()
                    rate = (placed / total * 100) if total > 0 else 0
                    st.metric("Placed", placed, f"{rate:.1f}%")
                
                with col3:
                    avg_pkg = dept_data[dept_data['placed']]['package'].mean()
                    st.metric("Avg Package", f"₹{avg_pkg:.1f}L" if not pd.isna(avg_pkg) else "₹0L")
                
                with col4:
                    internship_rate = (dept_data['internship'].sum() / total * 100) if total > 0 else 0
                    st.metric("Internship Rate", f"{internship_rate:.1f}%")
                
                # Year-wise trend for selected department
                years = [2021, 2022, 2023, 2024]
                dept_rates = []
                
                for year in years:
                    year_data = dept_data[dept_data['year'] == year]
                    if len(year_data) > 0:
                        rate = (year_data['placed'].sum() / len(year_data) * 100) if len(year_data) > 0 else 0
                        dept_rates.append(rate)
                    else:
                        dept_rates.append(0)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=years, y=dept_rates,
                    mode='lines+markers',
                    name=f'{selected_dept} Placement Rate',
                    line=dict(color='orange', width=3)
                ))
                
                fig.update_layout(
                    title=f'{selected_dept} Placement Trend (2021-2024)',
                    xaxis_title='Year',
                    yaxis_title='Placement Rate (%)',
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🎯 Placement Forecast & Predictions")
        
        # Generate forecast
        forecast_data = dashboard.generate_forecast()
        
        # Display forecast metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_predicted = forecast_data['predicted_placements'].sum()
            st.metric("Total Predicted Placements", f"{total_predicted:,}")
        
        with col2:
            avg_predicted_pkg = forecast_data['predicted_package'].mean()
            st.metric("Predicted Avg Package", f"₹{avg_predicted_pkg:.1f}L")
        
        with col3:
            peak_month = forecast_data.loc[forecast_data['predicted_placements'].idxmax(), 'month']
            st.metric("Peak Placement Month", peak_month)
        
        # Forecast visualization
        fig = go.Figure()
        
        # Predicted placements
        fig.add_trace(go.Scatter(
            x=forecast_data['month'],
            y=forecast_data['predicted_placements'],
            mode='lines+markers',
            name='Predicted Placements',
            line=dict(color='blue', width=3)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_data['month'].tolist() + forecast_data['month'].tolist()[::-1],
            y=forecast_data['confidence_upper'].tolist() + forecast_data['confidence_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='80% Confidence Interval'
        ))
        
        fig.update_layout(
            title='Monthly Placement Forecast (Next 12 Months)',
            xaxis_title='Month',
            yaxis_title='Number of Placements',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth predictions
        st.subheader("📈 Growth Predictions")
        
        # Calculate growth rates
        current_metrics = dashboard.calculate_metrics(2024)
        predicted_growth = 15  # 15% predicted growth
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            predicted_rate = current_metrics['placement_rate'] * (1 + predicted_growth/100)
            st.metric(
                "Predicted Placement Rate",
                f"{predicted_rate:.1f}%",
                f"+{predicted_growth}%"
            )
        
        with col2:
            predicted_package = current_metrics['avg_package'] * 1.1  # 10% increase
            st.metric(
                "Predicted Avg Package",
                f"₹{predicted_package:.1f}L",
                "+10%"
            )
        
        with col3:
            # Based on historical data
            historical_growth = []
            for year in [2021, 2022, 2023, 2024]:
                metrics = dashboard.calculate_metrics(year)
                historical_growth.append(metrics['placement_rate'])
            
            avg_growth = np.mean(np.diff(historical_growth))
            st.metric(
                "Historical Avg Growth",
                f"{avg_growth:.1f}%",
                "Per Year"
            )
        
        # Recommendations based on forecast
        st.subheader("🎯 Strategic Recommendations")
        
        recommendations = [
            "Schedule major placement drives in October-November (peak season)",
            "Focus on skill development programs in summer for better placement outcomes",
            "Increase industry collaborations for internship opportunities",
            "Provide special training for departments with lower placement rates"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.info(f"{i}. {rec}")
    
    with tab4:
        st.subheader("🤖 AI-Powered Insights & Recommendations")
        
        # Generate insights
        insights = dashboard.generate_insights()
        
        # Display insights
        for insight in insights:
            if insight['type'] == 'positive':
                with st.container(border=True):
                    st.success(f"### ✅ {insight['title']}")
                    st.write(insight['description'])
            elif insight['type'] == 'warning':
                with st.container(border=True):
                    st.warning(f"### ⚠️ {insight['title']}")
                    st.write(insight['description'])
            else:
                with st.container(border=True):
                    st.info(f"### 📊 {insight['title']}")
                    st.write(insight['description'])
        
        # Predictive analytics
        st.subheader("🔮 Predictive Analytics")
        
        # Student success prediction
        st.write("### 🎓 Student Success Predictor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA", 6.0, 10.0, 8.0, 0.1)
            projects = st.number_input("Number of Projects", 0, 10, 3)
            internships = st.number_input("Internships", 0, 5, 1)
        
        with col2:
            skills = st.slider("Technical Skills", 5, 50, 15)
            department = st.selectbox("Department", dashboard.departments)
            extracurricular = st.slider("Extracurricular Score", 0, 100, 70)
        
        if st.button("🔍 Predict Placement Probability", type="primary"):
            # Simplified prediction model
            base_score = 50
            
            # Add contributions
            cgpa_score = (cgpa - 6.0) * 10  # 0-40 points
            projects_score = projects * 5    # 0-50 points
            internships_score = internships * 10  # 0-50 points
            skills_score = skills * 1        # 5-50 points
            dept_factor = 1.2 if department in ['CSE', 'IT'] else 1.0
            extracurricular_score = extracurricular * 0.3  # 0-30 points
            
            total_score = (base_score + cgpa_score + projects_score + 
                          internships_score + skills_score + extracurricular_score) * dept_factor
            
            probability = min(total_score, 95)
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Placement Probability", f"{probability:.1f}%")
            
            with col2:
                expected_package = round(4.0 + (cgpa - 6.0) * 1.5 + internships * 0.8, 1)
                st.metric("Expected Package", f"₹{expected_package}L")
            
            with col3:
                readiness = "High" if probability >= 80 else "Medium" if probability >= 60 else "Low"
                st.metric("Readiness Level", readiness)
            
            # Recommendations
            st.subheader("🎯 Personalized Recommendations")
            
            recs = []
            if cgpa < 7.5:
                recs.append("Improve CGPA to at least 7.5 for better opportunities")
            if projects < 2:
                recs.append("Complete at least 2 quality projects")
            if internships == 0:
                recs.append("Secure at least one internship")
            if skills < 10:
                recs.append("Learn additional technical skills")
            
            if recs:
                for rec in recs:
                    st.warning(f"• {rec}")
            else:
                st.success("✅ Student profile is strong for placements!")
        
        # Export options
        st.subheader("📥 Export & Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                "📄 Download Full Report",
                data=dashboard.data.to_csv(),
                file_name="placement_analytics_report.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Generate summary report
            summary = {
                "overview": dashboard.calculate_metrics(),
                "department_performance": dashboard.get_department_performance().to_dict(),
                "forecast": dashboard.generate_forecast().to_dict(),
                "generated_at": datetime.now().isoformat()
            }
            
            st.download_button(
                "📊 Download Summary",
                data=json.dumps(summary, indent=2),
                file_name="placement_summary.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Refresh Analytics", use_container_width=True):
                st.rerun()
