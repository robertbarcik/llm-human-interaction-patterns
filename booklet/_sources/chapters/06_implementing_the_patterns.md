# Chapter 6: Implementing the Patterns

The preceding chapters described what to build and why. This chapter describes how to build it. Every section produces an artifact --- a prompt template, a decision table, a configuration, a workflow, or a checklist --- that can be taken directly into a production system. The goal is not to restate theory but to translate it into implementation.

## Prompt Templates for Structured Output

The interaction patterns described in Chapters 2 through 5 depend on the LLM agent producing output in specific formats. Left to its own defaults, a model will generate fluent, conversational prose --- exactly the wrong format for an operator making time-sensitive decisions. Structured output requires structured prompts. The three templates below address the most common formatting needs: situation reporting, uncertainty expression, and confidence classification.

### Template 1: SBAR-Formatted Output

Chapter 4 introduced the SBAR framework adapted for AI agent output: WHAT HAPPENED, WHAT I TRIED, WHAT I RECOMMEND, RISK LEVEL, COST OF INACTION, and EVIDENCE. The following system prompt instructs the agent to use this structure for every recommendation.

```
You are an AI operations agent. Structure EVERY recommendation using this exact format:

WHAT HAPPENED: [One sentence. State the event or condition you detected.]

WHAT I TRIED: [List the investigative actions you took and what you found. Include negative findings ("no anomalies detected in X").]

WHAT I RECOMMEND: [One specific action. State the expected outcome.]

RISK LEVEL: [CRITICAL / HIGH / MEDIUM / LOW. One sentence justifying the classification.]

COST OF INACTION: [What happens if the operator does nothing? Include a time estimate if possible.]

EVIDENCE: [List specific data sources, log entries, metric values, or KB articles that support your assessment. Use references the operator can verify independently.]

Rules:
- Never skip a section. If you have nothing for a section, write "None identified."
- WHAT I RECOMMEND must contain exactly one recommended action, not a list of options.
- COST OF INACTION must describe a concrete consequence, not a vague risk statement.
- EVIDENCE must reference specific, verifiable data --- not summaries of data.
```

**Example output:**

```
WHAT HAPPENED: Pod checkout-service-7b4f has crash-looped 4 times 
in the last 12 minutes in the prod-eu-west cluster.

WHAT I TRIED: Pulled container logs (OOMKilled on each restart), 
checked memory allocation (limit: 512Mi, peak usage before kill: 
508Mi), reviewed recent deployments (v3.12.1 deployed 47 minutes 
ago, added PDF receipt generation feature), checked other pods in 
the service (3 of 8 pods affected, all processing PDF receipts).

WHAT I RECOMMEND: Increase memory limit for checkout-service to 
1024Mi. Expected outcome: pods stabilize, PDF receipt generation 
completes without OOM kills.

RISK LEVEL: MEDIUM. Service is degraded (3 of 8 pods cycling) but 
not down. Load balancer is routing around affected pods.

COST OF INACTION: If additional pods begin processing PDF receipts, 
more pods will OOM. At current traffic levels, full service 
degradation is likely within 30--60 minutes.

EVIDENCE: [Pod logs: OOMKilled x4] [Metrics: memory peak 508/512Mi] 
[Deployment log: v3.12.1 at 14:23 UTC] [Git diff: +PDF generation]
```

**Watch for:** The most common failure mode is the model conflating Assessment and Recommendation --- producing a RISK LEVEL that is actually a recommendation ("RISK LEVEL: HIGH --- we should restart the service immediately") or a WHAT I RECOMMEND that is actually an assessment ("I recommend monitoring the situation"). Enforce the distinction in your prompt and in post-processing validation. A second failure mode is omitting COST OF INACTION or filling it with a tautology ("If no action is taken, the problem will persist"). Explicitly instruct the model to describe a concrete consequence with a timeline.

### Template 2: First-Person Uncertainty Expression

Chapter 5 discussed the Kim et al. (FAccT 2024) finding that first-person uncertainty expression ("I'm not sure, but...") decreases operator confidence while increasing decision accuracy. The following template implements this behavior, keyed to a confidence threshold.

