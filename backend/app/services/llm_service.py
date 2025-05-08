from abc import ABC, abstractmethod
from decouple import config
import httpx
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abstract Base Class
class LLMService(ABC):
    @abstractmethod
    async def generate_response(self, query: str) -> str:
        """Generate a response from the LLM based on the query"""
        pass

# OpenAI  Implementation
class OpenAIService(LLMService):
    def __init__(self, api_key: str):
        logger.info("Initializing OpenAI service")
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            logger.error("OpenAI package not installed. Please run 'pip install openai'")
            raise
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            raise
        
    async def generate_response(self, query: str) -> str:
        try:
            logger.info("Sending request to OpenAI API")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides accurate and concise information. Answer the user's query with well-formatted responses."},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")

# DeepSeek Implementation
class DeepSeekService(LLMService):
    def __init__(self, api_key: str):
        logger.info("Initializing DeepSeek service")
        if not api_key or api_key == "your_deepseek_api_key_here":
            logger.error("DeepSeek API key not provided or using placeholder value")
            raise ValueError("Valid DeepSeek API key is required")
            
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
    async def generate_response(self, query: str) -> str:
        try:
            logger.info(f"Sending request to DeepSeek API: {self.api_url}")
            
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            logger.info(f"Request payload: {json.dumps(payload)}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                logger.info(f"DeepSeek API response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_msg = f"API returned status code {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
        except httpx.TimeoutException:
            error_msg = "Request to DeepSeek API timed out"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.RequestError as e:
            error_msg = f"Error making request to DeepSeek API: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"DeepSeek API error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

# Factory function to get the appropriate LLM service
def get_llm_service() -> LLMService:
    provider = config("LLM_PROVIDER", default="openai").lower()
    logger.info(f"Using LLM provider: {provider}")
    
    try:
        if provider == "openai":
            api_key = config("OPENAI_API_KEY")
            return OpenAIService(api_key)
        elif provider == "deepseek":
            api_key = config("DEEPSEEK_API_KEY")
            return DeepSeekService(api_key)
        else:
            error_msg = f"Unsupported LLM provider: {provider}"
            logger.error(error_msg)
            raise ValueError(error_msg)
    except Exception as e:
        logger.error(f"Error initializing LLM service: {str(e)}")
        raise