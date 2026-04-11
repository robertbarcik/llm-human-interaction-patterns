# Chapter 4: Context Presentation

How you present information determines what the operator sees. And what the operator sees determines what they decide. This is not a metaphor. It is a measurable, reproducible phenomenon: the same incident data, presented in different formats, produces different decisions from the same operators with statistically significant consistency.

The cognitive challenges described in Chapter 3 -- automation bias, anchoring, alert fatigue -- are not fixed properties of human cognition. They are properties of the interaction between human cognition and information design. A well-designed presentation format can reduce anchoring. A poorly designed one can amplify it. The format is not a cosmetic layer applied after the engineering is done. It is a load-bearing element of the system architecture.

This chapter presents four evidence-based frameworks for context presentation at the AI-human seam, with specific guidance on how to apply each one in operational AI systems.

## The SBAR Framework

SBAR -- Situation, Background, Assessment, Recommendation -- is a structured communication framework developed by the **United States Navy** for use on nuclear submarines, where communication errors between crew members could have catastrophic consequences. The framework was subsequently adapted for healthcare by **Kaiser Permanente** in the early 2000s, where it became the basis for clinical handoff communication across thousands of hospitals.

### The Evidence

The adoption of SBAR in healthcare, facilitated through the TeamSTEPPS (Team Strategies and Tools to Enhance Performance and Patient Safety) program developed by the Department of Defense and the Agency for Healthcare Research and Quality, produced one of the most dramatic improvements in communication quality ever documented in a controlled study. Before TeamSTEPPS implementation, observers rated the adequacy of nurse-to-physician communication in the study population at **4.8%**. After implementation -- with SBAR as the core communication structure -- adequacy ratings rose to **100%**.

The magnitude of this improvement demands explanation. The information available to the nurses did not change. Their clinical knowledge did not change. What changed was the structure in which they communicated. SBAR gave them a framework that ensured they included all critical information, presented it in a predictable order, and made an explicit distinction between observation (Situation, Background) and interpretation (Assessment, Recommendation).

### SBAR Adapted for AI Agent Output

The same principles apply directly to how an AI agent communicates with a human operator. An unstructured output -- a wall of text summarizing an investigation -- forces the operator to extract structure, which is exactly the kind of cognitive work that leads to missed information and anchoring on the first pattern recognized. A structured output reduces cognitive load and ensures completeness.

For operational AI systems, SBAR can be adapted into a six-element framework:

| Element | SBAR Equivalent | Content | Purpose |
|---------|----------------|---------|---------|
| **WHAT HAPPENED** | Situation | Concise statement of the event or condition detected | Orient the operator to the current state |
| **WHAT I TRIED** | Background | Actions the AI agent took during investigation or initial remediation | Provide context on what is already known and ruled out |
| **WHAT I RECOMMEND** | Recommendation | Specific recommended action with expected outcome | Give the operator a clear decision point |
| **RISK LEVEL** | Assessment | Severity classification with brief justification | Calibrate the urgency of the operator's response |
| **COST OF INACTION** | (Extension) | What happens if no action is taken, with estimated timeline | Counter the status quo bias and create urgency where warranted |
| **EVIDENCE** | (Extension) | Links to logs, metrics, traces, and knowledge base articles | Enable independent verification and deep investigation |

The extensions beyond standard SBAR -- Cost of Inaction and Evidence -- address specific challenges of AI-human interaction. Cost of Inaction counters the natural human tendency toward inaction when faced with uncertainty (the status quo bias). Evidence addresses automation bias by providing the raw material for independent verification, rather than asking the operator to trust the AI's synthesis alone.

### Practical Example

Consider an AI agent that has detected a potential security incident. Here is the same information presented in three formats:

**Format 1: Raw Dump**

```
Alert ID: SEC-2026-04891. Source: SIEM correlation rule CR-142. 
Timestamp: 2026-04-11T03:42:17Z. Multiple failed SSH login attempts 
detected from IP 198.51.100.42 targeting hosts prod-web-01 through 
prod-web-08. Total attempts: 847 over 23 minutes. Source IP 
geolocation: São Paulo, Brazil. No successful authentications. 
Rate: ~37 attempts/minute. Pattern consistent with credential stuffing. 
Threat intel: IP not in known blocklists. Previous activity from 
this IP: none in last 90 days. Host vulnerability scan (last 7 days): 
prod-web-03 has unpatched OpenSSH (CVE-2024-6387). Current SSH 
configuration: password authentication enabled on all hosts. 
Fail2ban status: active, threshold set at 10 failures/5 minutes, 
current ban list does not include source IP due to distributed 
timing pattern...
```

**Format 2: SBAR Structure**