```
You are an AI operations agent. After analyzing each situation, 
internally assess your confidence in your recommendation on a 
scale from 0 to 100.

If your confidence is 75 or above:
  Present your recommendation directly, without hedging.

If your confidence is below 75:
  Begin your recommendation with a first-person uncertainty 
  expression. Use phrases like:
  - "I'm not confident about this, but..."
  - "I'm uncertain here --- my best assessment is..."
  - "I don't have strong evidence for this, but..."
  
  Then state what specifically you are uncertain about and why.

Never use vague, third-person hedging like "it is possible that" 
or "there may be an issue with." Always use first-person language 
that attributes the uncertainty to your own judgment.

After your recommendation, state your confidence level explicitly:
  [Confidence: XX/100 — one-sentence reason]
```

**Example output at high confidence (82/100):**

```
The root cause is a connection pool exhaustion in the payments 
database. The connection count has been at the maximum (100) for 
the past 14 minutes, and all timed-out requests correlate with 
payment processing endpoints.

Recommended action: Increase max_connections from 100 to 200 and 
investigate the long-running queries holding connections open.

[Confidence: 82/100 — Strong correlation between connection pool 
saturation and error pattern; confirmed via two independent metrics.]
```

**Example output at low confidence (38/100):**

```
I'm not confident about this, but my best assessment is that the 
intermittent 502 errors are caused by the new rate limiter 
configuration deployed this morning. I'm uncertain because the 
errors started approximately 90 minutes after the deployment, not 
immediately, and I cannot find a clear causal link in the logs.

Recommended action: Temporarily disable the new rate limiter and 
observe whether 502 errors subside.

[Confidence: 38/100 — Temporal correlation is weak; no direct 
evidence linking the rate limiter to the 502 responses.]
```

**Watch for:** Models tend toward one of two failure modes with uncertainty expression. The first is universal hedging --- the model prepends "I'm not sure" to every response regardless of actual confidence, which trains operators to ignore the signal entirely. The second is false precision --- the model never drops below 70/100 even when its reasoning is clearly speculative. Both modes require calibration (see Section 5 of this chapter). If you observe universal hedging, raise the threshold or add few-shot examples of confident responses. If you observe false precision, add explicit instructions to lower confidence when reasoning depends on assumptions rather than evidence.

### Template 3: Graduated Confidence with Reasoning

For systems where a numeric confidence score is too granular and a binary high/low is too coarse, the following template implements a categorical confidence system with mandatory reasoning.

```
You are an AI operations agent. For every recommendation, classify 
your confidence using exactly one of these levels:

CONFIRMED — I have verified this through multiple independent 
sources. I am certain this is correct.

HIGH — Strong evidence supports this conclusion. One or more 
independent signals corroborate it.

MODERATE — The evidence is suggestive but not conclusive. There 
are plausible alternative explanations.

LOW — I am reasoning from limited or indirect evidence. My 
conclusion is an educated guess.

SPECULATIVE — I have very little evidence. This is my best 
hypothesis, but it could easily be wrong.

After the confidence label, provide exactly one sentence explaining 
what evidence supports (or fails to support) your assessment.

Format: [Confidence: LEVEL — reasoning sentence]
```

**Example output:**

```
The disk space alert on db-primary-01 is caused by unrotated 
PostgreSQL WAL files accumulating in pg_wal/. Current usage is 
94% with 847 WAL files totaling 13.2 GB.

Recommended action: Run pg_archivecleanup to remove WAL files 
older than the last successful backup checkpoint.

[Confidence: CONFIRMED — Verified via df output, ls -la pg_wal/, 
and pg_controldata showing last checkpoint LSN.]
```

**Watch for:** The model's self-reported confidence may not match its actual accuracy. A model that labels 40% of its recommendations as CONFIRMED but is only correct 70% of the time in that band is poorly calibrated and will erode operator trust. Categorical confidence labels must be empirically validated against outcome data. Section 5 of this chapter describes how to do this. Until calibration data is available, treat these labels as hypotheses, not guarantees.

## Graduated Autonomy Decision Framework

Chapter 2 introduced five structural patterns. The question every implementation team faces is: which pattern applies to which action? The following framework provides a systematic method for making that classification.

> **Terminology note:** If you have read *Building Agentic AI*, the risk classification system (LOW/MEDIUM/HIGH) and assertiveness levels (cautious/balanced/autonomous) described there map directly to the Recommend & Wait through Execute & Report spectrum below. The taxonomies are complementary: *Building Agentic AI* addresses the agent-internal engineering; this guide addresses the operator-facing interaction design.

**Step 1: Enumerate actions.** List every action your AI agent is capable of taking. Include investigative actions (querying a database, pulling logs), communicative actions (sending alerts, creating tickets), and operational actions (restarting services, modifying configurations, blocking IPs).

