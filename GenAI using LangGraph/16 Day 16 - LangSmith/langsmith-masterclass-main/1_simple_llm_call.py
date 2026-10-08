from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv(".env.langsmith")

# We can also change project's name from here.
os.environ["LANGSMITH_PROJECT"] = 'custom_project_name'

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

model = ChatOpenAI(model = "gpt-3.5-turbo", temperature = 0.7)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# We can also add our custom configuration (Optional)
config = {"run_name": 'simple_chain',
         'tags': ['llm_app', 'question_answer'],
         "metadata": {"model": 'gpt-3.5-turbo', "temp": 0.7, 'parser': 'str_output_parser'}
         }

# run_name: To give custom run name. By-default 'RunableSequence'

result = chain.invoke({"question": "What is the capital of Japan?"}, config = config)
print(result)
