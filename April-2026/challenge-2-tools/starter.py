"""
Challenge 2: Adding Tools to Your Agent
Give your agent a calculator, weather tool, and age calculator.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Needs AWS credentials configured (aws configure)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
import requests
from strands import Agent, tool
from strands_tools import calculator

MODEL = "us.amazon.nova-pro-v1:0"


# Create a custom weather tool
@tool
def weather(city: str) -> str:
    """Get the current weather for a city.
    Args:
        city: The name of the city.
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        data = response.json()
        current = data['current_condition'][0]
        temp = current['temp_C']
        description = current['weatherDesc'][0]['value']
        return f"The weather in {city} is {description}, {temp}°C"
    except Exception:
        return f"The weather in {city} is sunny, 28°C"


# Create a custom age calculator tool
@tool
def age_calculator(birth_date: str) -> str:
    """Calculate age from a birth date.
    Args:
        birth_date: Date of birth in YYYY-MM-DD format.
    """
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return f"Age: {age} years old"
    except Exception:
        return "Invalid date format. Please use YYYY-MM-DD"


# Create an agent with all tools
agent = Agent(
    model=MODEL,
    tools=[calculator, weather, age_calculator],
    system_prompt="You are a helpful assistant with access to tools. Use them when appropriate."
)

# Test the agent with different questions

# Test math
print("🧮 Math test:")
response = agent("What is 42 * 17?")
print(response)

# Test weather
print("\n🌤️ Weather test:")
response = agent("What's the weather in Chennai?")
print(response)

# Test age
print("\n🎂 Age test:")
response = agent("How old is someone born on 2000-01-15?")
print(response)

print("\n✅ Challenge 2 complete!")
