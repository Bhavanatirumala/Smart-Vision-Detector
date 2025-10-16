"""
Authentication module for Smart Vision Detector
Handles admin login and session management
"""

import streamlit as st
from database import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
    
    def login_form(self):
        """Display login form"""
        st.subheader("🔐 Admin Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if self.db.verify_admin(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        # Show default credentials for demo
        st.info("""
        **Demo Credentials:**
        - Username: `admin`
        - Password: `admin123`
        """)
    
    def logout(self):
        """Logout admin user"""
        if 'authenticated' in st.session_state:
            del st.session_state['authenticated']
        if 'username' in st.session_state:
            del st.session_state['username']
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def require_auth(self):
        """Require authentication, redirect to login if not authenticated"""
        if not self.is_authenticated():
            st.error("🔒 Access denied. Please login to access admin panel.")
            self.login_form()
            return False
        return True
