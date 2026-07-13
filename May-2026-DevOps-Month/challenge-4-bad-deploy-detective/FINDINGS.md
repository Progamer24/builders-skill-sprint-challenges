# Challenge 4 — Findings

## Root cause

**The Lambda function's IAM role lacks permission to read from the DynamoDB table.** 

The template creates:
- A Lambda function (`challenge4-app-fn`) with code that looks correct
- A DynamoDB table (`challenge4-data`)
- An IAM role (`challenge4-AppRole`) for the Lambda

However, **the role is missing the `dynamodb:GetItem` permission** on the table resource. When the Lambda tries to read an item from DynamoDB, AWS IAM blocks the call:

```
AccessDeniedException: User is not authorized to perform: dynamodb:GetItem 
on resource: arn:aws:dynamodb:us-east-1:<ACCOUNT>:table/challenge4-data 
because no identity-based policy allows the dynamodb:GetItem action
```

**This is the classic "Bad Deploy" scenario:** The code is correct, but configuration changed (permissions were revoked or never granted), breaking the app silently.

The DevOps Agent identified this by:
1. Examining Lambda function logs (showing AccessDeniedException)
2. Checking the Lambda's IAM role
3. Discovering the missing DynamoDB permission
4. Noting the mismatch between what the code *requires* (GetItem on table) and what the role *allows*

## Fix applied

**Grant the Lambda's IAM role permission to read from the DynamoDB table.**

The fix is purely configuration—**no code changes needed**. Add an inline policy to the Lambda's role:

**Policy to add:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:<ACCOUNT_ID>:table/challenge4-data"
    }
  ]
}
```

**Steps (AWS Console):**
1. IAM → **Roles** → search for `challenge-4-AppRole-*`
2. **Add inline policy** → **JSON** → paste the policy above
3. Name it `AllowReadChallenge4Table` → **Create**
4. Return to Lambda → **Test** → now returns **200 OK** with the product:
   ```json
   {
     "statusCode": 200,
     "body": "{\"item\": {\"id\": {\"S\": \"1\"}, \"product\": {\"S\": \"Builders Hoodie\"}, \"price\": {\"N\": \"49\"}}}"
   }
   ```
5. Verify `challenge4-app-fn-errors` alarm returns to **OK**

## Evidence

- ✅ Screenshot 1: DevOps Agent investigation showing:
  - Lambda function logs with the AccessDeniedException error
  - IAM role details (`challenge4-AppRole-*`)
  - Missing `dynamodb:GetItem` permission
  - Agent conclusion: "Grant the Lambda role read access to the table"

- ✅ Screenshot 2: Recovery - After adding the policy:
  - Lambda **Test** tab shows successful response (statusCode 200)
  - Response body includes the product from DynamoDB
  - CloudWatch alarm `challenge4-app-fn-errors` transitions to OK (green)

---

## Key Learnings

**This challenge illustrates the "permissions creep" problem in real deployments.**

1. **Principle of Least Privilege = Debugging Difficulty** - Tight permissions catch bugs early (like this), but make troubleshooting harder because the error is not obvious from code inspection

2. **IAM is the source of truth, not the code** - The Lambda code is 100% correct. The failure is purely AWS IAM. This is why:
   - Code reviews alone won't catch it
   - DevOps tools that understand AWS configuration (like the agent) are essential

3. **"Bad Deploys" are config changes, not code bugs** - Modern deployments update both code and infrastructure. A missing permission can slip through if:
   - The role changed during deployment
   - A shared policy was revoked
   - Permissions were accidentally scoped too narrowly

4. **Integration testing catches this** - If the template included an IAM policy granting the Lambda access, this wouldn't happen. But many deployments use "admin roles" in dev and then tighten in prod—catching this late

**For SRE teams:** 
- Monitor IAM policy changes (CloudTrail)
- Test with least-privilege roles early
- Use the agent to audit cross-service permissions (S3 → Lambda, Lambda → DynamoDB, etc.)

This challenge demonstrates why you need intelligence at the permission level, not just code level.
