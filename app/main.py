# app/main.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Campus Placement AI",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Campus Placement Prediction AI")
st.markdown("""
This AI tool predicts whether a student will get placed based on their academic and personal profile.
Upload your dataset or use the sample data to get predictions.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose an option:", 
                         ["Home", "Upload Data", "Data Analysis", "Model Training", "Predictions", "About"])

# Initialize session state for data storage
if 'df' not in st.session_state:
    st.session_state.df = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'encoders' not in st.session_state:
    st.session_state.encoders = {}

# Sample data for demo
def create_sample_data():
    """Create sample campus placement data"""
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'CGPA': np.random.uniform(6.0, 10.0, n_samples),
        'Internships': np.random.randint(0, 4, n_samples),
        'Projects': np.random.randint(0, 6, n_samples),
        'Backlogs': np.random.randint(0, 3, n_samples),
        'Communication_Score': np.random.randint(1, 11, n_samples),
        'Technical_Score': np.random.randint(1, 11, n_samples),
        'Department': np.random.choice(['CSE', 'ECE', 'ME', 'CE', 'IT'], n_samples),
        'Gender': np.random.choice(['Male', 'Female'], n_samples)
    }
    
    # Create target variable (Placement status) based on features
    placement_score = (data['CGPA'] * 0.3 + 
                      data['Internships'] * 0.2 + 
                      data['Projects'] * 0.15 + 
                      data['Communication_Score'] * 0.15 +
                      data['Technical_Score'] * 0.2 -
                      data['Backlogs'] * 0.5)
    
    data['Placed'] = (placement_score > 5.0).astype(int)
    
    return pd.DataFrame(data)

# Home page
if option == "Home":
    st.header("Welcome to Campus Placement AI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📊 **Data Analysis**")
        st.write("Analyze student data and visualize patterns")
    
    with col2:
        st.success("🤖 **AI Prediction**")
        st.write("Predict placement chances using ML algorithms")
    
    with col3:
        st.warning("📈 **Insights**")
        st.write("Get actionable insights for improvement")
    
    st.markdown("---")
    
    # Show sample data preview
    st.subheader("Sample Data Preview")
    sample_df = create_sample_data()
    st.dataframe(sample_df.head(), use_container_width=True)
    
    # Statistics
    st.subheader("Sample Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(sample_df))
    
    with col2:
        placed_count = sample_df['Placed'].sum()
        st.metric("Placed Students", placed_count)
    
    with col3:
        placement_rate = (placed_count / len(sample_df)) * 100
        st.metric("Placement Rate", f"{placement_rate:.1f}%")
    
    with col4:
        avg_cgpa = sample_df['CGPA'].mean()
        st.metric("Average CGPA", f"{avg_cgpa:.2f}")

# Upload Data page
elif option == "Upload Data":
    st.header("📁 Upload Your Data")
    
    upload_method = st.radio("Choose data source:", 
                           ["Upload CSV file", "Use Sample Data", "Enter Data Manually"])
    
    if upload_method == "Upload CSV file":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success("✅ Data uploaded successfully!")
                st.dataframe(df.head(), use_container_width=True)
                st.write(f"Shape: {df.shape}")
                st.write("Columns:", df.columns.tolist())
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    elif upload_method == "Use Sample Data":
        if st.button("Load Sample Data"):
            df = create_sample_data()
            st.session_state.df = df
            st.success("✅ Sample data loaded successfully!")
            st.dataframe(df.head(), use_container_width=True)
    
    else:  # Manual data entry
        st.info("Enter data manually (for testing)")
        num_rows = st.number_input("Number of students:", min_value=1, max_value=50, value=5)
        
        if st.button("Generate Manual Data"):
            df = create_sample_data().head(num_rows)
            st.session_state.df = df
            st.success("✅ Manual data generated!")
            st.dataframe(df, use_container_width=True)

# Data Analysis page
elif option == "Data Analysis":
    st.header("📊 Data Analysis")
    
    if st.session_state.df is None:
        st.warning("Please upload data first from the 'Upload Data' page.")
    else:
        df = st.session_state.df
        
        # Show data info
        st.subheader("Dataset Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Data Shape:**", df.shape)
            st.write("**Columns:**", df.columns.tolist())
        
        with col2:
            st.write("**Data Types:**")
            st.write(df.dtypes)
        
        # Show missing values
        st.subheader("Missing Values")
        missing_data = df.isnull().sum()
        if missing_data.sum() == 0:
            st.success("✅ No missing values found!")
        else:
            st.warning("Missing values detected:")
            st.write(missing_data[missing_data > 0])
        
        # Show statistics
        st.subheader("Statistical Summary")
        st.write(df.describe())
        
        # Visualizations
        st.subheader("Data Visualizations")
        
        viz_option = st.selectbox("Choose visualization:", 
                                ["Placement Distribution", "CGPA Distribution", 
                                 "Feature Correlation", "Department-wise Analysis"])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if viz_option == "Placement Distribution":
            placement_counts = df['Placed'].value_counts()
            ax.pie(placement_counts.values, labels=['Not Placed', 'Placed'], 
                  autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
            ax.set_title('Placement Distribution')
        
        elif viz_option == "CGPA Distribution":
            ax.hist(df['CGPA'], bins=20, edgecolor='black', alpha=0.7)
            ax.set_xlabel('CGPA')
            ax.set_ylabel('Frequency')
            ax.set_title('CGPA Distribution')
        
        elif viz_option == "Feature Correlation":
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                corr_matrix = numeric_df.corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
                ax.set_title('Feature Correlation Matrix')
        
        elif viz_option == "Department-wise Analysis":
            if 'Department' in df.columns:
                dept_placement = df.groupby('Department')['Placed'].mean() * 100
                dept_placement.plot(kind='bar', ax=ax, color='skyblue')
                ax.set_xlabel('Department')
                ax.set_ylabel('Placement Rate (%)')
                ax.set_title('Department-wise Placement Rates')
                ax.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)

# Model Training page
elif option == "Model Training":
    st.header("🤖 Model Training")
    
    if st.session_state.df is None:
        st.warning("Please upload data first from the 'Upload Data' page.")
    else:
        df = st.session_state.df
        
        st.subheader("Select Features and Target")
        
        # Get numeric columns for features
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target from features if it exists
        if 'Placed' in numeric_cols:
            numeric_cols.remove('Placed')
        
        # Feature selection
        selected_features = st.multiselect(
            "Select features for prediction:",
            numeric_cols,
            default=numeric_cols[:min(4, len(numeric_cols))]
        )
        
        # Target selection
        target_col = st.selectbox(
            "Select target variable (placement status):",
            df.columns.tolist()
        )
        
        if selected_features and target_col:
            # Prepare data
            X = df[selected_features]
            y = df[target_col]
            
            # Encode categorical target if needed
            if y.dtype == 'object':
                le = LabelEncoder()
                y = le.fit_transform(y)
                st.session_state.encoders[target_col] = le
                st.info(f"Target encoded: {list(le.classes_)}")
            
            # Split data
            test_size = st.slider("Test set size:", 0.1, 0.5, 0.2, 0.05)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Model training
            if st.button("Train Model"):
                with st.spinner("Training model..."):
                    # Initialize and train model
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)
                    
                    # Store model in session state
                    st.session_state.model = model
                    
                    # Calculate accuracy
                    train_score = model.score(X_train, y_train)
                    test_score = model.score(X_test, y_test)
                    
                    # Display results
                    st.success("✅ Model trained successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Training Accuracy", f"{train_score:.2%}")
                    with col2:
                        st.metric("Testing Accuracy", f"{test_score:.2%}")
                    
                    # Feature importance
                    st.subheader("Feature Importance")
                    feature_importance = pd.DataFrame({
                        'Feature': selected_features,
                        'Importance': model.feature_importances_
                    }).sort_values('Importance', ascending=False)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(feature_importance['Feature'], feature_importance['Importance'])
                    ax.set_xlabel('Importance')
                    ax.set_title('Feature Importance')
                    st.pyplot(fig)

# Predictions page
elif option == "Predictions":
    st.header("🔮 Make Predictions")
    
    if st.session_state.model is None:
        st.warning("Please train the model first from the 'Model Training' page.")
    else:
        model = st.session_state.model
        df = st.session_state.df
        
        st.subheader("Predict for New Student")
        
        # Get feature names from model (assuming it's been trained)
        if hasattr(model, 'feature_names_in_'):
            feature_names = model.feature_names_in_
        else:
            # Get numeric columns from original data
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'Placed' in numeric_cols:
                numeric_cols.remove('Placed')
            feature_names = numeric_cols[:model.n_features_in_]
        
        # Create input form for each feature
        input_data = {}
        cols = st.columns(2)
        
        for i, feature in enumerate(feature_names):
            with cols[i % 2]:
                if df[feature].dtype in [np.float64, np.int64]:
                    min_val = float(df[feature].min())
                    max_val = float(df[feature].max())
                    default_val = float(df[feature].mean())
                    input_data[feature] = st.number_input(
                        feature,
                        min_value=min_val,
                        max_value=max_val,
                        value=default_val
                    )
                else:
                    unique_vals = df[feature].unique()
                    input_data[feature] = st.selectbox(feature, unique_vals)
        
        # Make prediction
        if st.button("Predict Placement"):
            # Prepare input for prediction
            input_df = pd.DataFrame([input_data])
            
            # Make prediction
            prediction = model.predict(input_df)[0]
            prediction_proba = model.predict_proba(input_df)[0]
            
            # Display result
            st.subheader("Prediction Result")
            
            if prediction == 1 or prediction == 'Placed':
                st.success(f"🎉 **HIGH CHANCE OF PLACEMENT**")
                st.write(f"Probability: {prediction_proba[1]:.1%}")
            else:
                st.error(f"⚠️ **LOW CHANCE OF PLACEMENT**")
                st.write(f"Probability: {prediction_proba[0]:.1%}")
            
            # Show probability breakdown
            st.subheader("Probability Breakdown")
            fig, ax = plt.subplots(figsize=(8, 4))
            labels = ['Not Placed', 'Placed'] if len(prediction_proba) == 2 else ['Class 0', 'Class 1']
            ax.bar(labels, prediction_proba, color=['red', 'green'])
            ax.set_ylabel('Probability')
            ax.set_title('Placement Probability')
            ax.set_ylim([0, 1])
            for i, v in enumerate(prediction_proba):
                ax.text(i, v + 0.02, f'{v:.1%}', ha='center')
            st.pyplot(fig)

# About page
else:  # option == "About"
    st.header("ℹ️ About This App")
    
    st.markdown("""
    ## Campus Placement Prediction AI
    
    ### 📋 Features:
    1. **Data Upload & Management** - Upload your own dataset or use sample data
    2. **Data Analysis** - Explore data with visualizations and statistics
    3. **Machine Learning** - Train AI models to predict placement outcomes
    4. **Predictions** - Get real-time predictions for individual students
    5. **Insights** - Understand key factors affecting placement
    
    ### 🎯 Purpose:
    This tool helps educational institutions and students:
    - Predict placement chances based on academic performance
    - Identify areas for improvement
    - Make data-driven decisions for career preparation
    
    ### 🛠️ Technologies Used:
    - **Streamlit** - Web application framework
    - **Scikit-learn** - Machine learning library
    - **Pandas & NumPy** - Data manipulation
    - **Matplotlib & Seaborn** - Data visualization
    
    ### 👨‍💻 How to Use:
    1. Upload your student data or use sample data
    2. Explore the data through analysis visualizations
    3. Train a machine learning model
    4. Make predictions for individual students
    5. Use insights to improve placement strategies
    
    ---
    
    *For educational purposes only. Predictions are based on historical data patterns.*
    """)
    
    st.info("💡 **Tip**: Start by uploading your data or using the sample data to explore the app's features.")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ for Campus Placement Prediction | AI-Powered Insights")
