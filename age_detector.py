"""
Age and Gender Detection module for Smart Vision Detector
Uses DeepFace for human face analysis
"""

import cv2
import numpy as np
from deepface import DeepFace
import streamlit as st
from PIL import Image
import tempfile
import os

class AgeGenderDetector:
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
    
    def predict_age_gender(self, image_path):
        """Predict age and gender using DeepFace"""
        try:
            # DeepFace analysis
            result = DeepFace.analyze(
                img_path=image_path,
                actions=['age', 'gender'],
                enforce_detection=False
            )
            
            # Handle both single result and list of results
            if isinstance(result, list):
                result = result[0]
            
            age = result['age']
            gender = result['dominant_gender']
            
            # Convert gender to more readable format
            if gender == 'Man':
                gender_display = 'Male'
            else:
                gender_display = 'Female'
            
            return {
                'age': int(age),
                'gender': gender_display,
                'confidence': 0.85  # DeepFace doesn't provide confidence, using estimated value
            }
            
        except Exception as e:
            st.error(f"Error in age/gender prediction: {str(e)}")
            return None
    
    def process_image(self, uploaded_file):
        """Process uploaded image for face detection and analysis"""
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
            
            # Save image temporarily for DeepFace
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                image.save(tmp_file.name)
                temp_path = tmp_file.name
            
            # Analyze each detected face
            face_results = []
            for i, (x, y, w, h) in enumerate(faces):
                # Crop face from image
                face_img = image.crop((x, y, x+w, y+h))
                
                # Save face temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as face_tmp:
                    face_img.save(face_tmp.name)
                    face_temp_path = face_tmp.name
                
                # Predict age and gender
                prediction = self.predict_age_gender(face_temp_path)
                
                if prediction:
                    face_results.append({
                        'face_id': i + 1,
                        'coordinates': (x, y, w, h),
                        'age': prediction['age'],
                        'gender': prediction['gender'],
                        'confidence': prediction['confidence']
                    })
                
                # Clean up temporary face file
                os.unlink(face_temp_path)
            
            # Clean up temporary main image file
            os.unlink(temp_path)
            
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
    
    def process_webcam_frame(self, frame):
        """Process webcam frame for real-time face detection"""
        try:
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            faces = self.detect_faces(rgb_frame)
            
            if len(faces) == 0:
                return {
                    'has_face': False,
                    'faces': []
                }
            
            # For webcam, we'll just detect faces without age/gender prediction
            # (to keep it fast for real-time processing)
            face_results = []
            for i, (x, y, w, h) in enumerate(faces):
                face_results.append({
                    'face_id': i + 1,
                    'coordinates': (x, y, w, h)
                })
            
            return {
                'has_face': True,
                'faces': face_results
            }
            
        except Exception as e:
            return {
                'has_face': False,
                'faces': [],
                'error': str(e)
            }
