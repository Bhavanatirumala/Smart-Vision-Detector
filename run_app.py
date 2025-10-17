"""
Simple script to run the Smart Vision Detector app
"""
import subprocess
import sys
import os

def run_streamlit_app():
    """Run the Streamlit app"""
    try:
        print("🚀 Starting Smart Vision Detector...")
        print("📱 The app will open at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the app")
        print("-" * 50)
        
        # Run streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app_simple.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.runOnSave", "true"
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Python is installed")
        print("2. Install requirements: pip install streamlit opencv-python pillow bcrypt pandas")
        print("3. Try running: python -m streamlit run app_simple.py")

if __name__ == "__main__":
    run_streamlit_app()
