# Chapter 3: Five Structural Patterns

Not all AI-human handoffs are alike. The appropriate pattern depends on the risk of the action, the time available, and the expertise of the operator. A security analyst triaging thousands of alerts per day needs a fundamentally different interaction pattern than a site reliability engineer approving a database failover. An IT service desk agent resolving password resets operates under different constraints than a compliance officer reviewing AI-generated audit findings.

This chapter defines five structural patterns that cover the full spectrum of human-AI interaction in operations, maps them to established automation taxonomies, and provides a decision framework for selecting the right pattern for a given operational context.

## The Sheridan-Verplank Foundation

Before examining the patterns, it is worth grounding them in the taxonomy that has structured automation research for nearly five decades. In 1978, Thomas Sheridan and William Verplank proposed a 10-level scale of automation, ranging from full human control to full machine autonomy. Their framework remains the most widely cited reference point for automation design, and every modern framework (including those from PagerDuty, the Cloud Security Alliance, and NIST) can be mapped back to it.

| Level | Description | Operational Example |
|-------|------------|---------------------|
| 1 | The computer offers no assistance; the human does everything | Manual log analysis with grep and text editors |
| 2 | The computer offers a complete set of action alternatives | AI lists all possible root causes for an alert |
| 3 | The computer narrows the selection down to a few alternatives | AI identifies the 3 most likely root causes with supporting evidence |
| 4 | The computer suggests one alternative | AI recommends a specific remediation action |
| 5 | The computer suggests one alternative and executes it if the human approves | AI recommends rolling back a deployment and pre-stages the rollback command |
| 6 | The computer allows the human a restricted time to veto before automatic execution | AI will auto-scale infrastructure in 60 seconds unless the operator cancels |
| 7 | The computer executes automatically, then informs the human | AI auto-remediates a known issue and posts a summary to the incident channel |
| 8 | The computer executes automatically and informs the human only if asked | AI silently handles routine certificate renewals; status available in dashboard |
| 9 | The computer executes automatically and informs the human only if it decides to | AI resolves issues autonomously and only alerts humans for novel failure modes |
| 10 | The computer decides everything, acts autonomously, ignores the human | Fully autonomous system with no human interface (rarely appropriate in operations) |

The five patterns described below map to clusters within this scale, but they are defined by operational characteristics rather than by abstract automation levels. They answer the practitioner's question: "How should my AI agent interact with my human operators for this specific type of work?"

## Pattern 1: Recommend and Wait

**Sheridan-Verplank Levels 4-5 | The AI recommends; the human decides and acts.**

In this pattern, the AI agent analyzes the situation, gathers evidence, and presents a single recommended action to the human operator. The agent then waits. No action is taken until the human explicitly approves, modifies, or rejects the recommendation.

This is the safest pattern and the appropriate default for any action where the consequences of an error are significant and irreversible.

### PagerDuty SRE Agent

PagerDuty's SRE Agent exemplifies this pattern in production incident response. When an alert fires, the agent automatically gathers context: it pulls recent deployment history, queries monitoring dashboards, checks for correlated alerts across services, and examines relevant runbooks. It then presents the on-call engineer with a synthesized assessment and a recommended action, for example: "Roll back deployment v2.4.7 to v2.4.6. Evidence: error rate increased 340% within 8 minutes of deployment, correlated with this commit changing the database connection pooling configuration."

The engineer reviews the recommendation, examines the evidence, and either approves the rollback or investigates further. The agent does not execute the rollback autonomously. This is deliberate: production rollbacks can have cascading effects, and the engineer's contextual knowledge (awareness of an ongoing data migration, knowledge that v2.4.6 had its own issues, recognition that the error rate spike might be a measurement artifact) is essential to the decision.

### Johns Hopkins Sepsis AI

In healthcare, Johns Hopkins deployed an AI system for early sepsis detection that operates squarely in the Recommend and Wait pattern. The system continuously monitors patient vitals and laboratory results, using machine learning to identify the subtle early indicators of sepsis that human clinicians frequently miss. When the system detects a high-probability case, it alerts the clinical team with a recommended treatment protocol.

