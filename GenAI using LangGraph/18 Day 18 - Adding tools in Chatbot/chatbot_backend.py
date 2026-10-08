# We have added LangSmith's API key, endpoint and project's name in .env.chatbot file 
# So just load that particular files using load_dotenv()
# We don't need to make any changes in backend file.

import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import requests

from tools import google_search, whether_search, fetch_train_details


load_dotenv(".env.chatbot")    # Serper_API_KEY is added in .env.chatbot file
os.environ['LANGSMITH_PROJECT'] = 'Chatbot_2'

#----------------------------------------------------------------------------------------------------------------------

# Creating the model
model_gemini = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash')

model_openai = ChatOpenAI(
    model = 'gpt-3.5-turbo'
)

#----------------------------------------------------------------------------------------------------------------------
# Creating Tools


#----------------------------------------------------------------------------------------------------------------------
# Binding tools
tools_list = [google_search, whether_search, fetch_train_details]
model_with_tools = model_openai.bind_tools(tools_list)
#----------------------------------------------------------------------------------------------------------------------

# Defining the state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#----------------------------------------------------------------------------------------------------------------------

# Defining nodes
def chat_node(state: ChatState) ->ChatState:

    # Fetching messages
    messages = state["messages"]

    # Invokig model
    response = model_with_tools.invoke(messages)

    # Appending AI's response to the messages list
    return {"messages": [response]}

#----------------------------------------------------------------------------------------------------------------------

# Creatinh checkpointer
conn = sqlite3.connect(database = 'chatbot.db', check_same_thread = False)   # Always keep check_same_thread as False
checkpointer = SqliteSaver(conn = conn)

#----------------------------------------------------------------------------------------------------------------------
# tool node
tools_node = ToolNode(tools_list)

# Defining graph
graph = StateGraph(ChatState)

# Adding nodes
graph.add_node('chat_node', chat_node)
graph.add_node("tools", tools_node)

# Creating edges
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools', 'chat_node')

# Compiling the graph
workflow = graph.compile(name = 'Streamlit chatbot', checkpointer = checkpointer)

#----------------------------------------------------------------------------------------------------------------------

# Function to get threads list
def get_all_threads():
    generator = checkpointer.list(None)

    threads = set()

    for thread in generator:
        thread_id = thread.config['configurable'] ['thread_id']

        threads.add(thread_id)

    return list(threads)