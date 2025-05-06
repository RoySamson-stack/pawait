from abc import ABC, abstractmethod
from decouple import config
import httpx
import json
import os

# LLM Service Abstract Base Class
class LLMService(ABC):
    @abstractmethod
    async def generate_response(self, query: str) -> str:
        """Generate a response from the LLM based on the query"""
        pass

# # OpenAI (ChatGPT) Implementation
# class OpenAIService(LLMService):
#     def __init__(self, api_key: str):
#         import openai
#         self.client = openai.OpenAI(api_key=api_key)
        
#     async def generate_response(self, query: str) -> str:
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant that provides accurate and concise information. Answer the user's query with well-formatted responses."},
#                     {"role": "user", "content": query}
#                 ],
#                 temperature=0.7,
#                 max_tokens=500
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             raise Exception(f"OpenAI API error: {str(e)}")

# # Anthropic (Claude) Implementation
# class AnthropicService(LLMService):
#     def __init__(self, api_key: str):
#         import anthropic
#         self.client = anthropic.Anthropic(api_key=api_key)
        
#     async def generate_response(self, query: str) -> str:
#         try:
#             response = self.client.completions.create(
#                 model="claude-instant-1",
#                 prompt=f"\n\nHuman: {query}\n\nAssistant:",
#                 max_tokens_to_sample=500,
#                 temperature=0.7
#             )
#             return response.completion
#         except Exception as e:
#             raise Exception(f"Anthropic API error: {str(e)}")

# # Google (Gemini) Implementation
# class GoogleService(LLMService):
#     def __init__(self, api_key: str):
#         import google.generativeai as genai
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel('gemini-pro')
        
#     async def generate_response(self, query: str) -> str:
#         try:
#             response = self.model.generate_content(query)
#             return response.text
#         except Exception as e:
#             raise Exception(f"Google API error: {str(e)}")

# DeepSeek Implementation
class DeepSeekService(LLMService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
    async def generate_response(self, query: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": query}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"API returned status code {response.status_code}: {response.text}")
        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")

# Factory function to get the appropriate LLM service
def get_llm_service() -> LLMService:
    provider = config("LLM_PROVIDER", default="openai").lower()
    
    if provider == "openai":
        api_key = config("OPENAI_API_KEY")
        return OpenAIService(api_key)
    # elif provider == "anthropic":
    #     api_key = config("ANTHROPIC_API_KEY")
    #     return AnthropicService(api_key)
    # elif provider == "google":
    #     api_key = config("GOOGLE_API_KEY")
    #     return GoogleService(api_key)
    elif provider == "deepseek":
        api_key = config("DEEPSEEK_API_KEY")
        return DeepSeekService(api_key)
    # else:
    #     raise ValueError(f"Unsupported LLM provider: {provider}")