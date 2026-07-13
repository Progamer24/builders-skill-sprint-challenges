# AWS DevOps Agent Skill Sprint - Complete Workshop Guide

## Table of Contents
1. [Pre-Workshop Setup](#pre-workshop-setup)
2. [Challenge 1: Meet Your Agent](#challenge-1-meet-your-agent)
3. [Challenge 2: First Investigation](#challenge-2-first-investigation)
4. [Challenge 3: Stress & Diagnose](#challenge-3-stress--diagnose)
5. [Challenge 4: Bad Deploy Detective](#challenge-4-bad-deploy-detective)
6. [Challenge 5: Build Your Own](#challenge-5-build-your-own)
7. [Cleanup & Decommissioning](#cleanup--decommissioning)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Pre-Workshop Setup

### Prerequisites
- ✅ AWS Account (with AWS DevOps Agent free trial enabled)
- ✅ AWS CLI configured with credentials
- ✅ Browser (Chrome, Firefox, Safari, Edge)
- ✅ Text editor for viewing/editing files
- ✅ $5 budget alert set up (cost control)

### Step 1: Create Budget Alert (5 minutes)

**Why:** AWS DevOps Agent is paid. A budget alert prevents surprise charges.

**Steps:**
1. Open AWS Console → Search `Budgets` → Click **Budgets**
2. Click **Create budget** → Select **Use a template**
3. Choose **Monthly cost budget**
4. Set **Budget amount: $5**
5. Enter your email address
6. Click **Create budget**

**Expected Outcome:** You'll receive an email alert if spending crosses $5

---

### Step 2: Enable AWS DevOps Agent Service (5 minutes)

**Steps:**
1. AWS Console → Search `DevOps Agent` → Click **AWS DevOps Agent**
2. If prompted: Click **Enable**, **Start free trial**, or **Get started**
3. Wait for page to load (takes ~30 seconds)
4. Verify you see the agent dashboard

**Expected Outcome:** DevOps Agent console is accessible

---

### Step 3: Create an Agent Space (10 minutes)

**What is an Agent Space?** It's the agent's workspace—defines which AWS resources it can investigate.

**Steps:**
1. In DevOps Agent console → Click **Create Space** (or **Create Agent Space**)
2. **Name:** `bss-may-2026-workshop`
3. **AWS Account:** Select your account (default)
4. **IAM Role:** Select **Read-only** access (or default)
5. **Region:** `us-east-1` (all challenges use this region)
6. Click **Create** → Wait for confirmation

**Expected Outcome:** You see a new Agent Space card labeled `bss-may-2026-workshop`

---

### Step 4: Access the DevOps Agent Web App (5 minutes)

**Steps:**
1. From the Agent Space card → Click **Open Agent** (or similar button)
2. You'll be redirected to the DevOps Agent web interface
3. You should see:
   - **Chat** tab (or Chat box)
   - **Investigations** tab
   - **Topology** view

**Expected Outcome:** DevOps Agent web app is open and ready for queries

**Test:** Try asking the agent: `What is your name?` (agent should respond)

---

## Challenge 1: Meet Your Agent

**Duration:** 10-15 minutes  
**Difficulty:** ⭐ Easy  
**Cost:** ~$0 (no resources created)

### Goal
Prove the agent works by asking natural-language questions about your AWS account.

### Execution Steps

#### Step 1: Ask About Your Resources (3 minutes)

**In DevOps Agent Chat box:**
1. Type: `What resources do I have in this account?`
2. Press Enter or click **Send**
3. **Wait:** Agent may take 5-30 seconds to respond

**Expected Response:**
```
"Based on my investigation of your AWS account, I can see:
- CloudFormation stacks: [list]
- Lambda functions: [count]
- EC2 instances: [count]
- [Other resources]
"
```

**What to observe:**
- Agent provides a natural-language summary
- No dashboard clicking required
- Agent speaks conversationally

**Screenshot Point 1:** Capture the agent's response

---

#### Step 2: Ask About Health Status (3 minutes)

**In DevOps Agent Chat box:**
1. Type: `Is anything unhealthy right now?`
2. Press Enter
3. Wait for response

**Expected Response:**
```
"Currently, I see X resources with potential issues:
- [Issue 1]: [Description]
- [Issue 2]: [Description]

These alarms are firing: [Alarm names]
"
```

**What to observe:**
- Agent identifies any unhealthy resources
- It mentions specific alarms
- It prioritizes by severity (if multiple issues)

**Screenshot Point 2:** Capture the health status response

---

#### Step 3: Ask for a Health Summary (3 minutes)

**In DevOps Agent Chat box:**
1. Type: `Give me a health summary of my environment.`
2. Press Enter
3. Wait for comprehensive response

**Expected Response:**
```
"Here's a summary of your environment:
- Overall health: [Good/Warning/Critical]
- Total resources: [Number]
- Healthy: [Count]
- Warning: [Count]
- Critical: [Count]

Key areas: [...]
"
```

**What to observe:**
- Agent synthesizes multiple data sources
- Clear summary format
- Actionable insights

**Screenshot Point 3:** Capture the summary

---

#### Step 4: Explore Bonus Features (2-5 minutes)

**Optional but recommended:**

**A) Follow-up Question:**
- Ask: `Which of those resources are in us-east-1?`
- Observe: Agent maintains conversation context

**B) Topology View:**
- Click **Topology** tab (if available)
- View visual map of your resources
- Take screenshot

**C) Ask About a Specific Service:**
- Ask: `Show me my Lambda functions`
- Ask: `What EC2 instances do I have?`

**What to observe:**
- Agent can drill down into specific services
- It understands service-specific concepts
- Multi-turn conversations work

---

### Challenge 1: Success Criteria

✅ Agent responds to natural-language questions  
✅ Agent identifies resources in your account  
✅ Agent provides health summary  
✅ Agent maintains conversation context  
✅ Screenshots captured

### Evidence to Collect

1. **Screenshot 1:** Agent's response to "What resources do I have?"
2. **Screenshot 2:** Agent's response to "Is anything unhealthy?"
3. **Screenshot 3:** Agent's health summary
4. **Screenshot 4 (optional):** Topology view

### Move to Challenge 2
Once Challenge 1 is documented, proceed to Challenge 2. Don't close the Agent Space—you'll reuse it.

---

## Challenge 2: First Investigation

**Duration:** 20-30 minutes  
**Difficulty:** ⭐⭐ Medium  
**Cost:** ~$0.10 (small Lambda invocations)

### Goal
Deploy a broken Lambda, trigger failures, ask the agent to investigate, and apply a fix.

### Execution Steps

#### Step 1: Prepare the Template File (2 minutes)

**Location:** `challenge-2-first-investigation/template.yaml`

**What it contains:**
- Lambda function: `challenge2-broken-fn`
- IAM role with basic Lambda execution permissions
- CloudWatch alarm: `challenge2-broken-fn-errors`

**Do not edit.** We'll use it as-is to trigger failures.

---

#### Step 2: Deploy Infrastructure via CloudFormation (5 minutes)

**Option A: AWS CLI** (Recommended - faster)

**Terminal command:**
```bash
cd "c:\Users\karan\AWS\builders-skill-sprint-challenges\May-2026-DevOps-Month"

aws cloudformation deploy \
  --stack-name challenge-2 \
  --template-file challenge-2-first-investigation/template.yaml \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

**Expected output:**
```
Waiting for changeset to be created..
Successfully created/updated stack - challenge-2 in [Region]
```

**Wait for:** Stack creation completes (~30-60 seconds)

---

**Option B: AWS Console** (Point-and-click)

1. AWS Console → Search `CloudFormation` → Click **CloudFormation**
2. Click **Create stack** → **With new resources (standard)**
   > ⚠️ **Do NOT choose "With existing resources (import)"** — this causes errors
3. Under **Prepare template** → Choose **Choose an existing template**
4. Select **Upload a template file** → **Choose file**
5. Navigate to: `challenge-2-first-investigation/template.yaml` → **Open**
6. Click **Next**
7. **Stack name:** `challenge-2`
8. Click **Next** → **Next** again
9. ☑️ Tick **"I acknowledge that AWS CloudFormation might create IAM resources"**
10. Click **Submit**
11. **Wait for:** Status shows **CREATE_COMPLETE** (1-2 minutes)

---

#### Step 3: Trigger Lambda Failures (3 minutes)

**Why:** The agent needs to see failures to diagnose.

**Steps:**
1. AWS Console → Search `Lambda` → Click **Lambda**
2. Find function: `challenge2-broken-fn` → Click it
3. Click **Test** tab
4. In **Event name** field: Type anything (e.g., `test1`) or leave default
5. Click **Test** button
6. ❌ Observe: **"Error"** or **"Unhandled exception"** appears
7. **Repeat:** Click Test 3-4 more times (total 4-5 failures)

**Why repeat?** CloudWatch alarm needs multiple failures to trigger.

**Expected output in response body:**
```json
{"errorMessage": "name 'config' is not defined", "errorType": "NameError"}
```

**Screenshot Point 1:** Capture the Lambda test error

---

#### Step 4: Wait for Alarm to Trigger (2 minutes)

**Steps:**
1. AWS Console → Search `CloudWatch` → Click **CloudWatch**
2. Click **Alarms** in left sidebar
3. Search for: `challenge2-broken-fn-errors`
4. **Wait:** Alarm status changes to **ALARM** (red) — might take 1-2 minutes
5. Take screenshot of red alarm

**Why?** Alarms evaluate every 60 seconds. Multiple failures trigger it.

**Expected state:** Alarm shows:
- Status: **ALARM** (red)
- Reason: "Error count ≥ 1"

**Screenshot Point 2:** Capture the red ALARM state

---

#### Step 5: Ask DevOps Agent to Investigate (5 minutes)

**In DevOps Agent Chat:**

1. Type:
```
The Lambda function challenge2-broken-fn is failing on every invocation. 
The error alarm is firing. Investigate the root cause and tell me how to fix it.
```

2. Press Enter → **Wait 10-30 seconds** for agent analysis

**Expected response from agent:**
```
"I've investigated the Lambda function challenge2-broken-fn. 
I found the root cause:

ERROR FOUND:
The function has a NameError: 'config' is not defined

LOCATION: index.py, line 4
CODE: return {"result": config["value"]}

ROOT CAUSE:
The variable 'config' is referenced but never defined.

FIX:
Define the config dictionary before using it:
config = {"value": "..."}
return {"result": config["value"]}
"
```

**What to observe:**
- Agent found the exact error
- Agent located the problematic line
- Agent provided a solution

**Screenshot Point 3:** Capture the agent's investigation output

---

#### Step 6: Apply the Fix (5 minutes)

**Steps:**

1. In Lambda console → **Code** tab (click the tab, don't close)
2. **Find:** The code editor showing the broken function
3. **Current code:**
```python
def handler(event, context):
    # This function is broken on purpose. Use the DevOps Agent to
    # find out why every invocation fails.
    return {"result": config["value"]}
```

4. **Replace with:**
```python
def handler(event, context):
    # Fixed: define config with a value
    config = {"value": "Challenge 2 fixed!"}
    return {"result": config["value"]}
```

5. Click **Deploy** button (or **Save**)
6. **Wait:** Deploy completes (~5 seconds)

**Expected:** Deployment success notification

---

#### Step 7: Verify the Fix (5 minutes)

**Steps:**

1. Still in Lambda console → Click **Test** tab
2. Click **Test** button
3. ✅ **Observe:** Success response with statusCode 200:
```json
{"result": "Challenge 2 fixed!"}
```

4. AWS Console → CloudWatch → Alarms
5. Click `challenge2-broken-fn-errors` alarm
6. **Wait:** Status changes to **OK** (green) — may take 1-2 minutes
7. Refresh the page if needed

**Expected state:** Alarm shows:
- Status: **OK** (green)
- Reason: "No errors"

**Screenshot Point 4:** Capture the successful test + green alarm

---

#### Step 8: Ask Agent to Confirm Recovery (2 minutes)

**In DevOps Agent Chat:**

1. Type: `Has the Lambda challenge2-broken-fn recovered and is now healthy?`
2. Press Enter
3. Agent should confirm the function is now working

**Expected response:**
```
"Yes, challenge2-broken-fn is now healthy. 
The function is executing successfully with no errors. 
The alarm has transitioned to OK."
```

**Screenshot Point 5:** Capture the confirmation

---

### Challenge 2: Completion Checklist

- ✅ Stack created (challenge-2 visible in CloudFormation)
- ✅ Lambda deployed (challenge2-broken-fn visible)
- ✅ Failures triggered (4-5 test invocations failed)
- ✅ Alarm fired (challenge2-broken-fn-errors showed ALARM)
- ✅ Agent investigated (identified NameError)
- ✅ Fix applied (defined config variable)
- ✅ Function recovered (test returned 200 OK)
- ✅ Alarm cleared (status changed to OK)
- ✅ Agent confirmed (health restored)

### Evidence to Collect

1. Lambda test error (NameError)
2. CloudWatch alarm in ALARM state (red)
3. DevOps Agent investigation output
4. Lambda test success (200 OK)
5. CloudWatch alarm in OK state (green)
6. Agent confirmation of recovery

### Move to Challenge 3
Keep Challenge 2 stack running. Proceed to Challenge 3.

---

## Challenge 3: Stress & Diagnose

**Duration:** 25-35 minutes  
**Difficulty:** ⭐⭐⭐ Hard  
**Cost:** ~$0.30 (EC2 t3.micro for ~30 minutes)

### Goal
Deploy an EC2 instance with runaway processes, diagnose the high CPU, and recover it.

### Execution Steps

#### Step 1: Deploy Infrastructure (5 minutes)

**Option A: AWS CLI**

```bash
aws cloudformation deploy \
  --stack-name challenge-3 \
  --template-file challenge-3-stress-and-diagnose/template.yaml \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

**Expected output:**
```
Successfully created/updated stack - challenge-3
```

---

**Option B: AWS Console**

1. CloudFormation → **Create stack** → **With new resources (standard)**
2. **Upload template file** → `challenge-3-stress-and-diagnose/template.yaml`
3. **Stack name:** `challenge-3`
4. ☑️ Acknowledge IAM resources
5. **Submit**
6. **Wait:** Status → **CREATE_COMPLETE** (~2-3 minutes)

---

#### Step 2: Wait for CPU Stress & Alarm to Fire (5 minutes)

**Why:** The EC2 bootstrap script starts CPU-intensive processes automatically. The alarm takes time to evaluate.

**Steps:**

1. AWS Console → Search `CloudWatch` → **Alarms**
2. Search for: `challenge3-high-cpu`
3. **Initial state:** Should show **INSUFFICIENT_DATA** or **OK**
4. **Wait:** 2-5 minutes for the alarm to evaluate and trigger
5. **Expected:** Alarm transitions to **ALARM** (red)
6. Refresh page periodically to see status change

**What's happening in the background:**
- EC2 instance is launching
- Bootstrap script runs `/bin/bash -c 'while true; do :; done'` (busy-loop)
- CPU usage climbs to 100%
- CloudWatch samples CPU every minute
- Alarm fires when threshold exceeded

**Screenshot Point 1:** Capture the alarm in ALARM state (red)

---

#### Step 3: Ask DevOps Agent to Investigate (5 minutes)

**In DevOps Agent Chat:**

1. Type:
```
My EC2 instance challenge3-stress is slow and the high CPU alarm is firing. 
Investigate the root cause and tell me how to fix it.
```

2. Press Enter → **Wait 15-30 seconds**

**Expected response:**
```
"I've investigated the instance challenge3-stress. 
I found the cause of the high CPU usage:

DIAGNOSIS:
The instance is running runaway CPU-intensive processes. 
I can see infinite loops consuming all available CPU.

PROCESS DETAILS:
- Multiple bash processes running: 'while true; do :; done'
- Each core has one process pinned at 100%
- This is causing the CPU alarm to trigger

SOLUTION:
Connect to the instance via Session Manager and kill the processes:
1. Open Session Manager terminal to the instance
2. Run: killall bash (or kill specific PIDs)
3. Verify: run 'top' to confirm CPU returns to normal
4. The alarm should clear after ~2 minutes
"
```

**What to observe:**
- Agent identified the exact cause (runaway processes)
- Agent provided specific fix steps
- Agent mentioned Session Manager (no SSH keys needed)

**Screenshot Point 2:** Capture the agent's diagnosis

---

#### Step 4: Connect via Session Manager (3 minutes)

**Why Session Manager?** No SSH keys, no bastion hosts, no security group management.

**Steps:**

1. AWS Console → Search `EC2` → **Instances**
2. Find instance: `challenge3-stress` → Click it
3. Click **Connect** button (top right)
4. Select **Session Manager** tab
5. Click **Connect** button
6. **Wait:** Terminal window opens (~5-10 seconds)

**You should see:**
- Black terminal window
- Prompt: `[ssm-user@...]$ `
- Ready for commands

**Screenshot Point 3:** Capture the Session Manager terminal

---

#### Step 5: Diagnose the Processes (3 minutes)

**In Session Manager terminal:**

**Command 1: View running processes**
```bash
ps aux | grep "while"
```

**Expected output:**
```
root     12345  100.0  0.0  1234  500 ?  R  12:34   0:15 /bin/bash -c while true; do :; done
root     12346  100.0  0.0  1234  500 ?  R  12:34   0:16 /bin/bash -c while true; do :; done
...
```

**What to observe:**
- Multiple bash processes
- Each at ~100% CPU
- Running the infinite loop command

**Command 2: Check CPU usage in real-time**
```bash
top -b -n 1 | head -20
```

**Expected output:**
```
%CPU column shows: 100.0, 100.0, 100.0, ... (one per core)
```

**Screenshot Point 4:** Capture the ps output showing the processes

---

#### Step 6: Kill the Processes (2 minutes)

**In Session Manager terminal:**

**Command: Kill all bash processes**
```bash
killall bash
```

**Expected output:**
```
[Connection terminated or similar]
```

**Why connection ends?** You killed the bash processes, including the one running the terminal.

**What's happening:**
- All infinite-loop processes terminated
- CPU usage drops immediately
- EC2 becomes responsive again

**This is expected and normal.**

---

#### Step 7: Wait for Alarm to Clear (5 minutes)

**Steps:**

1. AWS Console → CloudWatch → **Alarms**
2. Find: `challenge3-high-cpu`
3. **Wait:** Status transitions from **ALARM** to **OK** (green)
   - This takes ~1-2 minutes
4. **Why?** Alarm evaluates every 60 seconds. After 1-2 minutes of low CPU, it clears
5. Refresh page periodically to see status change

**Expected state:**
- Status: **OK** (green)
- Reason: "CPUUtilization below threshold"
- Metrics graph shows CPU spike → drop

**Screenshot Point 5:** Capture the alarm in OK state (green)

**Bonus:** Take screenshot of CPU graph showing the spike and recovery

---

#### Step 8: Reconnect & Verify (2 minutes)

**Optional: Verify CPU is back to normal**

1. EC2 → `challenge3-stress` → **Connect** → **Session Manager** → **Connect**
2. Terminal opens again (because we killed the terminal process before)
3. Run: `top -b -n 1 | head -5`
4. **Observe:** CPU shows <5% usage (normal)
5. Exit: `exit` or Ctrl+C

**Screenshot Point 6:** Capture the normal CPU usage

---

#### Step 9: Ask Agent to Confirm Recovery (2 minutes)

**In DevOps Agent Chat:**

1. Type: `Has the EC2 instance challenge3-stress recovered? Is the CPU alarm back to OK?`
2. Press Enter

**Expected response:**
```
"Yes, challenge3-stress has recovered successfully. 
The CPU alarm is now in OK state. 
CPU utilization is back to normal levels (<10%)."
```

**Screenshot Point 7:** Capture the confirmation

---

### Challenge 3: Completion Checklist

- ✅ Stack created (challenge-3 in CloudFormation)
- ✅ EC2 instance launched (visible in EC2 Instances)
- ✅ Alarm fired (challenge3-high-cpu → ALARM)
- ✅ Agent investigated (identified processes)
- ✅ Session Manager connected
- ✅ Processes identified (ps aux output)
- ✅ Processes killed (killall bash)
- ✅ Alarm cleared (challenge3-high-cpu → OK)
- ✅ CPU verified normal (<5%)
- ✅ Agent confirmed recovery

### Evidence to Collect

1. CloudWatch alarm in ALARM state (red)
2. DevOps Agent diagnosis
3. Session Manager terminal (ps aux output)
4. CPU graph showing spike + recovery
5. CloudWatch alarm in OK state (green)
6. Agent confirmation

### Move to Challenge 4
Keep Challenge 3 stack running. Proceed to Challenge 4.

⚠️ **Important:** Challenge 3 (EC2) has hourly costs. Delete it as soon as you finish.

---

## Challenge 4: Bad Deploy Detective

**Duration:** 20-30 minutes  
**Difficulty:** ⭐⭐⭐⭐ Expert  
**Cost:** ~$0.05 (Lambda + DynamoDB)

### Goal
Deploy a Lambda that fails because of permission issues (not code bugs), diagnose it, and fix it via IAM.

### Execution Steps

#### Step 1: Deploy Infrastructure (5 minutes)

**Option A: AWS CLI**

```bash
aws cloudformation deploy \
  --stack-name challenge-4 \
  --template-file challenge-4-bad-deploy-detective/template.yaml \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

---

**Option B: AWS Console**

1. CloudFormation → **Create stack** → **With new resources (standard)**
2. **Upload template file** → `challenge-4-bad-deploy-detective/template.yaml`
3. **Stack name:** `challenge-4`
4. ☑️ Acknowledge IAM
5. **Submit**
6. **Wait:** Status → **CREATE_COMPLETE** (~1-2 minutes)

---

#### Step 2: Trigger Lambda Failures (3 minutes)

**Steps:**

1. AWS Console → **Lambda** → Find: `challenge4-app-fn`
2. Click function → **Test** tab
3. **Event name:** Leave default or enter `test1`
4. Click **Test** → ❌ **Error** appears
5. **Repeat:** Click Test 3-4 more times

**Expected error message:**
```
AccessDeniedException: User is not authorized to perform: 
dynamodb:GetItem on resource: arn:aws:dynamodb:us-east-1:...:table/challenge4-data
```

**Key observation:** The error is NOT a code error. The code is fine. It's a permission issue.

**Screenshot Point 1:** Capture the AccessDeniedException error

---

#### Step 3: Wait for Alarm (1-2 minutes)

**Steps:**

1. CloudWatch → **Alarms**
2. Find: `challenge4-app-fn-errors`
3. **Wait:** Alarm transitions to **ALARM** (red)

**Screenshot Point 2:** Capture the alarm in ALARM state

---

#### Step 4: Ask DevOps Agent to Investigate (5 minutes)

**In DevOps Agent Chat:**

1. Type:
```
My app challenge4-app-fn started failing on every request after a deploy. 
The code looks correct, but something changed. Investigate the root cause 
and tell me how to fix it.
```

2. Press Enter → **Wait 15-30 seconds**

**Expected response:**
```
"I've investigated challenge4-app-fn and found the root cause is NOT in the code.

ROOT CAUSE - PERMISSION ISSUE:
The Lambda's IAM role lacks permission to read from the DynamoDB table.

ERROR DETAILS:
AccessDeniedException: User is not authorized to perform dynamodb:GetItem 
on resource: arn:aws:dynamodb:us-east-1:...:table/challenge4-data

ANALYSIS:
- Lambda code is correct (it calls ddb.get_item())
- The role exists but has no DynamoDB permissions
- This suggests the permission was never granted or was revoked during deploy

FIX REQUIRED:
Add an inline policy to the Lambda's IAM role granting dynamodb:GetItem access:

{
  'Effect': 'Allow',
  'Action': ['dynamodb:GetItem'],
  'Resource': 'arn:aws:dynamodb:us-east-1:<ACCOUNT>:table/challenge4-data'
}
"
```

**What to observe:**
- Agent identified the issue is NOT code
- Agent found the exact permission missing
- Agent provided the policy to add

**Screenshot Point 3:** Capture the agent's investigation

---

#### Step 5: Add the IAM Permission (5 minutes)

**Steps:**

1. AWS Console → Search `IAM` → **Roles**
2. **Search for:** `challenge-4-AppRole` (it's a long name like `challenge-4-AppRole-OQXKioT2aD8p`)
3. Click the role → Opens role details
4. Click **Add inline policy** (or **Create inline policy**)
5. Click **JSON** tab
6. **Delete** the default template
7. **Paste** this policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:657709068147:table/challenge4-data"
    }
  ]
}
```

⚠️ **Replace** `657709068147` with your AWS account ID (from agent output or AWS Console top-right)

8. Click **Review policy** (or next)
9. **Policy name:** `AllowReadChallenge4Table`
10. Click **Create policy**

**Expected:** Confirmation: "Policy created successfully"

**Screenshot Point 4:** Capture the policy being added

---

#### Step 6: Verify Permission (2 minutes)

**Back in IAM → Role details:**
- Scroll down to **Inline policies**
- You should see: `AllowReadChallenge4Table`
- It's now attached to the role

**Screenshot Point 5:** Capture the policy attached

---

#### Step 7: Seed DynamoDB with Test Data (3 minutes)

**Why:** The Lambda reads from DynamoDB. We need sample data.

**Option A: AWS CLI**

```bash
aws dynamodb put-item \
  --table-name challenge4-data \
  --item '{"id": {"S": "1"}, "product": {"S": "Builders Hoodie"}, "price": {"N": "49"}}' \
  --region us-east-1
```

---

**Option B: DynamoDB Console**

1. AWS Console → Search `DynamoDB` → **Tables**
2. Find: `challenge4-data` → Click it
3. Click **Explore table items** (or **Items** tab)
4. Click **Create item** (or **Put item**)
5. **Paste** or **manually enter:**
```json
{
  "id": "1",
  "product": "Builders Hoodie",
  "price": 49
}
```
6. Click **Create** or **Save**

**Expected:** Item appears in table

---

#### Step 8: Test the Lambda (5 minutes)

**Steps:**

1. Lambda → `challenge4-app-fn` → **Test** tab
2. **Wait:** 2-3 seconds for permission to propagate
3. Click **Test**
4. ✅ **Success!** Response should show:
```json
{
  "statusCode": 200,
  "body": "{\"item\": {\"id\": {\"S\": \"1\"}, \"product\": {\"S\": \"Builders Hoodie\"}, \"price\": {\"N\": \"49\"}}}"
}
```

**What to observe:**
- Now it works!
- Data from DynamoDB is returned
- No more AccessDeniedException

**Screenshot Point 6:** Capture the successful Lambda test (200 OK)

---

#### Step 9: Verify Alarm Clears (2-3 minutes)

**Steps:**

1. CloudWatch → **Alarms** → Find: `challenge4-app-fn-errors`
2. **Wait:** Status transitions to **OK** (green)
3. Refresh page if needed

**Screenshot Point 7:** Capture the alarm in OK state

---

#### Step 10: Ask Agent to Confirm (2 minutes)

**In DevOps Agent Chat:**

1. Type: `Has challenge4-app-fn recovered? Is the permission issue resolved?`
2. Press Enter

**Expected response:**
```
"Yes, challenge4-app-fn is now healthy. 
The DynamoDB permission has been granted, and the function is executing successfully. 
The error alarm has cleared."
```

**Screenshot Point 8:** Capture the confirmation

---

### Challenge 4: Completion Checklist

- ✅ Stack created (challenge-4 in CloudFormation)
- ✅ Lambda + DynamoDB deployed
- ✅ Failures triggered (4-5 test invocations)
- ✅ Alarm fired (challenge4-app-fn-errors → ALARM)
- ✅ Agent investigated (identified permission issue)
- ✅ IAM policy added (dynamodb:GetItem granted)
- ✅ DynamoDB seeded (test item created)
- ✅ Lambda tested (200 OK response)
- ✅ Alarm cleared (→ OK)
- ✅ Agent confirmed recovery

### Evidence to Collect

1. Lambda test error (AccessDeniedException)
2. CloudWatch alarm in ALARM state (red)
3. DevOps Agent investigation output
4. IAM policy being added (JSON)
5. Lambda test success (200 OK)
6. CloudWatch alarm in OK state (green)
7. Agent confirmation

### Move to Challenge 5
Keep Challenge 4 stack running. Proceed to Challenge 5.

---

## Challenge 5: Build Your Own

**Duration:** 30-45 minutes  
**Difficulty:** 🚀 Innovative  
**Cost:** ~$0.10 (Lambda + S3)

### Goal
Design a realistic, multi-layer incident scenario and show the agent investigating it.

### Execution Steps

#### Step 1: Plan Your Scenario (5 minutes)

**This is where you get creative!**

**Recommended Scenarios:**

**A) Cost Optimization Detective (Recommended)**
- Lambda that processes files from S3
- S3 bucket has versioning enabled (cost bloat)
- Lambda role missing S3 permissions
- Lambda timeout too short for large files
- Three layers: permission + cost + timeout

**B) Cross-Service Permissions**
- Lambda writes to SNS
- Lambda role missing SNS:Publish
- SNS topic configured for DLQ
- DLQ sends to SQS
- Multiple permission layers

**C) Data Integrity Issue**
- Lambda reads from DynamoDB
- Missing partition key in query
- Eventual consistency issues
- Missing read capacity
- Multiple root causes

**For this guide,** we'll execute Scenario A (Cost Optimization)

---

#### Step 2: Create Infrastructure (10 minutes)

**We'll create manually via console and CLI rather than CloudFormation.**

**Part A: Create S3 Bucket**

1. AWS Console → **S3** → **Create bucket**
2. **Bucket name:** `challenge5-data-bucket-<random>` (S3 names are global, so add randomness)
3. **Region:** `us-east-1`
4. Click **Create**
5. Click the bucket → **Properties**
6. Scroll to **Versioning**
7. Click **Edit** → Enable versioning
8. **Save changes**

**Why enable versioning?** It creates old versions = storage cost increase. Agent will find this waste.

**Screenshot Point 1:** Capture versioning enabled

---

**Part B: Create DynamoDB Table**

1. AWS Console → **DynamoDB** → **Create table**
2. **Table name:** `challenge5-metrics`
3. **Partition key:** `timestamp` (String)
4. **Billing mode:** Pay-per-request
5. Click **Create**

**Wait:** Table becomes active (~10 seconds)

---

**Part C: Create IAM Role for Lambda**

1. AWS Console → **IAM** → **Roles** → **Create role**
2. **Trusted entity:** AWS service → **Lambda**
3. Click **Next**
4. **Add permissions:** Search for `AWSLambdaBasicExecutionRole` → Check it
5. Click **Next**
6. **Role name:** `challenge5-role`
7. Click **Create role**
8. Click the role → **Add inline policy** → **JSON**

**Paste this policy (intentionally WITHOUT S3 permissions):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

9. **Policy name:** `ProcessLogsPolicy`
10. Click **Create policy**

---

**Part D: Create Lambda Function**

1. AWS Console → **Lambda** → **Create function**
2. **Function name:** `challenge5-cost-detective`
3. **Runtime:** Python 3.12
4. **Change default execution role:** Use existing role → `challenge5-role`
5. Click **Create**

**Now edit the code:**

6. In **Code** tab, replace the code with:
```python
import boto3
import json
import os

s3 = boto3.client('s3')
ddb = boto3.client('dynamodb')

def handler(event, context):
    """Process cost report data from S3 and store metrics"""
    
    bucket = os.environ.get('BUCKET_NAME', 'challenge5-data-bucket')
    table = os.environ.get('TABLE_NAME', 'challenge5-metrics')
    
    try:
        # This will fail - no S3 permission
        response = s3.get_object(Bucket=bucket, Key='report.json')
        data = json.loads(response['Body'].read())
        
        # Store metrics in DynamoDB
        ddb.put_item(
            TableName=table,
            Item={
                'timestamp': {'S': '2026-07-14T00:00:00Z'},
                'metric': {'S': 'cost_report'},
                'value': {'N': json.dumps(data.get('total', 0))}
            }
        )
        
        return {'statusCode': 200, 'body': 'Success'}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
```

7. Add environment variables → Click **Configuration** → **Environment variables** → **Edit**
8. Add:
   - Key: `BUCKET_NAME` → Value: `challenge5-data-bucket-<your-suffix>`
   - Key: `TABLE_NAME` → Value: `challenge5-metrics`
9. Click **Save**
10. **Increase timeout:** Click **General configuration** → Edit → **Timeout: 2 seconds** → Save

**Why 2 seconds?** Lambda needs 10+ seconds to download large files. 2 is too short.

---

#### Step 3: Trigger Failures (3 minutes)

**Steps:**

1. Lambda → `challenge5-cost-detective` → **Test** tab
2. Click **Test** (3-4 times)
3. ❌ **Observe:** Errors (AccessDeniedException for S3, or Timeout)

**Expected errors:**
```
1st attempt: AccessDeniedException (no S3 permission)
2nd attempt: Timeout (if file large)
3rd+ attempts: Similar errors
```

**Screenshot Point 2:** Capture the errors

---

#### Step 4: Create S3 Test Files (3 minutes)

**Put files in S3 for testing:**

1. AWS Console → **S3** → `challenge5-data-bucket-*`
2. Click **Upload** → Create some files:
   - Create a small JSON file: `report.json` with `{"total": 1000}`
   - Upload 2-3 versions (to create versioning history)
   
**Why?** This creates old versions that waste storage.

**Screenshot Point 3:** Capture S3 bucket with versioning history

---

#### Step 5: Ask Agent to Investigate (5 minutes)

**In DevOps Agent Chat:**

1. Type:
```
My Lambda function challenge5-cost-detective processes cost reports from S3 
but is failing with permission errors and timeouts. I also notice my S3 bill 
is higher than expected. Investigate all the issues and prioritize the fixes 
by severity.
```

2. Press Enter → **Wait 20-30 seconds**

**Expected response (comprehensive):**
```
"I've completed a full investigation of your cost report system. 
I found THREE distinct issues:

CRITICAL - PERMISSION ISSUE:
- Lambda role lacks s3:GetObject permission
- Function cannot read from S3
- Error: AccessDeniedException
- Impact: 100% function failure
- Fix: Add s3:GetObject to role IAM policy

MEDIUM - COST BLOAT:
- S3 bucket has versioning enabled with no lifecycle policy
- Currently storing: [X] old versions consuming [X]GB
- Cost impact: $[X]/month
- Fix: Add lifecycle rule to delete versions >30 days old

LOW - TIMEOUT RISK:
- Lambda timeout set to 2 seconds
- Processing large files requires 10+ seconds
- Some invocations timeout
- Fix: Increase timeout to 30 seconds

RECOMMENDED FIX ORDER:
1. Add S3 permission (immediate)
2. Increase timeout (immediate)
3. Add lifecycle policy (scheduled)
"
```

**What to observe:**
- Agent found ALL THREE issues
- Agent ranked by severity
- Agent provided specific fixes for each

**Screenshot Point 4:** Capture the comprehensive investigation output

---

#### Step 6: Apply Fixes (10 minutes)

**Fix 1: Add S3 Permission**

1. IAM → Roles → `challenge5-role` → **Add inline policy** → **JSON**
2. Paste:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::challenge5-data-bucket-*",
        "arn:aws:s3:::challenge5-data-bucket-*/*"
      ]
    }
  ]
}
```
3. **Name:** `AllowS3Access`
4. Click **Create policy**

---

**Fix 2: Increase Lambda Timeout**

1. Lambda → `challenge5-cost-detective` → **Configuration** → **General configuration** → **Edit**
2. **Timeout:** Change from 2 to 30 seconds
3. Click **Save**

---

**Fix 3: Add S3 Lifecycle Policy**

1. S3 → `challenge5-data-bucket-*` → **Management** tab
2. Scroll to **Lifecycle rules**
3. Click **Create lifecycle rule**
4. **Rule name:** `DeleteOldVersions`
5. **Apply to all objects in bucket:** ☑️ Yes
6. Under **Non-current version expiration** → Enable ☑️
7. **Delete versions:** 30 days
8. Click **Create rule**

---

#### Step 7: Verify Fixes (5 minutes)

**Test Lambda:**
1. Lambda → `challenge5-cost-detective` → **Test**
2. ✅ **Success!** Should return:
```json
{"statusCode": 200, "body": "Success"}
```

**Screenshot Point 5:** Capture successful Lambda test

---

**Verify Lifecycle Policy:**
1. S3 → `challenge5-data-bucket-*` → **Management**
2. Confirm: `DeleteOldVersions` rule shows as **Enabled**

**Screenshot Point 6:** Capture lifecycle rule

---

#### Step 8: Ask Agent to Confirm Multi-Issue Resolution (2 minutes)

**In DevOps Agent Chat:**

1. Type: `I've applied all the fixes. Can you confirm the Lambda is now healthy and the cost issues are resolved?`
2. Press Enter

