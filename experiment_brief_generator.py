import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=" * 60)
print("AI Experiment Brief Generator")
print("Powered by Claude | Inspired by Optimizely AI")
print("=" * 60)

business_problem = input("\nWhat is the business problem you are trying to solve? \n> ")
metric = input("\nWhat metric are you trying to improve? (e.g. conversion rate, retention) \n> ")
target_user = input("\nWho is the target user? (e.g. new users, all users, paid users) \n> ")
proposed_change = input("\nWhat change are you proposing to test? \n> ")
success_criteria = input("\nWhat does success look like? (e.g. 5% improvement in conversion) \n> ")

prompt = f"""
You are an expert experimentation strategist with deep knowledge 
of A/B testing, CRO, and product analytics.

A product team has come to you with the following:

Business Problem: {business_problem}
Metric to Improve: {metric}
Target User: {target_user}
Proposed Change: {proposed_change}
Success Criteria: {success_criteria}

Generate a structured A/B test brief with the following sections:
1. Hypothesis
2. Primary Metric
3. Secondary Metrics to Monitor
4. Experiment Design
5. Risks and Considerations
6. Recommendation if Successful
7. Recommendation if Unsuccessful
"""

print("\nGenerating your experiment brief...\n")

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("=" * 60)
print("EXPERIMENT BRIEF")
print("=" * 60)
print(message.content[0].text)
print("=" * 60)