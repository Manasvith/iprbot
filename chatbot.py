import os
import openai
from constants import OPENAI_API_KEY
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import time
import warnings
from gtts import gTTS  # Import Google Text-to-Speech
import streamlit as st
import tempfile  # To save and load temporary audio files

warnings.filterwarnings("ignore")

# Set the API key
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)
# Memory
Explanation_Memory = ConversationBufferMemory(input_key='query', memory_key='chat_history')

# Prompt Template
detailed_prompt_template = PromptTemplate(
    input_variables=["query"],
    template=""" 
    You are an expert in intellectual property rights based in India. Your task is to provide accurate and helpful responses related to intellectual property rights only.

    The user has asked:
    {query}

    Provide a response that is relevant to intellectual property rights. If the query is not related to intellectual property rights, state that you can only assist with queries related to intellectual property rights.
    """
)

#llm

llm = openai.OpenAI(temperature=0.5, model = "ft:gpt-4o-mini-2024-07-18:personal:chatbotipr:AHTOq6OT")

chain1 = LLMChain(llm=llm, prompt=detailed_prompt_template, output_key='Explanation', verbose=True, memory=Explanation_Memory)


# Function to call the fine-tuned model
def handle_query(query):
    response = chain1.run({"query": query})
    return response

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

# Streamlit application setup
st.set_page_config(layout="centered")
st.markdown("<h1 style='text-align: center;'> Chatbot for IPR </h1>", unsafe_allow_html=True)

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []

if "query" not in st.session_state:
    st.session_state.query = ""

if "display_response" not in st.session_state:
    st.session_state.display_response = ""

# Clear button logic
def clear_history():
    st.session_state.history = []
    st.session_state.display_response = ""
    st.rerun()

# CSS for styling buttons
st.markdown(r'''
            <style>
                div.stButton > button:first-child {
                    border: 0px; 
                    background-color: transparent; 
            }
            </style>
            ''', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .red-button {
        background-color: red;
        color: white;
        border: none;
        padding: 0.4em 1em;
        border-radius: 0.3em;
        cursor: pointer;
        font-size: 1em;
        margin: 0.5em 0;
    }
    .red-button:hover {
        background-color: darkred;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Streamlit logic
with st.container():
    # Reset Conversation Button
    reset_btn = st.button("Reset Conversation", use_container_width=True, type='primary')

    if reset_btn:
        clear_history() 
    
    query = st.chat_input("Enter your query here:")

    if query:
        # Handle the query and update history
        response = handle_query(query=query)
        st.session_state.history.append({"query": query, "response": response})
        st.session_state.display_response = response

    # If no history, display a message that the conversation is empty after reset
    if not st.session_state.history:
        st.write("Conversation reset. Start a new chat.")
    else:
        # Loop through the entire chat history and display the latest message first
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.chat_message(name="user"):
                st.write(entry["query"])
            with st.chat_message(name="ai"):
                if i == 0:  # Stream the latest response (since we're reversing, index 0 is the latest)
                    st.write(stream_data(entry['response']))
                    
                    # Generate speech for the response and play it
                    audio_file = generate_speech(entry['response'])
                    st.audio(audio_file)
                else:  # Display previous responses without streaming
                    st.write(entry["response"])

with st.sidebar: 
    st.markdown("<h2 style='text-align:center;'> Conversation History </h2>", unsafe_allow_html=True)
    
    # Display conversation history as buttons, but ensure that it vanishes after reset
    for i, entry in enumerate(reversed(st.session_state.history)):
        if st.button(f"{i+1}\. {entry['query']}", key=f"history_{i}", use_container_width=True):
            continue
