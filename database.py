"""
Database module for storing emotion detection results.
Stores: user names, uploaded/captured images, and model predictions.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

DATABASE_NAME = "emotion_detection_results.db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

def init_database():
    """Initialize database with required schema."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create table for storing detection results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            detected_emotion TEXT NOT NULL,
            confidence REAL,
            detection_method TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_detection(user_name, image_path, detected_emotion, confidence=None, detection_method='webcam', notes=''):
    """
    Insert a new emotion detection record into the database.
    
    Args:
        user_name (str): Name of the user
        image_path (str): Path to the image file
        detected_emotion (str): Detected emotion label
        confidence (float): Confidence score of prediction (0-1)
        detection_method (str): Either 'webcam' or 'upload'
        notes (str): Additional notes
    
    Returns:
        int: ID of inserted record or None if failed
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO emotion_detections 
            (user_name, image_path, detected_emotion, confidence, detection_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_name, image_path, detected_emotion, confidence, detection_method, notes))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_detections(user_name=None, limit=50):
    """
    Retrieve emotion detection records from database.
    
    Args:
        user_name (str): Filter by user name (optional)
        limit (int): Maximum number of records to retrieve
    
    Returns:
        list: List of detection records
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if user_name:
            cursor.execute('''
                SELECT * FROM emotion_detections 
                WHERE user_name = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (user_name, limit))
        else:
            cursor.execute('''
                SELECT * FROM emotion_detections 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        records = cursor.fetchall()
        conn.close()
        
        return records
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def get_emotion_statistics(user_name=None):
    """
    Get emotion statistics from database.
    
    Args:
        user_name (str): Filter by user name (optional)
    
    Returns:
        dict: Dictionary with emotion counts
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if user_name:
            cursor.execute('''
                SELECT detected_emotion, COUNT(*) as count 
                FROM emotion_detections 
                WHERE user_name = ? 
                GROUP BY detected_emotion 
                ORDER BY count DESC
            ''', (user_name,))
        else:
            cursor.execute('''
                SELECT detected_emotion, COUNT(*) as count 
                FROM emotion_detections 
                GROUP BY detected_emotion 
                ORDER BY count DESC
            ''')
        
        stats = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return stats
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return {}

def delete_detection(record_id):
    """Delete a detection record by ID."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM emotion_detections WHERE id = ?', (record_id,))
        
        conn.commit()
        conn.close()
        
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

# Initialize database on module import
if not os.path.exists(DATABASE_PATH):
    init_database()
