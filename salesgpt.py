from core.mongodb import Mongo
from openai import OpenAI
from typing import Dict, List, Any, Optional, Tuple, Union
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def get_data(
    database_name: str, collection_name: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """Fetch data from MongoDB with specified limit."""
    try:
        return Mongo(database_name, collection_name).get_data_json([{"$limit": limit}])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def query_openai(
    prompt: str, model: str, api_key: Optional[str] = None
) -> Optional[Any]:
    """Query OpenAI with the given prompt and model."""
    try:
        client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        return client.responses.create(model=model, input=prompt)
    except Exception as e:
        print(f"Error querying OpenAI: {e}")
        return None


def get_token_info(response: Any) -> Tuple[int, int, int]:
    """Extract token usage information from OpenAI response."""
    try:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        return input_tokens, output_tokens, input_tokens + output_tokens
    except Exception as e:
        print(f"Error extracting token info: {e}")
        return 0, 0, 0


def get_response_text(response: Any) -> str:
    """Extract text from OpenAI response."""
    try:
        return response.output[0].content[0].text
    except Exception as e:
        print(f"Error extracting response text: {e}")
        return "No response text available"


def get_response(
    prompt: str,
    data: List[Dict[str, Any]],
    model: str = "gpt-4.1-nano-2025-04-14",
    api_key: Optional[str] = OPENAI_API_KEY,
) -> Dict[str, Union[str, Tuple[int, int, int]]]:
    api_prompt = f"{prompt} Dataset: {data}"
    response = query_openai(api_prompt, model, api_key)

    if not response:
        return {"text": "Failed to get response", "tokens": (0, 0, 0)}

    tokens = get_token_info(response)
    text = get_response_text(response)

    return {"text": text, "tokens": tokens}


def main():
    api_key = OPENAI_API_KEY
    database_name = "deep-diver-v2"
    collection_name = "ai-ingestion"
    data_limits = 1000

    prompt = """
        You are a senior business data analyst preparing for a weekly review of sales data of a telecommunications company selling home fibre internet subscriptions. You have been provided a dataset.

        The dataset contains sales records with the following fields:
        - "Probability 90% Date": The date when the probability of closing the sale is 90%. We take this as when the sale is closed.
        - "Channel": The sales channel (ONLINE, INSIDE SALES, DEALER)
        - "Funnel Bandwidth": The selected bandwidth of subscription by the user, in Mbps
        - "Funn Monthcontractperiod": The contract period in months selected by the user
        - "Blk State": The state in which the sale was made
        - "Signups": The total sales amount for that channel, bandwidth, contract, and state on that day

        The week to be reviewed is the week beginning 2025-04-07 (Monday) and ending 2025-04-13 (Sunday).

        Summarize the following dataset and return it in the below JSON-formatted response. Only output the JSON response. Do not include any other text.

        {
            "Total Sales in Period": (the total sales for the week),
            "Sales by Bandwidth": {
                    200 : (the total sales for the week with "Funnel Bandwidth" 200),
                    600 : (the total sales for the week with "Funnel Bandwidth" 600),
                    1000 : (the total sales for the week with "Funnel Bandwidth" 1000),
                    2000 : (the total sales for the week with "Funnel Bandwidth" 2000),
            },
            "Sales by Bandwidth (%): {
                    200 : (the total sales for the week with "Funnel Bandwidth" 200 as a percentage of total sales),
                    600 : (the total sales for the week with "Funnel Bandwidth" 600 as a percentage of total sales),
                    1000 : (the total sales for the week with "Funnel Bandwidth" 1000 as a percentage of total sales),
                    2000 : (the total sales for the week with "Funnel Bandwidth" 2000 as a percentage of total sales),
            },
            "Sales by Channel": {
                    "ONLINE" : (the total sales for the week with "Channel" ONLINE),
                    "INSIDE SALES" : (the total sales for the week with "Channel" INSIDE SALES),
                    "DEALER" : (the total sales for the week with "Channel" DEALER),
            },
            "Sales by Channel (%): {
                    "ONLINE" : (the total sales for the week with "Channel" ONLINE as a percentage of total sales),
                    "INSIDE SALES" : (the total sales for the week with "Channel" INSIDE SALES as a percentage of total sales),
                    "DEALER" : (the total sales for the week with "Channel" DEALER as a percentage of total sales),
            },
        }
    """

    data = get_data(database_name, collection_name, limit=data_limits)
    result = get_response(prompt=prompt, data=data, api_key=api_key)

    input_tokens, output_tokens, total_tokens = result["tokens"]
    print(
        f"\nInput Tokens: {input_tokens}. Output Tokens: {output_tokens}. Total Tokens: {total_tokens}\n"
    )
    print("Output:")
    print(result["text"])
    print("\n")


if __name__ == "__main__":
    main()