**Expected response:**
```
"Confirmed. I can see that:

✓ Lambda now has S3 permission (policy added)
✓ Timeout increased to 30 seconds
✓ S3 lifecycle rule is active (deleting old versions)

The function is executing successfully. 
The permission error is resolved.
Your S3 costs should decrease as old versions are purged.

All issues addressed."
```

**Screenshot Point 7:** Capture the confirmation

---

### Challenge 5: Completion Checklist

- ✅ Scenario designed (multi-layer incident)
- ✅ Infrastructure created (Lambda + S3 + DynamoDB + IAM)
- ✅ Intentional misconfigurations applied (permission + timeout + versioning)
- ✅ Failures triggered (Lambda tests fail)
- ✅ Agent investigated (identified 3 issues)
- ✅ Fixes prioritized (by severity)
- ✅ Fixes applied (permission + timeout + lifecycle)
- ✅ Lambda tested (200 OK)
- ✅ Policies verified (active)
- ✅ Agent confirmed recovery

### Evidence to Collect

1. Lambda test errors (permission + timeout)
2. S3 versioning enabled + history
3. DevOps Agent comprehensive investigation
4. Agent ranking of issues (critical, medium, low)
5. IAM policy being added
6. Lambda timeout being increased
7. S3 lifecycle rule being created
8. Lambda test success (200 OK)
9. Lifecycle rule verification
10. Agent confirmation of all fixes

