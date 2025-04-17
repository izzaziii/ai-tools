from core.boreport import BOReport
from core.mongodb import Mongo
from claude import Anthropic


def add_data():
    database_name = "deep-diver-v2"
    collection_name = "test"
    data = BOReport().df
    Mongo(database_name, collection_name).replace_data(data=data)


def get_data():
    database_name = "deep-diver-v2"
    collection_name = "ai-ingestion"
    pipeline = []
    mongo = Mongo(database_name, collection_name)
    df = mongo.get_data(pipeline)
    return df


df = get_data()
json_data = df.to_dict(orient="records")

anthropic_client = Anthropic(api_key="")

response = anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system="Analyze the following data. Return interesting insights and trends.",
    messages=[{"role": "user", "content": f"Analyze this data: {json_data}"}],
    max_tokens=2000,
    stream=True,
)

# Correctly handle the streaming response
for chunk in response:
    # Check if it's a content delta event
    if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
        print(chunk.delta.text, end="")
    # For debugging other event types
    elif hasattr(chunk, "type"):
        pass  # Silently ignore other event types
