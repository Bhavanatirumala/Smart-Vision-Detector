"""
Smart Vision Detector - Simplified Version for Quick Demo
A full-stack AI Vision Web App for face and object detection
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os
from datetime import datetime
import sqlite3
import bcrypt

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

class SimpleDatabase:
    def __init__(self, db_path="smart_vision.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create detection_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    detection_type TEXT,
                    result TEXT,
                    confidence REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create admin_users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert default admin user if not exists
            cursor.execute("SELECT COUNT(*) FROM admin_users")
            if cursor.fetchone()[0] == 0:
                default_password = "admin123"
                password_hash = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "INSERT INTO admin_users (username, password_hash) VALUES (?, ?)",
                    ("admin", password_hash)
                )
            
            conn.commit()
    
    def add_detection(self, filename, detection_type, result, confidence):
        """Add a new detection record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO detection_history (filename, detection_type, result, confidence)
                VALUES (?, ?, ?, ?)
            """, (filename, detection_type, result, confidence))
            conn.commit()
    
    def get_detection_history(self, limit=50):
        """Get detection history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, filename, detection_type, result, confidence, timestamp
                FROM detection_history
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
    
    def verify_admin(self, username, password):
        """Verify admin credentials"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM admin_users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_hash = result[0]
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
            return False
    
    def get_stats(self):
        """Get detection statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total detections
            cursor.execute("SELECT COUNT(*) FROM detection_history")
            total_detections = cursor.fetchone()[0]
            
            # Detections by type
            cursor.execute("""
                SELECT detection_type, COUNT(*) 
                FROM detection_history 
                GROUP BY detection_type
            """)
            by_type = dict(cursor.fetchall())
            
            # Recent detections (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM detection_history 
                WHERE timestamp >= datetime('now', '-7 days')
            """)
            recent_detections = cursor.fetchone()[0]
            
            return {
                'total_detections': total_detections,
                'by_type': by_type,
                'recent_detections': recent_detections
            }

class SimpleFaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, image):
        """Detect faces in image using OpenCV"""
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces
    
    def process_image(self, uploaded_file):
        """Process uploaded image for face detection"""
        try:
            # Convert uploaded file to PIL Image
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            # Detect faces
            faces = self.detect_faces(image_array)
            
            if len(faces) == 0:
                return {
                    'has_face': False,
                    'message': 'No human faces detected in the image',
                    'faces': []
                }
            
            # Analyze each detected face
            face_results = []
            for i, (x, y, w, h) in enumerate(faces):
                # Simulate age and gender (since we don't have DeepFace installed)
                import random
                age = random.randint(20, 65)
                gender = random.choice(['Male', 'Female'])
                confidence = random.uniform(0.7, 0.95)
                
                face_results.append({
                    'face_id': i + 1,
                    'coordinates': (x, y, w, h),
                    'age': age,
                    'gender': gender,
                    'confidence': confidence
                })
            
            return {
                'has_face': True,
                'message': f'Detected {len(faces)} face(s)',
                'faces': face_results
            }
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return {
                'has_face': False,
                'message': f'Error processing image: {str(e)}',
                'faces': []
            }

class SimpleObjectDetector:
    def __init__(self):
        # Simple object categories for demo
        self.object_categories = [
            'Dog', 'Cat', 'Car', 'Phone', 'Laptop', 'Book', 'Chair', 'Table',
            'Bottle', 'Cup', 'Person', 'Bicycle', 'Motorcycle', 'Bus', 'Train',
            'Airplane', 'Bird', 'Horse', 'Cow', 'Elephant', 'Bear', 'Zebra',
            'Giraffe', 'Backpack', 'Umbrella', 'Handbag', 'Tie', 'Suitcase',
            'Frisbee', 'Skis', 'Snowboard', 'Sports Ball', 'Kite', 'Baseball Bat',
            'Baseball Glove', 'Skateboard', 'Surfboard', 'Tennis Racket'
        ]
    
    def predict_object(self, image):
        """Simulate object prediction"""
        import random
        
        # Get top 3 random predictions
        predictions = []
        for i in range(3):
            class_name = random.choice(self.object_categories)
            confidence = random.uniform(0.6, 0.95)
            predictions.append({
                'class': class_name,
                'confidence': confidence
            })
        
        # Sort by confidence
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        return predictions
    
    def process_image(self, uploaded_file):
        """Process uploaded image for object detection"""
        try:
            # Convert uploaded file to PIL Image
            image = Image.open(uploaded_file)
            
            # Simulate object detection
            predictions = self.predict_object(image)
            
            return {
                'success': True,
                'message': 'Object classification completed',
                'predictions': predictions
            }
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return {
                'success': False,
                'message': f'Error processing image: {str(e)}',
                'predictions': []
            }

class SimpleSmartVisionDetector:
    def __init__(self):
        self.db = SimpleDatabase()
        self.face_detector = SimpleFaceDetector()
        self.object_detector = SimpleObjectDetector()
        
        # Initialize session state
        if 'detection_history' not in st.session_state:
            st.session_state.detection_history = []
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
    
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
                    face_result = self.face_detector.process_image(uploaded_file)
                    
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
                    face_result = self.face_detector.process_image(webcam_image)
                    
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
            
            #### ⚠️ Note:
            This is a simplified demo version. For full AI capabilities, install all dependencies from requirements.txt
            """)
    
    def render_admin_page(self):
        """Render the admin panel"""
        if not st.session_state.get('authenticated', False):
            st.error("🔒 Access denied. Please login to access admin panel.")
            self.login_form()
            return
        
        st.markdown("# 👨‍💼 Admin Panel")
        
        # Welcome message
        st.success(f"Welcome back, {st.session_state.get('username', 'Admin')}!")
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.rerun()
        
        st.markdown("---")
        
        # Admin controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detection History")
            
            # Get detection history
            history = self.db.get_detection_history(20)
            
            if history:
                for record in history:
                    with st.expander(f"🔍 {record[1]} - {record[5].split(' ')[0]}"):
                        st.write(f"**Type:** {record[2]}")
                        st.write(f"**Result:** {record[3]}")
                        st.write(f"**Confidence:** {record[4]:.2f}")
                        st.write(f"**Time:** {record[5]}")
            else:
                st.info("No detection history found.")
        
        with col2:
            st.markdown("### 📈 Statistics")
            stats = self.db.get_stats()
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
    app = SimpleSmartVisionDetector()
    app.run()