### Challenge 5 Complete!
You've completed the most innovative challenge—a real-world, multi-layer investigation.

---

## Cleanup & Decommissioning

**Critical:** AWS resources cost money. Delete everything when done.

### Part 1: Delete CloudFormation Stacks (10 minutes)

**Why important:** EC2 (Challenge 3) costs $0.02/hour. Leaving it running overnight = $0.48 waste.

**Option A: AWS CLI (Fastest)**

```bash
# Delete all stacks
aws cloudformation delete-stack --stack-name challenge-2 --region us-east-1
aws cloudformation delete-stack --stack-name challenge-3 --region us-east-1
aws cloudformation delete-stack --stack-name challenge-4 --region us-east-1

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name challenge-2 --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name challenge-3 --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name challenge-4 --region us-east-1

echo "All stacks deleted!"
```

---

**Option B: AWS Console**

1. CloudFormation → Stacks
2. Select `challenge-2` → Click **Delete** → Confirm
3. Select `challenge-3` → Click **Delete** → Confirm
4. Select `challenge-4` → Click **Delete** → Confirm
5. **Wait:** Each takes 1-2 minutes to delete
6. All three should show **Status:** **Delete in progress** → **DELETE_COMPLETE**

**Timeline:**
- Challenge 2 (Lambda): ~1 minute
- Challenge 3 (EC2): ~2 minutes
- Challenge 4 (Lambda + DynamoDB): ~1-2 minutes

