import streamlit as st
from utils import get_chat_response, add_system_prompt

st.set_page_config(page_title="ChatBuddy AI", page_icon="🤖")
st.title("🤖 ChatBuddy - Your AI Assistant")
st.caption("Powered by Groq (Free)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [add_system_prompt()]
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm ChatBuddy. What would you like to talk about today?"
    })

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selector
    model_options = {
        "llama-3.3-70b-versatile": "🐫 Llama 3.3 (70B) - Best quality",
        "llama-3.1-8b-instant": "⚡ Llama 3.1 (8B) - Fastest",
        "gemma2-9b-it": "🎯 Gemma 2 (9B) - Good balance"
    }
    selected_model = st.selectbox(
        "Choose Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0
    )
    
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7, 0.1)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [add_system_prompt()]
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Chat cleared! How can I help you?"
        })
        st.rerun()
    
    st.divider()
    st.caption("💡 Tip: Lower temperature = more focused answers")
    st.caption(f"Current model: **{selected_model}**")

# Displaying chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Adding user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Getting AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_chat_response(
                st.session_state.messages, 
                model=selected_model,  # Pass selected model
                temperature=temperature
            )
            st.markdown(response)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})