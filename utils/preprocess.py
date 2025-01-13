import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

def load_encoders():
    """
    Loads saved encoders and scaler from disk.

    Returns:
        scaler: StandardScaler object.
        label_encoders: Dictionary of LabelEncoders for categorical features.
        target_encoder: LabelEncoder for target variable.
    """
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    with open('models/target_encoder.pkl', 'rb') as f:
        target_encoder = pickle.load(f)
    return scaler, label_encoders, target_encoder

def preprocess_input(input_data, feature_columns, label_encoders):
    """
    Preprocesses user input data for model prediction.

    Args:
        input_data (dict): Dictionary of user inputs.
        feature_columns (list): List of all required feature names.
        label_encoders (dict): Dictionary of LabelEncoders for categorical features.

    Returns:
        pd.DataFrame: Processed input data in DataFrame format.
    """
    processed_input = {}

    # Encode categorical features
    for col, encoder in label_encoders.items():
        if col in input_data:
            value = input_data[col]
            if value in encoder.classes_:
                processed_input[col] = encoder.transform([value])[0]
            else:
                processed_input[col] = 0  # Default for unseen categories
        else:
            processed_input[col] = 0  # Default for missing features

    # Handle numeric and remaining features
    for col in feature_columns:
        if col not in processed_input:
            processed_input[col] = input_data.get(col, 0)  # Default for missing values

    # Convert to DataFrame and ensure correct column order
    processed_df = pd.DataFrame([processed_input])

    # Add missing columns
    missing_cols = set(feature_columns) - set(processed_df.columns)
    for col in missing_cols:
        processed_df[col] = 0  # Default missing columns to zero

    # Log final processed input for debugging
    print("Processed Input DataFrame:")
    print(processed_df.head())

    return processed_df[feature_columns]

def scale_features(input_df, scaler):
    """
    Scales features using the saved scaler.

    Args:
        input_df (pd.DataFrame): Processed input DataFrame.
        scaler (StandardScaler): Pre-fitted scaler object.

    Returns:
        pd.DataFrame: Scaled features as a DataFrame.
    """
    scaled_data = scaler.transform(input_df)
    return pd.DataFrame(scaled_data, columns=input_df.columns)

def inverse_transform_prediction(prediction, target_encoder):
    """
    Converts the numeric prediction back to its original label.

    Args:
        prediction (int or array-like): Model prediction.
        target_encoder (LabelEncoder): Pre-fitted LabelEncoder for target variable.

    Returns:
        str: Original class label corresponding to the prediction.
    """
    return target_encoder.inverse_transform([prediction])[0]
