from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages

load_dotenv()

# Creating the model
model_gemini = ChatGoogleGenerativeAI(
    model = 'gemini-1.5-flash')

model_openai = ChatOpenAI(
    model = 'gpt-3.5-turbo'
)

# Defining the state

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Defining nodes
def chat_node(state: ChatState) ->ChatState:

    # Fetching messages
    messages = state["messages"]

    # Invokig model
    response = model_openai.invoke(messages)

    # Appending AI's response to the messages list
    return {"messages": [response]}

# Creatinh checkpointer
conn = sqlite3.connect(database = 'chatbot.db', check_same_thread = False)
checkpointer = SqliteSaver(conn = conn)

# Defining graph
graph = StateGraph(ChatState)

# Adding nodes
graph.add_node('chat_node', chat_node)

# Creating edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compiling the graph
workflow = graph.compile(name = 'Streamlit chatbot', checkpointer = checkpointer)

# Function to get threads list
def get_all_threads():
    generator = checkpointer.list(None)

    threads = set()

    for thread in generator:
        thread_id = thread.config['configurable'] ['thread_id']

        threads.add(thread_id)

    return list(threads)