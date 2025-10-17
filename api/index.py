"""
Smart Vision Detector - Vercel Compatible Version
Optimized for Vercel serverless deployment
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import json
from datetime import datetime
import random

app = FastAPI(title="Smart Vision Detector", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage for demo
detection_history = []

class SimpleFaceDetector:
    def __init__(self):
        # Simplified face detection without OpenCV for Vercel compatibility
        self.face_cascade = None
    
    def detect_faces(self, image):
        # Simulate face detection for demo purposes
        # In a real deployment, you'd use OpenCV or a cloud API
        height, width = image.shape[:2]
        
        # Simulate face detection based on image characteristics
        if width > 200 and height > 200:
            # Simulate finding 1-2 faces in larger images
            num_faces = random.randint(0, 2)
            faces = []
            for i in range(num_faces):
                x = random.randint(0, width//2)
                y = random.randint(0, height//2)
                w = random.randint(50, 150)
                h = random.randint(50, 150)
                faces.append([x, y, w, h])
            return faces
        return []

class SimpleObjectDetector:
    def __init__(self):
        self.object_categories = [
            'Dog', 'Cat', 'Car', 'Phone', 'Laptop', 'Book', 'Chair', 'Table',
            'Bottle', 'Cup', 'Person', 'Bicycle', 'Motorcycle', 'Bus', 'Train',
            'Airplane', 'Bird', 'Horse', 'Cow', 'Elephant', 'Bear', 'Zebra',
            'Giraffe', 'Backpack', 'Umbrella', 'Handbag', 'Tie', 'Suitcase',
            'Frisbee', 'Skis', 'Snowboard', 'Sports Ball', 'Kite', 'Baseball Bat',
            'Baseball Glove', 'Skateboard', 'Surfboard', 'Tennis Racket',
            'Camera', 'Watch', 'Sunglasses', 'Hat', 'Shoe', 'Shirt', 'Pants',
            'Dress', 'Coat', 'Gloves', 'Scarf', 'Belt', 'Necklace', 'Ring',
            'Earrings', 'Wallet', 'Key', 'Pen', 'Pencil', 'Notebook', 'Calculator'
        ]
    
    def predict_object(self, image):
        predictions = []
        for i in range(3):
            class_name = random.choice(self.object_categories)
            confidence = random.uniform(0.6, 0.95)
            predictions.append({
                'class': class_name,
                'confidence': confidence
            })
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        return predictions

# Initialize components
face_detector = SimpleFaceDetector()
object_detector = SimpleObjectDetector()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Vision Detector</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
            }
            .container { 
                max-width: 1200px; margin: 0 auto; 
                background: white; border-radius: 15px; 
                padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
            }
            .header { text-align: center; margin-bottom: 30px; }
            .header h1 { 
                font-size: 3rem; 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                margin: 0; 
            }
            .upload-area { 
                border: 2px dashed #667eea; border-radius: 10px; 
                padding: 40px; text-align: center; margin: 20px 0; 
                background: #f8f9ff; 
            }
            .btn { 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                color: white; border: none; padding: 12px 30px; 
                border-radius: 25px; cursor: pointer; font-size: 16px; 
                margin: 10px; transition: all 0.3s ease;
            }
            .btn:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
            }
            .result-card { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; border-radius: 15px; margin: 20px 0; 
            }
            .face-card { 
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                color: white; padding: 20px; border-radius: 15px; margin: 20px 0; 
            }
            .object-card { 
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                color: white; padding: 20px; border-radius: 15px; margin: 20px 0; 
            }
            .image-preview { max-width: 100%; border-radius: 10px; margin: 20px 0; }
            .loading { text-align: center; padding: 40px; }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; margin: 20px 0; 
            }
            .stat-card { 
                background: white; padding: 20px; border-radius: 10px; 
                text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.1); 
            }
            .demo-notice {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                color: #856404;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Smart Vision Detector</h1>
                <p>Advanced AI-powered vision detection for faces and objects</p>
            </div>
            
            <div class="demo-notice">
                <strong>🎯 Demo Mode:</strong> This is a simplified version optimized for Vercel deployment. 
                Face and object detection uses simulated AI for demonstration purposes.
            </div>
            
            <div class="upload-area">
                <h3>📸 Upload an Image</h3>
                <input type="file" id="imageInput" accept="image/*" style="margin: 20px 0;">
                <br>
                <button class="btn" onclick="analyzeImage()">🔍 Analyze Image</button>
            </div>
            
            <div id="imagePreview"></div>
            <div id="results"></div>
            <div id="loading" class="loading" style="display: none;">
                <h3>🔍 Analyzing image...</h3>
                <p>Processing with AI...</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📊 Total Detections</h3>
                    <p id="totalDetections">0</p>
                </div>
                <div class="stat-card">
                    <h3>🎭 Face Detections</h3>
                    <p id="faceDetections">0</p>
                </div>
                <div class="stat-card">
                    <h3>🎯 Object Detections</h3>
                    <p id="objectDetections">0</p>
                </div>
            </div>
        </div>

        <script>
            let imageData = null;
            
            document.getElementById('imageInput').addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        imageData = e.target.result;
                        document.getElementById('imagePreview').innerHTML = `
                            <h3>📷 Image Preview</h3>
                            <img src="${imageData}" class="image-preview" alt="Uploaded image">
                        `;
                    };
                    reader.readAsDataURL(file);
                }
            });
            
            async function analyzeImage() {
                if (!imageData) {
                    alert('Please select an image first!');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                
                try {
                    const response = await fetch(imageData);
                    const blob = await response.blob();
                    
                    const formData = new FormData();
                    formData.append('file', blob, 'image.jpg');
                    
                    const result = await fetch('/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await result.json();
                    displayResults(data);
                    updateStats();
                    
                } catch (error) {
                    document.getElementById('results').innerHTML = `
                        <div class="result-card">
                            <h3>❌ Error</h3>
                            <p>Failed to analyze image: ${error.message}</p>
                        </div>
                    `;
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            function displayResults(data) {
                let html = '';
                
                if (data.type === 'face') {
                    data.results.forEach((face, index) => {
                        html += `
                            <div class="face-card">
                                <h3>👤 Face #${index + 1}</h3>
                                <p><strong>Age:</strong> ${face.age} years old</p>
                                <p><strong>Gender:</strong> ${face.gender}</p>
                                <p><strong>Confidence:</strong> ${(face.confidence * 100).toFixed(1)}%</p>
                            </div>
                        `;
                    });
                } else if (data.type === 'object') {
                    html += `
                        <div class="object-card">
                            <h3>🎯 Primary Detection</h3>
                            <p><strong>Object:</strong> ${data.primary.class}</p>
                            <p><strong>Confidence:</strong> ${(data.primary.confidence * 100).toFixed(1)}%</p>
                        </div>
                    `;
                    
                    if (data.alternatives && data.alternatives.length > 0) {
                        html += '<h4>🔍 Alternative Predictions</h4>';
                        data.alternatives.forEach((alt, index) => {
                            html += `
                                <div class="result-card">
                                    <p><strong>#${index + 2}:</strong> ${alt.class} (${(alt.confidence * 100).toFixed(1)}%)</p>
                                </div>
                            `;
                        });
                    }
                }
                
                document.getElementById('results').innerHTML = html;
            }
            
            async function updateStats() {
                try {
                    const response = await fetch('/stats');
                    const stats = await response.json();
                    
                    document.getElementById('totalDetections').textContent = stats.total_detections;
                    document.getElementById('faceDetections').textContent = stats.face_detections;
                    document.getElementById('objectDetections').textContent = stats.object_detections;
                } catch (error) {
                    console.error('Failed to update stats:', error);
                }
            }
            
            updateStats();
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = np.array(image)
        
        faces = face_detector.detect_faces(image_array)
        
        if len(faces) > 0:
            face_results = []
            for i, (x, y, w, h) in enumerate(faces):
                age = random.randint(20, 65)
                gender = random.choice(['Male', 'Female'])
                confidence = random.uniform(0.7, 0.95)
                
                face_results.append({
                    'face_id': i + 1,
                    'coordinates': [int(x), int(y), int(w), int(h)],
                    'age': age,
                    'gender': gender,
                    'confidence': confidence
                })
            
            # Store detection
            detection_history.append({
                'filename': file.filename,
                'type': 'Human Face',
                'result': f"Detected {len(faces)} face(s)",
                'confidence': 0.85,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'type': 'face',
                'count': len(faces),
                'results': face_results
            }
        else:
            predictions = object_detector.predict_object(image)
            
            if predictions:
                top_prediction = predictions[0]
                
                # Store detection
                detection_history.append({
                    'filename': file.filename,
                    'type': 'Object',
                    'result': f"Detected: {top_prediction['class']}",
                    'confidence': top_prediction['confidence'],
                    'timestamp': datetime.now().isoformat()
                })
                
                return {
                    'type': 'object',
                    'primary': top_prediction,
                    'alternatives': predictions[1:]
                }
            else:
                raise HTTPException(status_code=400, detail="No faces or objects detected")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        total = len(detection_history)
        face_count = sum(1 for h in detection_history if h['type'] == "Human Face")
        object_count = sum(1 for h in detection_history if h['type'] == "Object")
        
        return {
            'total_detections': total,
            'face_detections': face_count,
            'object_detections': object_count
        }
    except Exception as e:
        return {'total_detections': 0, 'face_detections': 0, 'object_detections': 0}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Smart Vision Detector is running!"}

# Vercel handler
handler = app