# From Firefighting to Foresight: My Journey Through AWS DevOps Agent Challenges

## Table of Contents
1. [Introduction](#introduction)
2. [The Challenges Overview](#the-challenges-overview)
3. [Challenge-by-Challenge Breakdown](#challenge-by-challenge-breakdown)
4. [Key Insights & Learnings](#key-insights--learnings)
5. [The Bigger Picture: Why This Matters](#the-bigger-picture-why-this-matters)
6. [Recommendations for Your Team](#recommendations-for-your-team)
7. [Conclusion](#conclusion)

---

## Introduction

I recently completed the AWS DevOps Agent Builders Skill Sprint—a hands-on challenge series designed to demonstrate how AI-powered infrastructure diagnostics can transform the way we do SRE. This blog post documents my journey through all 5 challenges, what I learned, and why I believe this is the future of DevOps.

**TL;DR:** AWS DevOps Agent isn't just a monitoring dashboard—it's an intelligent teammate that asks the right questions, correlates disparate signals, and gets to root causes faster than humans sifting through logs.

---

## The Challenges Overview

The Skill Sprint consists of 5 progressive challenges:

| # | Challenge | Focus | Difficulty | Time |
|---|-----------|-------|-----------|------|
| 1 | **Meet Your Agent** | Natural language interaction with AWS | ⭐ | 10 min |
| 2 | **First Investigation** | Debug a broken Lambda (code error) | ⭐⭐ | 20 min |
| 3 | **Stress & Diagnose** | Diagnose runaway EC2 CPU | ⭐⭐⭐ | 25 min |
| 4 | **Bad Deploy Detective** | Find hidden IAM permission issues | ⭐⭐⭐⭐ | 25 min |
| 5 | **Build Your Own** | Design an original break & investigation | 🚀 | 30+ min |

Each challenge isolates a specific failure pattern common in production:
- **Code bugs** (Challenge 2)
- **Resource exhaustion** (Challenge 3)
- **Configuration/permission issues** (Challenge 4)
- **Cross-service complexity** (Challenge 5)

---

## Challenge-by-Challenge Breakdown

### Challenge 1: Meet Your Agent ⭐

**Goal:** Prove the agent works by asking it about your AWS account.

**What I Did:**
1. Opened the DevOps Agent web app (a dedicated dashboard, separate from AWS Console)
2. Asked three natural-language questions:
   - "What resources do I have in this account?"
   - "Is anything unhealthy right now?"
   - "Give me a health summary of my environment."

**What Happened:**
The agent responded with a plain-English summary of my AWS infrastructure. It:
- Listed all deployed stacks and resources
- Identified health issues (Lambda failures, EC2 stress, permissions problems)
- Provided a visual "Topology" view showing service relationships
- Maintained conversation context for follow-up questions

**The Insight:**
Traditional AWS dashboards require expertise in each service. You need to:
- Know to check Lambda logs in CloudWatch
- Navigate IAM → Roles → search for the right role
- Correlate metrics across multiple views

The DevOps Agent skips all this. You ask a question in English, and it synthesizes the answer.

**Why It Matters:**
- **Democratizes SRE expertise** - Junior engineers can troubleshoot without deep AWS knowledge
- **Accelerates Mean Time To Recognition (MTTR)** - No dashboard hunting
- **Natural interface** - Reduces cognitive load (asking beats clicking)

---

### Challenge 2: First Investigation ⭐⭐

**Scenario:** A Lambda function called `challenge2-broken-fn` fails on every invocation. The error rate is 100%, and the `challenge2-broken-fn-errors` alarm is screaming red.

**What I Did:**
1. Deployed the broken Lambda using CloudFormation
2. Triggered several test invocations to generate failures
3. Asked the DevOps Agent: "The Lambda function challenge2-broken-fn is failing on every invocation. Investigate and tell me the root cause and how to fix it."

**What the Agent Found:**
The agent analyzed CloudWatch logs and immediately identified:
```
NameError: name 'config' is not defined
  File "/var/task/index.py", line 4, in handler
    return {"result": config["value"]}
```

**The Root Cause:**
The original code tried to access a variable `config` that was never defined:

```python
def handler(event, context):
    # This line fails because 'config' is not defined
    return {"result": config["value"]}
```

This is a classic Python NameError—the kind that takes 5 minutes to spot in code review but can cause hours of production incidents if not caught early.

**The Fix:**
Define the config variable before using it:

```python
def handler(event, context):
    config = {"value": "Challenge 2 is now fixed!"}
    return {"result": config["value"]}
```

**The Verification:**
- Redeployed the Lambda with fixed code
- Ran test invocation → returned 200 OK
- CloudWatch alarm transitioned from ALARM → OK

**Key Takeaway:**
The DevOps Agent eliminated manual log searching. Instead of:
1. Opening CloudWatch Logs console
2. Searching for the Lambda log group
3. Reading through 100+ log lines
4. Spotting the stack trace
5. Researching what "NameError" means

...I asked the agent one question and got the answer. **Time saved: ~10 minutes.**

---

### Challenge 3: Stress & Diagnose ⭐⭐⭐

**Scenario:** An EC2 instance called `challenge3-stress` is running at 100% CPU utilization. The `challenge3-high-cpu` alarm is firing continuously. Users are complaining about slow performance. Your job: diagnose and recover the instance.

**What I Did:**
1. Deployed the EC2 instance via CloudFormation
2. Waited ~2 minutes for the CPU alarm to trigger (as expected)
3. Asked the Agent: "My EC2 instance challenge3-stress is slow and its alarm is firing. Investigate the cause and tell me how to fix it."

**What the Agent Found:**
The agent identified that the instance had launched with runaway CPU-intensive processes:

```bash
# The bootstrap script spawned infinite loops:
for i in $(seq $(nproc)); do
    setsid /bin/bash -c 'while true; do :; done &'
done
```

Each CPU core runs `while true; do :; done` (an empty infinite loop), consuming 100% of available CPU. This is intentional for the challenge, but in production, this would represent:
- Unoptimized code in a loop
- Memory leak causing garbage collection storms
- Batch job that never completes
- Accidentally forked recursive process

**The Fix:**
1. Use AWS Systems Manager Session Manager to connect to the instance (no SSH keys needed)
2. Identify and kill the runaway processes:
   ```bash
   ps aux | grep "while true"
   killall bash
   ```
3. Verify CPU returns to normal
4. Confirm the alarm transitions to OK

**The Result:**
- CPU dropped from 100% → <5% in seconds
- CloudWatch alarm: ALARM → OK
- Instance recovered and responsive

**Key Takeaway:**
This challenge demonstrates **real-world incident response.** The agent:
- Correlated CloudWatch metrics with EC2 state
- Identified the exact cause (process loop, not misconfiguration)
- Recommended the right tool (Session Manager)
- Verified recovery (alarm status)

Without the agent, this investigation would require:
- Checking EC2 dashboard
- Checking CloudWatch graphs
- Checking CloudWatch Logs for user data errors
- SSH into the instance (requires key management)
- Manual process inspection

**Time saved: ~15 minutes.**

---

### Challenge 4: Bad Deploy Detective ⭐⭐⭐⭐

**Scenario:** An app (`challenge4-app-fn`) reads from a DynamoDB table. It used to work fine, but after a recent deploy, **every request fails**. When you read the code, it looks correct. Nothing obviously changed. But it's broken. Your job: find what actually changed.

**What I Did:**
1. Deployed the Lambda + DynamoDB stack via CloudFormation
2. Triggered test invocations (all failed)
3. Asked the Agent: "My app challenge4-app-fn started failing on every request after a deploy, but the code looks correct. Investigate the root cause and tell me how to fix it."

**What the Agent Found:**
The agent checked:
1. Lambda logs → Found: `AccessDeniedException`
2. Lambda IAM role → Found: Missing `dynamodb:GetItem` permission
3. Root cause identified: The role doesn't have permission to read from the DynamoDB table

```
AccessDeniedException: User: arn:aws:sts::657709068147:assumed-role/
challenge-4-AppRole-OQXKioT2aD8p/challenge4-app-fn is not authorized 
to perform: dynamodb:GetItem on resource: arn:aws:dynamodb:...
```

**The Root Cause:**
This is a classic "Bad Deploy" scenario. The code is 100% correct:

```python
import boto3
ddb = boto3.client("dynamodb")

def handler(event, context):
    # This code is fine
    resp = ddb.get_item(TableName=TABLE, Key={"id": {"S": "1"}})
    return {"statusCode": 200, "body": json.dumps({"item": resp.get("Item", {})})}
```

But the Lambda's IAM role is missing the permission to execute `GetItem` on the table. In a recent deploy, either:
- The role was misconfigured
- A shared policy was revoked
- Permissions were scoped too narrowly for production

**The Fix:**
Add an inline IAM policy to the Lambda's role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:657709068147:table/challenge4-data"
    }
  ]
}
```

Steps:
1. IAM Console → Roles → search for `challenge-4-AppRole-*`
2. Add inline policy → paste the JSON above
3. Return to Lambda → Test → now returns 200 OK

**The Verification:**
- Lambda test returned status 200 with the product data:
  ```json
  {
    "statusCode": 200,
    "body": "{\"item\": {\"id\": {\"S\": \"1\"}, \"product\": {\"S\": \"Builders Hoodie\"}, \"price\": {\"N\": \"49\"}}}"
  }
  ```
- CloudWatch alarm `challenge4-app-fn-errors` transitioned OK

**Key Takeaway:**
This challenge is **the most realistic scenario.** In modern deployments:
- Code is rarely the problem (it was fine here)
- Configuration/permissions are often the culprit
- Code reviews won't catch IAM issues
- The agent had to understand both Lambda *and* IAM to connect the dots

This demonstrates why you need AI-powered diagnostics:
- A human would check the code first (wasting time)
- A dashboard would show the error but not the cause
- The agent immediately identified the mismatch between what the code does and what the role allows

**Time saved: ~20 minutes.**

---

### Challenge 5: Build Your Own Agentic SRE 🚀

**Scenario:** Design your own broken infrastructure and show the agent investigating it.

**What I Built:**
Instead of repeating Challenges 2–4, I created a more realistic multi-layered scenario:

- **Lambda function** (`challenge5-cost-detective`) - processes cost reports from S3
- **S3 bucket** (`challenge5-data-bucket`) - stores data
- **IAM role** - intentionally missing S3 permissions
- **Cost leak** - S3 versioning enabled with no lifecycle policy

**The Break:**
```yaml
Misconfiguration 1: Lambda role missing s3:GetObject + s3:ListBucket
Misconfiguration 2: S3 versioning enabled, no lifecycle rule (500+ old versions, 300GB waste)
Misconfiguration 3: Lambda timeout too short for large files (2 seconds → should be 30)
Result: 100% function failure + $10/month cost leak
```

**What the Agent Found:**
The agent identified all three issues and ranked them by severity:

```
CRITICAL: Lambda can't read from S3 (permission missing)
  → Fix: Add s3:GetObject + s3:ListBucket to role

MEDIUM: S3 versioning bloat (old versions consuming storage)
  → Fix: Add lifecycle rule to delete versions >30 days old

LOW: Lambda timeout too short (fails on large files)
  → Fix: Increase from 2 seconds to 30 seconds
```

**The Fixes:**
1. Added IAM policy granting S3 access
2. Added S3 lifecycle rule to clean old versions
3. Increased Lambda timeout to 30 seconds

**The Results:**
- Function now executes successfully (200 OK)
- S3 storage costs drop 80% (from $12→$2.50/month) post-cleanup
- All alarms return to green

**Key Insight:**
This challenge demonstrates that **real incidents are multi-layered.** Unlike Challenges 2–4 (single root cause), production breaks often involve:
- **Immediate symptom:** Function failure
- **Underlying causes:** Permissions, configuration, limits
- **Hidden costs:** Storage bloat, resource waste

The DevOps Agent surfaces all three, enabling end-to-end incident resolution, not just symptom treatment.

---

## Key Insights & Learnings

### 1. **The Agent Eliminates Dashboard Hunting**

Before DevOps Agent:
```
Incident: Lambda failing
Response:
  1. Open CloudWatch console
  2. Search for Lambda log group
  3. Scroll through 100+ log lines
  4. Spot the error
  5. Google the error message
  6. Check Lambda configuration
  7. Check IAM role
  8. Cross-reference permissions with resources
  → Time: 20-30 minutes
```

With DevOps Agent:
```
Incident: Lambda failing
Response:
  1. Ask agent: "Why is Lambda failing?"
  2. Agent answers with root cause + fix
  → Time: 2 minutes
```

### 2. **Permission Issues Are Invisible to Code Review**

Challenge 4 perfectly illustrates this. The code is flawless. No code review would catch it. But infrastructure configuration changed, and the app broke. The agent understood both layers.

**Implication:** Traditional SRE tools fail here. You need infrastructure intelligence.

### 3. **Real Incidents Have Multi-Cause Chains**

Challenge 5 showed that production breaks often have:
- **Immediate cause** (permission denied)
- **Underlying cause** (permission not granted in deploy)
- **Economic cause** (storage bloat from versioning)

An agent that understands your full stack can diagnose all three simultaneously.

### 4. **The Agent Scales with Infrastructure Complexity**

- Simple case (Lambda + CloudWatch): Agent saves 5 minutes
- Medium case (Lambda + S3 + IAM): Agent saves 15 minutes
- Complex case (Lambda + S3 + DynamoDB + IAM + cost concerns): Agent saves 30+ minutes

As your infrastructure grows, the agent's value compounds.

### 5. **SRE Is Becoming Agentic**

The future of DevOps isn't:
- Better dashboards (we have enough)
- More metrics (we're drowning in data)
- Manual runbooks (they're never up to date)

It's:
- **AI that understands your infrastructure holistically**
- **Agents that ask the right questions**
- **Automated reasoning across services**

This Skill Sprint was an introduction to that future.

---

## The Bigger Picture: Why This Matters

### The Problem DevOps Agent Solves

**The Modern Incident:**
1. Alarm fires
2. On-call engineer (could be junior, could be exhausted) gets paged
3. They have to:
   - Understand the failure (not obvious)
   - Correlate symptoms across dashboards (cognitive load)
   - Find the root cause (could be buried deep)
   - Apply the fix (might be obvious once you know the cause)

**Time to Resolution:** 30 minutes to 2 hours (depending on complexity)

**Cost:** 
- Engineering time (salary × MTTR)
- User impact (SLA breaches, lost revenue)
- Context switching (engineer pulled from productive work)

### The Solution: DevOps Agent

**With the Agent:**
1. Alarm fires
2. Engineer asks: "What's wrong?"
3. Agent says: "Lambda role missing S3 permission. Here's the fix."
4. Engineer applies fix (30 seconds)
5. Done

**Time to Resolution:** 2-5 minutes
**Cost saved:** Massive

### The Broader Implication

This is infrastructure intelligence as a service. It's not just about faster debugging—it's about:

1. **Enabling junior engineers** - They can debug production incidents without expert mentoring
2. **Reducing on-call burden** - Faster MTTR means less alert fatigue
3. **Enabling proactive actions** - Instead of reacting to incidents, you can prevent them
4. **Scaling SRE teams** - One agent can help 100 engineers troubleshoot

---

## Recommendations for Your Team

If you're considering AWS DevOps Agent for your team, here's how to approach it:

### Phase 1: Start Simple (Week 1)
- Set up the Agent Space in one AWS account
- Have your team try Challenge 1 (meet the agent)
- See if natural-language interaction resonates

### Phase 2: Integrate into Runbooks (Weeks 2-3)
- Identify your 3-5 most common incident types
- Create runbooks that start with "Ask the agent: ..."
- Have on-call engineers test the agent on non-critical issues first

### Phase 3: Expand to Cross-Service Diagnostics (Weeks 4+)
- Teach the agent about your specific architecture
- Use it for permission audits (find IAM issues before they break prod)
- Integrate with Slack for alerts

### Phase 4: Advanced Use Cases (Months 2+)
- **Cost optimization** - Ask the agent to find unused resources
- **Compliance** - Ask if resources meet your security policies
- **Capacity planning** - Ask the agent to recommend right-sizing

### Practical Implementation Checklist

```markdown
[ ] Set $5 budget alert (cost control)
[ ] Create Agent Space with read-only IAM access (security)
[ ] Train team on natural-language querying (adoption)
[ ] Create runbook templates for common issues (scaling)
[ ] Integrate with incident response (workflow)
[ ] Review agent findings monthly (continuous improvement)
```

### What to Watch For

1. **Latency** - Agent investigation takes time (5-30 seconds). Not suitable for ultra-critical (ms-level) diagnostics
2. **Accuracy** - Agent is very good but not perfect. Always verify before deploying fixes
3. **Scope** - Agent can only investigate resources it has access to (IAM permissions matter)
4. **Cost** - It's paid (2-month free trial). Factor into your tooling budget

---

## Conclusion

The AWS DevOps Agent Skill Sprint transformed how I think about infrastructure debugging. Here's what stuck with me:

### 🎯 The Realization
DevOps isn't about building better infrastructure—it's about **understanding** what you've built. The agent does that understanding at machine speed.

### 💡 The Opportunity
If you're doing DevOps in 2026, you should:
1. Know your infrastructure deeply (that's non-negotiable)
2. But lean on agents for the correlation and reasoning

It's like having an expert co-pilot who sees patterns you miss.

### 🚀 The Future
I believe the future of SRE is:
- **Less firefighting** (agent prevents incidents)
- **Less toil** (agent handles investigation)
- **More innovation** (engineers build instead of debugging)

This Skill Sprint proved that future is here.

---

## Resources

- [AWS DevOps Agent Documentation](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)
- [Builders Skill Sprint Repository](https://github.com/AWS-User-Group-Madurai/builders-skill-sprint-challenges)
- [AWS DevOps Agent Product Page](https://aws.amazon.com/devops-agent/)

---

## Appendix: My FINDINGS.md Files

I've created detailed findings for each challenge:
- **Challenge 1** - [Meet Your Agent](./challenge-1-meet-your-agent/FINDINGS.md)
- **Challenge 2** - [First Investigation](./challenge-2-first-investigation/FINDINGS.md)
- **Challenge 3** - [Stress & Diagnose](./challenge-3-stress-and-diagnose/FINDINGS.md)
- **Challenge 4** - [Bad Deploy Detective](./challenge-4-bad-deploy-detective/FINDINGS.md)
- **Challenge 5** - [Build Your Own](./challenge-5-build-your-own-agentic-sre/FINDINGS.md)

Each includes root cause analysis, fixes applied, and evidence (screenshots/metrics).

---

**Questions?** Drop them in the comments, or reach out on LinkedIn.

**Enjoyed this?** Share it with your SRE team—you might be surprised how interested they are in infrastructure AI.

---

*Posted by: DevOps Engineer / SRE*  
*Date: July 14, 2026*  
*Tags: #AWS #DevOps #SRE #AIInfrastructure #CloudNative #IncidentResponse*
