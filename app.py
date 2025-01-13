import streamlit as st
from utils.auth import login_user, logout_user, signup_user
from utils.database import initialize_database
from modules.home import render_home
from modules.login import render_login
from modules.signup import render_signup
from modules.dashboard import render_dashboard
from modules.predictions import render_predictions

# Initialize the database on app startup
initialize_database()

# Streamlit App Configuration
st.set_page_config(page_title="Customer Purchase Prediction", page_icon="📊", layout="wide")

# Function to handle logout logic
def logout():
    if "authenticated" in st.session_state:
        st.session_state["authenticated"] = False
    if "username" in st.session_state:
        st.session_state["username"] = ""
    st.sidebar.success("Logged out successfully!")
    st.experimental_rerun()

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "menu" not in st.session_state:
    st.session_state["menu"] = "Home"
if "redirect_to" not in st.session_state:
    st.session_state["redirect_to"] = None

# Handle redirection
if st.session_state["redirect_to"]:
    st.session_state["menu"] = st.session_state["redirect_to"]
    st.session_state["redirect_to"] = None

# Sidebar Navigation with Buttons (Add unique keys for each button)
st.sidebar.title("Navigation")
if st.sidebar.button("Home", key="btn_home"):
    st.session_state["menu"] = "Home"
if st.sidebar.button("Login", key="btn_login"):
    st.session_state["menu"] = "Login"
if st.sidebar.button("Signup", key="btn_signup"):
    st.session_state["menu"] = "Signup"
if st.sidebar.button("Dashboard", key="btn_dashboard"):
    st.session_state["menu"] = "Dashboard"
if st.sidebar.button("Predictions", key="btn_predictions"):
    st.session_state["menu"] = "Predictions"

# Page Routing
if st.session_state["menu"] == "Home":
    render_home()

elif st.session_state["menu"] == "Login":
    if not st.session_state["authenticated"]:
        render_login()
    else:
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout", key="btn_logout"):
            logout()

elif st.session_state["menu"] == "Signup":
    render_signup()

elif st.session_state["menu"] == "Dashboard":
    if st.session_state["authenticated"]:
        render_dashboard()
    else:
        st.warning("Please log in to access the dashboard.")
        st.session_state["redirect_to"] = "Dashboard"

elif st.session_state["menu"] == "Predictions":
    if st.session_state["authenticated"]:
        render_predictions()
    else:
        st.warning("Please log in to make predictions.")
        st.session_state["redirect_to"] = "Predictions"

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Customer Purchase Prediction")
