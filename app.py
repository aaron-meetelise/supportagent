import streamlit as st
import openai
import pandas as pd
import json
import os

# Set your OpenAI API key
openai.api_key = st.secrets.openai_api_key

# Load and convert the knowledge base
csv_file = 'CRM Tickets Knowledge - Sheet1.csv'
df = pd.read_csv(csv_file)
knowledge_base_json = df.to_json(orient='records')

def query_openai(prompt, knowledge_base):
    # Combine the prompt with the knowledge base
    combined_prompt = f"Knowledge base: {knowledge_base}\n\nUser: {prompt}\nAssistant:"
    
    # Call the OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Or the model you prefer
        messages=[
            {"role": "system", "content": "You are a support agenet assistant."},
            {"role": "user", "content": combined_prompt}
        ],
        max_tokens=1500,
        temperature=0.0
    )
    
    return response['choices'][0]['message']['content'].strip()

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
