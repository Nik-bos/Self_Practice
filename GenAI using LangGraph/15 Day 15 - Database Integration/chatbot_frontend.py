import streamlit as st
from chatbot_backend import workflow, get_all_threads
from langchain_core.messages import HumanMessage
import uuid    # To generate unique thread_ids

# ************************************************ Utility functions ************************************************ 

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()    # Generating new thread_id
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    CONFIG = {"configurable": {"thread_id": thread_id}}
    state = workflow.get_state(config = CONFIG)

    return state.values.get('messages', [])

# ************************************************ Session Setup ************************************************ 

# Checking if message_history present in session_state
if 'message_history' not in st.session_state:
    st.session_state["message_history"] = []

# Checking if thread_id present in session_state
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

# Maintaining a list of all thread_ids
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = get_all_threads()

# Adding current thread_id to chat_threads
add_thread(st.session_state['thread_id'])

# ************************************************ Sidebar UI ************************************************ 

st.sidebar.title("LangGraph Chatbot")    # Adds title

if st.sidebar.button("New Chat"):    # Adds a clickable button with title 'New Chat'
    reset_chat()
    
st.sidebar.header("My Conversations")    # Adds a header named "My Conversations"

# After header, display the current thread_id
#st.sidebar.text(st.session_state['thread_id'])

# Displaying all thread_id in sidebar
for thread_id in st.session_state['chat_threads'] [::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'ai'

            append = {'role': role, "content": message.content }
            temp_messages.append(append)

        st.session_state['message_history'] = temp_messages
        
# ************************************************ Loading conversation ************************************************ 

# Loading the conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])

# ************************************************ User input and LLM's response ************************************************ 

# Taking user input and adding it to the message_history
# Invoking LLM and adding it to the message_history

# We will add history in below format
# {"role": 'user', "content": '...'}
user_input = st.chat_input("Type here...")

if user_input:

    # Append user_input to history
    st.session_state["message_history"].append({"role": "user", "content": user_input})

    # printing user_input
    with st.chat_message("user"):
        st.text(user_input)

    # invoking workflow
    initial_state = {"messages": [HumanMessage(content = user_input)]}
    CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}

    stream_generator = workflow.stream(
        input = initial_state,
        config = CONFIG,
        stream_mode = 'messages'
    )
    
    # Printing model's message
    with st.chat_message("ai"):
        ai_message = st.write_stream(message_chunk.content for message_chunk, metadata in stream_generator)

    # Adding assistant message to history
    st.session_state["message_history"].append({"role": "ai", "content": ai_message})