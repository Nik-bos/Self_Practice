import streamlit as st
from chatbot_backend import workflow
from langchain_core.messages import HumanMessage

if 'message_history' not in st.session_state:
    st.session_state["message_history"] = []


# Displaying history first
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here...")

if user_input:

    # Append to history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # invoking workflow
    initial_state = {"messages": [HumanMessage(content = user_input)]}
    CONFIG = {"configurable": {"thread_id": '1'}}
    response = workflow.invoke(initial_state, config = CONFIG)

    ai_message = response['messages'][-1].content

    # Adding assistant message (Keeping same as user_message)
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)