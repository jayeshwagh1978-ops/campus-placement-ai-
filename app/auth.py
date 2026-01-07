import streamlit as st
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from database.models import User
from database.connection import get_db
import bcrypt

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key-change-in-production"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user"""
    with get_db() as db:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def init_session_state():
    """Initialize session state for authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'token' not in st.session_state:
        st.session_state.token = None

def login_form():
    """Display login form"""
    st.title("🔐 Login to Campus Placement AI")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user_type = st.selectbox("User Type", ["Student", "College", "Company"])
        
        submitted = st.form_submit_button("Login", type="primary")
        
        if submitted:
            user = authenticate_user(username, password)
            if user:
                # Create access token
                access_token = create_access_token(
                    data={"sub": user.username, "type": user.user_type},
                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                
                # Update session state
                st.session_state.authenticated = True
                st.session_state.user = user
                st.session_state.user_type = user.user_type
                st.session_state.token = access_token
                
                st.success(f"Welcome back, {user.full_name or user.username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    # Demo credentials
    with st.expander("Demo Credentials"):
        st.write("**Student:** username: student1, password: password123")
        st.write("**College:** username: college1, password: password123")
        st.write("**Company:** username: company1, password: password123")

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_type = None
    st.session_state.token = None
    st.rerun()

def require_auth():
    """Decorator to require authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not st.session_state.get('authenticated', False):
                st.warning("Please login to access this page")
                login_form()
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """Get current user from session"""
    return st.session_state.get('user')

def get_current_user_type():
    """Get current user type from session"""
    return st.session_state.get('user_type')
