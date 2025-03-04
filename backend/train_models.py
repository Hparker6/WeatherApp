import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import pandas as pd
from datetime import datetime, timedelta

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic weather data for training
    """
    np.random.seed(42)
    
    # Generate features
    base_temp = np.random.normal(15, 5, n_samples)  # Base temperature
    humidity = np.random.uniform(30, 90, n_samples)
    pressure = np.random.normal(1013, 10, n_samples)
    wind_speed = np.random.exponential(5, n_samples)
    
    # Generate target variables with some realistic relationships
    temp_high = base_temp + np.random.normal(5, 2, n_samples) + 0.1 * humidity
    temp_low = base_temp - np.random.normal(5, 2, n_samples) - 0.05 * humidity
    
    # Rain probability (binary for now)
    rain = (humidity > 70) & (pressure < 1010) | (wind_speed > 10)
    rain = rain.astype(int)
    
    # Create feature matrix
    X = np.column_stack([base_temp, humidity, pressure, wind_speed])
    
    return X, temp_high, temp_low, rain

def train_models():
    # Generate synthetic data
    X, temp_high, temp_low, rain = generate_synthetic_data()
    
    # Split data
    X_train, X_test, high_train, high_test, low_train, low_test, rain_train, rain_test = train_test_split(
        X, temp_high, temp_low, rain, test_size=0.2, random_state=42
    )
    
    # Train temperature high model
    high_model = RandomForestRegressor(n_estimators=100, random_state=42)
    high_model.fit(X_train, high_train)
    
    # Train temperature low model
    low_model = RandomForestRegressor(n_estimators=100, random_state=42)
    low_model.fit(X_train, low_train)
    
    # Train rain probability model
    rain_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rain_model.fit(X_train, rain_train)
    
    # Evaluate models
    print("Temperature High RMSE:", np.sqrt(mean_squared_error(high_test, high_model.predict(X_test))))
    print("Temperature Low RMSE:", np.sqrt(mean_squared_error(low_test, low_model.predict(X_test))))
    print("Rain Prediction Accuracy:", accuracy_score(rain_test, rain_model.predict(X_test)))
    
    # Save models
    joblib.dump(high_model, 'ml_models/temp_high_model.joblib')
    joblib.dump(low_model, 'ml_models/temp_low_model.joblib')
    joblib.dump(rain_model, 'ml_models/rain_model.joblib')

if __name__ == "__main__":
    # Create ml_models directory if it doesn't exist
    import os
    os.makedirs('ml_models', exist_ok=True)
    
    train_models()