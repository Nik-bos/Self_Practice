from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["LANGSMITH_PROJECT"] = "Subgraph Example_2"

# Initializing the model
model = ChatOpenAI(model="gpt-3.5-turbo")

class ParentState(TypedDict):
    question: str
    english_answer: str
    hindi_answer: str

    # Defining the translation node

def translation_node(state: ParentState):
    text = state['english_answer']

    prompt = f'''Translate the below given text into Hindi. Do not add any extra comments.
    
    Text: {text}
    '''

    translated_text = model.invoke(prompt)

    return {'hindi_answer': translated_text.content.strip()}

subgraph_builder = StateGraph(ParentState)

subgraph_builder.add_node('translation_node', translation_node)

# Creating edges
subgraph_builder.add_edge(START, 'translation_node')

subgraph = subgraph_builder.compile()

# Defining answer node
def generate_answer(state: ParentState):
    question = state['question']

    prompt = f'''Answer the below given question.
    
    Question: {question}'''

    answer = model.invoke(prompt).content.strip()

    return {'english_answer': answer}

parent_builder = StateGraph(ParentState)

# Adding nodes
parent_builder.add_node('generate_answer', generate_answer)
parent_builder.add_node('translate', subgraph)


# Adding edges
parent_builder.add_edge(START, 'generate_answer')
parent_builder.add_edge('generate_answer', 'translate')

final_workflow = parent_builder.compile()

if __name__ == "__main__":

    initial_input = {
        'question': 'Considering all indian shashtras and saints sayings, make me believe that NAAM JAPP will keep Bhagwan Krishna with me and save me from every sorrows and circumstances.'
    }

    response = final_workflow.invoke(initial_input)

    print("="*25, 'Final Response', "="*25)
    print(response)

    print("="*25, 'Hindi Translation', "="*25)
    print(response['hindi_answer'])