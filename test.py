from core.openai_client import OpenAIClient
from core.ols import OLS


# Get OLS data
ols = OLS()
df = ols.get_ols_dataframe(start_date="2025-04-15", end_date="yesterday")

# Transform to JSON
json_data = df.to_dict(orient="records")

# Request analysis from OpenAI
client = OpenAIClient()
prompt = f"""
    Assume the role of a data analyst for a telecommunications company.

    You are given a dataset in JSON format. Your task is to write a written report on the dataset for the website optimization team.

    Your report should include insights and patterns found in the data, as well as any recommendations for improving website performance based on the data.

    Think step-by-step before writing the report. First, think of what the website optimization team would care about most. Next, when listing down your insights, ensure that they are relevant to the website optimization team. Finally, order the insights by projected impact.

    Information on the dataset:
    - traffic: The number of users who visited the website.
    - view_item: The number of users who started the sales process.
    - type_addr: The number of users who typed an installation address.
    - add_contact: The number of users who added a contact info.
    - add_addr: The number of users who successfully added an installation address.
    - add_date: The number of users who successfully added an installation date.
    - checkout: The number of users who started the checkout process.
    - purchase: The number of users who completed a purchase.
    - date: The date of the event.

    Context on our telecommunications business:
    - We sell home fibre internet plans.
    - We have a website where users can sign up for our services.
    - Our network coverage is not available in all areas, and only in densely populated areas. This means that we have to be careful about how we market our services, lest we get too much interest in areas where we cannot provide service.
    - We are a small player in the telecommunications market, and we are trying to grow our market share.

    Limit your report to a maximum of 300 words.



    Dataset: {json_data}
    """
response = client.get_completion(prompt, model="gpt-4.1-mini-2025-04-14")
print(response["tokens"])
print(response["text"])
