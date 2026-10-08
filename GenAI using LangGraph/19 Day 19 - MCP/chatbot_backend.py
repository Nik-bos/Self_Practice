# This whole session is incomplete. I skipped it and moved to Rag using Langgraph.

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
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition


import asyncio
from tools import google_search, weather_search, fetch_train_details

print("RUNNING UPDATED FILE ✅")


load_dotenv(".env.chatbot")    # Serper_API_KEY is added in .env.chatbot file
os.environ['LANGSMITH_PROJECT'] = 'Chatbot_2'

# Creating the model
model_openai = ChatOpenAI(
    model = 'gpt-3.5-turbo'
)

#----------------------------------------------------------------------------------------------------------------------
# Creating Tools


#----------------------------------------------------------------------------------------------------------------------
# Binding tools
tools_list = [google_search, weather_search, fetch_train_details]
model_with_tools = model_openai.bind_tools(tools_list)
#----------------------------------------------------------------------------------------------------------------------

# Defining the state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#----------------------------------------------------------------------------------------------------------------------

def build_graph():

    # Defining nodes
    async def chat_node(state: ChatState) ->ChatState:

        # Fetching messages
        messages = state["messages"]

        # Invokig model
        response = await model_with_tools.ainvoke(messages)

        # Appending AI's response to the messages list
        return {"messages": [response]}

    # tool node
    tools_node = ToolNode(tools_list)    # ToolNode is internally asynchronous. So we don't need to make it 

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
    workflow = graph.compile(name = 'Streamlit chatbot')

    return workflow

#----------------------------------------------------------------------------------------------------------------------

async def main():

    chatbot = build_graph()

    question = {'messages': [HumanMessage(content = 'When train_no 22959 reaches Rajkot.')]}
    response = await chatbot.ainvoke(question)

    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())