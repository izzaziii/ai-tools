from openai import OpenAI
from typing import Dict, List, Any, Optional, Tuple, Union
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())


class OpenAIClient:
    """
    A client class for interacting with OpenAI API.

    This class provides a simple interface for sending prompts to OpenAI models
    and processing the responses, including token counting.

    Example usage:
    >>> client = OpenAIClient()
    >>> prompt = (
    >>>     "Explain adstock effects in advertising in simple terms. Keep it under 250 words."
    >>> )
    >>> response = client.get_completion(prompt, model="o4-mini-2025-04-16")
    >>> print(response["tokens"])
    >>> print(response["text"])

    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI client with API key.

        Args:
            api_key: Optional API key for OpenAI. If not provided, will look for
                    OPENAI_API_KEY in environment variables.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def query(self, prompt: str, model: str) -> Optional[Any]:
        """
        Send a query to OpenAI API.

        Args:
            prompt: The prompt text to send to the model
            model: The OpenAI model ID to use

        Returns:
            The raw OpenAI response or None if an error occurs
        """
        try:
            return self.client.responses.create(model=model, input=prompt)
        except Exception as e:
            print(f"Error querying OpenAI: {e}")
            return None

    def get_token_info(self, response: Any) -> Tuple[int, int, int]:
        """
        Extract token usage information from an OpenAI response.

        Args:
            response: The OpenAI response object

        Returns:
            Tuple of (input_tokens, output_tokens, total_tokens)
        """
        try:
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            return input_tokens, output_tokens, input_tokens + output_tokens
        except Exception as e:
            print(f"Error extracting token info: {e}")
            return 0, 0, 0

    def get_response_text(self, response: Any, model: str = "") -> str:
        """
        Extract text content from an OpenAI response, handling GPT-4.1 models.
        """
        try:
            return response.__dict__["output"][0].content[0].text
        except Exception as e:
            print(f"Error extracting response text: {e}")
            return "No response text available"

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
            if "gpt-4.1-mini" in model:
                return round((input_tokens * 0.4 + output_tokens * 1.6) / 1_000_000, 6)
            return 0.0
        except Exception as e:
            print(f"Error estimating cost: {e}")
            return 0.0

    def get_completion(
        self,
        prompt: str,
        data: List[Dict[str, Any]] = None,
        model: str = "gpt-4.1-mini-2025-04-14",
    ) -> Dict[str, Any]:
        """
        Get a completion from OpenAI with the given prompt and optional data.

        Args:
            prompt: The prompt text to send to the model
            data: Optional data to append to the prompt
            model: The OpenAI model ID to use (defaults to gpt-4.1-mini)

        Returns:
            Dictionary containing the response text, token usage, and estimated cost
        """
        api_prompt = prompt
        if data:
            api_prompt = f"{prompt} Dataset: {data}"

        response = self.query(api_prompt, model)
        if not response:
            return {"text": "Failed to get response", "tokens": (0, 0, 0), "cost": 0.0}

        tokens = self.get_token_info(response)
        text = self.get_response_text(response)
        cost = self.estimate_cost(tokens[0], tokens[1], model)
        return {
            "text": text,
            "tokens": {"input": tokens[0], "output": tokens[1], "total": tokens[2]},
            "cost": {"cost in USD ($)": cost},
        }