```
WHAT HAPPENED: Credential stuffing attack in progress against 8 
production web servers from a single IP (198.51.100.42, São Paulo).

WHAT I TRIED: Queried threat intel (IP not in known blocklists), 
checked for successful auths (none found), reviewed SSH configs 
(password auth enabled on all 8 hosts), checked fail2ban (active 
but not triggered due to distributed timing).

WHAT I RECOMMEND: Block IP 198.51.100.42 at the network firewall 
and disable password-based SSH authentication on all production hosts.

RISK LEVEL: Medium. No breach detected yet, but prod-web-03 has 
an unpatched OpenSSH vulnerability (CVE-2024-6387) that could be 
exploited if the attacker shifts tactics.

COST OF INACTION: Continued brute-force attempts with potential 
exploitation of CVE-2024-6387 on prod-web-03. If the vulnerability 
is exploited, the attacker gains shell access to a production server.

EVIDENCE: [SIEM Alert] [SSH Logs] [Vuln Scan Report] [Threat Intel Query]
```

**Format 3: Progressive Disclosure (detailed in the next section)**

```
Layer 1 (5-second glance):
  🟡 MEDIUM | Credential stuffing on 8 prod web servers | 
  Recommend: Block source IP + disable password auth

Layer 2 (30-second assessment):
  [Full SBAR as above]

Layer 3 (deep dive):
  [Complete evidence chain with log excerpts, CVE details, 
  network topology, historical context]
```

The raw dump contains all the same information as the SBAR format, but it forces the operator to perform the cognitive work of structuring it. Under the time pressure and alert volume typical of security operations, this cognitive work is exactly what gets skipped -- and its omission is what leads to missed context and poor decisions.

## The Klein Recognition-Primed Decision Model

Gary Klein's Recognition-Primed Decision (RPD) model, developed through field studies of firefighters, military commanders, and intensive care nurses, fundamentally challenges the classical model of decision-making as a process of comparing alternatives.

### The Evidence

Klein's research found that **78% of expert decisions were made in under one minute**, and the process was not comparison-based but recognition-based. Experts did not generate a list of options, evaluate each against criteria, and select the best. Instead, they recognized the current situation as similar to a previously encountered pattern, retrieved the action that worked in that pattern, mentally simulated whether it would work in the current situation, and either executed it or modified it.

This has a direct and counterintuitive design implication: **presenting multiple options to an expert operator may degrade decision quality rather than improve it.** The expert's cognitive process is optimized for evaluating a single option against the situation, not for comparing options against each other. A system that presents three possible root causes with pros and cons for each is fighting the expert's natural decision process. A system that presents the single most likely root cause with supporting evidence and a recommended action is working with it.

### Design Implication for AI Agents

Present the AI's **single recommended action first**, with supporting evidence. Make alternative explanations available on demand (progressive disclosure, discussed below), but do not force the expert to process them before evaluating the primary recommendation.

This does not mean hiding alternatives. It means structuring the presentation so that the operator's first cognitive engagement is with the most likely hypothesis, which is the engagement pattern that matches how experts actually think. If the primary recommendation does not match the operator's pattern recognition -- if something feels wrong -- the operator will seek alternatives. The system should make that easy. But it should not force it as the default path.

> **Key distinction:** For novice operators, presenting alternatives may be valuable because novices lack the pattern library that enables recognition-primed decisions. The optimal presentation format depends on the operator's expertise level -- another argument for adaptive interfaces that adjust to the user.

## Time Pressure and Decision Quality

The interaction between time pressure and AI assistance is more nuanced than "faster is better" or "slower is safer." Research by Swaroop et al. at Harvard (2023) found that different types of AI assistance have different accuracy-time tradeoffs, and the optimal type of assistance depends on the time available for the decision.

Under low time pressure, operators benefited most from AI assistance that provided explanations and supporting evidence -- the kind of assistance that enables analytical reasoning and independent verification. Under high time pressure, operators benefited most from simple, direct recommendations -- the kind of assistance that supports rapid pattern matching.

More concerning, the research found that under time pressure, **decisions became riskier and overreliance on AI increased**. Operators under time pressure were more likely to accept the AI's recommendation without evaluation, more likely to choose the riskier option when the AI suggested it, and less likely to notice errors in the AI's reasoning.

### Design Implication

The presentation format should adapt to the urgency of the situation:

- **Low urgency (minutes to hours):** Present full SBAR with evidence links, encourage independent verification, apply cognitive forcing functions (see Chapter 3).
- **Moderate urgency (seconds to minutes):** Present SBAR summary with single recommended action, make evidence available but do not require review.
- **High urgency (immediate):** Present action and severity only, with one-click execution. Log the decision for post-hoc review.

