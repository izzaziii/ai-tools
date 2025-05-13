from anthropic import Anthropic
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv("C:\\Users\\izzaz\\Documents\\2 Areas\\GitHub\\ai-tools\\.env")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


def create_client(api_key: str) -> Anthropic:
    """
    Create an Anthropic client with the provided API key.
    Args:
        api_key: The API key for Anthropic.
    Returns:
        An instance of the Anthropic client.
    """
    return Anthropic(api_key=api_key)


def create_message(
    system_prompt: str,
    user_prompt: list[str],
    model: str = "claude-3-7-sonnet-20250219",
    max_tokens: int = 30000,
    temperature: float = 0.3,
    stream: bool = False,
):
    """
    Create a message object for the Anthropic API.

    Args:
        system (str): A system message defining the conversation context.
        messages (list[str]): A list of message strings representing conversation history.
        model (str, optional): The model identifier to use. Defaults to "claude-3-7-sonnet-20250219".
        max_tokens (int, optional): Maximum number of tokens allowed in the response. Defaults to 30000.
        temperature (float, optional): Sampling temperature for response generation. Defaults to 0.3.

    Returns:
        object: The created message object as returned by the client's messages.create() method.
    """
    return client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        stream=stream,
        messages=[{"role": "user", "content": user_prompt}],
    )


def create_stream(
    system_prompt: str,
    user_prompt: list[str],
    model: str = "claude-3-7-sonnet-20250219",
    max_tokens: int = 30000,
    temperature: float = 0.3,
):
    """
    Create a message object for the Anthropic API.

    Args:
        system (str): A system message defining the conversation context.
        messages (list[str]): A list of message strings representing conversation history.
        model (str, optional): The model identifier to use. Defaults to "claude-3-7-sonnet-20250219".
        max_tokens (int, optional): Maximum number of tokens allowed in the response. Defaults to 30000.
        temperature (float, optional): Sampling temperature for response generation. Defaults to 0.3.

    Returns:
        object: The created message object as returned by the client's messages.create() method.
    """
    return client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )


def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """
    Estimate the cost of a request to the Anthropic API.
    Args:
        input_tokens: Number of input tokens.
        output_tokens: Number of output tokens.
        model: The model used for the request.
    Returns:
        Estimated cost in USD.
    """
    # Example pricing structure (replace with actual pricing)
    pricing = {
        "claude-3-7-sonnet-20250219": {"input": 3 / 1e6, "output": 3 / 1e6},
        "claude-3-5-haiku-20241022": {"input": 0.8 / 1e6, "output": 4 / 1e6},
    }
    if model in pricing:
        input_cost = pricing[model]["input"]
        output_cost = pricing[model]["output"]
        cost = (input_tokens * input_cost) + (output_tokens * output_cost)
        if cost < 0.01:
            print("Estimated cost: < $0.01")
        else:
            print(f"Estimated cost: ${cost:.2f}")
    else:
        print(f"Model {model} not found in pricing structure.")


if __name__ == "__main__":
    client = create_client(ANTHROPIC_API_KEY)

    sample_dataset_path = r"C:\Users\izzaz\OneDrive - TIME DotCom Berhad\4 Archives\Assessment 2\marketing.csv"
    sample_data = pd.read_csv(sample_dataset_path)

    system_prompt = "You are a data analyst."
    user_prompt = f"""
        Please analyze the following data.

        Please provide:
        1. Executive Summary (key insights in 3-4 bullets)
        2. Data Quality Assessment (missing values, data types, potential issues)
        3. Univariate Analysis (distribution of key variables)
        4. Multivariate Analysis (correlations, relationships between variables)
        5. Marketing-specific Insights (customer patterns, segments, actionable findings)
        6. Recommendations for further analysis

        Format as markdown with clear headings and bullet points. Use tables where necessary.

        {sample_data}
    """

    stream = create_message(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        stream=True,
    )

    for chunk in stream:
        if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
            print(chunk.delta.text, end="", flush=True)
