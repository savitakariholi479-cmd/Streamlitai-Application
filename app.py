import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Page configuration
st.set_page_config(page_title="My Chatbot For Project", page_icon="✍️")

st.title("✍️ My Chatbot For Project")
st.write("Generate articles, emails, stories, captions, code, and more.")

# Sidebar
st.sidebar.header("Settings")

model = st.sidebar.selectbox(
    "Choose Model",
    [
        "openai/gpt-4o-mini",
        "openai/gpt-4.1-mini",
        "openai/gpt-5"
    ]
)

temperature = st.sidebar.slider(
    "Creativity",
    0.0,
    1.5,
    0.7
)

max_tokens = st.sidebar.slider(
    "Maximum Tokens",
    100,
    2000,
    500
)

# User Input
prompt = st.text_area(
    "Enter your prompt",
    height=200,
    placeholder="Example: Write a professional email requesting leave..."
)

if st.button("Generate Text"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional AI writing assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                result = response.choices[0].message.content

                st.subheader("Generated Text")
                st.write(result)

                st.download_button(
                    "Download",
                    result,
                    file_name="generated_text.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {e}")
                