---

### Part 2: Cleanup Manual Resources (Challenge 5)

1. **S3 Bucket:** AWS Console → S3 → `challenge5-data-bucket-*` → **Delete**
   - ⚠️ Empty the bucket first (delete all objects)
   - Then delete the bucket
2. **DynamoDB Table:** DynamoDB → `challenge5-metrics` → **Delete table**
3. **IAM Role:** IAM → Roles → `challenge5-role` → **Delete role**
4. **Lambda Function:** Lambda → `challenge5-cost-detective` → **Delete function**

---

### Part 3: Delete Agent Space (Optional)

**If you want to fully clean up:**

1. DevOps Agent console → Your Agent Space → **Delete Space**
2. Confirm deletion

**Not required** if you plan to use the agent again.

---

### Part 4: Verification Checklist

```bash
# Verify all stacks deleted
aws cloudformation list-stacks --query 'StackSummaries[?StackStatus==`DELETE_COMPLETE`]' --region us-east-1

# Verify Lambda functions deleted
aws lambda list-functions --region us-east-1 | grep challenge

# Verify EC2 instances terminated
aws ec2 describe-instances --filters "Name=tag:Name,Values=challenge3-stress" --region us-east-1
```

**Expected output:** Empty (no resources found)

---

### Cost Verification

