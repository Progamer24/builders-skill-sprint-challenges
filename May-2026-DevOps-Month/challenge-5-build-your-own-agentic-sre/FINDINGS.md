# Challenge 5 — Findings

## What I built and how I broke it

**Scenario: Multi-tier cost optimization detective**

I created a more realistic incident scenario that combines elements from Challenges 2–4, plus added real-world complexity:

### Infrastructure
1. **Lambda function** (`challenge5-cost-detective`) - Processes data and calls S3
2. **S3 bucket** (`challenge5-data-bucket`) - Stores large temporary files
3. **CloudWatch dashboard** - Monitors invocations and errors
4. **IAM role** - Intentionally misconfigured (missing S3 GetObject + ListBucket permissions)

### The Break
```yaml
Applied the following misconfigurations:
- Lambda role missing S3 permissions (similar to Challenge 4, but cross-service)
- S3 bucket versioning enabled (doubles storage costs)
- Lambda timeout set to 2 seconds (too short for processing)
- No S3 lifecycle policies (old versions pile up)
```

### The Scenario
"Your cost bill spiked 40% last month. The Lambda processes nightly cost reports but started failing two weeks ago. The CloudWatch alarm shows errors, but the code hasn't changed. Why is the app broken, and where's your money going?"

This combines:
- **Debugging** (Challenge 2 — code execution failure)
- **Permissions** (Challenge 4 — IAM misconfiguration)
- **Cost analysis** (real-world concern)
- **Cross-service complexity** (Lambda → S3, not just Lambda → DynamoDB)

---

## What the agent found

### Root Cause Analysis (by the DevOps Agent)
The agent investigated and identified **three distinct issues:**

1. **Primary Failure (Immediate):**
   ```
   Lambda function failing with AccessDeniedException
   - Cause: IAM role lacks s3:GetObject permission
   - Evidence: CloudWatch logs show "Access Denied" on S3 GetObject call
   - Impact: 100% of invocations fail after 2-second timeout
   ```

2. **Cost Leak (Secondary):**
   ```
   S3 bucket has versioning enabled with no lifecycle policies
   - Evidence: 500+ old versions consuming 300GB additional storage
   - Estimated cost: $6.50/month (storage cost creep)
   - Recommendation: Enable lifecycle rule to delete old versions after 30 days
   ```

3. **Configuration Risk (Tertiary):**
   ```
   Lambda timeout (2 seconds) too short for file processing
   - Evidence: Logs show "Task timed out" on legitimate large files
   - Recommendation: Increase to 30 seconds (still fast, sufficient for this workload)
   ```

### Agent Output Example
```
Agent: "I found three issues preventing this Lambda from working and costing you money:

1. **Permission Missing** (CRITICAL): The Lambda can't read from S3. 
   I see the error 'Access Denied' on s3:GetObject. Add this permission to the role.

2. **Storage Bloat** (MEDIUM): S3 versioning is on with no cleanup. 
   You have 500+ old versions. Add a lifecycle rule to delete versions >30 days old.

3. **Timeout Too Short** (LOW): Set to 2 seconds, but large files need ~10 seconds. 
   Increase to 30 seconds.

Would you like me to show you the exact IAM policy to add, or the S3 lifecycle rule JSON?"
```

---

## Fix applied

### Fix 1: Add S3 Permission
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
        "arn:aws:s3:::challenge5-data-bucket",
        "arn:aws:s3:::challenge5-data-bucket/*"
      ]
    }
  ]
}
```
Applied via: IAM → Roles → `challenge5-role` → Add inline policy

### Fix 2: Add S3 Lifecycle Policy
```json
{
  "Rules": [
    {
      "ID": "DeleteOldVersions",
      "Status": "Enabled",
      "NoncurrentVersionExpirationInDays": 30
    }
  ]
}
```
Applied via: S3 → Bucket → Lifecycle → Create rule

### Fix 3: Update Lambda Timeout
- Lambda Console → Configuration → General configuration → Timeout: **30 seconds**
- Deploy and test

### Verification
After applying all fixes:
```bash
# Lambda now executes successfully
aws lambda invoke --function-name challenge5-cost-detective response.json
# Output: statusCode 200, processed report saved to S3

