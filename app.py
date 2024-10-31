import streamlit as st
import runpy
from constants import SUPABASE_PROJECT_API_KEY, SUPABASE_PROJECT_URL
from supabase import create_client, Client
import supabase
import time

url = SUPABASE_PROJECT_URL
api_key = SUPABASE_PROJECT_API_KEY
supabase: Client = create_client(url, api_key)

# Function to validate login
def login(email, password):
    response = supabase.table("Users").select("*").eq("email", email).eq("password", password).execute()
    if len(response.data) > 0:
        st.session_state.user_email = email
        return True
    return False

# Function to register user
def register_user(email, password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match"
    response = supabase.table("Users").select("*").eq("email", email).execute()
    if len(response.data) > 0:
        return False, "Email already registered"
    supabase.table("Users").insert({"email": email, "password": password}).execute() 
    return True, "Registration successful"

def stream_write(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.02)

# Handle login and register state in session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login page
def login_page():

    st.title(stream_write("Login Page"))

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(email, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.warning("Incorrect email or password")

    if st.button("Register"):
        st.session_state.show_register = True
        st.rerun()

# Register page
def register_page():
    st.title("Register Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        success, message = register_user(email, password, confirm_password)
        if success:
            st.success(message)
            st.session_state.show_register = False
            st.rerun()
        else:
            st.warning(message)

    if st.button("Back to Login"):
        st.session_state.show_register = False
        st.rerun()

# Control flow based on login and register state
if st.session_state.logged_in:
    # Instead of calling a function, we load the entire app file
    runpy.run_path("test.py")  # This will execute app.py as a script
elif 'show_register' in st.session_state and st.session_state.show_register:
    register_page()
else:
    login_page()
