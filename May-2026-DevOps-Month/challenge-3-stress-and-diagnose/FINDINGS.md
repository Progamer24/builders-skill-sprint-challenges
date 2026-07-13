# Challenge 3 — Findings

## Root cause

**The EC2 instance is running one or more runaway CPU-intensive processes (busy-loop CPU stress).** 

The CloudFormation template for this challenge bootstraps the t3.micro EC2 instance with a UserData script that launches CPU stress processes at startup:

```bash
for i in $(seq $(nproc)); do
    setsid /bin/bash -c 'while true; do :; done &'
done
```

This spawns one busy-loop process per CPU core (on a t3.micro, that's 2 cores). Each process runs `while true; do :; done` - an infinite loop that performs no work but consumes 100% of available CPU. The `setsid` ensures these processes persist after cloud-init completes.

**Result:** CPU utilization immediately pins to 100%, triggering the `challenge3-high-cpu` CloudWatch alarm.

The DevOps Agent identifies this by:
1. Checking CloudWatch CPU metrics (showing 100% sustained usage)
2. Correlating with EC2 instance details
3. Suggesting investigation tools like Session Manager for deeper diagnostics

## Fix applied

**Stop the runaway processes to recover CPU capacity.**

Using AWS Session Manager (click-to-connect terminal):

```bash
# List all running processes and find the busy-loop
ps aux | grep "while true"

# Kill the offending processes
killall bash

# Or more surgical approach:
kill -9 <pid-of-busy-process>

# Verify CPU returns to normal
top
```

After stopping the processes, the instance CPU drops to normal levels (<5%), and the CloudWatch alarm automatically transitions from **ALARM** to **OK**.

## Evidence

- ✅ Screenshot 1: AWS DevOps Agent diagnosis showing:
  - CPU utilization at 100% (steady-state)
  - CloudWatch `challenge3-high-cpu` alarm in ALARM state
  - Agent recommendation: "Stop the infinite loop processes consuming CPU"
  - EC2 instance details and Session Manager connection option

- ✅ Screenshot 2: Recovery - After killing the busy-loop processes:
  - CPU drops to <5% utilization
  - CloudWatch `challenge3-high-cpu` alarm transitions to OK (green)
  - CloudWatch graph shows sharp downward spike after process termination

---

## Key Learnings

**This challenge simulates a real "noisy neighbor" incident.** 

1. **Runaway processes are common causes of incidents** - Unoptimized loops, infinite recursion, memory leaks, or misconfigured batch jobs frequently cause CPU/memory spikes

2. **DevOps Agents can diagnose resource exhaustion** - The agent quickly correlated CloudWatch metrics with EC2 instance state, eliminating manual dashboard hunting

3. **Session Manager provides incident response access** - No SSH keys, no bastion hosts, no security group rules—just one click to troubleshoot

4. **Observability feeds diagnostic power** - CloudWatch metrics alone don't explain *why*, but combined with EC2 state and logs, the agent (and human) can form hypothesis

**For SRE teams:** This demonstrates why you need three layers:
- **Visibility** (CloudWatch, logs)
- **Diagnosability** (Session Manager access)
- **Intelligence** (DevOps Agent to connect the dots)

The agent handles layer 3, accelerating investigation from hours to minutes.
