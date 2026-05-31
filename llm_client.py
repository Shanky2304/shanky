from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMClient(ABC):

    @abstractmethod
    def chat(self, messages, tool_functions):
        pass

class GroqClient(LLMClient):
    def __init__(self):
        self.client = OpenAI (
            api_key= os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

    def chat(self, messages, tools):
        response = self.client.chat.completions.create(
            model= os.getenv("GROQ_MODEL"),
            messages=messages,
            tools=tools,
        )

        choice = response.choices[0]
        return choice
    
class CerebrasClient(LLMClient):
    def __init__(self):
        self._client = OpenAI(api_key=os.getenv("CEREBRAS_API_KEY"), base_url="https://api.cerebras.ai/v1")

    def chat(self, messages: list, tools: list):
        response = self._client.chat.completions.create(
            model=os.getenv("CEREBRAS_MODEL"),
            messages=messages,
            tools=tools,
        )
        return response.choices[0]    