import streamlit as st
from utils.auth import login_user
from utils.database import fetch_user_id

def render_login():
    """
    Renders the Login page for the Streamlit app.
    """
    st.title("Login to Your Account")

    # Input fields for username and password
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    # Add a unique key to the "Login" button
    if st.button("Login", key="btn_login_submit"):
        if login_user(username, password):
            user_id = fetch_user_id(username)
            if user_id:
                # Update session state variables
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["user_id"] = user_id
                st.session_state["menu"] = "Dashboard"  # Redirect to the Dashboard
                st.success("Login successful! Redirecting...")
            else:
                st.error("User not found. Please try again.")
        else:
            st.error("Invalid username or password. Please try again.")

    # Link to the signup page
    st.write("Don't have an account? [Sign up](#signup)")
