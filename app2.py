#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import os
import base64
import openai

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- API Key ---
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()

# --- LLM ---
chat = ChatOpenAI(model="gpt-4o-mini")

# --- Prompt Template ---
system_template = (
    "あなたは、{source_lang} を {target_lang} に翻訳する優秀な翻訳アシスタントです。"
    "翻訳結果以外は出力しないでください。"
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("human", "{text}")
    ]
)

# --- Session State ---
if "response" not in st.session_state:
    st.session_state["response"] = ""

# --- 音声読み上げ（TTS） ---
def speak(text):
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    audio_bytes = speech.read()
    st.audio(audio_bytes, format="audio/mp3")


# --- 翻訳処理 ---
def communicate():
    text = st.session_state["user_input"]

    prompt_value = chat_prompt.format_prompt(
        source_lang=st.session_state["source_lang"],
        target_lang=st.session_state["target_lang"],
        text=text
    )

    response = chat.invoke(prompt_value)
    st.session_state["response"] = response.content


# --- UI ---
st.title("翻訳アプリ")
st.write("LangChain を使った翻訳アプリです。")

options = [
    "日本語",
    "英語",
    "スペイン語",
    "ポルトガル語",
    "フランス語",
    "ドイツ語",
    "韓国語",
    "中国語"
]

st.session_state["source_lang"] = st.selectbox("翻訳元", options)
st.session_state["target_lang"] = st.selectbox("翻訳先", options)

st.text_input("翻訳する文章を入力してください。", key="user_input")
st.button("翻訳", type="primary", on_click=communicate)

# --- 結果表示 ---
if st.session_state["response"]:
    st.write("翻訳結果:")
    st.write(st.session_state["response"])

    if st.button("🔊 音声で聞く"):
        speak(st.session_state["response"])