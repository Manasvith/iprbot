import openai
from constants import OPENAI_API_KEY, SUPABASE_PROJECT_API_KEY, SUPABASE_PROJECT_URL
import time
import warnings
import streamlit as st
from supabase import create_client, Client
import datetime
from gtts import gTTS
import tempfile

warnings.filterwarnings("ignore")

# Set the API key
openai.api_key = OPENAI_API_KEY
client = openai.OpenAI(api_key=OPENAI_API_KEY)
user_email = st.session_state.get('user_email', 'Unknown User')

# Initialize Supabase client
url = SUPABASE_PROJECT_URL
api_key = SUPABASE_PROJECT_API_KEY
supabase: Client = create_client(url, api_key)

# Function to handle query
def handle_query(query):
    finetuned_response = client.chat.completions.create(
        model="ft:gpt-4o-2024-08-06:personal:chatbotipr:AIEPCh2c",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert in intellectual property rights based in India. Your task is to provide accurate and helpful responses related to intellectual property rights only. The user has asked {query}. Provide a response that is relevant to intellectual property rights and their related laws and Acts. If the query is not related to intellectual property rights, state that you can only assist with queries related to intellectual property rights."""
            },
            {"role": "user", "content": query}
        ],
        temperature=0.3,
        max_tokens=10000
    )

    return finetuned_response.choices[0].message.content

# Function to stream the data slowly
def stream_data(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Function to generate speech from text and play it
def generate_speech(text):
    tts = gTTS(text=text, lang='en')  # Generate speech from text using gTTS
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)  # Save the speech to a temporary file
        return fp.name

# Clear button logic
def clear_history():
    st.session_state.current_history = []
    st.session_state.retrieved_history = []
    st.session_state.display_response = ""
    st.rerun()

# Logout button and Reset conversation
def add_logout_button():
    user_email = st.session_state.get('user_email', 'Unknown User')
    st.markdown(f"""
    <div style="padding: 10px 0;">
        <p style="margin: 0; font-size: 16px; text-align: center;">Logged in as: <strong>{user_email}</strong></p>
    </div>
    <hr style="border: none; border-bottom: 1px solid #ccc;">
    """, unsafe_allow_html=True)

    # Create five columns for spacing and buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    with col2:
        if st.button("Logout", key="logout-button", help="Logout and return to the Login page", type="primary"):
            # Clear all session state upon logout
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col4:
        if st.button("Reset", key="reset", help="Resets the conversation by erasing the current queries and responses", type='primary'):
            clear_history()

# Call the function at the top of your app
add_logout_button()

# Function to retrieve and display history on the main screen
def retrieve_history(date):
    responses = supabase.table("prompts").select("query", "response").eq("date", date).execute()
    st.session_state.retrieved_history = responses.data  # Update retrieved history
    st.session_state.current_history = []  # Clear current history
    st.session_state.display_response = ""  # Clear any ongoing response stream
    st.rerun()

# Streamlit application setup
st.markdown("<h1 style='text-align: center;'> Chatbot for IPR </h1>", unsafe_allow_html=True)

# Session state initialization
if "current_history" not in st.session_state:
    st.session_state.current_history = []

if "retrieved_history" not in st.session_state:
    st.session_state.retrieved_history = []

if "display_response" not in st.session_state:
    st.session_state.display_response = ""

# Main content display logic
with st.container():
    query = st.chat_input("Enter your query here:")

    if query:
        # Clear retrieved_history when a new query is entered
        st.session_state.retrieved_history = []
        
        response = handle_query(query=query)
        st.session_state.current_history.append({"query": query, "response": response})
        st.session_state.display_response = response

        # Store the new prompt in the database
        supabase.table("prompts").insert({
            "user": user_email, 
            "date": datetime.datetime.now().strftime('%Y-%m-%d'), 
            "query": query, 
            "response": response
        }).execute()

    # Display either retrieved history or current conversation
    if st.session_state.retrieved_history:
        st.markdown("<h2 style='text-align: center;'> Retrieved Conversation History </h2>", unsafe_allow_html=True)
        for i, entry in enumerate(reversed(st.session_state.retrieved_history)):
            with st.chat_message(name="user"):
                st.write(entry["query"])
            with st.chat_message(name="ai"):
                st.write(entry["response"])

    elif st.session_state.current_history:
        st.markdown("<h2 style='text-align: center;'> Current Conversation </h2>", unsafe_allow_html=True)
        # Loop through the current conversation and display messages
        for i, entry in enumerate(reversed(st.session_state.current_history)):
            with st.chat_message(name="user"):
                st.write(entry["query"])
            with st.chat_message(name="ai"):
                if i == 0 and st.session_state.display_response:  # Stream the latest response
                    st.write(stream_data(entry['response']))
                    # Optional "Play Audio" button at the end of the AI response
                    if st.button("Play Audio for Current Response", key="audio_button_current"):
                        audio_file = generate_speech(entry['response'])
                        st.audio(audio_file)
                else:  # Display previous responses without streaming
                    st.write(entry["response"])
    else:
        st.write("Conversation reset. Start a new chat.")

# Sidebar for browsing conversation history
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'> Conversation History </h2>", unsafe_allow_html=True)
    
    history = supabase.table("first_prompts_per_date_view").select("*").eq("user", user_email).execute()

    if len(history.data) > 0:
        for i in range(len(history.data), 0, -1):
            query_text = history.data[i-1]['query']
            date_text = history.data[i-1]['date']
            # Truncate query_text for display purposes if too long
            display_query = (query_text[:20] + '...') if len(query_text) > 20 else query_text
            if st.button(f"{i}. {display_query}", key=f"history_{i}", use_container_width=True):
                retrieve_history(date_text)
    else:
        st.write("No past conversations found.")
