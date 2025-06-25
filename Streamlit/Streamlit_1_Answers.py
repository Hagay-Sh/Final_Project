import streamlit as st
from my_module_chat import ChatGPT_Prompt_Parameter_Tuner

st.title("Prompt Parameter Tuner")
st.write("Experiment with OpenAI generation settings interactively")


st.markdown("<br></br>", unsafe_allow_html=True)  # Adds vertical space

# Parameter sliders
st.sidebar.title("⚙️ Settings")
st.sidebar.header("Choose Options")
add_slider_temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.0, step=0.1)
add_slider_top_p = st.sidebar.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.0, step=0.1)
add_slider_max_tokens = st.sidebar.slider("Max Tokens", 16, 512, 150, step=16)




st.subheader("Chat with GPT")
st.write("")
st.markdown('<u>Try the folowing prompt:</u>', unsafe_allow_html=True)
st.markdown('<p style="font-size:25px">"Write a short story about a robot who learns to paint"</p>', unsafe_allow_html=True)


# User input
prompt = st.chat_input("Your prompt")

if prompt:
    response = ChatGPT_Prompt_Parameter_Tuner(prompt, add_slider_temperature, add_slider_top_p, add_slider_max_tokens)

    st.chat_message("assistant").write(response)