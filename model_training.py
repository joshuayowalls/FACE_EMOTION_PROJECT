import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Paths
data_dir = "datasets/train"  # Path to your training images
img_size = 48
batch_size = 32

# Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    data_dir, target_size=(img_size, img_size), color_mode='grayscale',
    batch_size=batch_size, class_mode='categorical', subset='training'
)

val_gen = datagen.flow_from_directory(
    data_dir, target_size=(img_size, img_size), color_mode='grayscale',
    batch_size=batch_size, class_mode='categorical', subset='validation'
)

# CNN Model
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')  # 7 emotions
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_gen, validation_data=val_gen, epochs=25)

model.save("face_emotions_model.h5")
print(" Model training completed and saved.")
