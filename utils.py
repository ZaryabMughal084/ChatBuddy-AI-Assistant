# utils.py , Groq Version with CURRENT MODELS
import os
from dotenv import load_dotenv
from groq import Groq

# Load the environment variables from .env file
load_dotenv()

# Get the API key with error checking
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(" GROQ_API_KEY not found! Please check your .env file")

# Initialize the client
client = Groq(api_key=api_key)

def get_chat_response(messages, model="llama-3.3-70b-versatile", temperature=0.7):
    """
    Get response from Groq API using current available models
    
    Available models (March 2026):
    - llama-3.3-70b-versatile (best, recommended)
    - llama-3.1-8b-instant (fastest)
    - gemma2-9b-it (good alternative)
    """
    try:
        # Convert messages format for Groq (remove system messages or handle)
        clean_messages = []
        for msg in messages:
            # Groq accepts system, user, assistant roles
            if msg["role"] in ["system", "user", "assistant"]:
                clean_messages.append(msg)
        
        response = client.chat.completions.create(
            model=model,
            messages=clean_messages,
            temperature=temperature,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def add_system_prompt():
    """
    System prompt for the assistant
    """
    system_prompt = """You are a friendly, helpful AI assistant named "ChatBuddy".
You respond in a warm, conversational tone.
Keep answers concise (2-3 sentences max).
If you don't know something, say "I'm not sure, but I can help find out!" """
    
    return {"role": "system", "content": system_prompt}