1. AWS Console → **Billing** → **Cost Explorer** (or via AWS CLI)
2. **Check:** No new charges after cleanup
3. Verify your budget alert doesn't trigger

---

## Troubleshooting Guide

### Challenge 2: Lambda Test Shows "No permissions"

**Problem:**
```
Lambda doesn't have permission to write logs
```

**Solution:**
- The template already includes `AWSLambdaBasicExecutionRole` in the IAM role
- Wait 2-3 seconds for permissions to propagate
- Refresh the Lambda page and try again

---

### Challenge 2: Alarm Not Firing

**Problem:**
```
Alarm still shows INSUFFICIENT_DATA after multiple tests
```

**Solution:**
1. Make sure you clicked **Test** button (not just viewing the code)
2. Check the Lambda's error rate: Lambda → **Monitor** → **Error count** tab
3. CloudWatch checks every 60 seconds, so wait at least 2 minutes
4. Refresh CloudWatch Alarms page
5. Try 2-3 more test invocations

---

### Challenge 3: Session Manager Connection Fails

**Problem:**
```
Session Manager button is greyed out or connection times out
```

**Solution:**
1. **Wait:** Instance needs 1-2 minutes after launch to register with Systems Manager
2. **Refresh:** Click the instance → **Connect** again
3. **Check IAM:** The template includes `AmazonSSMManagedInstanceCore` policy
4. **Manual SSH:** If Session Manager fails, use SSH as fallback (requires security group rules)