**Step 2: Assess four dimensions for each action.** For each action on your list, evaluate:

| Dimension | Question | Scale |
|-----------|----------|-------|
| Consequence severity | What is the worst realistic outcome if this action is wrong? | Low / Medium / High / Critical |
| Reversibility | Can this action be undone? How quickly and at what cost? | Instant / Minutes / Hours / Difficult / Irreversible |
| Time sensitivity | What is the operational cost of waiting for human approval? | Low (can wait hours) / Medium (minutes matter) / High (seconds matter) |
| AI confidence | How reliably can the model make this decision correctly? | Based on calibration data, not intuition |

**Step 3: Map to pattern.** Use the following decision logic:

- **High consequence + Irreversible** = Recommend & Wait (Levels 4--5), regardless of time sensitivity
- **High consequence + Reversible + Time-critical** = Recommend & Wait with pre-staged action (Level 5)
- **Medium consequence + Reversible** = Recommend & Wait or Execute & Report, depending on calibrated confidence
- **Low consequence + Reversible + Time-critical** = Execute & Report (Level 7)
- **Any consequence level + Low AI confidence** = Recommend & Wait, always

### Action Classification Worksheet

The following worksheet demonstrates the framework applied to common infrastructure operations actions. Use it as a template --- replace the example rows with your own agent's action inventory.

| Action | Consequence if Wrong | Reversible? | Time to Decide | Confidence Required | Pattern | Autonomy Level |
|--------|---------------------|-------------|----------------|--------------------:|---------|:--------------:|
| Restart crashed pod | Low (pod restarts anyway) | Yes (instant) | High (downtime ongoing) | Low | Execute & Report | L7 |
| Scale up replicas | Low (cost increase) | Yes (scale down) | High (load spike) | Low | Execute & Report | L7 |
| Block IP via WAF | Medium (may block legitimate users) | Yes (unblock) | High (active attack) | Medium | Recommend & Wait | L5 |
| Failover database | High (data integrity risk) | Difficult (manual reconciliation) | Medium (degraded service) | High | Recommend & Wait | L4 |
| Roll back deployment | Medium (feature regression) | Yes (re-deploy) | Medium (errors accumulating) | Medium | Recommend & Wait | L5 |
| Modify firewall rules | High (may break connectivity) | Yes but complex (rule ordering) | Low (planned change) | High | Recommend & Wait | L4 |
| Deploy config change | High (may cause outage) | Yes (revert commit) | Low (planned change) | High | Draft & Refine | L5 |
| Delete old log data | Medium (permanent data loss) | No (irreversible) | Low (storage cleanup) | Medium | Recommend & Wait | L4 |

> **Key insight:** The worksheet often reveals that teams have granted their agents too much autonomy for irreversible actions and too little for trivially reversible ones. If your agent requires human approval to restart a crashed pod but autonomously modifies firewall rules, the classification is inverted.

## Circuit Breaker and Fallback Architecture

Chapter 6 described the circuit breaker pattern and its rationale. This section provides the implementation specification: what to monitor, what thresholds to set, and what fallbacks to configure.

### Three Levels of Circuit Breakers

An LLM agent system has three categories of dependencies, each requiring its own circuit breaker configuration.

**Level 1: LLM API circuit breaker.** This monitors response latency and error rate from the model provider. It trips after N consecutive failures (recommended starting value: 3) or when the error rate exceeds P% in a rolling time window (recommended starting values: 30% error rate in a 60-second window). Fallback options, in order of preference: route to a backup LLM provider with an adapted prompt; return pre-generated responses from a cache of common scenarios; escalate directly to human with raw context data and no AI synthesis. The choice depends on whether a backup provider is contractually and technically available.

**Level 2: Tool execution circuit breaker.** This monitors the tools the agent calls --- monitoring APIs, ticketing systems, knowledge bases, databases. Each tool gets its own circuit breaker instance because tool failures are typically independent. A monitoring API outage should not prevent the agent from querying the knowledge base. Trips after 5 consecutive failures or 50% error rate in a 120-second window (adjust per tool criticality). Fallback: skip the failing tool and note its unavailability in the output ("Note: monitoring API unavailable --- metrics data not included in this assessment"), use cached data from the last successful query, or escalate to human if the tool is essential to the action.

