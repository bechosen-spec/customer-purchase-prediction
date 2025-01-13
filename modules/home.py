import streamlit as st

def render_home():
    """
    Renders the Home page for the Streamlit app.
    """
    st.title("Welcome to the Customer Purchase Prediction App 📊")
    st.write(
        "This platform leverages advanced machine learning models to predict customer purchase behavior "
        "and provide actionable insights for businesses. Whether you're optimizing inventory, targeting "
        "advertisements, or understanding your customers better, we've got you covered!"
    )

    st.header("Features")
    st.write(
        "- **Accurate Predictions**: Predict customer purchase behavior using advanced ensemble models.\n"
        "- **User-Friendly Interface**: Easily input data and get predictions in real-time.\n"
        "- **Detailed Insights**: Access analytics and visualizations to aid decision-making.\n"
        "- **Secure and Personalized**: Your data and predictions are securely stored for future reference."
    )

    st.header("Get Started")
    st.write(
        "- **New User?** [Sign up](#signup) to create an account and start making predictions.\n"
        "- **Returning User?** [Log in](#login) to access your dashboard and past predictions."
    )
