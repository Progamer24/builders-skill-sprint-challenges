# Challenge 2 — Findings

## Root cause

**The Lambda function has an undefined variable error (NameError).** 

The original code attempts to access `config["value"]` but the `config` variable is never defined or initialized. The function crashes with:
```
NameError: name 'config' is not defined
```

This is a classic Python error where a variable is referenced before it's assigned a value. The DevOps Agent immediately identified this by analyzing the CloudWatch logs.

## Fix applied

**Define the config dictionary before accessing it.**

**Original broken code:**
```python
def handler(event, context):
    # This function is broken on purpose
    return {"result": config["value"]}  # ❌ config is undefined!
```

**Fixed code:**
```python
def handler(event, context):
    # Define config with a default value
    config = {"value": "Challenge 2 is now fixed!"}
    return {"result": config["value"]}  # ✅ config is defined
```

After deploying the fixed code, the Lambda function executes successfully and returns the expected response.

## Evidence

- ✅ Screenshot 1: AWS DevOps Agent analysis showing the root cause - the NameError in CloudWatch logs and the undefined `config` variable
- ✅ Screenshot 2: The Lambda function test returning `statusCode: 200` with successful response `{"result": "Challenge 2 is now fixed!"}` and the `challenge2-broken-fn-errors` alarm returning to **OK** (green status)

---

## Key Learnings

**Common Python errors are easy to miss during code reviews.** This challenge demonstrates how:

1. **DevOps Agents democratize debugging** - The agent can analyze Lambda logs and pinpoint syntax/runtime errors without needing Python expertise
2. **CloudWatch integration is crucial** - Logs provide the exact evidence (stack trace) needed for diagnosis
3. **Automation catches simple mistakes** - This type of error would normally require manual log searching; the agent automated that discovery

**For SRE teams:** The ability to quickly identify that a function is broken (not misconfigured, but actually broken code) reduces toil and enables faster remediation.
