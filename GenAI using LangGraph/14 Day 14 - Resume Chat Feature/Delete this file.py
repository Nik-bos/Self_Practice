import streamlit as st
from langchain_core.messages import HumanMessage
import uuid
from chatbot_backend import workflow

st.title("**Custom Chatbot using LangGraph**")


# ************************************************ Utility Functions ************************************************ 
def generate_thread_id():
    
    thread_id = uuid.uuid4()
    return thread_id

def add_new_thread(thread_id):
    if thread_id not in st.session_state['list_thread_ids']:
        st.session_state['list_thread_ids'].append(thread_id)

def reset():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_new_thread(thread_id)
    st.session_state['history'] = []

def load_conversation(thread_id):
    CONFIG = {'configurable': {'thread_id': thread_id}}
    state = workflow.get_state(config = CONFIG)

    return state.values.get('messages', [])
    
    

# ************************************************ Session States ************************************************ 

if "history" not in st.session_state:
    st.session_state['history'] = []

if 'thread_id' not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "list_thread_ids" not in st.session_state:
    st.session_state['list_thread_ids'] = []

add_new_thread(st.session_state['thread_id'])


# ************************************************ Sidebar ************************************************ 

if st.sidebar.button("New Chat"):
    reset()

st.sidebar.title("My Conversations.")

# Displaying all thread_id in sidebar
for thread_id in st.session_state['list_thread_ids'] [::-1]:
    thread_button = st.sidebar.button(str(thread_id), key = f'thread_{thread_id}')
    if thread_button:
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            append = {'role': role, "content": message.content }
            temp_messages.append(append)

        st.session_state['history'] = temp_messages


# ************************************************ Load conversation ************************************************ 

if "history" in st.session_state:
    for message in st.session_state['history']:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# ************************************************ Main Program ************************************************ 

user_input = st.chat_input("Type here...")

if user_input:

    with st.chat_message(name = 'user'):
        st.write(user_input)

    initial_state = {'messages': [HumanMessage(user_input)]}
    CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}

    stream_generator = workflow.stream(
        input = initial_state,
        config = CONFIG,
        stream_mode = 'messages'
    )

     # Printing model's message
    with st.chat_message('assistant'):
        ai_message = st.write_stream(message_chunk.content for message_chunk, metadata in stream_generator)

    # Storing user_input and ai_message in session_state['history']
    store_user_input = {'role': 'user', 'content': user_input}
    st.session_state['history'].append(store_user_input)

    store_ai_message = {'role': 'assistant', 'content': ai_message}
    st.session_state['history'].append(store_ai_message)

    