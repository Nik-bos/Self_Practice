from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv(".env.langsmith")
os.environ['LANGSMITH_PROJECT'] = "Sequential LLM APP"


prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model_1 = ChatOpenAI(model = 'gpt-3.5-turbo', temperature = 0.8)
model_2 = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0.5)

parser = StrOutputParser()

chain = prompt1 | model_1 | parser | prompt2 | model_2 | parser

config = {"run_name": 'sequential_llm',
          "tags": ['llm_app', 'report_generation', 'summarization'],
          'metadata': {'model_1': 'gpt-3.5-turbo',
                       "model_1_temp": 0.7,
                       "model_2": 'gpt-4o-mini',
                       'model_2_temp': 0.5,
                       'parser': 'str_output_parser'
                      },
          'configurable': {'thread_id': '1'}
         }

result = chain.invoke({'topic': 'Indian Shankhya Darshan'}, config = config)

print(result)
