import streamlit as st
from utils.auth import is_authenticated, login_user, logout_user, signup_user
from utils.database import initialize_database
from pages.home import render_home
from pages.login import render_login
from pages.signup import render_signup
from pages.dashboard import render_dashboard
from pages.predictions import render_predictions

# Initialize the database on app startup
initialize_database()

# Streamlit App Configuration
st.set_page_config(page_title="Customer Purchase Prediction", page_icon="📊", layout="wide")

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Login", "Signup", "Dashboard", "Predictions"])

# Page Routing
if menu == "Home":
    render_home()

elif menu == "Login":
    if not st.session_state["authenticated"]:
        render_login()
    else:
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.sidebar.info("Logged out successfully!")
            st.experimental_rerun()

elif menu == "Signup":
    render_signup()

elif menu == "Dashboard":
    if st.session_state["authenticated"]:
        render_dashboard()
    else:
        st.warning("Please log in to access the dashboard.")

elif menu == "Predictions":
    if st.session_state["authenticated"]:
        render_predictions()
    else:
        st.warning("Please log in to make predictions.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Customer Purchase Prediction")
