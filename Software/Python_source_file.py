Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import pandas as pd
... from sklearn.model_selection import train_test_split
... from sklearn.preprocessing import LabelEncoder, StandardScaler
... from tensorflow import keras
... from tensorflow.keras import layers
... import matplotlib.pyplot as plt
... import numpy as np
... 
... # Load the dataset from CSV
... data = pd.read_csv("/content/drive/MyDrive/dataset.csv")
... 
... # Split dataset into features (X) and target (y)
... X = data.drop(columns=['GESTURE'])
... y = data['GESTURE']
... 
... # Encode categorical target variable
... label_encoder = LabelEncoder()
... y_encoded = label_encoder.fit_transform(y)
... 
... # Normalize input features
... scaler = StandardScaler()
... X_scaled = scaler.fit_transform(X)
... 
... # Split data into train and test sets
... X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)
... 
... # Building the Model
... model = keras.Sequential([
...     layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
...     layers.Dropout(0.5),  # Adding dropout for regularization
...     layers.Dense(128, activation='relu'),
...     layers.Dropout(0.5),  # Adding dropout for regularization
...     layers.Dense(64, activation='relu'),
...     layers.Dense(len(label_encoder.classes_), activation='softmax')  # Output layer with softmax activation for multi-class classification
... ])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Using sparse categorical cross-entropy for multi-class classification
              metrics=['accuracy'])

# Training the Model
history = model.fit(X_train, y_train, epochs=50, batch_size=64, validation_split=0.2)

# Smoothing the training curves using exponential moving averages (EMA)
def smooth_curve(points, factor=0.8):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

smoothed_accuracy = smooth_curve(history.history['accuracy'])
smoothed_val_accuracy = smooth_curve(history.history['val_accuracy'])

# Plotting Smoothed Accuracy Graph
plt.plot(range(1, len(smoothed_accuracy) + 1), smoothed_accuracy, label='accuracy')
plt.plot(range(1, len(smoothed_val_accuracy) + 1), smoothed_val_accuracy, label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

# Evaluating the Model on Test Data
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')
