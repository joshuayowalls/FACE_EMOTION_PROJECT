"""
Emotion Detection Model Training Script
This module trains a CNN model to detect human emotions from facial expressions.
Model Architecture: Convolutional Neural Network with dropout regularization
Supported Emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral (7 classes)
Input Shape: 48x48 grayscale images
Output: Emotion class prediction
"""

try:
    # Prefer tensorflow.keras (bundled with TensorFlow)
    # Assign names from tf.keras to avoid direct "from tensorflow.keras.*" static import issues
    from tensorflow import keras # type: ignore
    Sequential = keras.models.Sequential
    Conv2D = keras.layers.Conv2D
    MaxPooling2D = keras.layers.MaxPooling2D
    Flatten = keras.layers.Flatten
    Dense = keras.layers.Dense
    Dropout = keras.layers.Dropout
    ImageDataGenerator = keras.preprocessing.image.ImageDataGenerator
    EarlyStopping = keras.callbacks.EarlyStopping
    ReduceLROnPlateau = keras.callbacks.ReduceLROnPlateau
except Exception:
    # Fallback to standalone Keras if tensorflow.keras is not available
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from keras.preprocessing.image import ImageDataGenerator # type: ignore
    from keras.callbacks import EarlyStopping, ReduceLROnPlateau

import os
import sys

# Configuration
DATA_DIR = "datasets/train"  # Path to your training images
IMG_SIZE = 48
BATCH_SIZE = 32
EPOCHS = 25
MODEL_OUTPUT_PATH = "face_emotions_model.h5"

# Emotion labels
EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
NUM_EMOTIONS = len(EMOTION_LABELS)

def build_model(img_size=IMG_SIZE, num_classes=NUM_EMOTIONS):
    """
    Build CNN model for emotion detection.
    
    Args:
        img_size (int): Input image size (default: 48)
        num_classes (int): Number of emotion classes (default: 7)
    
    Returns:
        Sequential: Compiled Keras model
    """
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def prepare_data(data_dir, img_size=IMG_SIZE, batch_size=BATCH_SIZE):
    """
    Prepare training and validation data generators.
    
    Args:
        data_dir (str): Path to training data directory
        img_size (int): Target image size
        batch_size (int): Batch size for training
    
    Returns:
        tuple: (train_generator, val_generator)
    """
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        horizontal_flip=True,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        validation_split=0.2
    )
    
    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        color_mode='grayscale',
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        color_mode='grayscale',
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    return train_gen, val_gen

def train_model(model, train_gen, val_gen, epochs=EPOCHS):
    """
    Train the emotion detection model.
    
    Args:
        model (Sequential): Keras model to train
        train_gen: Training data generator
        val_gen: Validation data generator
        epochs (int): Number of training epochs
    
    Returns:
        History: Training history object
    """
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7)
    ]
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    return history

def main():
    """Main function to orchestrate model training."""
    try:
        # Check if data directory exists
        if not os.path.exists(DATA_DIR):
            print(f"Error: Data directory '{DATA_DIR}' not found!")
            print("Please ensure your training data is in the 'datasets/train' directory")
            print("Directory structure should be: datasets/train/emotion_class/images/")
            sys.exit(1)
        
        print("=" * 60)
        print("Emotion Detection Model Training")
        print("=" * 60)
        print(f"Emotion Classes: {', '.join(EMOTION_LABELS)}")
        print(f"Image Size: {IMG_SIZE}x{IMG_SIZE}")
        print(f"Batch Size: {BATCH_SIZE}")
        print(f"Epochs: {EPOCHS}")
        print("=" * 60)
        
        # Build model
        print("\n[1/3] Building model architecture...")
        model = build_model(IMG_SIZE, NUM_EMOTIONS)
        print(f"Model built successfully!")
        print(model.summary())
        
        # Prepare data
        print("\n[2/3] Preparing training and validation data...")
        train_gen, val_gen = prepare_data(DATA_DIR, IMG_SIZE, BATCH_SIZE)
        print(f"Training samples: {train_gen.samples}")
        print(f"Validation samples: {val_gen.samples}")
        
        # Train model
        print("\n[3/3] Training model...")
        history = train_model(model, train_gen, val_gen, EPOCHS)
        
        # Save model
        print(f"\nSaving model to '{MODEL_OUTPUT_PATH}'...")
        model.save(MODEL_OUTPUT_PATH)
        print(f"✓ Model training completed and saved successfully!")
        
        # Print final metrics
        print("\n" + "=" * 60)
        print("Training Summary:")
        print(f"Final Training Accuracy: {history.history['accuracy'][-1]:.4f}")
        print(f"Final Validation Accuracy: {history.history['val_accuracy'][-1]:.4f}")
        print(f"Final Training Loss: {history.history['loss'][-1]:.4f}")
        print(f"Final Validation Loss: {history.history['val_loss'][-1]:.4f}")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
