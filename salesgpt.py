from core.mongodb import Mongo
from core.openai_client import OpenAIClient
from typing import Dict, List, Any


def get_data(
    database_name: str, collection_name: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """Fetch data from MongoDB with specified limit."""
    try:
        return Mongo(database_name, collection_name).get_data_json([{"$limit": limit}])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def main():
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

    # Initialize the client
    client = OpenAIClient()  # Will use API key from environment variable

    # Get a completion
    result = client.get_completion(
        prompt=prompt,
        data=data,  # Optional
        model="gpt-4.1-nano-2025-04-14",  # Optional, this is the default
    )

    # Access the response
    response_text = result["text"]
    input_tokens, output_tokens, total_tokens = result["tokens"]

    print(
        f"\nInput Tokens: {input_tokens}. Output Tokens: {output_tokens}. Total Tokens: {total_tokens}\n"
    )
    print("Output:")
    print(response_text)
    print("\n")


if __name__ == "__main__":
    main()
