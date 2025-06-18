import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import os
import base64

# === Config ===
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]  # Set this in Streamlit Cloud secrets
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# === Predefined responses (optional) ===
PREDEFINED = {
    "life story": "I grew up in Calicut, Kerala, developed a passion for tech early on, and now I love solving problems with AI.",
    "superpower": "My superpower is adaptability—I learn fast and thrive in new environments.",
    "grow": "I want to grow in leadership, deep AI research, and public speaking.",
    "misconception": "People think I'm quiet, but I just think before I speak.",
    "boundaries": "I push my limits by tackling uncomfortable challenges regularly."
}

# === Mistral Response Function ===
def query_mistral(prompt):
    payload = {
        "model": MODEL,
        "prompt": f"[INST] {prompt} [/INST]",
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.9
    }
    res = requests.post("https://api.together.xyz/v1/completions", headers=HEADERS, json=payload)
    if res.status_code == 200:
        return res.json()['choices'][0]['text'].strip()
    else:
        return "Sorry, I couldn't generate a response."

# === TTS Player ===
def text_to_audio(text):
    tts = gTTS(text=text)
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        b64_audio = base64.b64encode(f.read()).decode()
    os.remove("response.mp3")
    audio_html = f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>"""
    st.markdown(audio_html, unsafe_allow_html=True)

# === Streamlit UI ===
st.title("🗣️ Voice Bot Interview - Powered by Mistral 7B")
st.markdown("Ask a behavioral interview question below.")

question = st.text_input("Your Question")

if st.button("🎤 Ask") and question:
    st.write(f"**You asked:** {question}")
    matched = next((v for k, v in PREDEFINED.items() if k in question.lower()), None)
    answer = matched if matched else query_mistral(question)
    st.success(f"🤖 Avinash: {answer}")
    text_to_audio(answer)

st.markdown("---")
st.info("This app uses Together.ai + Mistral-7B and is deployable on Streamlit Cloud.")
