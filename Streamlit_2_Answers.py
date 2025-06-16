import streamlit as st
from my_module_chat_conv import ChatGPT_Conversation



st.title("Chat with GPT")
st.subheader("with Conversation Continuity")

# Initialize chat history (no system message)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # st.chat_message(msg["role"]).write(msg["content"])  --  Alternatively -- instead "with"
        st.markdown(msg["content"])
    

# Chat input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):  # st.chat_message("user").write(user_input)  --  Alternatively -- instead "with"
        st.markdown(user_input)
    

    # Get assistant response from OpenAI
    with st.spinner("Thinking..."):
        reply = ChatGPT_Conversation(st.session_state.messages)

    # Add assistant reply to history and display it
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):  # st.chat_message("assistant").write(reply)  --  Alternatively -- instead "with"
        st.markdown(reply)
    
