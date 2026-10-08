from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

load_dotenv()

# Creating the model
model_gemini = ChatGoogleGenerativeAI(
    model = 'gemini-1.5-flash')

# Defining the state

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Defining nodes
def chat_node(state: ChatState) ->ChatState:

    # Fetching messages
    messages = state["messages"]

    # Invokig model
    response = model_gemini.invoke(messages)

    # Appending AI's response to the messages list
    return {"messages": [response]}

# Creatinh checkpointer
checkpointer = InMemorySaver()

# Defining graph
graph = StateGraph(ChatState)

# Adding nodes
graph.add_node('chat_node', chat_node)

# Creating edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# Compiling the graph
workflow = graph.compile(name = 'Streamlit chatbot', checkpointer = checkpointer)