This maps directly to the Progressive Disclosure framework discussed next.

## Progressive Disclosure

Progressive disclosure is an information architecture principle that organizes content into layers of increasing detail, allowing the user to access the level of detail they need without being overwhelmed by the level they do not. In operational AI systems, it is the primary mechanism for supporting both the rapid pattern-matching of experts and the thorough analysis of novices within a single interface.

### The Three Layers

**Layer 1: The 5-Second Glance**

This is what the operator sees when they first look at the screen, scan a notification, or glance at a dashboard. It must communicate three things in five seconds or less:

- **Severity** (visual indicator: color, icon, or categorical label)
- **Summary** (one sentence: what happened and what is at stake)
- **Recommended action** (one phrase: what to do)

Layer 1 supports the expert's recognition-primed decision process. An experienced operator scanning Layer 1 either recognizes the pattern and acts, or does not recognize it and drills down. There is no wasted cognitive effort on detail that is not needed for the initial recognition.

Example:
```
🔴 CRITICAL | Database primary failover detected, replication lag 
increasing | Recommend: Promote replica db-replica-02 to primary
```

**Layer 2: The 30-Second Assessment**

This is the SBAR brief with confidence levels. It provides enough context for the operator to evaluate the AI's recommendation, ask clarifying questions, or form an alternative hypothesis. It is the layer where the operator transitions from pattern recognition to analytical reasoning.

Layer 2 includes:
- Full SBAR structure (What Happened, What I Tried, What I Recommend, Risk Level, Cost of Inaction)
- AI confidence level (discussed in the next section)
- Key metrics and their trends
- Relevant recent changes or events

**Layer 3: The Deep Dive**

This is the full evidence chain -- raw logs, metrics timeseries, configuration diffs, knowledge base articles, historical incident records, and the AI's reasoning chain. It is used for post-incident review, for cases where the operator disagrees with the AI's assessment, or for novel situations that do not match any known pattern.

Layer 3 is also where evidence linking (discussed below) provides its value, allowing the operator to trace the AI's conclusions back to specific data points.

### Why Three Layers

Three is not arbitrary. Cognitive load research consistently shows that humans can effectively process 3-5 chunks of information at a time (Miller, 1956; Cowan, 2001). Three layers map to three distinct cognitive modes:

| Layer | Time | Cognitive Mode | Decision Type | User State |
|-------|------|----------------|---------------|------------|
| Layer 1 | 5 seconds | Pattern recognition | Act or investigate further | Scanning, triaging |
| Layer 2 | 30 seconds | Analytical reasoning | Approve, modify, or reject recommendation | Focused evaluation |
| Layer 3 | Minutes to hours | Deep analysis | Root cause investigation, post-incident review | Deliberate investigation |

## Confidence Communication

How an AI agent communicates its confidence in a recommendation is one of the most consequential and most frequently mishandled aspects of context presentation.

### The Problem with Raw Probabilities

The intuitive approach -- presenting a numerical probability ("87% confidence this is a credential stuffing attack") -- is worse than useless for most operators. Research consistently shows that:

- Humans miscalibrate probabilities, overweighting low probabilities and underweighting high ones (Kahneman & Tversky, 1979).
- Numerical probabilities create false precision. "87% confidence" implies a level of calibration that no current LLM possesses.
- Different operators interpret the same probability differently. "87%" might feel near-certain to one operator and uncomfortably uncertain to another.

### Categorical Confidence with Calibration

A more effective approach uses categorical labels mapped to defined probability ranges and operational implications:

| Category | Probability Range | Operational Implication |
|----------|------------------|------------------------|
| **Confirmed** | >95% | Evidence is conclusive; proceed with recommended action |
| **High confidence** | 80-95% | Strong evidence; recommendation is likely correct but verify key assumptions |
| **Moderate confidence** | 60-80% | Supporting evidence exists but alternative explanations are plausible; investigate before acting |
| **Low confidence** | 40-60% | Evidence is ambiguous; treat as a lead for investigation, not a basis for action |
| **Speculative** | <40% | Insufficient evidence; further investigation required before any action |

The value of categorical labels is not precision -- it is calibration of operator behavior. "High confidence" communicates not just a probability but an expected response: verify key assumptions, then act. "Low confidence" communicates a different expected response: investigate further. The label guides behavior in a way that a number does not.

### Uncertainty Visualization

Research by Reyes et al. (2025) found that presenting uncertainty visualizations -- graphical representations of the AI's confidence distribution rather than a single point estimate -- **enhanced appropriate trust for 58% of participants**. Operators who saw uncertainty visualizations were better at calibrating their trust: trusting high-confidence outputs more and low-confidence outputs less, compared to operators who received only point estimates.

