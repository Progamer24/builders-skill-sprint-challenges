# Challenge 1 — Findings

## What I asked the agent

I queried the AWS DevOps Agent with the following questions:
1. `What resources do I have in this account?`
2. `Is anything unhealthy right now?`
3. `Give me a health summary of my environment.`

## What the agent told me

The agent provided a comprehensive plain-English summary of my AWS account, identifying:
- All deployed CloudFormation stacks and their resources
- The Lambda functions deployed for the challenges (challenge2-broken-fn, challenge4-app-fn)
- The EC2 instance for Challenge 3 (challenge3-stress)
- The DynamoDB table for Challenge 4 (challenge4-data)
- Overall health status of resources
- Any alarms or issues detected across the environment

The agent demonstrated its ability to understand natural language queries and provide actionable insights about the AWS infrastructure without requiring complex dashboard navigation.

## Evidence

- ✅ Screenshot: The DevOps Agent successfully answered all three questions in plain English, demonstrating it understood the AWS account context
- ✅ Screenshot: The Topology view shows a visual map of all resources in the account, organized by service type

## Key Learnings

**Challenge 1 introduces the foundation:** The AWS DevOps Agent acts as an intelligent AWS teammate. Rather than hunting through the console, you ask it questions and get conversational responses. This challenge proves the agent can:
- Understand natural language queries
- Aggregate information across multiple AWS services
- Communicate findings in human-friendly language
- Maintain conversation context for follow-up questions

---

**What this demonstrates for DevOps teams:**
The agent eliminates the need for expertise in every AWS service. A junior engineer or on-call operator can ask straightforward questions and get immediate insights, accelerating Mean Time To Resolution (MTTR).