---

### Challenge 3: Alarm Doesn't Fire Despite High CPU

**Problem:**
```
CPU graph shows 100%, but alarm stays OK
```

**Solution:**
1. **Threshold:** Alarm fires when CPU ≥ 70% for 1 evaluation period (60 seconds)
2. **Wait:** CloudWatch evaluates every 60 seconds
3. **Calculation:** If CPU sustained for 2 minutes, alarm should fire
4. **Check settings:** CloudWatch Alarms → `challenge3-high-cpu` → **Edit alarm**
   - Verify threshold is 70%
   - Verify period is 60 seconds

---

### Challenge 4: Lambda Still Shows "AccessDenied" After Policy Added

**Problem:**
```
Added the policy, but Lambda still fails with AccessDeniedException
```

**Solution:**
1. **IAM Propagation:** New inline policies take 10-15 seconds to propagate
2. **Wait:** 30 seconds, then try Lambda Test again
3. **Verify:** IAM → Role → **Inline policies** → Confirm policy shows in list
4. **Check resource ARN:** Policy must reference the correct DynamoDB table ARN
   - Format: `arn:aws:dynamodb:us-east-1:657709068147:table/challenge4-data`
   - Replace account ID with your actual account

---

### Challenge 4: DynamoDB Item Not Found

**Problem:**
```
Lambda returns success (200) but item is empty: {"item": {}}
```

