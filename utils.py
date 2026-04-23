import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq()

def get_chat_response(messages, model="llama-3.3-70b-versatile", temperature=0.7):
    try:
        clean_messages = []
        for msg in messages:
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
        return f"Error: {str(e)}"

def add_system_prompt():
    system_prompt = """You are a friendly, helpful AI assistant named "ChatBuddy".
You respond in a warm, conversational tone.
Keep answers concise (2-3 sentences max).
If you don't know something, say "I'm not sure, but I can help find out!" """
    return {"role": "system", "content": system_prompt}
