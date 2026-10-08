from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import requests
from dotenv import load_dotenv

load_dotenv(".env.chatbot")    # Serper_API_KEY is added in .env.chatbot file


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