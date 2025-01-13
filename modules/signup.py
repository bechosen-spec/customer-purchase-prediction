import streamlit as st
from utils.auth import signup_user

def render_signup():
    """
    Renders the Signup page for the Streamlit app.
    """
    st.title("Create a New Account")

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        else:
            if signup_user(username, password):
                st.success("Account created successfully! You can now log in.")
                st.write("[Go to Login](#login)")
            else:
                st.error("Username already exists. Please choose a different one.")

    st.write("Already have an account? [Log in](#login)")