**Solution:**
1. Make sure you seeded the DynamoDB table with data
2. DynamoDB → `challenge4-data` → **Explore table items**
3. Verify item with ID "1" exists
4. If not, create it (see Step 7 in Challenge 4 instructions)

---

### Agent Takes Too Long to Respond

**Problem:**
```
Agent chat box shows loading animation for >60 seconds
```

**Solution:**
1. **Normal:** Agent analysis takes 10-30 seconds, sometimes up to 60
2. **Wait:** Be patient for complex scenarios (Challenge 5)
3. **Refresh:** If >2 minutes, refresh the page
4. **Try again:** Rephrase the question more simply
5. **Check scope:** Agent only investigates resources in your Agent Space
   - If resource deployed to wrong region, agent can't see it

---

### CloudFormation Stack Creation Failed

**Problem:**
```
Stack creation failed with: "DeletionPolicy is missing"
```

**Solution:**
- This happens if you use "Import existing resources" instead of "standard"
- **Fix:** Delete the failed stack and try again with:
  - CloudFormation → **Create stack** → **With NEW resources (standard)**
  - NOT "With existing resources (import)"

---

### S3 Bucket Name Conflict

**Problem:**
```
Error: Bucket name already exists
```

**Solution:**
- S3 bucket names must be globally unique
- Add a random suffix: `challenge5-data-bucket-<randomstring>`
- Or use: `challenge5-data-bucket-$(date +%s)`
- Example: `challenge5-data-bucket-1721000000`

