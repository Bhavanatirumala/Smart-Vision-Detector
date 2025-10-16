# 🧠 Smart Vision Detector

A full-stack AI Vision Web Application built with Python and Streamlit that can detect human faces and objects in images using advanced machine learning models.

## ✨ Features

### 🎯 Core Functionality
- **Human Face Detection**: Uses OpenCV for face detection
- **Age & Gender Prediction**: Leverages DeepFace for accurate age and gender estimation
- **Object Classification**: Utilizes MobileNetV2 for object recognition and classification
- **Webcam Support**: Real-time image capture and analysis
- **Image Upload**: Support for JPG, JPEG, and PNG formats

### 👨‍💼 Admin Panel
- **Secure Authentication**: Password-protected admin access with bcrypt hashing
- **Detection History**: View all past detections with timestamps
- **Statistics Dashboard**: Comprehensive analytics and metrics
- **History Management**: Delete individual records or clear entire history
- **Data Export**: Download detection history as CSV

### 🎨 Modern UI
- **Responsive Design**: Clean, modern interface with gradient backgrounds
- **Card-based Results**: Beautiful result cards with confidence scores
- **Progress Indicators**: Loading spinners during AI processing
- **Sidebar Navigation**: Easy switching between Home and Admin panels
- **Mobile-friendly**: Responsive design for all device sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd Smart\ Vision\ Detector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically open in your default browser

## 📁 Project Structure

```
Smart Vision Detector/
├── app.py                  # Main Streamlit application
├── auth.py                 # Admin authentication system
├── age_detector.py         # Human face detection and age/gender prediction
├── object_detector.py      # Object classification using MobileNetV2
├── database.py             # SQLite database operations
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── smart_vision.db        # SQLite database (created automatically)
```

## 🔧 Configuration

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

> ⚠️ **Security Note**: Change the default password in production environments by modifying the database directly or updating the `database.py` file.

### Environment Variables (Optional)
You can set these environment variables for additional configuration:
- `DB_PATH`: Custom database file path (default: `smart_vision.db`)
- `ADMIN_USERNAME`: Custom admin username
- `ADMIN_PASSWORD`: Custom admin password

## 🎯 How to Use

### For End Users

1. **Upload an Image**
   - Click "Browse files" to select an image from your device
   - Supported formats: JPG, JPEG, PNG

2. **Use Webcam**
   - Switch to the "Webcam" tab
   - Click "Take a picture" to capture with your camera

3. **View Results**
   - The AI will automatically detect faces or objects
   - For faces: See age, gender, and confidence scores
   - For objects: See classification with confidence percentages

### For Administrators

1. **Access Admin Panel**
   - Use the sidebar navigation to go to "Admin Panel"
   - Login with admin credentials

2. **View Detection History**
   - See all past detections with timestamps
   - View statistics and analytics

3. **Manage Data**
   - Delete individual detection records
   - Clear entire detection history
   - Download history as CSV file

## 🛠️ Technical Details

### AI Models Used

1. **Face Detection**: OpenCV Haar Cascade Classifier
2. **Age/Gender Prediction**: DeepFace with VGG-Face model
3. **Object Classification**: TensorFlow MobileNetV2 with ImageNet weights

### Database Schema

**detection_history table:**
- `id`: Primary key
- `filename`: Name of the processed file
- `detection_type`: Type of detection (Human Face/Object)
- `result`: Detection results
- `confidence`: Confidence score
- `timestamp`: When the detection was made

**admin_users table:**
- `id`: Primary key
- `username`: Admin username
- `password_hash`: Bcrypt hashed password
- `created_at`: Account creation timestamp

### Performance Considerations

- **Face Detection**: Optimized for real-time processing
- **Object Classification**: Uses lightweight MobileNetV2 for fast inference
- **Database**: SQLite for simple deployment and data persistence
- **Memory**: Efficient image preprocessing to minimize memory usage

## 🔒 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Streamlit session state for authentication
- **Input Validation**: File type and size validation
- **SQL Injection Protection**: Parameterized queries

## 🐛 Troubleshooting

### Common Issues

1. **Model Download Issues**
   ```
   Error: Unable to download DeepFace models
   Solution: Ensure stable internet connection for initial model download
   ```

2. **Memory Issues**
   ```
   Error: Out of memory during processing
   Solution: Try with smaller images or restart the application
   ```

3. **Camera Access**
   ```
   Error: Cannot access webcam
   Solution: Grant camera permissions in your browser
   ```

### Performance Tips

- Use images under 2MB for faster processing
- Ensure good lighting for face detection
- Close other applications to free up system resources

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 2GB free space
- **CPU**: Dual-core processor
- **Python**: 3.8+

### Recommended Requirements
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **CPU**: Quad-core processor
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **OpenCV**: For computer vision capabilities
- **DeepFace**: For facial analysis
- **TensorFlow**: For deep learning models
- **ImageNet**: For object classification training data

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the error messages in the console
3. Ensure all dependencies are correctly installed
4. Verify your Python version compatibility

---

**Made with ❤️ using Python, Streamlit, and AI**
