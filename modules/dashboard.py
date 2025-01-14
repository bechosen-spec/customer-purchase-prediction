import streamlit as st
from utils.database import fetch_user_predictions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def render_dashboard():
    """
    Renders the Dashboard page for the Streamlit app.
    """
    st.title("Your Dashboard")

    # Check if the user is logged in
    if not st.session_state.get("authenticated", False):
        st.warning("You need to log in to view your dashboard.")
        return

    user_id = st.session_state.get("user_id", "Unknown User")

    st.header("Past Predictions")
    predictions = fetch_user_predictions(user_id)

    if not predictions:
        st.info("You have no saved predictions. Start making predictions to see them here!")
        return

    # Convert predictions to a DataFrame for easy manipulation
    predictions_df = pd.DataFrame(predictions)

    # Ensure DataFrame columns exist
    required_columns = ["timestamp", "input_data", "prediction_result"]
    for col in required_columns:
        if col not in predictions_df.columns:
            st.error(f"Missing expected column: {col}")
            return

    # Display DataFrame
    st.subheader("Your Prediction History")
    st.dataframe(predictions_df)

    # Visual Insights Section
    st.header("Visual Insights")

    # Distribution of Predictions
    st.subheader("Prediction Distribution")
    try:
        plt.figure(figsize=(8, 6))
        sns.countplot(x="prediction_result", data=predictions_df, palette="viridis")
        plt.title("Prediction Result Distribution")
        plt.xlabel("Prediction Result")
        plt.ylabel("Count")
        st.pyplot(plt)
    except Exception as e:
        st.error(f"An error occurred while plotting prediction distribution: {e}")

    # Time-based Trend
    st.subheader("Predictions Over Time")
    try:
        predictions_df["timestamp"] = pd.to_datetime(predictions_df["timestamp"])
        trend = predictions_df.groupby(predictions_df["timestamp"].dt.date).size()

        plt.figure(figsize=(10, 6))
        trend.plot(kind="line", marker="o", color="blue")
        plt.title("Predictions Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Predictions")
        plt.grid()
        st.pyplot(plt)
    except Exception as e:
        st.error(f"An error occurred while plotting predictions over time: {e}")
