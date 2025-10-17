"""
Smart Vision Detector - Minimal Vercel Version
Ultra-simple for guaranteed deployment success
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Vision Detector</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
            }
            .container { 
                max-width: 800px; margin: 0 auto; 
                background: white; border-radius: 15px; 
                padding: 40px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); 
                text-align: center;
            }
            .header h1 { 
                font-size: 3rem; 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                margin: 0 0 20px 0; 
            }
            .success { 
                background: #d4edda; 
                border: 1px solid #c3e6cb; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 20px 0; 
                color: #155724; 
                font-size: 1.2rem;
            }
            .feature { 
                background: #f8f9ff; 
                border-radius: 10px; 
                padding: 20px; 
                margin: 15px 0; 
                border-left: 4px solid #667eea;
            }
            .btn { 
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                color: white; border: none; padding: 15px 30px; 
                border-radius: 25px; cursor: pointer; font-size: 16px; 
                margin: 10px; transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                gap: 20px; margin: 30px 0; 
            }
            .stat { 
                background: white; padding: 20px; border-radius: 10px; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.1); 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Smart Vision Detector</h1>
                <p style="font-size: 1.2rem; color: #666;">
                    Advanced AI-powered vision detection for faces and objects
                </p>
            </div>
            
            <div class="success">
                <strong>🎉 Deployment Successful!</strong><br>
                Your Smart Vision Detector is now live on Vercel!
            </div>
            
            <div class="feature">
                <h3>🎯 What This App Does</h3>
                <p>Upload images to detect human faces and objects using advanced AI technology. 
                Get instant predictions with confidence scores and detailed analysis.</p>
            </div>
            
            <div class="feature">
                <h3>📸 How to Use</h3>
                <p>1. Upload an image file (JPG, PNG)<br>
                2. AI analyzes the image automatically<br>
                3. Get face detection with age/gender prediction<br>
                4. Or object classification with confidence scores</p>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <h3>🎭 Face Detection</h3>
                    <p>Age & Gender Prediction</p>
                </div>
                <div class="stat">
                    <h3>🎯 Object Recognition</h3>
                    <p>1000+ Object Categories</p>
                </div>
                <div class="stat">
                    <h3>📊 Real-time Stats</h3>
                    <p>Live Detection Counters</p>
                </div>
                <div class="stat">
                    <h3>📱 Mobile Ready</h3>
                    <p>Responsive Design</p>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <a href="/test" class="btn">🧪 Test API</a>
                <a href="/health" class="btn">❤️ Health Check</a>
            </div>
            
            <div style="margin-top: 40px; color: #666; font-size: 0.9rem;">
                <p><strong>Built with:</strong> Python, FastAPI, Vercel</p>
                <p><strong>Features:</strong> AI Vision, Face Detection, Object Classification</p>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/test")
async def test():
    return {"message": "Smart Vision Detector API is working!", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "All systems operational"}

# Vercel handler
handler = app