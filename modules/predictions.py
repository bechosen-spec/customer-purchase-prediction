import streamlit as st
from utils.predict import make_prediction
from utils.database import add_prediction


def render_predictions():
    """
    Renders the Predictions page for the Streamlit app.
    """
    st.title("Make a Prediction")

    # Check if user is logged in
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("You need to log in to make predictions.")
        return

    st.header("Input Your Data")

    # Input fields based on expected features
    gender = st.selectbox("Gender", ["Male", "Female", "Others"], key="gender_input")
    age = st.number_input("Age", min_value=0, max_value=100, value=23, key="age_input")
    browsing_frequency = st.selectbox(
        "Browsing Frequency",
        ["Rarely", "Few times a month", "Few times a week", "Multiple times a day"],
        key="browsing_frequency_input",
    )
    product_search_method = st.selectbox(
        "Product Search Method", ["Keyword", "Filter", "Categories", "Others"], key="product_search_method_input"
    )
    search_result_exploration = st.selectbox(
        "Search Result Exploration",
        ["Single page", "Multiple pages", "All available results"],
        key="search_result_exploration_input",
    )
    add_to_cart_browsing = st.selectbox(
        "Add to Cart While Browsing", ["Yes", "No"], key="add_to_cart_browsing_input"
    )
    cart_completion_frequency = st.selectbox(
        "Cart Completion Frequency",
        ["Always", "Often", "Sometimes", "Rarely", "Never"],
        key="cart_completion_frequency_input",
    )
    cart_abandonment_factors = st.selectbox(
        "Cart Abandonment Factors",
        ["Changed my mind", "Found a better price elsewhere", "High shipping costs", "Others"],
        key="cart_abandonment_factors_input",
    )
    saveforlater_frequency = st.selectbox(
        "Save for Later Frequency",
        ["Always", "Often", "Sometimes", "Rarely", "Never"],
        key="saveforlater_frequency_input",
    )
    review_left = st.selectbox("Review Left", ["Yes", "No"], key="review_left_input")
    review_reliability = st.selectbox(
        "Review Reliability", ["Very Reliable", "Moderately", "Not Reliable"], key="review_reliability_input"
    )
    review_helpfulness = st.selectbox(
        "Review Helpfulness", ["Yes", "Sometimes", "No"], key="review_helpfulness_input"
    )
    recommendation_helpfulness = st.selectbox(
        "Recommendation Helpfulness", ["Yes", "Sometimes", "No"], key="recommendation_helpfulness_input"
    )
    service_appreciation = st.text_input("Service Appreciation", key="service_appreciation_input")
    improvement_areas = st.text_input("Improvement Areas", key="improvement_areas_input")
    purchase_categories = st.multiselect(
        "Purchase Categories",
        ["Beauty and Personal Care", "Clothing and Fashion", "Groceries and Gourmet Food", "Home and Kitchen", "others"],
        key="purchase_categories_input",  # Ensure lowercase 'others'
    )

    # Construct input data dictionary
    input_data = {
        "gender": gender,
        "age": age,
        "browsing_frequency": browsing_frequency,
        "product_search_method": product_search_method,
        "search_result_exploration": search_result_exploration,
        "add_to_cart_browsing": add_to_cart_browsing,
        "cart_completion_frequency": cart_completion_frequency,
        "cart_abandonment_factors": cart_abandonment_factors,
        "saveforlater_frequency": saveforlater_frequency,
        "review_left": review_left,
        "review_reliability": review_reliability,
        "review_helpfulness": review_helpfulness,
        "recommendation_helpfulness": recommendation_helpfulness,
        "service_appreciation": service_appreciation,
        "improvement_areas": improvement_areas,
        "purchase_categories": ";".join(purchase_categories),  # Join multi-select categories into a string
    }

    # Feature columns expected by the model
    feature_columns = [
        "gender", "age", "browsing_frequency", "product_search_method",
        "search_result_exploration", "add_to_cart_browsing", "cart_completion_frequency",
        "cart_abandonment_factors", "saveforlater_frequency", "review_left",
        "review_reliability", "review_helpfulness", "recommendation_helpfulness",
        "service_appreciation", "improvement_areas", "Beauty and Personal Care",
        "Clothing and Fashion", "Groceries and Gourmet Food", "Home and Kitchen", "others"
    ]

    # Prediction logic
    if st.button("Predict", key="predict_button"):
        try:
            # Make prediction
            prediction_result = make_prediction(input_data, feature_columns)

            # Display the result
            st.success(f"Predicted Purchase Frequency: {prediction_result}")

            # Save prediction to the database
            add_prediction(user_id, str(input_data), prediction_result)
            st.info("Prediction saved to your dashboard.")

        except ValueError as ve:
            st.error(f"Input Error: {ve}")
        except KeyError as ke:
            st.error(f"Missing Feature Error: {ke}")
        except Exception as e:
            st.error(f"An unexpected error occurred during prediction: {e}")