The results, published in *Nature Medicine* in 2022, are striking with an honest asterisk: the system (TREWS) caught 82% of sepsis cases, and mortality fell 18.7% in relative terms (3.3 percentage points absolute), but specifically among patients whose alert a provider confirmed within three hours, compared to those confirmed later. The benefit lives in the speed of the human response to the recommendation, which is precisely this pattern's point. The system does not administer treatment. It does not order labs. It recommends, and the clinical team, with their knowledge of the patient's history, comorbidities, and current treatment plan, decides.

> **Key insight:** Recommend and Wait is no mere conservative fallback: it is a high-performance pattern when the AI's analysis is genuinely valuable but the human's contextual knowledge is essential to the final decision. The mortality reduction at Johns Hopkins was achieved entirely through better recommendations acted on faster, not through autonomous action.

### When to Use This Pattern

- The action is irreversible or expensive to reverse (production deployments, security blocks, patient treatments)
- The human operator has domain expertise that the AI cannot fully capture (organizational context, recent conversations, political considerations)
- Regulatory or compliance requirements mandate human approval
- The AI system is newly deployed and trust has not yet been established

## Pattern 2: Triage and Escalate

**Sheridan-Verplank Levels 3-5 | The AI filters, prioritizes, and routes; the human handles what remains.**

In this pattern, the AI agent processes a high-volume stream of inputs (alerts, tickets, requests) and performs initial triage. It classifies items by severity and type, filters out noise, enriches items with relevant context, and routes them to the appropriate human operator or team. The human works from a curated, prioritized queue rather than a raw feed.

This pattern is most valuable in environments where the volume of inputs overwhelms human processing capacity.

### Splunk Agentic SOC

The scale of the problem in security operations is staggering. Vectra AI's 2026 survey of 1,450 SOC practitioners puts the average at 2,992 security alerts per day, of which 63% go entirely unaddressed. (The alert count has actually been falling year over year as detection stacks consolidate; the unaddressed share has not moved much.) Industry surveys put manual investigation time at roughly 70 minutes per alert actually examined. The arithmetic is brutal: even with a full team, the majority of alerts receive no human attention at all.

Splunk's Agentic SOC addresses this by deploying AI agents that perform the initial investigation autonomously. When an alert fires, the agent queries relevant data sources (SIEM logs, endpoint telemetry, threat intelligence feeds), correlates the alert with known attack patterns, checks for false positive indicators, and produces a structured investigation summary. Splunk's own claim is that investigations which took analysts the better part of an hour now complete in seconds; treat the precise ratio as marketing, but the order-of-magnitude compression of first-pass triage is real across vendors.

The agent does not decide whether the alert represents a real threat. It presents the analyst with a structured brief (including the alert details, correlated evidence, historical context, and a preliminary assessment) and the analyst makes the determination. But critically, the agent also assigns a priority score, ensuring that the most likely genuine threats surface first. Analysts work from the top of a prioritized queue rather than from a chronological feed.

### ServiceNow AI Agents

ServiceNow has taken the Triage and Escalate pattern to enterprise scale with its Now Assist platform, shipping more than 300 pre-built AI agent skills and agentic workflows. In IT service management, AI agents automatically classify incoming tickets, extract key information, identify relevant knowledge base articles, and route tickets to the appropriate resolution group.

For straightforward requests (password resets, access provisioning, standard software installations) the agent may resolve the ticket autonomously (shifting into an Execute and Report pattern). For complex or ambiguous issues, it enriches the ticket with diagnostic information and escalates to a human agent who receives a pre-investigated case rather than a raw complaint.

### When to Use This Pattern

- Input volume exceeds human processing capacity (thousands of alerts or tickets per day)
- The majority of inputs are routine, false positive, or low-priority
- The cost of delayed response to high-priority items is significant
- Human expertise is the bottleneck and must be focused on the highest-value work

## Pattern 3: Execute and Report

**Sheridan-Verplank Levels 7-8 | The AI acts autonomously and informs the human afterward.**

