"""
Smart Vision Detector - Main Streamlit Application
A full-stack AI Vision Web App for face and object detection
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from datetime import datetime

# Import our custom modules
from database import Database
from auth import AuthManager
from age_detector import AgeGenderDetector
from object_detector import ObjectDetector

# Page configuration
st.set_page_config(
    page_title="Smart Vision Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .face-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .object-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9ff;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class SmartVisionDetector:
    def __init__(self):
        self.db = Database()
        self.auth = AuthManager()
        self.age_detector = AgeGenderDetector()
        self.object_detector = ObjectDetector()
        
        # Initialize session state
        if 'detection_history' not in st.session_state:
            st.session_state.detection_history = []
    
    def render_header(self):
        """Render the main header"""
        st.markdown('<h1 class="main-header">🧠 Smart Vision Detector</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Advanced AI-powered vision detection for faces and objects
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        st.sidebar.markdown("## 🧭 Navigation")
        
        page = st.sidebar.radio(
            "Choose a page:",
            ["🏠 Home", "👨‍💼 Admin Panel"],
            index=0
        )
        
        st.sidebar.markdown("---")
        
        # Show detection stats
        stats = self.db.get_stats()
        st.sidebar.markdown("### 📊 Detection Stats")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Total Detections", stats['total_detections'])
        with col2:
            st.metric("Recent (7 days)", stats['recent_detections'])
        
        # Show detection types
        if stats['by_type']:
            st.sidebar.markdown("### 🔍 By Type")
            for detection_type, count in stats['by_type'].items():
                st.sidebar.write(f"**{detection_type.title()}**: {count}")
        
        return page
    
    def render_upload_section(self):
        """Render image upload section"""
        st.markdown("### 📸 Image Input")
        
        # Create tabs for different input methods
        tab1, tab2 = st.tabs(["📁 Upload Image", "📷 Webcam"])
        
        with tab1:
            st.markdown("""
            <div class="upload-area">
                <p>Upload an image file (JPG, PNG, JPEG)</p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=['jpg', 'jpeg', 'png'],
                help="Upload an image to detect faces or objects"
            )
            
            if uploaded_file is not None:
                return self.process_uploaded_image(uploaded_file)
        
        with tab2:
            st.markdown("### 📷 Webcam Capture")
            
            # Webcam capture
            webcam_image = st.camera_input("Take a picture with your webcam")
            
            if webcam_image is not None:
                return self.process_webcam_image(webcam_image)
        
        return None
    
    def process_uploaded_image(self, uploaded_file):
        """Process uploaded image"""
        try:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                with st.spinner("🔍 Analyzing image..."):
                    # Try face detection first
                    face_result = self.age_detector.process_image(uploaded_file)
                    
                    if face_result['has_face']:
                        return self.display_face_results(face_result, uploaded_file.name)
                    else:
                        # Try object detection
                        object_result = self.object_detector.process_image(uploaded_file)
                        return self.display_object_results(object_result, uploaded_file.name)
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None
    
    def process_webcam_image(self, webcam_image):
        """Process webcam captured image"""
        try:
            # Display the captured image
            image = Image.open(webcam_image)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Captured Image", use_column_width=True)
            
            with col2:
                with st.spinner("🔍 Analyzing image..."):
                    # Try face detection first
                    face_result = self.age_detector.process_image(webcam_image)
                    
                    if face_result['has_face']:
                        return self.display_face_results(face_result, f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                    else:
                        # Try object detection
                        object_result = self.object_detector.process_image(webcam_image)
                        return self.display_object_results(object_result, f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        
        except Exception as e:
            st.error(f"Error processing webcam image: {str(e)}")
            return None
    
    def display_face_results(self, face_result, filename):
        """Display face detection results"""
        st.markdown("### 🎭 Face Detection Results")
        
        if face_result['has_face']:
            for face in face_result['faces']:
                st.markdown(f"""
                <div class="face-card">
                    <h3>👤 Face #{face['face_id']}</h3>
                    <p><strong>Age:</strong> {face['age']} years old</p>
                    <p><strong>Gender:</strong> {face['gender']}</p>
                    <p><strong>Confidence:</strong> {face['confidence']:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Save to database
            result_text = f"Detected {len(face_result['faces'])} face(s)"
            self.db.add_detection(filename, "Human Face", result_text, 0.85)
            
            return {
                'type': 'face',
                'count': len(face_result['faces']),
                'results': face_result['faces']
            }
        else:
            st.warning("❌ No faces detected. Trying object detection...")
            return None
    
    def display_object_results(self, object_result, filename):
        """Display object detection results"""
        st.markdown("### 🎯 Object Detection Results")
        
        if object_result['success'] and object_result['predictions']:
            # Display top prediction prominently
            top_prediction = object_result['predictions'][0]
            
            st.markdown(f"""
            <div class="object-card">
                <h3>🎯 Primary Detection</h3>
                <p><strong>Object:</strong> {top_prediction['class']}</p>
                <p><strong>Confidence:</strong> {top_prediction['confidence']:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show additional predictions
            if len(object_result['predictions']) > 1:
                st.markdown("#### 🔍 Alternative Predictions")
                for i, pred in enumerate(object_result['predictions'][1:], 2):
                    st.markdown(f"""
                    <div class="result-card">
                        <p><strong>#{i}:</strong> {pred['class']} ({pred['confidence']:.1%})</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Save to database
            result_text = f"Detected: {top_prediction['class']} ({top_prediction['confidence']:.1%})"
            self.db.add_detection(filename, "Object", result_text, top_prediction['confidence'])
            
            return {
                'type': 'object',
                'primary': top_prediction,
                'alternatives': object_result['predictions'][1:]
            }
        else:
            st.error("❌ No objects detected or error in processing")
            return None
    
    def render_home_page(self):
        """Render the main home page"""
        self.render_header()
        
        # Upload section
        result = self.render_upload_section()
        
        # Display instructions if no image uploaded
        if result is None:
            st.markdown("""
            ### 🚀 How to Use Smart Vision Detector
            
            1. **Upload an Image**: Click "Browse files" to select an image from your device
            2. **Use Webcam**: Click the "Webcam" tab to capture an image with your camera
            3. **Get Results**: The AI will automatically detect faces or objects and provide predictions
            
            #### 🔍 What We Detect:
            - **Human Faces**: Age and gender prediction using advanced AI
            - **Objects**: Classification of everyday objects using MobileNetV2
            
            #### 💡 Tips for Best Results:
            - Use clear, well-lit images
            - Ensure faces are clearly visible for age/gender detection
            - For objects, make sure the main subject is in focus
            """)
    
    def render_admin_page(self):
        """Render the admin panel"""
        if not self.auth.require_auth():
            return
        
        st.markdown("# 👨‍💼 Admin Panel")
        
        # Welcome message
        st.success(f"Welcome back, {st.session_state.get('username', 'Admin')}!")
        
        # Logout button
        if st.button("🚪 Logout"):
            self.auth.logout()
        
        st.markdown("---")
        
        # Admin controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detection History")
            
            # Get detection history
            history = self.db.get_detection_history(20)
            
            if history:
                for record in history:
                    with st.expander(f"🔍 {record[1]} - {record[4].strftime('%Y-%m-%d %H:%M')}"):
                        st.write(f"**Type:** {record[2]}")
                        st.write(f"**Result:** {record[3]}")
                        st.write(f"**Confidence:** {record[4]:.2f}")
                        
                        if st.button(f"🗑️ Delete", key=f"delete_{record[0]}"):
                            self.db.delete_detection(record[0])
                            st.success("Record deleted!")
                            st.rerun()
            else:
                st.info("No detection history found.")
        
        with col2:
            st.markdown("### ⚙️ Admin Actions")
            
            # Clear all history
            if st.button("🧹 Clear All History", type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    self.db.clear_history()
                    st.success("All history cleared!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm clearing all history")
            
            # Download history
            if st.button("📥 Download History"):
                history = self.db.get_detection_history()
                if history:
                    # Create a simple CSV-like format
                    csv_data = "ID,Filename,Type,Result,Confidence,Timestamp\n"
                    for record in history:
                        csv_data += f"{record[0]},{record[1]},{record[2]},{record[3]},{record[4]},{record[5]}\n"
                    
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv_data,
                        file_name=f"detection_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No history to download")
            
            # Statistics
            stats = self.db.get_stats()
            st.markdown("### 📈 Statistics")
            st.metric("Total Detections", stats['total_detections'])
            st.metric("Recent Detections (7 days)", stats['recent_detections'])
            
            if stats['by_type']:
                st.markdown("#### By Detection Type:")
                for detection_type, count in stats['by_type'].items():
                    st.write(f"**{detection_type.title()}**: {count}")
    
    def run(self):
        """Main application runner"""
        page = self.render_sidebar()
        
        if page == "🏠 Home":
            self.render_home_page()
        elif page == "👨‍💼 Admin Panel":
            self.render_admin_page()

# Run the application
if __name__ == "__main__":
    app = SmartVisionDetector()
    app.run()
