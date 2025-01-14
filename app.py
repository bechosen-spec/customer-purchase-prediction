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
    if "user_id" in st.session_state:
        st.session_state["user_id"] = None
    st.session_state["menu"] = "Home"  # Redirect to Home after logout
    st.success("Logged out successfully!")

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "menu" not in st.session_state:
    st.session_state["menu"] = "Home"

# Sidebar Navigation
st.sidebar.title("Navigation")
if not st.session_state["authenticated"]:
    # Display login/signup options for unauthenticated users
    with st.sidebar:
        if st.button("Home", key="btn_home"):
            st.session_state["menu"] = "Home"
        if st.button("Login", key="btn_login"):
            st.session_state["menu"] = "Login"
        if st.button("Signup", key="btn_signup"):
            st.session_state["menu"] = "Signup"
else:
    # Display dashboard and logout for authenticated users
    st.sidebar.success(f"Welcome, {st.session_state['username']}!")
    with st.sidebar:
        if st.button("Dashboard", key="btn_dashboard"):
            st.session_state["menu"] = "Dashboard"
        if st.button("Predictions", key="btn_predictions"):
            st.session_state["menu"] = "Predictions"
        if st.button("Logout", key="btn_logout"):
            logout()

# Page Routing
if st.session_state["menu"] == "Home":
    render_home()

elif st.session_state["menu"] == "Login":
    if not st.session_state["authenticated"]:
        # Render the login page and handle login logic
        username, user_id, authenticated = render_login()
        if authenticated:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["user_id"] = user_id
            st.session_state["menu"] = "Predictions"  # Redirect to Predictions after login
            st.success("Login successful! Redirecting...")
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
        st.warning("You need to log in to view your dashboard.")

elif st.session_state["menu"] == "Predictions":
    if st.session_state["authenticated"]:
        render_predictions()
    else:
        st.warning("You need to log in to make predictions.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 Customer Purchase Prediction")
