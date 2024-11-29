# LLM-Powered Chatbot

This project involves developing a chatbot powered by OpenAI's "GPT-40" model, with custom fine-tuning to improve its ability to generate message-formatted responses based on credible internet sources. The interface is built using Streamlit, and the backend is powered by Supabase, a relational cloud database. The application also integrates speech recognition and output functionalities, making it accessible and interactive. Additionally, the chatbot supports translation of responses to Indian languages using AWS Translate Service. The entire application is deployed on the Streamlit Cloud Platform.

## Features
- **LLM-Powered Chatbot**: Built on OpenAI's GPT-40 model and fine-tuned with message-formatted responses sourced from credible internet information.
- **Streamlit Interface**: Easy-to-use interface for seamless interaction with the chatbot.
- **Speech Input & Output**: Speech input is captured through Streamlit’s audio recorder, and speech output is provided using the Google Text-To-Speech module.
- **Translation Support**: Responses can be translated into Indian languages using AWS Translate Service.
- **Database Integration**: Powered by Supabase for storing relevant data and project information.
- **Deployment**: Deployed on Streamlit Cloud Platform for easy access and scalability.

## Installation

### Prerequisites
1. Python 3.x
2. Streamlit
3. OpenAI API access
4. Supabase account
5. AWS account for Translate Service

### Setup Instructions

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/LLM-Powered-Chatbot.git
    cd LLM-Powered-Chatbot
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    - OpenAI API key
    - Supabase credentials
    - AWS Translate credentials

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Components

### 1. **LLM (GPT-40) Fine-Tuning**
   - Fine-tuned GPT-40 model using message-formatted responses from credible sources.
   - Ensures the chatbot provides relevant and accurate information.
   
### 2. **Streamlit Interface**
   - A user-friendly interface where users can interact with the chatbot in real-time.
   
### 3. **Speech Input and Output**
   - Speech input functionality using Streamlit's audio recorder and speech recognition module.
   - Speech output using Google Text-To-Speech, making the chatbot more accessible.

### 4. **Translation to Indian Languages**
   - The chatbot's responses can be translated to several Indian languages via AWS Translate, ensuring wider accessibility.

### 5. **Supabase Database Integration**
   - Supabase provides a relational database for storing chat logs and other user-specific data securely.

### 6. **Deployment on Streamlit Cloud**
   - The app is deployed on the Streamlit Cloud platform for easy access and maintenance.

## Technologies Used
- **OpenAI GPT-40**: Base model for chatbot responses.
- **Streamlit**: For building and deploying the interactive web interface.
- **Supabase**: Relational database for backend data storage.
- **Speech Recognition**: For capturing speech input.
- **Google Text-To-Speech**: For generating speech output.
- **AWS Translate**: For translating responses into Indian languages.

## Acknowledgments
- OpenAI for the GPT-40 model
- Streamlit for an easy-to-use web application framework
- Supabase for cloud database services
- AWS for translation services
- Google for Text-to-Speech API
