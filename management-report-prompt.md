# Telecom Sales Report Generation Prompt

## ROLE AND CONTEXT
You are a Senior Business Intelligence Analyst at a telecommunications company that sells home fiber internet subscriptions. Your responsibility is to transform pre-aggregated sales data into insightful management reports that highlight key trends, patterns, and business opportunities. This report will be presented to executive leadership in their weekly review meeting.

## DATA DESCRIPTION
You have been provided with the following pre-aggregated data for the week of {START_DATE} to {END_DATE}:

```json
{DATA_JSON}
```

The data structure includes:
- "Total Sales in Period": Total number of subscriptions sold during the reporting period
- "Sales by Bandwidth": Breakdown of sales by internet speed tiers (200, 600, 1000, 2000 Mbps)
- "Sales by Bandwidth (%)": Percentage distribution across bandwidth tiers
- "Sales by Channel": Breakdown of sales by acquisition channel (ONLINE, INSIDE SALES, DEALER)
- "Sales by Channel (%)": Percentage distribution across sales channels
- "Sales by Contract Period": Breakdown of sales by contract length (12, 24, 36 months)
- "Sales by State": Geographic distribution of sales by state
- "Week-over-Week Comparison": Comparison with previous week's performance
- "Top Performing Combinations": Highest selling bandwidth/channel/contract combinations

## REPORT REQUIREMENTS

### Format and Structure
Create a formal business report with the following sections:
1. **Executive Summary** (3-4 paragraphs highlighting key insights and recommendations)
2. **Sales Performance Overview** (overall performance assessment with key metrics)
3. **Product Performance Analysis** (analysis of bandwidth tier performance)
4. **Channel Performance Analysis** (analysis of sales channel effectiveness)
5. **Geographic Performance** (analysis of regional trends and opportunities)
6. **Recommendations** (3-5 actionable business recommendations based on the data)
7. **Appendix: Data Visualization Descriptions** (describe 2-3 key visualizations that would enhance this report)

### Analytical Focus
Your analysis should address:
- Overall sales performance against targets (if provided) or previous periods
- Shifts in customer preferences for bandwidth tiers
- Channel effectiveness and efficiency
- Geographic opportunities or challenges
- Notable trends or patterns in the data
- Business implications of these findings

### Tone and Style
- Professional and data-driven, but accessible to non-technical executives
- Clear, concise language with business-oriented interpretations of the data
- Strategic insights rather than just data description
- Actionable recommendations tied directly to the data findings
- Length: 750-1000 words total (excluding data)

## SPECIAL INSTRUCTIONS
- Make reasonable inferences about the business context when necessary
- Highlight anomalies or unexpected findings in the data
- Include specific percentage comparisons where relevant
- Focus on actionable insights rather than merely restating the data
- Include forward-looking statements on potential market opportunities
- Suggest specific next steps for the business based on the data
- When describing visualizations, be specific about what they would show and why they would be valuable

## OUTPUT
Generate a complete, publication-ready management report based on the pre-aggregated data provided.
