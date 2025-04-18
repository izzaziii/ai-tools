from typing import Any, Optional
import os
from dotenv import load_dotenv, find_dotenv

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

# Load environment variables
load_dotenv(find_dotenv())


class AnthropicClient:
    """
    A client class for interacting with the Anthropic API.
    Mimics the structure of OpenAIClient.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Anthropic client with API key.
        Args:
            api_key: Optional API key for Anthropic. If not provided, will look for
                    ANTHROPIC_API_KEY in environment variables.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if Anthropic is None:
            raise ImportError("anthropic package is not installed.")
        self.client = Anthropic(api_key=self.api_key)

    def stream_message(
        self, model: str, system: str, user_content: str, max_tokens: int = 2000
    ):
        """
        Stream a message to the Anthropic API and yield text chunks.
        Args:
            model: The Anthropic model name
            system: System prompt
            user_content: User message content
            max_tokens: Max tokens for the response
        Yields:
            Text chunks from the streaming response
        """
        try:
            response = self.client.messages.create(
                model=model,
                system=system,
                messages=[{"role": "user", "content": user_content}],
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in response:
                if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                    yield chunk.delta.text
        except Exception as e:
            print(f"Error streaming from Anthropic: {e}")
            return
