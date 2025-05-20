from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os


llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))


template = """
You are an AI assistant with expertise in construction project cost estimation and technical advice.
Answer the customer's question as clearly and helpfully as possible.

Question: {question}
"""

prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(prompt=prompt, llm=llm)

def ask_ai_agent(question: str) -> str:
    try:
        return chain.run(question=question)
    except Exception as e:
        return f"Error: {str(e)}"