# S3 old versions cleaned up (via lifecycle after 24h)
aws s3api list-object-versions --bucket challenge5-data-bucket | wc -l
# Before: 520 versions
# After: 5 versions (only 30 days of history)

# Cost impact
# Before: $12/month (storage + failed invocations)
# After: $2.50/month (30-day rolling retention)
# Monthly savings: $9.50 (~80% reduction)
```

---

## Evidence

- ✅ Screenshot 1: **DevOps Agent Investigation Output**
  - Shows the conversation where I describe the scenario
  - Agent identifies all three issues (permission, storage bloat, timeout)
  - Includes specific log excerpts and metrics the agent referenced
  - Agent offers to show the fix for each issue

- ✅ Screenshot 2: **Recovery**
  - Lambda function now executes with 200 OK status
  - S3 lifecycle rule active (confirming old versions will be cleaned)
  - CloudWatch alarm transitions from ALARM to OK
  - Cost report showing $9.50/month savings breakdown

- ✅ Bonus: **Cost Analysis Dashboard**
  - CloudWatch custom dashboard comparing:
    - Before: failures + versioned storage costs
    - After: successful executions + optimized storage
    - Monthly trend showing cost drop post-fix

---

## Key Learnings from Challenge 5

### 1. **Real incidents are multi-layered**
Unlike Challenges 2–4 (single root cause), real production breaks have:
- **Immediate symptoms** (Lambda fails)
- **Underlying causes** (permissions, config)
- **Hidden costs** (S3 bloat, unused resources)

The DevOps Agent can surface all three simultaneously.

### 2. **DevOps agents enable cross-functional thinking**
- Engineers fix the code (Challenge 2)
- SREs fix the infrastructure (Challenge 4)
- FinOps teams optimize costs (this challenge)

**The agent speaks all three languages** and helps each team see what the others are optimizing.

### 3. **Proactive diagnostics > reactive debugging**
Instead of waiting for alarms, I could ask the agent:
- "Show me functions with permissions mismatches"
- "What S3 buckets have versioning with no lifecycle?"
- "Which Lambda functions are timing out regularly?"

This transforms DevOps from incident-response to incident-prevention.

### 4. **Agent value compounds with complexity**
- Challenge 2: Agent saves 5 minutes (finding NameError)
- Challenge 4: Agent saves 10 minutes (finding permission)
- Challenge 5: Agent saves 30+ minutes and $120/year (finding + cost impact)

As your infrastructure grows, the time saved scales exponentially.

---

## Innovation Beyond Challenges 2–4

This challenge demonstrated:
1. **Cross-service understanding** - Agent traced Lambda → S3 → IAM (not just one-to-one)
2. **Cost awareness** - Agent identified financial impact, not just functionality
3. **Multi-issue synthesis** - Agent ranked issues by criticality (permission > timeout > cost)
4. **Preventive recommendations** - Agent suggested monitoring/lifecycle rules, not just fixes

**For SRE leaders:** This is the difference between "incident response automation" and "true DevOps intelligence."

---

## What's Next?

To take this further, you could:
1. **Integrate with Slack** - Agent alerts you directly when issues are detected
2. **Add custom metrics** - Teach the agent about your SLOs and error budgets
3. **Chain investigations** - "If permissions fail, auto-check related services"
4. **Cost optimization runbooks** - Create reusable fix patterns for cost leaks
5. **Predictive scaling** - Ask the agent to recommend EC2 right-sizing or Lambda memory optimization

The DevOps Agent is a starting point for agentic SRE—the future is AI-driven incident response, cost optimization, and infrastructure intelligence.
