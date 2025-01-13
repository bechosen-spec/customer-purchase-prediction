import pickle
import numpy as np
from utils.preprocess import preprocess_input, scale_features

def load_model():
    """
    Loads the trained machine learning model and associated encoders/scalers.

    Returns:
        tuple: Trained model, scaler, label encoders, and target encoder.
    """
    with open('models/rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    with open('models/target_encoder.pkl', 'rb') as f:
        target_encoder = pickle.load(f)

    return model, scaler, label_encoders, target_encoder

def make_prediction(input_data, feature_columns):
    """
    Prepares input data, makes a prediction, and returns the result.

    Args:
        input_data (dict): Dictionary containing raw user input data.
        feature_columns (list): List of all required feature names.

    Returns:
        str: Predicted class label.
    """
    try:
        # Load the trained model and preprocessing tools
        model, scaler, label_encoders, target_encoder = load_model()

        # Preprocess input data
        processed_input = preprocess_input(input_data, feature_columns, label_encoders)

        # Scale the features
        scaled_input = scale_features(processed_input, scaler)

        # Ensure correct dimensions
        scaled_input = np.array(scaled_input).reshape(1, -1)

        # Make prediction
        prediction = model.predict(scaled_input)

        # Convert prediction back to original label
        predicted_label = target_encoder.inverse_transform(prediction)[0]

        return predicted_label

    except Exception as e:
        raise RuntimeError(f"An error occurred during prediction: {e}")

def make_batch_predictions(input_data_list, feature_columns):
    """
    Prepares and predicts multiple data inputs.

    Args:
        input_data_list (list): List of dictionaries containing raw user input data.
        feature_columns (list): List of all required feature names.

    Returns:
        list: List of predicted class labels.
    """
    try:
        # Load the trained model and preprocessing tools
        model, scaler, label_encoders, target_encoder = load_model()

        # Preprocess and scale input data
        processed_inputs = [preprocess_input(data, feature_columns, label_encoders) for data in input_data_list]
        scaled_inputs = np.vstack([scale_features(data, scaler) for data in processed_inputs])

        # Make predictions
        predictions = model.predict(scaled_inputs)

        # Convert predictions back to original labels
        predicted_labels = target_encoder.inverse_transform(predictions)

        return predicted_labels

    except Exception as e:
        raise RuntimeError(f"An error occurred during batch prediction: {e}")
