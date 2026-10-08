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

    # Append user_input to history
    st.session_state["message_history"].append({"role": "user", "content": user_input})

    # printing user_input
    with st.chat_message("user"):
        st.text(user_input)

    # invoking workflow
    initial_state = {"messages": [HumanMessage(content = user_input)]}
    CONFIG = {"configurable": {"thread_id": '1'}}

    stream_generator = workflow.stream(
        input = initial_state,
        config = CONFIG,
        stream_mode = 'messages'
    )
    
    # Printing model's message
    with st.chat_message("assistant"):
        ai_message = st.write_stream(message_chunk.content for message_chunk, metadata in stream_generator)

    # Adding assistant message to history
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})