A complementary study at ACM FAccT (2025) found that **distance-based confidence scores** -- metrics that communicate how similar the current situation is to the training data the AI was calibrated on -- yielded **8.2% higher correct decisions** compared to traditional confidence scores. Distance-based scores help operators understand not just how confident the AI is, but how relevant its confidence calibration is to the current situation.

> **Key insight:** The goal of confidence communication is not to convey the AI's internal state accurately. It is to calibrate the operator's behavior appropriately. A confidence format that causes operators to verify high-confidence recommendations and investigate low-confidence ones is succeeding, regardless of how precisely it maps to the model's actual probability distribution.

## Evidence Linking and Explainability

The final component of context presentation is evidence linking: connecting the AI's conclusions and recommendations to the specific data points that support them. This serves two functions: it enables independent verification (countering automation bias), and it provides the raw material for the operator to construct their own situation awareness rather than relying entirely on the AI's synthesis.

### RAG Citations and Inline References

For AI agents using retrieval-augmented generation (RAG), the most straightforward form of evidence linking is inline citations: marking each claim in the AI's output with a reference to the source document, log entry, or metric that supports it. This is the same approach used in academic writing, adapted for operational context.

Example:
```
Root cause assessment: The connection pool exhaustion on db-primary-01 
[1] was triggered by the deployment of v2.4.7 at 14:32 UTC [2], which 
introduced a connection leak in the user authentication module [3]. 
Connection count increased from baseline 45 to maximum 500 over 
23 minutes [4], causing cascading timeouts in downstream services [5].

Sources:
[1] CloudWatch metric: db-primary-01 active connections (14:00-15:00 UTC)
[2] Deployment log: v2.4.7 release record
[3] Git diff: commit a3f7c2e, file auth/connection_pool.py, lines 142-158
[4] Connection pool metrics dashboard (link)
[5] Service dependency map with error propagation trace (link)
```

### Progressive Disclosure of Reasoning Chain

For more complex analyses, the AI's reasoning chain itself can be presented using progressive disclosure:

- **Layer 1:** Conclusion and recommended action (no reasoning).
- **Layer 2:** Key reasoning steps -- the 3-4 most important logical connections between evidence and conclusion.
- **Layer 3:** Full reasoning chain, including hypotheses that were considered and rejected, with evidence for and against each.

This approach respects the expert's recognition-primed decision process (Layer 1 is sufficient if the pattern is familiar) while providing the full audit trail for cases that require deeper analysis or post-incident review.

### The DARPA XAI Program

The Defense Advanced Research Projects Agency (DARPA) invested **$75 million** in its Explainable AI (XAI) program, which ran from 2017 to 2021 and tested multiple approaches to making AI systems' reasoning transparent to human operators. The key finding for operational context: **example-based explanations were the most effective** at improving human decision-making.

Rather than explaining the AI's internal logic ("the neural network assigned weight 0.73 to feature X"), example-based explanations present similar cases from the past and their outcomes: "This situation is similar to Incident INC-2025-3847, which was caused by a DNS misconfiguration and resolved by flushing the DNS cache. The resolution took 12 minutes and no customer impact was reported."

Example-based explanations work because they align with the recognition-primed decision model: they help the operator match the current situation to a known pattern, which is the cognitive process experts actually use.

## Putting It All Together

Effective context presentation at the AI-human seam integrates all four frameworks:

1. **Structure** the output using SBAR to ensure completeness and predictability.
2. **Prioritize** the recommended action first, consistent with the RPD model, and make alternatives available on demand.
3. **Layer** the information using progressive disclosure so that each operator can engage at the depth appropriate to their expertise and the situation's urgency.
4. **Calibrate** confidence communication using categorical labels with operational implications, not raw probabilities.
5. **Link** conclusions to evidence using inline citations and example-based explanations.

These are not independent design choices. They interact: SBAR provides the structure for Layer 2. The RPD model determines what goes in Layer 1. Confidence communication determines how the operator engages with Layers 1 and 2. Evidence linking populates Layer 3.

The result, when implemented cohesively, is a presentation format that:

- Supports fast pattern-matching for experienced operators (Layer 1, RPD alignment)
- Enables analytical evaluation when needed (Layer 2, SBAR structure)
- Provides full audit trail for post-hoc review and learning (Layer 3, evidence linking)
- Calibrates operator trust appropriately (confidence communication)
- Reduces automation bias by making independent verification easy (evidence linking)
- Reduces anchoring by presenting data before interpretation when time permits (SBAR ordering)

The next chapter examines how trust between human operators and AI agents develops, calibrates, and -- when mismanaged -- collapses.
