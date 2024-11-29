import streamlit as st
import runpy
from supabase import create_client, Client
import supabase
import re

url = st.secrets["SUPABASE_PROJECT_URL"]
api_key = st.secrets["SUPABASE_PROJECT_API_KEY"]
supabase: Client = create_client(url, api_key)

# Function to validate login
def login(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        st.session_state.user_email = email
        return True

    except Exception as e:
        return False


# Function to register user
def register_user(email, password, confirm_password):
    if password != confirm_password:
        return False, "Passwords do not match"
    
    response = supabase.table("Users").select("*").eq("email", email).execute();
    if len(response.data) > 0:
        return False, "User already registered"

    try:
        response = supabase.auth.sign_up({
        'email': email,
        'password': password
        })

        supabase.table("Users").insert({'email': email, 'password': password}).execute()
        return True, "Registration successful"
    except Exception as e:
        return False, e


# Handle login and register state in session
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login page
def login_page():
    st.markdown("<h1 style='text-align: center;'> Login </h1>", unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    flag = True
    col1, col2, col3, col4, col5 = st.columns(5)
    with col2:
        if st.button("Login"):
            if login(email, password):
                st.session_state.logged_in = True
            else:
                flag = False
    with col4:
        if st.button("Register"):
            st.session_state.show_register = True
            st.rerun()
    
    if st.session_state.logged_in == True:
        st.success("Logged in successfully!")
        st.rerun()
    if flag == False:
        st.warning("Login Attempt Unsuccesful")

# Register page
def register_page():
    st.markdown("<h1 style='text-align: center;'> Registration </h1>", unsafe_allow_html=True)

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
    runpy.run_path("chatbot.py")  # This will execute app.py as a script
elif 'show_register' in st.session_state and st.session_state.show_register:
    register_page()
else:
    login_page()