---

### Lambda Timeout During Test

**Problem:**
```
Lambda times out after waiting 10+ seconds
```

**Solution:**
1. **Check timeout setting:** Lambda → **Configuration** → **General configuration**
2. **Increase timeout:** Set to 30 seconds (vs. default 3)
3. **Try again:** Lambda Test
4. **Verify code:** Make sure Lambda isn't stuck in infinite loop

---

### Agent Can't Find Resources

**Problem:**
```
Agent says "I don't see any resources" or "Resource not found"
```

**Solution:**
1. **Check region:** Agent Space must monitor the same region as resources
   - All challenges use `us-east-1`
   - Verify Agent Space is set to `us-east-1`
2. **Wait:** Resources take 1-2 minutes to appear in agent's topology
3. **Refresh:** Close and reopen the agent chat
4. **Check access:** Agent Space IAM role must have read access to resources
   - If you restricted IAM scope, agent might not see everything

---

### Permission Denied When Adding IAM Policy

**Problem:**
```
Error: You do not have permission to edit this role
```

**Solution:**
1. **IAM permissions:** Your AWS user needs `iam:PutRolePolicy` permission
2. **Check:** Ask your AWS admin to grant IAM editing permissions
3. **Workaround:** Use AWS CLI (may work if console fails)
   ```bash
   aws iam put-role-policy --role-name challenge-4-AppRole-* --policy-name AllowReadChallenge4Table --policy-document file://policy.json
   ```

---

### DevOps Agent Charges Unexpected Cost

**Problem:**
```
Budget alert fired unexpectedly
```

**Solution:**
1. **Check billing:** AWS Billing → Cost Explorer
2. **Review charges:** Look for DevOps Agent fees (usually $0.01-0.10 per investigation)
3. **Limit investigations:** Use agent sparingly if cost is concern
4. **Review free tier:** First 2 months are free trial (no charges)
   - Verify free trial is enabled in DevOps Agent console

---

## Workshop Completion Summary

### What You've Accomplished

✅ **Challenge 1:** Experienced natural-language infrastructure debugging  
✅ **Challenge 2:** Found and fixed code errors via agent-guided investigation  
✅ **Challenge 3:** Diagnosed resource exhaustion and recovered live incident  
✅ **Challenge 4:** Identified hidden permission issues (not code bugs)  
✅ **Challenge 5:** Designed and debugged multi-layer real-world scenario  

### Key Skills Gained

1. **Infrastructure AI Interaction** - Asking agents for help
2. **Incident Triage** - Finding root causes faster
3. **Cross-Service Debugging** - Lambda + IAM + DynamoDB + S3 + EC2
4. **DevOps Thinking** - Code errors vs. configuration vs. permissions
5. **Cloud Cost Awareness** - Identifying storage bloat and waste

### Next Steps

1. **Submit findings** at [awsugmdu.in](https://www.awsugmdu.in/)
2. **Share learnings** with your team
3. **Adopt DevOps Agent** in your incident response workflow
4. **Train others** using this guide

---

## Appendix: Quick Command Reference

### Deploy All Challenges (Batch)
```bash
cd "c:\Users\karan\AWS\builders-skill-sprint-challenges\May-2026-DevOps-Month"

aws cloudformation deploy --stack-name challenge-2 --template-file challenge-2-first-investigation/template.yaml --capabilities CAPABILITY_IAM --region us-east-1
aws cloudformation deploy --stack-name challenge-3 --template-file challenge-3-stress-and-diagnose/template.yaml --capabilities CAPABILITY_IAM --region us-east-1
aws cloudformation deploy --stack-name challenge-4 --template-file challenge-4-bad-deploy-detective/template.yaml --capabilities CAPABILITY_IAM --region us-east-1
```

### Delete All Challenges (Batch)
```bash
aws cloudformation delete-stack --stack-name challenge-2 --region us-east-1
aws cloudformation delete-stack --stack-name challenge-3 --region us-east-1
aws cloudformation delete-stack --stack-name challenge-4 --region us-east-1

aws cloudformation wait stack-delete-complete --stack-name challenge-2 --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name challenge-3 --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name challenge-4 --region us-east-1
```

### Check Stack Status
```bash
aws cloudformation describe-stacks --region us-east-1 --query 'Stacks[?contains(StackName, `challenge`)].{Name:StackName,Status:StackStatus}'
```

### List Lambda Functions
```bash
aws lambda list-functions --region us-east-1 --query 'Functions[?contains(FunctionName, `challenge`)].{Name:FunctionName,Status:State}'
```

---

**Workshop Guide Complete!** 🎉

You now have step-by-step instructions to run, execute, and complete all 5 challenges of the AWS DevOps Agent Skill Sprint.