In this pattern, the AI agent takes action without waiting for human approval, then reports what it did. The human reviews the action after the fact and intervenes only if something went wrong. This pattern is appropriate only when three conditions are met: the action is well-understood, the action is reversible, and the cost of delay exceeds the cost of occasional errors.

### Dynatrace Davis AI

Dynatrace's Davis AI engine operates at the Execute and Report level for a defined set of remediation actions. When Davis detects a performance anomaly (say, a memory leak causing response time degradation in a microservice) it can automatically trigger a remediation action, such as disabling a problematic feature flag, scaling up a resource, or restarting a container.

The efficiency gains around Davis are quantifiable, with an attribution caveat: the widely cited 56% faster mean time to resolution comes from an IDC study (commissioned by Dynatrace) and describes AI-assisted investigation with humans in the loop, not the autonomous remediation itself, which Dynatrace markets separately without an attached percentage. What the autonomous tier verifiably provides: the system executes the remediation, logs the action with full context (what was detected, what action was taken, what the expected and actual outcomes were), and notifies the operations team.

Critically, Davis AI does not auto-remediate everything. The system maintains an explicit list of approved autonomous actions, each with defined rollback procedures. Actions outside this list are escalated to the Recommend and Wait pattern. This bounded autonomy (executing autonomously within defined guardrails, escalating outside them) is what makes the pattern safe at Sheridan Level 7 rather than reckless at Level 10.

### When to Use This Pattern

- The action is well-understood and has been successfully executed many times before
- The action is reversible within an acceptable time window
- The cost of delay (human approval latency) exceeds the expected cost of occasional errors
- Comprehensive logging and rollback mechanisms are in place
- The scope of autonomous action is explicitly bounded and regularly reviewed

> **Key distinction:** Execute and Report is not "set and forget." It requires more engineering investment than Recommend and Wait (not less) because the system must include monitoring of its own actions, automated rollback capabilities, and clear escalation paths for when autonomous remediation fails or produces unexpected results.

## Pattern 4: Draft and Refine

**Sheridan-Verplank Level 5 (adapted) | The AI produces a complete artifact; the human reviews, edits, and approves.**

This pattern differs from Recommend and Wait in a subtle but important way. Rather than recommending an action, the AI produces a complete work product (a code review, an incident report, a runbook update, a configuration change) that the human then refines. The human's role shifts from decision-maker to editor.

### GitHub Copilot Code Review

GitHub Copilot's code review capability provides the most scaled example of this pattern in production. As of early 2026, Copilot handles 1 in 5 code reviews on the platform, with more than 60 million reviews processed across over 12,000 organizations.

The interaction pattern is instructive. When a pull request is submitted, Copilot analyzes the changes, identifies potential issues (bugs, security vulnerabilities, style violations, performance concerns), and generates review comments with specific suggestions. The developer (or the pull request author) reviews these comments, accepts the ones that are valid, dismisses the ones that are not, and may engage in a back-and-forth with Copilot to refine specific suggestions.

WEX, a financial technology company, reported an approximately 30% productivity lift after adopting Copilot broadly (agent mode, coding agent, and code review together), not because the AI wrote more code, but in significant part because the review cycle was faster and more consistent. The AI handled the routine checks (style, common bug patterns, documentation gaps), freeing human reviewers to focus on architectural decisions, business logic correctness, and edge cases that require domain expertise.

### When to Use This Pattern

- The output is a complex artifact (code, documentation, configuration) rather than a binary decision
- Quality depends on iterative refinement rather than a single correct answer
- The human's expertise is in evaluation and editing rather than generation from scratch
- The volume of artifacts exceeds what humans can produce from scratch but not what they can review

## Pattern 5: Graduated Autonomy

**Dynamic across Sheridan-Verplank levels | The AI's autonomy level adjusts based on context, confidence, and track record.**

This is the meta-pattern: rather than fixing a single interaction pattern, the system dynamically adjusts the level of autonomy based on the specific situation. An AI agent might operate at Execute and Report for routine, well-understood issues, shift to Recommend and Wait for novel or high-risk situations, and escalate to full human control when it encounters something outside its training distribution.

### PagerDuty's Two Axes: Incident Tiers and Execution Modes