**Level 3: Quality gate circuit breaker.** This monitors the quality of the agent's own outputs --- the distribution of confidence scores, the pass rate of validation checks, and the rate of operator overrides. It trips when quality degrades below a defined threshold: for example, when more than 40% of recommendations in a 30-minute window are classified as LOW or SPECULATIVE confidence, or when the operator override rate exceeds 60% in the same window. Fallback: downshift autonomy level for all actions. Any action currently classified as Execute & Report reverts to Recommend & Wait. The system continues to analyze and recommend, but takes no autonomous action until the quality gate circuit breaker closes.

### Fallback Configuration Template

| Dependency | Failure Threshold | Fallback Action | Recovery Test | Escalation Path |
|------------|------------------|-----------------|---------------|-----------------|
| LLM API (primary) | 3 consecutive errors or 30% error rate / 60s | Route to backup provider; if unavailable, return cached responses | Single request to primary provider | Alert on-call engineer after 5 min in OPEN state |
| Monitoring API | 5 consecutive errors or 50% error rate / 120s | Use last cached metric snapshot (max age: 10 min); flag data staleness in output | Single health check query | Alert on-call if cached data exceeds max age |
| Ticketing system | 5 consecutive errors or 50% error rate / 120s | Queue ticket creation locally; retry on circuit close | Single ticket read query | Alert on-call after 15 min in OPEN state |
| Knowledge base | 3 consecutive errors or 30% error rate / 60s | Proceed without KB context; note in output: "Knowledge base unavailable" | Single search query | No escalation; log only |
| Action executor (e.g., K8s API) | 2 consecutive errors | Halt all autonomous actions; switch to Recommend & Wait | Single read-only API call (e.g., list pods) | Alert on-call immediately |

### State Machine

The circuit breaker state machine is identical across all three levels. Only the thresholds and fallback actions differ.

```
CLOSED ──(threshold exceeded)──► OPEN
  ▲                                │
  │                                │ (timeout elapsed)
  │                                ▼
  └──(test succeeds)──── HALF_OPEN
                            │
                            │ (test fails)
                            ▼
                           OPEN
```

**CLOSED:** Normal operation. Failure counter increments on each failure, resets on success or after the time window expires. **OPEN:** All requests routed to fallback. A recovery timeout begins (recommended starting value: 60 seconds for LLM API, 120 seconds for tools, 300 seconds for quality gate). **HALF_OPEN:** A single test request is sent to the primary path. Success returns to CLOSED and resets the failure counter. Failure returns to OPEN and doubles the recovery timeout, up to a configured maximum (recommended: 10 minutes).

## Kill Switch Architecture

Chapter 6 established the requirements and rationale for kill switches. This section specifies the architecture.

### What the Kill Switch Must Control

- All LLM API calls originating from the agent
- All tool invocations (MCP tool calls, function calls, API requests)
- All autonomous actions (anything the agent executes without human approval)
- All scheduled and queued actions (pending approvals, batched operations, cron-triggered tasks)

### What the Kill Switch Must NOT Control

- Monitoring and observability dashboards (operators need to see what happened)
- Logging and audit trail (the record must continue even when the agent stops)
- Manual operation interfaces (operators must be able to work without the agent)
- Alert routing to human operators (alerts must still reach people)

The distinction is critical. A kill switch that also disables monitoring leaves operators blind. A kill switch that stops logging destroys the evidence needed for incident review.

### Architecture

