"""
Challenge 3: Agent with Persistent Memory
Give your agent memory that survives restarts using FAISS.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Store some facts, then quit and restart to verify persistence
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from strands import Agent
from strands_tools import mem0_memory

MODEL = "us.amazon.nova-pro-v1:0"


# Create an agent with mem0_memory tool
agent = Agent(
    model=MODEL,
    tools=[mem0_memory],
    system_prompt="You are a helpful assistant with persistent memory. When the user tells you something to remember, store it. When they ask about their preferences, recall what you've stored."
)


print("🧠 Memory Agent Ready!")
print("Try: 'Remember that my name is [your name] and I love [food]'")
print("Then: 'What's my name and what food do I like?'")
print("Type 'quit' to exit.\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        response = agent(user_input)
        print(f"Agent: {response}")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 3 complete!")
