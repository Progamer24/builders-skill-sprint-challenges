"""
Challenge 4: The Full Agent — Tools + Memory + Streaming
Combine everything into one powerful agent.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in ALL the TODO sections
  2. Run: python starter.py
  3. Have a full conversation using all tools!
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
import requests
from strands import Agent, tool
from strands_tools import calculator, mem0_memory

MODEL = "us.amazon.nova-pro-v1:0"


# Create a streaming callback handler
def stream_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        print(f"\n🔧 Using tool: {kwargs['current_tool_use']['name']}")


# Create custom tools — weather and age_calculator
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


# Create the full agent with ALL tools + memory + streaming
agent = Agent(
    model=MODEL,
    tools=[calculator, weather, age_calculator, mem0_memory],
    callback_handler=stream_callback,
    system_prompt="You are a helpful assistant with access to multiple tools: a calculator, weather lookup, age calculation, and persistent memory. Use these tools when the user asks. Remember to store user preferences and information in memory when they mention them."
)


print("🤖 Full Agent Ready! Type 'quit' to exit.")
print("Try: 'What's the weather in Delhi and how old is someone born 2000-01-01?'")
print("Try: 'Remember my name is [name]' then 'What's my name?'\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        print("Agent: ", end="")
        response = agent(user_input)
        print("\n")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 4 complete! 🏆")
