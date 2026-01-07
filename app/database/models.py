from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    user_type = Column(String(20), nullable=False)  # student, college, company
    full_name = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    college_profile = relationship("College", back_populates="user", uselist=False)
    company_profile = relationship("Company", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    roll_number = Column(String(20), unique=True)
    department = Column(String(50))
    year = Column(Integer)
    cgpa = Column(Float)
    attendance = Column(Float)
    skills = Column(JSON)  # JSON array of skills
    projects = Column(JSON)  # JSON array of projects
    internships = Column(JSON)  # JSON array of internships
    resume_url = Column(String(200))
    linkedin_url = Column(String(200))
    github_url = Column(String(200))
    placement_status = Column(String(20), default='seeking')
    placement_company = Column(String(100))
    placement_package = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    applications = relationship("JobApplication", back_populates="student")
    interviews = relationship("Interview", back_populates="student")

class College(Base):
    __tablename__ = 'colleges'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    college_name = Column(String(200), nullable=False)
    university = Column(String(200))
    location = Column(String(100))
    accreditation = Column(String(50))
    established_year = Column(Integer)
    total_students = Column(Integer)
    departments = Column(JSON)  # JSON array of departments
    contact_person = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    website = Column(String(200))
    
    # Relationships
    user = relationship("User", back_populates="college_profile")
    placements = relationship("Placement", back_populates="college")

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    company_name = Column(String(200), nullable=False)
    industry = Column(String(100))
    location = Column(String(100))
    website = Column(String(200))
    description = Column(Text)
    contact_person = Column(String(100))
    contact_email = Column(String(100))
    contact_phone = Column(String(20))
    size = Column(String(50))  # Small, Medium, Large
    founded_year = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="company_profile")
    job_postings = relationship("JobPosting", back_populates="company")
    placements = relationship("Placement", back_populates="company")

class JobPosting(Base):
    __tablename__ = 'job_postings'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    skills_required = Column(JSON)  # JSON array of skills
    experience_required = Column(String(50))
    location = Column(String(100))
    salary_range = Column(String(100))
    job_type = Column(String(50))  # Full-time, Part-time, Internship
    posted_date = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)
    total_applications = Column(Integer, default=0)
    
    # Relationships
    company = relationship("Company", back_populates="job_postings")
    applications = relationship("JobApplication", back_populates="job_posting")

class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    job_posting_id = Column(Integer, ForeignKey('job_postings.id'), nullable=False)
    application_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='applied')  # applied, reviewed, shortlisted, rejected, hired
    resume_url = Column(String(200))
    cover_letter = Column(Text)
    application_score = Column(Float)  # AI-generated score
    
    # Relationships
    student = relationship("Student", back_populates="applications")
    job_posting = relationship("JobPosting", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")

class Interview(Base):
    __tablename__ = 'interviews'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    application_id = Column(Integer, ForeignKey('job_applications.id'))
    interview_date = Column(DateTime)
    interview_type = Column(String(50))  # Technical, HR, Managerial
    duration = Column(Integer)  # in minutes
    status = Column(String(50), default='scheduled')  # scheduled, completed, cancelled
    feedback = Column(Text)
    score = Column(Float)
    recording_url = Column(String(200))
    
    # Relationships
    student = relationship("Student", back_populates="interviews")
    company = relationship("Company")
    application = relationship("JobApplication", back_populates="interviews")

class Placement(Base):
    __tablename__ = 'placements'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    college_id = Column(Integer, ForeignKey('colleges.id'), nullable=False)
    job_role = Column(String(200))
    package = Column(Float)
    joining_date = Column(DateTime)
    offer_letter_url = Column(String(200))
    status = Column(String(50), default='offered')  # offered, accepted, joined
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")
    company = relationship("Company", back_populates="placements")
    college = relationship("College", back_populates="placements")

class Certificate(Base):
    __tablename__ = 'certificates'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    certificate_name = Column(String(200), nullable=False)
    issuing_organization = Column(String(200))
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    certificate_url = Column(String(200))
    blockchain_hash = Column(String(200))
    verified = Column(Boolean, default=False)
    
    # Relationships
    student = relationship("Student")

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    skill_name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    demand_score = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    metric_date = Column(DateTime, default=datetime.utcnow)
    entity_type = Column(String(50))  # student, college, company
    entity_id = Column(Integer)
    additional_data = Column(JSON)

# Create database engine
def init_database():
    """Initialize database connection"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./campus_placement.db')
    engine = create_engine(database_url)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    return SessionLocal

def get_db():
    """Get database session"""
    SessionLocal = init_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
