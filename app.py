#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

# Secrets Manager から読み込む
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

chat = ChatOpenAI(model="gpt-3.5-turbo")

# session_state にメッセージを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="あなたは優秀なアシスタントAIです。")
    ]

def communicate():
    messages = st.session_state["messages"]

    user_message = HumanMessage(
        content=st.session_state["user_input"]
    )
    messages.append(user_message)

    # ★ ここが重要：辞書形式で渡す
    response = chat.invoke({"messages": messages})

    messages.append(response)

    st.session_state["user_input"] = ""

st.title("My AI Assistant")
st.write("LangChainを使ったチャットボットです。")

st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

for message in reversed(st.session_state["messages"][1:]):
    speaker = "🙂"
    if message.type == "ai":
        speaker = "🤖"
    st.write(speaker + ": " + message.content)
