import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from typing import List, Dict, Any

class VideoInterviewSimulator:
    def __init__(self):
        self.questions_db = self.load_questions()
        self.feedback_criteria = self.load_feedback_criteria()
    
    def load_questions(self) -> Dict[str, List[Dict]]:
        """Load interview questions database"""
        return {
            "Technical": [
                {
                    "question": "Explain the difference between list and tuple in Python.",
                    "category": "Programming",
                    "difficulty": "Easy",
                    "hint": "Think about mutability and use cases."
                },
                {
                    "question": "What is the time complexity of binary search?",
                    "category": "Algorithms",
                    "difficulty": "Medium",
                    "hint": "Consider divide and conquer approach."
                },
                {
                    "question": "Explain how REST APIs work.",
                    "category": "Web Development",
                    "difficulty": "Medium",
                    "hint": "Talk about HTTP methods and statelessness."
                }
            ],
            "Behavioral": [
                {
                    "question": "Tell me about a time you faced a conflict at work.",
                    "category": "Teamwork",
                    "difficulty": "Medium",
                    "hint": "Use STAR method: Situation, Task, Action, Result."
                },
                {
                    "question": "Describe a project where you demonstrated leadership.",
                    "category": "Leadership",
                    "difficulty": "Hard",
                    "hint": "Focus on specific actions and outcomes."
                },
                {
                    "question": "How do you handle tight deadlines?",
                    "category": "Time Management",
                    "difficulty": "Easy",
                    "hint": "Talk about prioritization and communication."
                }
            ],
            "Scenario": [
                {
                    "question": "What would you do if you disagreed with your manager's decision?",
                    "category": "Professionalism",
                    "difficulty": "Hard",
                    "hint": "Emphasize respectful communication and data-driven approach."
                },
                {
                    "question": "How would you explain a technical concept to a non-technical stakeholder?",
                    "category": "Communication",
                    "difficulty": "Medium",
                    "hint": "Use analogies and avoid jargon."
                }
            ]
        }
    
    def load_feedback_criteria(self) -> Dict[str, List[str]]:
        """Load feedback criteria"""
        return {
            "Communication": [
                "Clarity of expression",
                "Vocabulary and terminology",
                "Pace and tone",
                "Confidence in delivery"
            ],
            "Content": [
                "Relevance to question",
                "Structure and organization",
                "Depth of knowledge",
                "Examples and evidence"
            ],
            "Presentation": [
                "Professional language",
                "Conciseness",
                "Engagement level",
                "Body language awareness"
            ]
        }
    
    def generate_feedback(self, answer: str, question: Dict) -> Dict[str, Any]:
        """Generate feedback for an answer"""
        feedback = {
            "strengths": [],
            "improvements": [],
            "score": random.randint(60, 95),
            "suggestions": []
        }
        
        # Analyze answer length
        word_count = len(answer.split())
        if word_count < 50:
            feedback["improvements"].append("Answer is too brief. Aim for 50-150 words.")
        elif word_count > 200:
            feedback["improvements"].append("Answer is too long. Try to be more concise.")
        else:
            feedback["strengths"].append("Good answer length.")
        
        # Check for structure indicators
        structure_indicators = ["first", "second", "third", "then", "next", "finally", "in conclusion"]
        if any(indicator in answer.lower() for indicator in structure_indicators):
            feedback["strengths"].append("Well-structured answer with clear organization.")
        else:
            feedback["improvements"].append("Consider using more structure (First, Second, Finally).")
        
        # Check for examples
        example_indicators = ["for example", "for instance", "such as", "specifically"]
        if any(indicator in answer.lower() for indicator in example_indicators):
            feedback["strengths"].append("Good use of specific examples.")
        else:
            feedback["improvements"].append("Add specific examples to strengthen your answer.")
        
        # Generate suggestions based on question type
        if question["category"] == "Technical":
            feedback["suggestions"].append("Be precise with technical terms.")
            feedback["suggestions"].append("Consider adding code examples if applicable.")
        elif question["category"] in ["Behavioral", "Scenario"]:
            feedback["suggestions"].append("Use STAR method for behavioral questions.")
            feedback["suggestions"].append("Focus on specific outcomes and learnings.")
        
        return feedback
    
    def simulate_interview_session(self, categories: List[str], duration_minutes: int) -> List[Dict]:
        """Simulate an interview session"""
        selected_questions = []
        
        for category in categories:
            if category in self.questions_db:
                selected_questions.extend(self.questions_db[category])
        
        # Select questions based on duration (approx 3 minutes per question)
        num_questions = min(len(selected_questions), duration_minutes // 3)
        interview_questions = random.sample(selected_questions, num_questions)
        
        return interview_questions

def show_interview_simulator():
    st.title("🎥 Video Interview Simulator")
    
    # Initialize simulator
    simulator = VideoInterviewSimulator()
    
    # Session setup
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interview_type = st.selectbox(
            "Interview Type",
            ["Technical", "Behavioral", "Mixed", "Mock Placement", "Company Specific"]
        )
    
    with col2:
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
    
    with col3:
        duration = st.selectbox(
            "Duration",
            ["5 minutes (Quick Practice)", "15 minutes (Standard)", "30 minutes (Comprehensive)"]
        )
    
    # Question categories
    st.subheader("Select Question Categories")
    categories = st.multiselect(
        "Choose categories to practice:",
        ["Technical", "Behavioral", "Scenario", "Problem Solving", "Leadership", "Communication"],
        default=["Technical", "Behavioral"]
    )
    
    # Start interview button
    if st.button("🎬 Start Mock Interview", type="primary", use_container_width=True):
        if not categories:
            st.error("Please select at least one category")
        else:
            # Calculate duration in minutes
            duration_mins = int(duration.split()[0])
            
            # Start interview session
            st.session_state.interview_session = simulator.simulate_interview_session(categories, duration_mins)
            st.session_state.current_question_index = 0
            st.session_state.answers = []
            st.session_state.feedback = []
            st.session_state.interview_start_time = datetime.now()
            st.session_state.interview_active = True
    
    # Interview interface
    if 'interview_active' in st.session_state and st.session_state.interview_active:
        st.divider()
        st.subheader("🎤 Live Interview Session")
        
        # Progress bar
        total_questions = len(st.session_state.interview_session)
        current_q = st.session_state.current_question_index
        
        progress = (current_q / total_questions) * 100 if total_questions > 0 else 0
        st.progress(progress / 100, text=f"Question {current_q + 1} of {total_questions}")
        
        # Current question
        if current_q < total_questions:
            question_data = st.session_state.interview_session[current_q]
            
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### ❓ Question {current_q + 1}")
                    st.markdown(f"**{question_data['question']}**")
                    st.caption(f"Category: {question_data['category']} | Difficulty: {question_data['difficulty']}")
                
                with col2:
                    # Timer
                    if 'question_start_time' not in st.session_state:
                        st.session_state.question_start_time = time.time()
                    
                    elapsed = int(time.time() - st.session_state.question_start_time)
                    mins, secs = divmod(elapsed, 60)
                    st.metric("⏱️ Time", f"{mins:02d}:{secs:02d}")
                    
                    # Hint button
                    if st.button("💡 Get Hint", use_container_width=True):
                        st.info(f"**Hint:** {question_data.get('hint', 'No hint available')}")
            
            # Answer input
            st.subheader("Your Answer")
            answer = st.text_area(
                "Type your answer below (aim for 100-200 words):",
                height=200,
                key=f"answer_{current_q}",
                placeholder="Start typing your answer here..."
            )
            
            # Recording simulation
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🎤 Record Audio", use_container_width=True):
                    st.info("Audio recording started... Speak clearly.")
            
            with col2:
                if st.button("📹 Record Video", use_container_width=True):
                    st.info("Video recording started... Maintain eye contact.")
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.answers.append({"question": question_data, "answer": "", "skipped": True})
                    st.session_state.current_question_index += 1
                    st.session_state.question_start_time = time.time()
                    st.rerun()
            
            with col2:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    if answer.strip():
                        # Generate feedback
                        feedback = simulator.generate_feedback(answer, question_data)
                        
                        # Store answer and feedback
                        st.session_state.answers.append({
                            "question": question_data,
                            "answer": answer,
                            "feedback": feedback,
                            "timestamp": datetime.now()
                        })
                        
                        st.session_state.current_question_index += 1
                        st.session_state.question_start_time = time.time()
                        
                        if current_q + 1 >= total_questions:
                            st.session_state.interview_active = False
                            st.session_state.interview_end_time = datetime.now()
                        
                        st.rerun()
                    else:
                        st.error("Please provide an answer before submitting")
            
            with col3:
                # Time suggestion
                st.info("💡 Aim to answer in 2-3 minutes")
        
        else:
            # Interview completed
            st.balloons()
            st.success("🎉 Interview Completed!")
            
            # Calculate statistics
            total_questions = len(st.session_state.answers)
            answered = len([a for a in st.session_state.answers if a.get('answer')])
            skipped = total_questions - answered
            
            # Display summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Questions", total_questions)
            
            with col2:
                st.metric("Answered", answered)
            
            with col3:
                st.metric("Skipped", skipped)
            
            with col4:
                avg_score = sum(a.get('feedback', {}).get('score', 0) for a in st.session_state.answers if a.get('feedback')) / answered if answered > 0 else 0
                st.metric("Avg Score", f"{avg_score:.1f}/100")
            
            # Detailed feedback
            st.subheader("📊 Detailed Feedback")
            
            for idx, answer_data in enumerate(st.session_state.answers):
                with st.expander(f"Question {idx + 1}: {answer_data['question']['question'][:50]}...", expanded=False):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if answer_data.get('skipped'):
                            st.warning("⚠️ Skipped")
                        elif answer_data.get('feedback'):
                            score = answer_data['feedback']['score']
                            st.metric("Score", f"{score}/100")
                            
                            # Score indicator
                            if score >= 85:
                                st.success("Excellent")
                            elif score >= 70:
                                st.info("Good")
                            elif score >= 60:
                                st.warning("Needs Improvement")
                            else:
                                st.error("Poor")
                    
                    with col2:
                        if answer_data.get('answer'):
                            st.write("**Your Answer:**")
                            st.write(answer_data['answer'][:300] + "..." if len(answer_data['answer']) > 300 else answer_data['answer'])
                            
                            if answer_data.get('feedback'):
                                feedback = answer_data['feedback']
                                
                                st.write("**Strengths:**")
                                for strength in feedback.get('strengths', []):
                                    st.success(f"✓ {strength}")
                                
                                st.write("**Areas for Improvement:**")
                                for improvement in feedback.get('improvements', []):
                                    st.warning(f"⚠️ {improvement}")
                                
                                st.write("**Suggestions:**")
                                for suggestion in feedback.get('suggestions', []):
                                    st.info(f"💡 {suggestion}")
            
            # Overall recommendations
            st.subheader("🎯 Overall Recommendations")
            
            recommendations = [
                "Practice answering common behavioral questions using the STAR method",
                "Record yourself answering questions to improve delivery",
                "Work on maintaining eye contact and confident posture",
                "Prepare 2-3 strong examples for common question types",
                "Practice
