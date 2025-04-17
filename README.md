# ai-tools

## Dev notes
1000 rows from mongo results in 60K tokens.
20000 rows from mongo results in 1200K tokens, or 1.2M.
We need an input window of 1.2M, at least.

salesgpt.py works well for small contexts, maybe for large ones its better to just process it here with CPU power.

Then we deliver it to the model for insights extraction or reports generation.
