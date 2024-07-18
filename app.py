import streamlit as st
import pandas as pd
import json
import os
import requests

# Set your Azure OpenAI API key from Streamlit secrets
azure_api_key = st.secrets["openai_api_key"]

# Set up Azure
azure_endpoint = "https://oai0-2lgwc6k5ex2by.openai.azure.com/"
azure_deployment_name = "chat"

# Load and convert the knowledge base
csv_file = 'CRM Tickets Knowledge - Sheet1.csv'
df = pd.read_csv(csv_file)
knowledge_base_json = df.to_json(orient='records')

def query_openai(prompt, knowledge_base):
    combined_prompt = f"Knowledge base: {knowledge_base}\n\nUser: {prompt}\nAssistant:"

    headers = {
        "Content-Type": "application/json",
        "api-key": azure_api_key
    }
    
    body = {
        "messages": [
            {"role": "system", "content": "You are a support agent assistant."},
            {"role": "user", "content": combined_prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.0
    }
    
    response = requests.post(
        f"{azure_endpoint}/openai/deployments/{azure_deployment_name}/chat/completions?api-version=2023-03-15-preview",
        headers=headers,
        json=body
    )
    
    response_json = response.json()
    return response_json.data.choices[0].message.content.strip()

# Streamlit app
st.title('Chatbot with Knowledge Base')

# Text input for the user's message
user_input = st.text_input("You:", "")

# Display area for the chatbot's response
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Handle the user input
if user_input:
    # Get the chatbot's response
    response = query_openai(user_input, knowledge_base_json)
    
    # Store the interaction in session state
    st.session_state['chat_history'].append((user_input, response))
    
    # Clear the input field
    st.text_input("You:", "", key="new")

# Display the chat history
for i, (user_msg, bot_msg) in enumerate(st.session_state['chat_history']):
    st.write(f"**You:** {user_msg}")
    st.write(f"**Bot:** {bot_msg}")