```
┌─────────────────────────────────────────────┐
│  OPERATOR INTERFACE                         │
│  ┌─────────────────────────────────────┐    │
│  │  [KILL SWITCH]  ← always visible    │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  INFRASTRUCTURE CONTROL PLANE       │    │
│  │  (external to AI agent process)     │    │
│  │                                     │    │
│  │  agent_enabled: true/false          │    │
│  │  ─────────────────────────────      │    │
│  │  append-only audit log              │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  AI AGENT PROCESS                   │    │
│  │  checks agent_enabled before        │    │
│  │  every LLM call and tool invocation │    │
│  │                                     │    │
│  │  CANNOT modify agent_enabled        │    │
│  │  CANNOT access audit log            │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

The `agent_enabled` flag lives in infrastructure the agent cannot reach --- a separate configuration store, a feature flag service, or a hardware switch. The agent reads this flag but cannot write to it. The audit log records every state change with timestamp, operator identity, and reason.

### Implementation Requirements

The agent process must check `agent_enabled` at two points: before every LLM API call, and before every tool invocation. This is a synchronous, blocking check --- not an asynchronous polling loop. If the flag is `false`, the agent immediately returns a standard "agent disabled" response without making the call.

Queued and scheduled actions require additional handling. When the kill switch is activated, the system must drain or cancel all pending actions. A kill switch that stops new actions but allows queued actions to execute is not a kill switch --- it is a pause button with a potentially long tail.

### Testing Cadence

Test the kill switch monthly. Each test should document:

- Who activated the kill switch
- How long from activation to full stop (target: under 5 seconds)
- What actions were in flight at the time of activation
- Whether any actions leaked through after activation
- How long from reactivation to normal operation

If any actions leak through during a test, the kill switch implementation has a bug. Fix it before the next production deployment.

## Confidence Calibration Workflow

The prompt templates in Section 1 instruct the model to report confidence levels. But a model's self-reported confidence is only useful if it correlates with actual accuracy. This section describes the operational workflow for calibrating confidence empirically.

### Step 1: Collect Baseline Data

Run the agent in Recommend & Wait mode --- no autonomous actions --- for a minimum of 200 recommendations. For each recommendation, record four data points: the agent's recommendation, the model's reported confidence (numeric or categorical), the human operator's decision (accept without modification, accept with modification, or reject), and the actual outcome (was the action correct or incorrect, assessed after the fact).

Two hundred is a minimum for statistical significance. For systems with high action diversity (many different types of recommendations), increase the sample size to ensure at least 30 observations per action type.

### Step 2: Build the Calibration Curve

Group recommendations by confidence band. For numeric confidence, use bands of 20 percentage points. For categorical confidence, use the categories directly. For each band, calculate the actual accuracy rate.

| Confidence Band | Count | Correct | Accuracy |
|-----------------|------:|--------:|---------:|
| 0--20% (SPECULATIVE) | 12 | 3 | 25% |
| 21--40% (LOW) | 28 | 14 | 50% |
| 41--60% (MODERATE) | 47 | 31 | 66% |
| 61--80% (HIGH) | 68 | 57 | 84% |
| 81--100% (CONFIRMED) | 45 | 42 | 93% |

A perfectly calibrated model would show accuracy that matches the midpoint of each confidence band: 10% accuracy in the 0--20% band, 30% in the 21--40% band, and so on. In practice, models are almost always overconfident --- their stated confidence exceeds their actual accuracy. The calibration curve quantifies by how much, which is the information you need to set operational thresholds.

### Step 3: Set Operational Thresholds

Based on calibration data, define the confidence boundaries that map to operational behavior:

- **Above X%** (where X is the confidence level at which accuracy exceeds your minimum acceptable rate): label as HIGH confidence. These recommendations may be candidates for autonomous execution if other criteria (consequence, reversibility) are met.
- **Between Y% and X%**: label as MODERATE. These recommendations are presented to the operator with standard formatting.
- **Below Y%** (where Y is the confidence level below which accuracy drops below an unacceptable rate): label as LOW. These recommendations trigger first-person uncertainty expression, require mandatory human review, and are never eligible for autonomous execution.

The specific values of X and Y depend on the operational context. An IT service desk handling password resets might set X=70 and Y=40. A system recommending security incident responses might set X=90 and Y=70.

### Step 4: Implement in Production

Map the calibrated confidence bands to autonomy levels and presentation formats:

| Calibrated Confidence | Presentation Format | Autonomy Level | Uncertainty Expression |
|-----------------------|--------------------:|:--------------:|:----------------------:|
| HIGH (above X%) | Standard SBAR | Per action classification worksheet | None |
| MODERATE (Y% to X%) | SBAR with explicit confidence statement | Recommend & Wait (maximum) | Optional |
| LOW (below Y%) | SBAR with first-person hedging | Recommend & Wait (mandatory) | Required |

### Step 5: Re-Calibrate on Schedule

Calibration drifts. Models change. Prompts change. Operational contexts change. Re-run Steps 1 through 3:

- Monthly, as a standing operational task
- Immediately after any model version change
- Immediately after any significant prompt modification
- After any change to the tools or data sources the agent uses

### Calibration Log Template

The following template captures the data needed for calibration. Maintain this log continuously; analyze it on the re-calibration schedule.

| # | Recommendation Summary | Model Confidence | Confidence Band | Human Decision | Outcome | Correct? |
|--:|------------------------|:----------------:|:---------------:|:--------------:|:-------:|:--------:|
| 1 | Restart pod checkout-service-7b4f (OOMKilled) | 88 | 81--100 | Accept | Pod stabilized | Yes |
| 2 | Block IP 198.51.100.42 (credential stuffing) | 74 | 61--80 | Accept with modification (added IP range) | Attack stopped | Yes |
| 3 | Roll back deployment v3.12.1 (error rate spike) | 62 | 61--80 | Reject (spike was transient) | Errors resolved without rollback | No |
| 4 | Increase DB connection pool to 200 | 45 | 41--60 | Accept | Pool exhaustion resolved | Yes |
| 5 | Failover to DR region (primary unresponsive) | 71 | 61--80 | Reject (primary recovered) | Primary recovered in 3 min | No |

> **Key insight:** Most teams skip calibration because it requires running the system in Recommend & Wait mode long enough to collect meaningful data. This is not a shortcut you can take. An uncalibrated confidence system is worse than no confidence system --- it teaches operators to ignore confidence signals entirely.

## Design Your System: Self-Assessment Worksheet

The patterns, templates, and frameworks in this booklet are only useful if they are applied systematically. The following worksheet consolidates the key design questions from every chapter into a single assessment. For each AI-human interaction point in your system --- each place where the agent produces output, takes action, or requests human input --- answer these ten questions.

### The Worksheet

| # | Question | Chapter Reference | Your Answer |
|--:|----------|:-----------------:|:-----------:|
| 1 | What pattern are you using for this action? (Recommend & Wait / Triage & Escalate / Execute & Report / Draft & Refine / Graduated Autonomy) | Chapter 2 | |
| 2 | Is the autonomy level appropriate for the action's consequence severity, reversibility, and time sensitivity? | This chapter, Section 2 | |
| 3 | How is context presented to the operator? (Raw dump / SBAR / Progressive disclosure) | Chapter 4 | |
| 4 | How is confidence communicated? (Raw probability / Categorical with calibration / None) | Chapter 5 | |
| 5 | Is the AI's recommendation shown before or after the operator forms their own assessment? | Chapter 3 (anchoring) | |
| 6 | Has confidence been empirically calibrated? When was the last calibration? | This chapter, Section 5 | |
| 7 | Does a kill switch exist? Is it external to the AI, always visible, and tested monthly? | This chapter, Section 4 | |
| 8 | Are circuit breakers implemented for all external dependencies? | This chapter, Section 3 | |
| 9 | Is there a tested fallback for when the AI is unavailable? | This chapter, Section 3 | |
| 10 | Is there a named human owner who is authorized to shut down the system? | Chapter 8 | |

### Scoring

Count the number of questions you can answer "yes" to (or, for questions 1, 3, and 4, can answer with a specific, deliberate choice rather than "I don't know" or "we haven't decided").

**8--10 affirmative answers:** Ready for graduated autonomy in production. Your system has the structural, psychological, and operational foundations for safe autonomous action at the levels defined by your action classification worksheet.

**5--7 affirmative answers:** Acceptable for Recommend & Wait in production. The system can safely analyze situations and present recommendations, but should not take autonomous actions until the remaining gaps are addressed. Prioritize the gaps: kill switch and circuit breakers (questions 7--9) before confidence calibration (question 6) before presentation optimization (questions 3--5).

**Below 5 affirmative answers:** Not ready for production deployment with any autonomous capability. The system may be useful as an internal analysis tool, but it lacks the safety infrastructure required for operator-facing deployment. Address the gaps systematically, starting with the action classification worksheet (question 2) and kill switch architecture (question 7).

### Using the Worksheet

This worksheet is not a one-time exercise. Re-assess quarterly, or after any significant change to the model, the tooling, or the operational context. Changes that should trigger a re-assessment include: upgrading or switching the LLM provider, adding new tools or data sources to the agent, expanding the agent's action inventory, changing the operator team (new hires, role changes), and any incident in which the agent's behavior was unexpected or harmful.

Keep completed worksheets. They form a design history that is invaluable during incident review ("What did we believe about this system's readiness when we promoted it to Execute & Report?") and during audits ("Show us your assessment of this system's safety infrastructure").

The patterns in this booklet are not prescriptions. They are tools for making deliberate, documented, defensible decisions about how AI agents and human operators work together. The worksheet ensures those decisions are made explicitly rather than by default --- and that they are revisited as conditions change.
