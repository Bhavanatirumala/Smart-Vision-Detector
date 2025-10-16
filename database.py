"""
Database module for Smart Vision Detector
Handles SQLite database operations for detection history and admin authentication
"""

import sqlite3
import bcrypt
from datetime import datetime
import os

class Database:
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
    
    def delete_detection(self, detection_id):
        """Delete a specific detection record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detection_history WHERE id = ?", (detection_id,))
            conn.commit()
    
    def clear_history(self):
        """Clear all detection history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detection_history")
            conn.commit()
    
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
