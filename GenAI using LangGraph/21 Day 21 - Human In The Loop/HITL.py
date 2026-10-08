from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AnyMessage, AIMessage, BaseMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
from typing import Annotated, TypedDict, List

# This is for Human In The Loop
from langgraph.types import interrupt, Command

load_dotenv('.env.chatbot')

model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash'
)

# Defining chat state

class ChatState(MessagesState):
    pass

# Creating chatnode

def chatnode(state: ChatState):

    decision = interrupt(
        {
            "type": 'approval',
            "type": "Model is about to answer the user question",
            'question': state['messages'][-1].content,
            'instruction': "Approve this request (yes/no)"
        }
    )

    if decision['approved'] == 'no':
        return {'messages': [AIMessage(content = 'Not approved')]}
    else:
        response = model.invoke(state['messages'][-1])
        return {'messages': [response]}
    
    # Creating stategraph
graph = StateGraph(ChatState)

# Adding nodes
graph.add_node('chatnode', chatnode)

# Adding edges
graph.add_edge(START, 'chatnode')

# Compiling
chatbot = graph.compile(checkpointer = MemorySaver())

