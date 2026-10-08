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
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import requests


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

# google search tool

@tool
def google_search(query: str)-> any:
    '''
    This function takes a query as input and searches for its answer on Google Search Engine.
    You and pass any query.
    '''
    
    search = GoogleSerperAPIWrapper(type = 'search')    
    
    return search.run(query)

# Whether tool
@tool
def weather_search(city:str) ->str:
    '''
    This function returns the live whether data of any city in the world.
    Pass any city name and it will return all the whether details.
    '''

    api_key = '6018a20db02a3eb6aa1ef7bffa662350'

    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"

    response = requests.get(url)

    return response.json()

# Train details tool
@tool
def fetch_train_details(train_number: str) -> str:

    '''
    Given train number, this function fetches all the deetails regarding
    train like train schedule, stations, station timings, when train reaches at different stations,
    Time when train departs from in-between stations, Names of In-between stations. 
    '''
    url = "https://irctc-insight.p.rapidapi.com/api/v1/train-details"
    headers = {
        "x-rapidapi-key": "a386df66c3msha0ef942c346306dp107a95jsn1c48df211ae1",
        "x-rapidapi-host": "irctc-insight.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    payload = {"trainNo": train_number}
    
    response = requests.post(url, json = payload, headers = headers)
    return response.json()

#----------------------------------------------------------------------------------------------------------------------
# Binding tools
tools_list = [google_search, weather_search, fetch_train_details]
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

# Creating checkpointer
checkpointer = MemorySaver()

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

# Using loop

# Defining thread_id
thread_id = '1'
# Defining threads

while True:
    user_input = input("Enter your message to chat: ")
    
    
    if user_input.strip().lower() in ['exit', 'bye', 'break', 'quit']:
        print("ThankYou")
        break
    else:
        
        message = {'messages': [HumanMessage(content = user_input)]}
        config = {"configurable": {'thread_id': "1"}}
        response = workflow.invoke(message, config = config)

        print(f'''User: {user_input}''')
        print(f'''AI: {response['messages'][-1].content}
        
        ''')


# Thread is same as user-id. 
# See, anyone can chat with this bot. How can it know who is chatting. So we pass thread.
# thread = '1', thread = '2', thread = '45', all are different users.