import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import threading
import queue
import time

class VideoInterviewProcessor:
    def __init__(self):
        self.setup_models()
        self.feedback_queue = queue.Queue()
        self.metrics = {
            "body_language": 0,
            "speech_clarity": 0,
            "confidence": 0,
            "engagement": 0
        }
        
    def setup_models(self):
        """Initialize MediaPipe and other models"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        self.mp_holistic = mp.solutions.holistic
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def analyze_body_language(self, frame):
        """Analyze body language from video frame"""
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        face_results = self.face_mesh.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        metrics = {
            "eye_contact": self.detect_eye_contact(face_results),
            "posture": self.analyze_posture(pose_results),
            "facial_expressions": self.analyze_expressions(face_results),
            "hand_gestures": self.detect_hand_gestures(pose_results)
        }
        
        return metrics
    
    def detect_eye_contact(self, face_results):
        """Detect if person is maintaining eye contact"""
        if face_results.multi_face_landmarks:
            # Calculate eye landmarks position
            # Simplified logic - in reality would use complex calculations
            return 85  # percentage
        return 0
    
    def analyze_posture(self, pose_results):
        """Analyze posture from pose landmarks"""
        if pose_results.pose_landmarks:
            # Calculate shoulder alignment, back straightness, etc.
            return 90
        return 0
    
    def generate_feedback(self, metrics):
        """Generate real-time feedback based on metrics"""
        feedback = []
        
        if metrics['eye_contact'] < 70:
            feedback.append("⚠️ Improve eye contact with the camera")
        
        if metrics['posture'] < 80:
            feedback.append("💺 Sit up straight for better posture")
        
        # Add more feedback based on other metrics
        
        return feedback

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.analyzer = VideoInterviewProcessor()
        self.frame_count = 0
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Analyze every 10th frame
        if self.frame_count % 10 == 0:
            metrics = self.analyzer.analyze_body_language(img)
            feedback = self.analyzer.generate_feedback(metrics)
            
            # Update metrics in session state
            if 'interview_metrics' not in st.session_state:
                st.session_state.interview_metrics = []
            
            st.session_state.interview_metrics.append({
                "timestamp": time.time(),
                "metrics": metrics,
                "feedback": feedback
            })
        
        self.frame_count += 1
        
        # Draw landmarks on frame (optional)
        # img = self.draw_landmarks(img)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def show_interview_simulator():
    st.title("🎥 Video Interview Simulator")
    
    # Interview type selection
    col1, col2, col3 = st.columns(3)
    with col1:
        interview_type = st.selectbox(
            "Interview Type",
            ["Technical", "HR", "Managerial", "Behavioral", "Mock Placement"]
        )
    with col2:
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard", "Expert"]
        )
    with col3:
        duration = st.selectbox(
            "Duration",
            ["5 minutes", "10 minutes", "15 minutes", "30 minutes"]
        )
    
    # Question categories
    st.subheader("Question Categories")
    categories = st.multiselect(
        "Select categories to practice:",
        ["Technical Skills", "Problem Solving", "Communication", 
         "Leadership", "Teamwork", "Scenario-based", "Coding Challenges"],
        default=["Technical Skills", "Communication"]
    )
    
    # Video interview section
    st.subheader("🎬 Start Video Interview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # WebRTC video stream
        ctx = webrtc_streamer(
            key="interview-simulator",
            video_processor_factory=VideoProcessor,
            media_stream_constraints={
                "video": {
                    "width": {"ideal": 640},
                    "height": {"ideal": 480},
                    "frameRate": {"ideal": 30}
                },
                "audio": True
            },
            async_processing=True,
        )
    
    with col2:
        # Real-time feedback panel
        st.subheader("📊 Real-time Feedback")
        
        if 'interview_metrics' in st.session_state and st.session_state.interview_metrics:
            latest = st.session_state.interview_metrics[-1]
            
            # Display metrics
            st.metric("Eye Contact", f"{latest['metrics'].get('eye_contact', 0)}%")
            st.metric("Posture Score", f"{latest['metrics'].get('posture', 0)}%")
            st.metric("Confidence Level", f"{latest['metrics'].get('confidence', 0)}%")
            
            # Display feedback
            st.subheader("💡 Suggestions")
            for fb in latest.get('feedback', []):
                st.info(fb)
        
        # Control buttons
        if st.button("⏸️ Pause Analysis", use_container_width=True):
            # Implement pause logic
            pass
        
        if st.button("📊 View Detailed Report", use_container_width=True):
            show_detailed_report()
    
    # Question panel
    st.subheader("❓ Interview Questions")
    
    # AI-generated questions based on selections
    questions = generate_questions(interview_type, categories, difficulty)
    
    with st.container(border=True):
        question_tab, answer_tab = st.tabs(["Question", "Your Answer"])
        
        with question_tab:
            current_q = st.selectbox(
                "Select Question:",
                questions,
                index=0
            )
            st.write(f"**Q:** {current_q}")
            
            # Speech recognition for answer
            if st.button("🎤 Record Answer", use_container_width=True):
                st.info("Recording... Speak your answer clearly")
                # Implement speech-to-text here
        
        with answer_tab:
            answer = st.text_area(
                "Type or record your answer:",
                height=150,
                placeholder="Type your answer here or use voice recording..."
            )
            
            if answer and st.button("🤖 Get AI Feedback on Answer"):
                with st.spinner("Analyzing your answer..."):
                    feedback = analyze_answer(current_q, answer)
                    st.success("Analysis complete!")
                    st.write(feedback)
    
    # Practice questions bank
    with st.expander("📚 Question Bank", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Technical Questions**")
            tech_questions = [
                "Explain your most challenging project",
                "How would you optimize this algorithm?",
                "Describe your experience with cloud technologies"
            ]
            for q in tech_questions:
                st.write(f"• {q}")
        
        with col2:
            st.write("**Behavioral Questions**")
            behavioral_questions = [
                "Tell me about a time you faced conflict",
                "Describe a leadership experience",
                "How do you handle pressure?"
            ]
            for q in behavioral_questions:
                st.write(f"• {q}")
        
        with col3:
            st.write("**Scenario Questions**")
            scenario_questions = [
                "What would you do if you disagreed with your manager?",
                "How would you prioritize multiple deadlines?",
                "Describe your problem-solving approach"
            ]
            for q in scenario_questions:
                st.write(f"• {q}")

def generate_questions(interview_type, categories, difficulty):
    """Generate AI-powered interview questions"""
    # This would use an LLM to generate context-aware questions
    sample_questions = [
        "Describe a challenging technical problem you solved and your approach.",
        "How do you stay updated with the latest technologies in your field?",
        "Explain a time when you had to work in a team with conflicting opinions.",
        "What metrics do you use to measure success in your projects?",
        "How would you explain a complex technical concept to a non-technical stakeholder?"
    ]
    return sample_questions

def analyze_answer(question, answer):
    """Analyze answer using AI"""
    # This would use an LLM to evaluate the answer
    feedback = """
    **Analysis of your answer:**
    
    ✅ **Strengths:**
    - Clear structure and organization
    - Good use of specific examples
    - Appropriate technical depth
    
    ⚠️ **Areas for improvement:**
    - Could include more quantifiable results
    - Consider adding more context about your role
    - Try to relate more directly to the job requirements
    
    💡 **Suggestions:**
    - Use STAR method (Situation, Task, Action, Result)
    - Include specific metrics or outcomes
    - Connect to the company's values or projects
    """
    return feedback

def show_detailed_report():
    """Show comprehensive interview report"""
    st.subheader("📈 Detailed Performance Report")
    
    if 'interview_metrics' in st.session_state:
        metrics_df = pd.DataFrame(st.session_state.interview_metrics)
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(
                metrics_df.set_index('timestamp')['metrics'].apply(
                    lambda x: x.get('eye_contact', 0)
                ),
                use_container_width=True
            )
            st.caption("Eye Contact Trend")
        
        with col2:
            st.line_chart(
                metrics_df.set_index('timestamp')['metrics'].apply(
                    lambda x: x.get('posture', 0)
                ),
                use_container_width=True
            )
            st.caption("Posture Trend")
        
        # Overall scores
        st.subheader("Overall Scores")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Body Language", "85/100", "+5")
        with col2:
            st.metric("Speech Clarity", "78/100", "+3")
        with col3:
            st.metric("Confidence", "82/100", "+7")
        with col4:
            st.metric("Overall", "82/100", "+4")
        
        # AI-powered suggestions
        st.subheader("🎯 Personalized Improvement Plan")
        suggestions = [
            "Practice maintaining eye contact for 70% of the interview",
            "Work on reducing filler words (um, ah)",
            "Record and review 3 mock interviews per week",
            "Join Toastmasters or speaking clubs",
            "Practice power poses before interviews"
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            st.write(f"{i}. {suggestion}")
