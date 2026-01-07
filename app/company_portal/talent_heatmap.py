import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import json

class TalentHeatmap:
    def __init__(self):
        self.colleges = self.load_colleges()
        self.skills = self.load_skills()
    
    def load_colleges(self) -> List[Dict]:
        """Load college data"""
        colleges = [
            {"name": "IIT Bombay", "location": "Mumbai", "tier": 1, "students": 8000},
            {"name": "IIT Delhi", "location": "Delhi", "tier": 1, "students": 7500},
            {"name": "IIT Madras", "location": "Chennai", "tier": 1, "students": 7000},
            {"name": "NIT Trichy", "location": "Trichy", "tier": 2, "students": 6000},
            {"name": "BITS Pilani", "location": "Pilani", "tier": 1, "students": 5500},
            {"name": "IIIT Hyderabad", "location": "Hyderabad", "tier": 2, "students": 5000},
            {"name": "VIT Vellore", "location": "Vellore", "tier": 2, "students": 25000},
            {"name": "SRM University", "location": "Chennai", "tier": 3, "students": 30000},
            {"name": "MIT Manipal", "location": "Manipal", "tier": 2, "students": 15000},
            {"name": "DTU Delhi", "location": "Delhi", "tier": 2, "students": 12000}
        ]
        return colleges
    
    def load_skills(self) -> List[str]:
        """Load skill list"""
        return [
            "Python", "Java", "JavaScript", "React", "Node.js",
            "AWS", "Docker", "Kubernetes", "SQL", "MongoDB",
            "Machine Learning", "Data Science", "AI", "DevOps",
            "Mobile Development", "UI/UX", "Cloud Computing"
        ]
    
    def generate_talent_data(self) -> pd.DataFrame:
        """Generate sample talent data"""
        np.random.seed(42)
        
        data = []
        for college in self.colleges:
            for skill in self.skills:
                # Generate talent count based on college tier and skill
                base_count = college['students'] // 100
                tier_factor = 1.5 if college['tier'] == 1 else 1.0 if college['tier'] == 2 else 0.7
                skill_factor = 1.2 if skill in ["Python", "Java", "JavaScript"] else 1.0
                
                talent_count = int(base_count * tier_factor * skill_factor * np.random.uniform(0.8, 1.2))
                
                data.append({
                    "College": college["name"],
                    "Location": college["location"],
                    "Tier": college["tier"],
                    "Skill": skill,
                    "Talent Count": talent_count,
                    "Avg CGPA": round(np.random.uniform(7.5, 9.0), 2),
                    "Placement Rate": round(np.random.uniform(70, 95), 1)
                })
        
        return pd.DataFrame(data)
    
    def filter_talent_data(self, df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Filter talent data based on criteria"""
        filtered_df = df.copy()
        
        if filters.get('locations'):
            filtered_df = filtered_df[filtered_df['Location'].isin(filters['locations'])]
        
        if filters.get('tiers'):
            filtered_df = filtered_df[filtered_df['Tier'].isin(filters['tiers'])]
        
        if filters.get('skills'):
            filtered_df = filtered_df[filtered_df['Skill'].isin(filters['skills'])]
        
        if filters.get('min_cgpa'):
            filtered_df = filtered_df[filtered_df['Avg CGPA'] >= filters['min_cgpa']]
        
        if filters.get('min_placement'):
            filtered_df = filtered_df[filtered_df['Placement Rate'] >= filters['min_placement']]
        
        return filtered_df
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate talent metrics"""
        total_talent = df['Talent Count'].sum()
        avg_cgpa = df['Avg CGPA'].mean()
        avg_placement = df['Placement Rate'].mean()
        
        # Top colleges
        college_talent = df.groupby('College')['Talent Count'].sum().sort_values(ascending=False)
        top_colleges = college_talent.head(5).to_dict()
        
        # Top skills
        skill_talent = df.groupby('Skill')['Talent Count'].sum().sort_values(ascending=False)
        top_skills = skill_talent.head(5).to_dict()
        
        # Location distribution
        location_talent = df.groupby('Location')['Talent Count'].sum().sort_values(ascending=False)
        top_locations = location_talent.head(5).to_dict()
        
        return {
            'total_talent': total_talent,
            'avg_cgpa': round(avg_cgpa, 2),
            'avg_placement': round(avg_placement, 1),
            'top_colleges': top_colleges,
            'top_skills': top_skills,
            'top_locations': top_locations,
            'college_count': df['College'].nunique(),
            'skill_count': df['Skill'].nunique()
        }

def show_talent_heatmap():
    st.title("🗺️ Campus Talent Heatmap")
    
    # Initialize heatmap
    heatmap = TalentHeatmap()
    
    # Generate talent data
    talent_data = heatmap.generate_talent_data()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🌍 Map View", "📊 Analytics", "🎯 Talent Search", "📈 Trends"])
    
    with tab1:
        st.subheader("Geographical Talent Distribution")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            locations = st.multiselect(
                "Select Locations",
                sorted(talent_data['Location'].unique()),
                default=talent_data['Location'].unique()[:3]
            )
        
        with col2:
            tiers = st.multiselect(
                "College Tiers",
                [1, 2, 3],
                default=[1, 2]
            )
        
        with col3:
            skills = st.multiselect(
                "Skills",
                heatmap.skills,
                default=heatmap.skills[:5]
            )
        
        # Apply filters
        filters = {
            'locations': locations,
            'tiers': tiers,
            'skills': skills
        }
        
        filtered_data = heatmap.filter_talent_data(talent_data, filters)
        
        # Calculate metrics
        metrics = heatmap.calculate_metrics(filtered_data)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Talent", f"{metrics['total_talent']:,}")
        
        with col2:
            st.metric("Avg CGPA", f"{metrics['avg_cgpa']}")
        
        with col3:
            st.metric("Avg Placement", f"{metrics['avg_placement']}%")
        
        with col4:
            st.metric("Colleges", metrics['college_count'])
        
        # Geographical visualization
        st.subheader("📍 Location-wise Talent Density")
        
        # Create location aggregation
        location_agg = filtered_data.groupby('Location').agg({
            'Talent Count': 'sum',
            'Avg CGPA': 'mean',
            'Placement Rate': 'mean',
            'College': 'nunique'
        }).reset_index()
        
        # Bubble chart
        fig = px.scatter(location_agg, 
                        x='Talent Count', 
                        y='Avg CGPA',
                        size='College',
                        color='Placement Rate',
                        hover_name='Location',
                        size_max=50,
                        title='Talent Distribution by Location',
                        color_continuous_scale='viridis')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # College-wise talent
        st.subheader("🏫 College Talent Distribution")
        
        college_agg = filtered_data.groupby(['College', 'Location', 'Tier']).agg({
            'Talent Count': 'sum',
            'Avg CGPA': 'mean'
        }).reset_index()
        
        # Sort and display top colleges
        top_colleges = college_agg.sort_values('Talent Count', ascending=False).head(10)
        
        fig = px.bar(top_colleges, 
                    x='College', 
                    y='Talent Count',
                    color='Tier',
                    title='Top Colleges by Talent Count',
                    hover_data=['Location', 'Avg CGPA'])
        
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📊 Talent Analytics Dashboard")
        
        # Skill analysis
        st.write("### 🛠️ Skill Analysis")
        
        skill_agg = filtered_data.groupby('Skill').agg({
            'Talent Count': 'sum',
            'Avg CGPA': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(skill_agg.sort_values('Talent Count', ascending=False).head(10),
                        x='Skill', y='Talent Count',
                        title='Top Skills by Talent Count',
                        color='Talent Count',
                        color_continuous_scale='blues')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(skill_agg, 
                            x='Talent Count', 
                            y='Avg CGPA',
                            size='Talent Count',
                            color='Skill',
                            title='Skill Distribution',
                            size_max=40)
            st.plotly_chart(fig, use_container_width=True)
        
        # Tier analysis
        st.write("### 🏆 College Tier Analysis")
        
        tier_agg = filtered_data.groupby('Tier').agg({
            'Talent Count': 'sum',
            'Avg CGPA': 'mean',
            'Placement Rate': 'mean',
            'College': 'nunique'
        }).reset_index()
        
        tier_agg['Tier'] = tier_agg['Tier'].astype(str)
        
        fig = px.bar(tier_agg, 
                    x='Tier', 
                    y=['Talent Count', 'Avg CGPA', 'Placement Rate'],
                    barmode='group',
                    title='Metrics by College Tier')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.write("### 🔗 Correlation Analysis")
        
        # Calculate correlations
        numeric_cols = ['Talent Count', 'Avg CGPA', 'Placement Rate']
        correlation = filtered_data[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            colorscale='RdBu',
            zmid=0,
            text=correlation.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(title='Correlation Matrix')
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.write("### 💡 Key Insights")
        
        insights = [
            f"**Top Skill:** {list(metrics['top_skills'].keys())[0]} with {list(metrics['top_skills'].values())[0]:,} talents",
            f"**Top Location:** {list(metrics['top_locations'].keys())[0]} with {list(metrics['top_locations'].values())[0]:,} talents",
            f"**Top College:** {list(metrics['top_colleges'].keys())[0]} with {list(metrics['top_colleges'].values())[0]:,} talents",
            f"**Overall Quality:** Average CGPA of {metrics['avg_cgpa']} with {metrics['avg_placement']}% placement rate"
        ]
        
        for insight in insights:
            st.info(insight)
    
    with tab3:
        st.subheader("🎯 Targeted Talent Search")
        
        # Search criteria
        st.write("### 🔍 Define Your Search Criteria")
        
        with st.form("talent_search"):
            col1, col2 = st.columns(2)
            
            with col1:
                required_skills = st.multiselect(
                    "Required Skills*",
                    heatmap.skills,
                    default=["Python", "Java"]
                )
                
                min_cgpa = st.slider("Minimum CGPA", 6.0, 10.0, 7.5, 0.1)
                
                location_preference = st.multiselect(
                    "Preferred Locations",
                    sorted(talent_data['Location'].unique())
                )
            
            with col2:
                experience_level = st.selectbox(
                    "Experience Level",
                    ["Freshers", "1-2 years", "3-5 years", "5+ years"]
                )
                
                min_placement = st.slider("Minimum College Placement Rate", 50.0, 100.0, 75.0, 0.1)
                
                college_tiers = st.multiselect(
                    "College Tiers",
                    [1, 2, 3],
                    default=[1, 2]
                )
            
            # Additional filters
            st.write("### 📊 Additional Filters")
            
            col3, col4 = st.columns(2)
            
            with col3:
                min_talent_per_college = st.number_input(
                    "Minimum Talent per College",
                    min_value=1,
                    max_value=1000,
                    value=50
                )
            
            with col4:
                sort_by = st.selectbox(
                    "Sort Results By",
                    ["Talent Count", "Avg CGPA", "Placement Rate", "College Tier"]
                )
            
            # Submit search
            submitted = st.form_submit_button("🔍 Search Talent", type="primary")
        
        if submitted and required_skills:
            with st.spinner("Searching for matching talent..."):
                # Apply filters
                search_filters = {
                    'skills': required_skills,
                    'min_cgpa': min_cgpa,
                    'min_placement': min_placement,
                    'tiers': college_tiers,
                    'locations': location_preference
                }
                
                # Filter data
                search_results = heatmap.filter_talent_data(talent_data, search_filters)
                
                # Further filter by skills combination
                if required_skills:
                    # Group by college and check if all required skills are present
                    college_skills = search_results.groupby('College')['Skill'].apply(list).reset_index()
                    
                    # Find colleges that have all required skills
                    matching_colleges = []
                    for _, row in college_skills.iterrows():
                        college_skill_list = row['Skill']
                        if all(skill in college_skill_list for skill in required_skills):
                            matching_colleges.append(row['College'])
                    
                    search_results = search_results[search_results['College'].isin(matching_colleges)]
                
                # Apply minimum talent per college filter
                college_totals = search_results.groupby('College')['Talent Count'].sum()
                qualified_colleges = college_totals[college_totals >= min_talent_per_college].index
                search_results = search_results[search_results['College'].isin(qualified_colleges)]
                
                # Aggregate results
                if not search_results.empty:
                    # Aggregate by college
                    college_results = search_results.groupby(['College', 'Location', 'Tier']).agg({
                        'Talent Count': 'sum',
                        'Avg CGPA': 'mean',
                        'Placement Rate': 'mean'
                    }).reset_index()
                    
                    # Sort results
                    sort_columns = {
                        'Talent Count': 'Talent Count',
                        'Avg CGPA': 'Avg CGPA',
                        'Placement Rate': 'Placement Rate',
                        'College Tier': 'Tier'
                    }
                    
                    college_results = college_results.sort_values(
                        sort_columns[sort_by],
                        ascending=False
                    )
                    
                    # Display results
                    st.success(f"✅ Found {len(college_results)} colleges matching your criteria")
                    
                    # Display top results
                    st.subheader("🏆 Top Matching Colleges")
                    
                    for idx, row in college_results.head(5).iterrows():
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 1, 1])
                            
                            with col1:
                                st.write(f"### {row['College']}")
                                st.write(f"📍 {row['Location']} | Tier {row['Tier']}")
                            
                            with col2:
                                st.metric("Total Talent", f"{row['Talent Count']:,}")
                            
                            with col3:
                                st.metric("Avg CGPA", f"{row['Avg CGPA']:.2f}")
                                st.metric("Placement", f"{row['Placement Rate']:.1f}%")
                    
                    # Detailed view
                    st.subheader("📋 Detailed College Analysis")
                    
                    selected_college = st.selectbox(
                        "Select College for Detailed View",
                        college_results['College'].tolist()
                    )
                    
                    if selected_college:
                        college_data = search_results[search_results['College'] == selected_college]
                        
                        # Skill distribution for selected college
                        skill_dist = college_data.groupby('Skill').agg({
                            'Talent Count': 'sum'
                        }).reset_index()
                        
                        fig = px.pie(skill_dist, 
                                    values='Talent Count', 
                                    names='Skill',
                                    title=f'Skill Distribution at {selected_college}')
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("📧 Contact Placement Cell", use_container_width=True):
                                st.success(f"Contact request sent to {selected_college}")
                        
                        with col2:
                            if st.button("📅 Schedule Campus Drive", use_container_width=True):
                                st.success(f"Campus drive scheduled for {selected_college}")
                        
                        with col3:
                            if st.button("👥 View Student Profiles", use_container_width=True):
                                st.info(f"Opening student profiles from {selected_college}")
                    
                    # Export options
                    st.subheader("📥 Export Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            "📄 Download CSV",
                            data=college_results.to_csv(),
                            file_name="talent_search_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.download_button(
                            "📊 Download Report",
                            data=college_results.to_json(),
                            file_name="talent_search_report.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
                else:
                    st.warning("No colleges found matching your criteria. Try broadening your search.")
        
        elif submitted and not required_skills:
            st.error("Please select at least one required skill")
    
    with tab4:
        st.subheader("📈 Talent Market Trends")
        
        # Generate trend data
        years = [2021, 2022, 2023, 2024]
        
        trend_data = []
        for year in years:
            for skill in heatmap.skills[:8]:  # Top 8 skills
                # Simulate growth trends
                base = 1000
                growth_rate = 0.15 if skill in ["Python", "Machine Learning", "AWS"] else 0.1
                talent_count = int(base * (1 + growth_rate) ** (year - 2021) * np.random.uniform(0.9, 1.1))
                
                trend_data.append({
                    'Year': year,
                    'Skill': skill,
                    'Talent Count': talent_count,
                    'Demand Score': np.random.randint(60, 100)
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        # Skill growth trends
        st.write("### 📈 Skill Growth Trends")
        
        selected_skills = st.multiselect(
            "Select Skills to Compare",
            heatmap.skills[:8],
            default=heatmap.skills[:3]
        )
        
        if selected_skills:
            filtered_trend = trend_df[trend_df['Skill'].isin(selected_skills)]
            
            fig = px.line(filtered_trend, 
                         x='Year', 
                         y='Talent Count',
                         color='Skill',
                         markers=True,
                         title='Talent Growth by Skill (2021-2024)')
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Demand vs Supply analysis
        st.write("### ⚖️ Demand vs Supply Analysis")
        
        # Calculate demand-supply ratio
        latest_data = trend_df[trend_df['Year'] == 2024]
        latest_data['Demand_Supply_Ratio'] = latest_data['Demand Score'] / (latest_data['Talent Count'] / 1000)
        
        fig = px.scatter(latest_data,
                        x='Talent Count',
                        y='Demand Score',
                        size='Demand_Supply_Ratio',
                        color='Skill',
                        hover_name='Skill',
                        title='Demand vs Supply Analysis (2024)',
                        size_max=40)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Emerging skills
        st.write("### 🚀 Emerging Skills")
        
        # Calculate growth rates
        emerging_data = []
        for skill in heatmap.skills:
            talent_2023 = trend_df[(trend_df['Year'] == 2023) & (trend_df['Skill'] == skill)]['Talent Count'].mean()
            talent_2024 = trend_df[(trend_df['Year'] == 2024) & (trend_df['Skill'] == skill)]['Talent Count'].mean()
            
            if talent_2023 > 0:
                growth_rate = ((talent_2024 - talent_2023) / talent_2023) * 100
                emerging_data.append({
                    'Skill': skill,
                    'Growth Rate': growth_rate,
                    'Talent 2024': talent_2024
                })
        
        emerging_df = pd.DataFrame(emerging_data).sort_values('Growth Rate', ascending=False)
        
        # Display top emerging skills
        st.subheader("Top 5 Emerging Skills")
        
        for idx, row in emerging_df.head(5).iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{row['Skill']}**")
                
                with col2:
                    st.metric("Growth Rate", f"{row['Growth Rate']:.1f}%")
                
                with col3:
                    st.metric("Talent Pool", f"{int(row['Talent 2024']):,}")
        
        # Recommendations
        st.write("### 🎯 Strategic Recommendations")
        
        recommendations = [
            "Focus hiring efforts on Python and Machine Learning talent (high demand)",
            "Consider colleges in Bangalore and Hyderabad for tech talent",
            "Partner with Tier 1 colleges for quality talent acquisition",
            "Invest in training programs for emerging skills like AI and Cloud Computing",
            "Schedule campus drives in October-November for best results"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.info(f"{i}. {rec}")
