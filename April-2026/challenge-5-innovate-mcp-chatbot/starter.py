"""
Challenge 5 (Innovate): Build Your Own MCP-Powered Agent

YOUR TASK:
  Build an innovative agent from scratch that connects to any MCP server.
  The most creative and useful agent gets a special shoutout! 🏆

RULES:
  - Must use Strands Agents SDK
  - Must use at least one MCP server
  - Must use Amazon Nova Pro (or any Bedrock model)
  - Must have an interactive chat loop
  - Must be YOUR OWN idea — be creative!

EXAMPLE MCP SERVERS:
  pip install awslabs.aws-documentation-mcp-server   # AWS Docs
  uvx awslabs.cdk-mcp-server@latest                  # AWS CDK
  uvx awslabs.cost-analysis-mcp-server@latest        # AWS Pricing

BROWSE MORE: https://github.com/modelcontextprotocol/servers

RESOURCES:
  - Strands MCP docs: https://strandsagents.com/latest/user-guide/concepts/tools/mcp-tools/
  - AWS MCP servers: https://github.com/awslabs/mcp

Build something that makes us go "whoa!" 🚀
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

import sys
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client

MODEL = "us.amazon.nova-pro-v1:0"

# Streaming callback for real-time output
def stream_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        print(f"\n📚 Using tool: {kwargs['current_tool_use']['name']}")

# Create the agent with MCP tools
try:
    print("🚀 Initializing AWS Expert Multi-Tool MCP Agent...")
    print("🔌 Connecting to AWS Documentation MCP Server...")
    
    # Create AWS Documentation MCP Client
    aws_docs_mcp = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command="awslabs.aws-documentation-mcp-server")
        )
    )
    
    with aws_docs_mcp:
        # List available tools from the MCP server
        tools = aws_docs_mcp.list_tools_sync()
        print(f"✅ Connected successfully! Found {len(tools)} AWS documentation tools.")
        
        # Create the agent
        agent = Agent(
            model=MODEL,
            tools=tools,
            callback_handler=stream_callback,
            system_prompt="""You are an AWS Expert Assistant powered by the latest AWS Documentation. 
You have access to comprehensive AWS service documentation and best practices.
Help users understand AWS services, architecture patterns, pricing, security best practices, and more.
When users ask about AWS, search the documentation and provide accurate, helpful, and well-structured information.
Always cite the source of your information from the AWS documentation."""
        )
        
        # Interactive chat loop
        print("=" * 60)
        print("🤖 AWS Expert Agent Ready!")
        print("=" * 60)
        print("\nAsk me anything about AWS services and best practices!")
        print("Examples:")
        print("  - 'What is Amazon S3 and how do I use it?'")
        print("  - 'How do I set up Lambda?'")
        print("  - 'What are AWS security best practices?'")
        print("  - 'Explain EC2 vs Fargate'")
        print("\nType 'quit' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("quit", "exit", "q"):
                    print("\n👋 Thanks for using AWS Expert Agent!")
                    break
                
                print("\nAgent: ", end="")
                response = agent(user_input)
                print("\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using AWS Expert Agent!")
                break

except Exception as e:
    print(f"❌ Error during initialization: {e}")
    print("\nMake sure:")
    print("  1. AWS Documentation MCP is installed: pip install awslabs.aws-documentation-mcp-server")
    print("  2. AWS credentials are configured: aws configure")
    print("  3. You have Bedrock access in your AWS account")

print("\n✅ Challenge 5 complete!")
