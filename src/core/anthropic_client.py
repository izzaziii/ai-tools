from typing import Optional
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

    Examples:
        ```python
        # Initialize the client with API key from environment variable
        client = AnthropicClient()

        # Or initialize with explicit API key
        client = AnthropicClient(api_key="your-api-key")

        # Stream a message
        model = "claude-3-sonnet-20240229"
        system_prompt = "You are a helpful assistant."
        user_message = "Tell me about quantum computing."

        # Stream the response
        for text_chunk in client.stream_message(
            model=model,
            system=system_prompt,
            user_content=user_message,
            max_tokens=1000
        ):
            print(text_chunk, end="", flush=True)

        # Estimate cost
        input_tokens = 100  # Example token count
        output_tokens = 500  # Example token count
        cost = client.estimate_cost(input_tokens, output_tokens, model)
        print(f"\nEstimated cost: ${cost}")
        ```
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

    def estimate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """
        Estimate the API call cost based on token usage and model.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name

        Returns:
            Estimated cost in USD
        """
        try:
            if model.startswith("claude-3-7-sonnet"):
                input_cost = 3 / 1e6
                output_cost = 15 / 1e6
            return (input_tokens * input_cost) + (output_tokens * output_cost)
        except Exception as e:
            print(f"Error estimating cost: {e}")
            return 0.0