PagerDuty's SRE Agent implements graduated autonomy along two axes. The first is a classification of incidents by who should lead: routine, well-understood incidents the agent can handle largely on its own; complex incidents handled collaboratively, with the agent investigating and the engineer directing; and high-stakes or novel incidents that remain human-led with the agent in a supporting role. The second axis is the execution mode: in Review mode the agent proposes every action and waits for approval, while Autonomous mode (the direction PagerDuty is building toward for well-bounded actions) executes and reports.

The assignment is not static, and this is the instructive part. The intended trajectory is that an action class starts in Review mode and earns autonomy as a track record accumulates and the team's trust in it is validated, deliberately, by the humans who own the system, not by a counter ticking past a threshold. Conversely, autonomy can be withdrawn: during a change freeze, after a major incident, or when confidence in a class of recommendations drops, an autonomous action class is downshifted back to Review.

### CSA Autonomy Levels

The Cloud Security Alliance published its AI Autonomy Levels framework in January 2026, defining six levels specifically for AI agents in security operations:

| CSA Level | Name | Description | Key Characteristic |
|-----------|------|-------------|--------------------|
| 0 | No AI | Fully manual operations | Baseline |
| 1 | Assistive AI | AI provides information; human decides and acts | Copilot mode |
| 2 | Supervised Autonomy | AI recommends actions; human approves | Recommend and Wait |
| 3 | Conditional Autonomy | AI acts within defined boundaries; human handles exceptions | Bounded Execute and Report |
| 4 | High Autonomy | AI acts independently for most tasks; human oversees | Execute and Report with monitoring |
| 5 | Full Autonomy | AI operates independently with minimal human involvement | Rarely appropriate for security |

The most useful idea to take from the CSA's discussion is **dynamic downshifting**: the principle that an AI agent should automatically reduce its autonomy level when it encounters uncertainty, novel situations, or conditions outside its training distribution. (The CSA article raises this as an open design question rather than a named framework component; this booklet recommends adopting it as a design rule.) A Level 4 agent that encounters a previously unseen attack pattern should downshift to Level 2, presenting its analysis and asking for human guidance rather than attempting autonomous remediation of something it does not understand.

> **Key insight:** Graduated autonomy is not about achieving the highest possible autonomy level but about achieving the right one for each specific decision at each specific moment. The best systems are not the most autonomous; they are the ones that know when to ask for help.

## Pattern Selection Framework

Choosing the right pattern requires evaluating four dimensions of the operational context:

| Pattern | Risk Tolerance | Time Sensitivity | Human Expertise Required | Reversibility |
|---------|---------------|-------------------|--------------------------|---------------|
| Recommend and Wait | Low (high-consequence actions) | Low to moderate (minutes to hours available) | High (contextual judgment essential) | Low (irreversible or costly to reverse) |
| Triage and Escalate | Moderate (prioritization errors are recoverable) | High (volume demands fast processing) | Moderate (expertise needed for escalated items) | Moderate (routing errors delay but don't prevent resolution) |
| Execute and Report | Moderate to high (accepts occasional errors) | Very high (delay cost exceeds error cost) | Low (actions are well-understood and procedural) | High (actions must be reversible) |
| Draft and Refine | Moderate (editing catches most errors) | Moderate (review cycle adds latency) | High (evaluation requires deep expertise) | High (artifacts can be revised before deployment) |
| Graduated Autonomy | Variable (adapts to context) | Variable (adapts to urgency) | Variable (adjusts to availability) | Variable (matches autonomy to reversibility) |

## Reference Frameworks

The five patterns described in this chapter draw on and are compatible with several established frameworks that practitioners should be aware of:

### Parasuraman, Sheridan, and Wickens (2000)

The four-stage model extends the original Sheridan-Verplank scale by recognizing that automation can be applied independently to four stages of human information processing: **information acquisition**, **information analysis**, **decision selection**, and **action implementation**. A system might be highly automated in information acquisition (automatically gathering logs and metrics) while remaining fully manual in decision selection (the human decides what to do). This decomposition is essential for designing nuanced interaction patterns that automate the right stages for the right reasons.

### NIST AI Risk Management Framework

NIST AI RMF provides a structured approach to identifying and mitigating risks in AI systems, organized around four functions: Govern, Map, Measure, and Manage. It does not prescribe specific interaction patterns but provides the risk assessment methodology that should inform pattern selection.

### Microsoft Human-AI Experience (HAX) Guidelines

Microsoft's 18 HAX Guidelines address the full lifecycle of human-AI interaction, from initial calibration ("Make clear how well the system can do what it can do") to error handling ("Support efficient correction") to long-term trust ("Encourage granular feedback"). They are particularly useful for the UX layer of seam design.

### Google PAIR (People + AI Research)

Google's PAIR Guidebook provides design guidance organized around the concept of "AI-first" design: starting from the AI's capabilities and limitations rather than from a traditional UX workflow. Its emphasis on mental models (helping users understand what the AI can and cannot do) aligns directly with the situation awareness concerns discussed in Chapter 1.

## Choosing Your Starting Point

For organizations beginning to deploy AI agents in operations, two practical recommendations:

**Start with Recommend and Wait.** It is the safest pattern, it builds the data needed to evaluate the AI's performance, and it establishes the trust foundation required for higher autonomy levels. Organizations that skip directly to Execute and Report without first validating the AI's recommendations in a Recommend and Wait mode are taking unnecessary risk.

**Design for Graduated Autonomy from the beginning.** Even if your initial deployment is purely Recommend and Wait, architect the system so that the autonomy level can be adjusted per action type without a redesign. Define the criteria for promotion and demotion. Instrument the system to track recommendation acceptance rates, override patterns, and outcome quality. The data you collect during Recommend and Wait is the foundation for every subsequent autonomy decision.

## From Levels to Teammates

An honest note on the scaffolding this chapter is built on. The Sheridan-Verplank scale and its descendants treat automation design as an allocation problem: list the functions, decide which ones the machine gets. That framing is nearly fifty years old, and the researchers who spent careers studying automated systems in the field spent the last twenty of those years arguing against it.

[Dekker and Woods](https://link.springer.com/article/10.1007/s101110200022) made the case bluntly in 2002 ("MABA-MABA or Abracadabra?"): automation does not *substitute* machine work for human work in fixed quantities. It transforms the human's work into something new, usually coordination and exception handling, and the interesting design questions live in that transformation, not in the allocation table. Klein, Woods, Bradshaw, Hoffman, and Feltovich followed in 2004 with [ten challenges for making automation a "team player"](https://ieeexplore.ieee.org/document/1363742/): can the machine and the human maintain common ground about what is happening? Is the machine's status and intent observable? Is it *directable* mid-task? Can it negotiate goals rather than just execute them? The National Academies' 2022 report on [human-AI teaming](https://nap.nationalacademies.org/catalog/26355/human-ai-teaming-state-of-the-art-and-research-needs) consolidated the shift: the research frontier treats the human and the AI as a team to be designed, not a scale to be set.

So why does this booklet still teach levels? Because levels are the right entry-level tool: they force the first necessary conversation (what may this system do without a person?) and they map cleanly onto risk, reversibility, and regulation. But notice that the best material in the coming chapters is already teaming material in disguise. SBAR is a common-ground protocol. Confidence communication is mutual predictability. The kill switch is directability in its bluntest form. Where a pattern in this chapter feels too static for your system (an agent that plans, acts, and re-plans does not sit still on one level), the teaming lens is the upgrade path: ask not "what level is this agent at" but "what does this agent need to tell my operator, and what does my operator need to be able to do to it, for the two of them to stay coordinated?"

<div class="demo-link">
<span class="demo-link-label">Try it yourself</span>
<a href="https://demos.barcik.training/demos/operators-dilemma.html#act5">The Operator's Dilemma, Act 5</a>: design the seam for a change-management agent yourself (autonomy level, context format, confidence display, safeguards) and get a critique of your choices.
</div>

The structural patterns define what the system does. The next chapter examines what the human does (and more importantly, what the human fails to do) when interacting with these patterns.
