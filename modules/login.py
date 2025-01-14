import streamlit as st
from utils.auth import login_user

def render_login():
    """
    Renders the Login page for the Streamlit app.
    """
    st.title("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = login_user(username, password)
        if user_id:
            st.success("Login successful!")
            return username, user_id, True  # Return username, user_id, and authenticated status
        else:
            st.error("Invalid username or password. Please try again.")
    return None, None, False  # Return None values if login fails
