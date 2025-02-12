import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/api/chat"

st.set_page_config(page_title="💰 Financial Chatbot", page_icon="🤖")
st.title("💰 Financial Chatbot")
st.write("Ask me anything about financial data, taxes, income, and more!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

user_input = st.chat_input("Enter your question...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = requests.post(API_URL, json={"query": user_input})

    if response.status_code == 200:
        data = response.json()
        results = data.get("response", [])

        def clean_text(text):
            return text.replace("\n", " ").replace("\r", " ").strip()

        bot_reply = "\n\n".join([f"💡 **{clean_text(res['text'])}**" for res in results])

        with st.chat_message("assistant"):
            st.markdown(bot_reply, unsafe_allow_html=True)

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    else:
        st.error("❌ Error fetching response from chatbot API.")
