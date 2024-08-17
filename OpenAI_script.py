from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import (email_schema)
import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")


class extensionEmailGenerator():
    def __init__(self):
        api_key = os.environ["OPEN_AI_API_KEY"]

        self.llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

        self.threads = []

    def generate_email(self, message: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a professional email writing assistant. You will be used by high end clients. Write emails based on a user's prompt."),
            ("user", "{input}")
        ])

        output_parser = PydanticOutputParser(pydantic_object=email_schema)
        llm_chain = prompt | self.llm | output_parser

        generated_email = llm_chain.invoke({"input": message})

        return generated_email
