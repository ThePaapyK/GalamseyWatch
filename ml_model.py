import tensorflow as tf
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

class GalamseyMLModel:
    def __init__(self):
        self.rf_model = None
        self.cnn_model = None
        
    def create_cnn_model(self, input_shape=(64, 64, 8)):
        """Create CNN model for satellite image classification"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.cnn_model = model
        return model
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest on tabular features"""
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.rf_model.fit(X_train, y_train)
        return self.rf_model
    
    def train_cnn(self, X_train, y_train, X_val, y_val, epochs=50):
        """Train CNN on satellite image patches"""
        if self.cnn_model is None:
            self.create_cnn_model(X_train.shape[1:])
        
        history = self.cnn_model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
            ]
        )
        
        return history
    
    def predict_galamsey(self, features, image_patches=None):
        """Ensemble prediction using both RF and CNN"""
        predictions = []
        
        # Random Forest prediction on tabular features
        if self.rf_model and features is not None:
            rf_pred = self.rf_model.predict_proba(features)[:, 1]
            predictions.append(rf_pred)
        
        # CNN prediction on image patches
        if self.cnn_model and image_patches is not None:
            cnn_pred = self.cnn_model.predict(image_patches).flatten()
            predictions.append(cnn_pred)
        
        # Ensemble average
        if len(predictions) > 1:
            final_pred = np.mean(predictions, axis=0)
        else:
            final_pred = predictions[0]
        
        return final_pred
    
    def save_models(self, rf_path='models/rf_model.pkl', cnn_path='models/cnn_model.h5'):
        """Save trained models"""
        if self.rf_model:
            joblib.dump(self.rf_model, rf_path)
        
        if self.cnn_model:
            self.cnn_model.save(cnn_path)
    
    def load_models(self, rf_path='models/rf_model.pkl', cnn_path='models/cnn_model.h5'):
        """Load pre-trained models"""
        try:
            self.rf_model = joblib.load(rf_path)
        except:
            print("RF model not found")
        
        try:
            self.cnn_model = tf.keras.models.load_model(cnn_path)
        except:
            print("CNN model not found")

def prepare_training_data():
    """Prepare training data from known galamsey sites"""
    # Known galamsey locations in Ghana
    galamsey_sites = [
        {"lat": 6.2027, "lon": -1.6640, "label": 1},  # Obuasi
        {"lat": 5.3006, "lon": -1.9959, "label": 1},  # Tarkwa
        {"lat": 5.9667, "lon": -1.7833, "label": 1},  # Dunkwa
        {"lat": 5.4333, "lon": -2.1333, "label": 1},  # Prestea
    ]
    
    # Non-mining control sites
    control_sites = [
        {"lat": 7.9465, "lon": -1.0232, "label": 0},  # Accra
        {"lat": 9.4034, "lon": -0.8424, "label": 0},  # Tamale
        {"lat": 5.6037, "lon": -0.1870, "label": 0},  # Tema
    ]
    
    return galamsey_sites + control_sites