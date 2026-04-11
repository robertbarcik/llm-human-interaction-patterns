# Chapter 5: Trust Calibration

Trust is not a binary. It is a calibration problem.

When a GenAI engineer deploys an AI agent into an operational environment --- an IT service desk, a network operations center, a clinical workflow --- the central design challenge is not accuracy. It is not latency, cost per token, or even safety in the abstract. The central challenge is ensuring that the humans who work alongside the agent trust it *exactly as much as it deserves to be trusted*. Not more. Not less. This chapter examines what trust in automated systems actually consists of, how it forms and breaks, and how to design interaction patterns that keep it properly calibrated.

## The Lee & See Framework: Performance, Process, Purpose

The foundational model for understanding trust in automation comes from Lee and See (2004), who synthesized decades of research into a three-dimensional framework. Trust, they argued, is not a single attitude but a composite of three distinct judgments:

- **Performance** --- *Can it do the job?* This dimension captures the operator's assessment of the system's competence: its accuracy, reliability, and consistency across the tasks it is expected to handle.
- **Process** --- *How does it work?* This dimension reflects understanding of the system's internal logic. An operator who can form a reasonable mental model of why the system produces a given output will calibrate trust more effectively than one who treats it as a black box.
- **Purpose** --- *Why was it built this way?* This dimension addresses the operator's belief about the designer's intent. Does the system serve the operator's goals, or does it optimize for something else?

Each dimension can be miscalibrated independently. An operator might trust the system's *performance* based on a run of good outcomes, while having no understanding of its *process* --- a combination that produces brittle trust, vulnerable to collapse at the first unexpected failure. Conversely, an operator who understands the *process* well but has never seen the system handle an edge case may calibrate performance trust too high.

> **Key distinction:** Overtrust leads to automation bias and complacency --- the operator stops checking the system's work, accepts incorrect recommendations, and loses situational awareness. Undertrust leads to disuse and inefficiency --- the operator ignores valid recommendations, duplicates effort, and negates the value of the system entirely. Both failure modes are well-documented in safety-critical domains, and both are present in every AI-augmented operation.

The practical implication for GenAI engineers is that trust calibration requires deliberate design across all three dimensions. Displaying accuracy metrics addresses Performance. Showing reasoning traces addresses Process. Documenting design decisions and optimization targets addresses Purpose. Neglecting any dimension creates a calibration gap.

## Dispositional, Situational, and Learned Trust

Hoff and Bashir (2015) extended the trust literature into a layered model that explains why different operators respond so differently to the same system. Their framework identifies three layers of trust that operate simultaneously:

**Dispositional trust** is the baseline. It reflects an individual's general tendency to trust or distrust automated systems, shaped by personality, culture, age, and prior experience with technology broadly. A 25-year-old engineer who grew up with recommendation algorithms arrives with a different dispositional baseline than a 55-year-old operations manager whose career predates the internet. Neither baseline is inherently better --- both can produce miscalibration.

**Situational trust** is context-dependent. It fluctuates based on the current operating environment: workload, time pressure, perceived risk, and the availability of alternatives. An operator under extreme time pressure in a P1 incident is more likely to accept an AI recommendation without scrutiny --- not because they trust the system more in any stable sense, but because the cost of verification feels higher than the risk of error. This is precisely when automation bias is most dangerous.

**Learned trust** is the layer that accumulates through direct experience with the specific system. It is the most powerful and the most designable. Merritt and Ilgen (2008) demonstrated that trust shifts rapidly from dispositional to learned within the first few interactions --- sometimes in as few as three to five encounters. This finding has profound design implications: the onboarding experience is not merely an introduction. It is the period during which the operator's long-term trust calibration is being established.

For GenAI engineers, this layered model suggests a phased approach to trust design:

1. **During onboarding**, account for dispositional variation. Do not assume a uniform starting point. Some operators will over-rely immediately; others will resist engagement entirely.
2. **During high-pressure operations**, design for situational trust inflation. Add friction --- confirmation steps, mandatory review of reasoning --- precisely when operators are most tempted to skip it.
3. **Across the operational lifecycle**, invest heavily in the learned trust layer. Provide transparent performance data. Surface failures honestly. Make the system's track record visible and navigable.

## First-Person Uncertainty Expression

One of the most actionable findings in recent trust calibration research comes from Kim et al. (FAccT 2024, Microsoft Research, N=404). The study examined how AI systems should communicate uncertainty and found that the *linguistic framing* of uncertainty matters as much as whether uncertainty is communicated at all.

When an AI system expressed uncertainty in the first person --- "I'm not sure, but I think this ticket should be categorized as a network issue" --- participants reported *decreased confidence* in the system's recommendation. At first glance, this seems like a failure. But the critical finding was that this decreased confidence was accompanied by *increased decision accuracy*. Participants who received first-person hedging were more likely to independently evaluate the recommendation, catch errors, and arrive at correct conclusions.

By contrast, general-perspective hedging --- "This might be a network issue" or "There is some uncertainty about the categorization" --- produced a weaker effect. The first-person framing appears to activate a different cognitive process: instead of treating uncertainty as a property of the problem (which the operator may not feel equipped to resolve), the first-person framing treats uncertainty as a property of the *system's judgment*, which the operator recognizes as something they can and should evaluate.

> **Key insight:** Designing an AI agent to say "I'm not sure" is not a concession of weakness. It is a calibration mechanism. The goal is not to maximize the operator's confidence in every recommendation --- it is to maximize the operator's accuracy in the decisions they make based on those recommendations.

The implementation pattern is straightforward but requires discipline:

- When model confidence is below a defined threshold (calibrated to the specific use case), prepend first-person uncertainty markers to the recommendation.
- Use specific language: "I'm not confident about this assessment" rather than vague hedging like "This could potentially be..."
- Pair the uncertainty expression with the system's reasoning, so the operator knows *what* the system is uncertain about and can focus their verification accordingly.

## Track Record Dashboards

A 2024 study of National Weather Service (NWS) forecasters who were integrating AI prediction tools into their workflow found a striking consensus: all forecasters deemed it essential to examine AI predictions for past cases before trusting the system's current output. They did not want to evaluate the AI on a single forecast. They wanted to see its track record --- particularly its failures.

This finding aligns with the learned trust layer in Hoff and Bashir's framework and points to a concrete design requirement: **track record dashboards**. These are not simple accuracy percentages. They are navigable histories that allow operators to build calibrated mental models of where the system succeeds and where it fails.

An effective track record dashboard for an AI-augmented operation should include:

- **Accuracy by action type.** An AI agent that correctly resolves 94% of password reset tickets but only 61% of VPN configuration issues needs those numbers displayed separately. A blended accuracy metric hides the variation that operators need for calibration.
- **Error logs with context.** When the system was wrong, what did it get wrong, and why? Searchable, categorized error histories allow operators to develop pattern recognition for the system's failure modes.
- **Escalation history.** How often does the system escalate to a human, and what happens after escalation? A system that escalates 40% of cases may be well-calibrated; a system that escalates 2% of cases may be dangerously overconfident.
- **Temporal trends.** Is the system improving, degrading, or stable? Operators who can see performance trends develop more sophisticated trust models than those who see only current snapshots.
- **Comparison to human baseline.** Where available, show how the AI's performance compares to unassisted human performance on the same task types. This grounds calibration in operational reality rather than abstract expectations.

## Trust Repair After Failures

Trust in automated systems, once damaged, follows an asymmetric trajectory that every GenAI engineer must account for. De Visser, Pak, and Shaw (2018) documented this pattern rigorously: trust declines rapidly after a failure --- often in a single event --- but recovers slowly, requiring multiple successful interactions to return to pre-failure levels. The asymmetry is not small. A single high-visibility failure can erase weeks or months of earned trust.

This asymmetry creates a design imperative: trust repair must be an active, designed process, not a passive consequence of resumed good performance. Simply continuing to operate correctly after a failure is insufficient. The system --- and the organization around it --- must take explicit repair actions.

Pak and Rovira (2023) investigated what kinds of repair actions are most effective and found a clear hierarchy: **substantive explanations outperform emotional apologies**. When an AI system fails and then provides a clear, technical explanation of why the failure occurred and what has changed to prevent recurrence, trust recovers faster than when the system (or its operators) simply acknowledges the error and expresses regret. This finding should not surprise engineers, but it has direct implications for incident communication design.

Effective trust repair strategies include:

1. **Immediate acknowledgment.** The system should surface its own failures rather than waiting for the operator to discover them. A system that says "I made an error in my previous recommendation --- here is what I got wrong" preserves more trust than one whose errors are discovered independently.
2. **Root cause explanation.** Provide a technically honest explanation of why the failure occurred, at the appropriate level of detail for the operator. "I hallucinated a non-existent API endpoint because the training data contained deprecated documentation" is more repair-effective than "An error occurred."
3. **Remediation evidence.** When possible, show what has changed. If a guardrail has been added, a prompt has been refined, or a knowledge base has been updated, communicate this concretely.
4. **Graduated re-engagement.** After a significant failure, temporarily increase the level of human oversight. This is not punishment --- it is a calibration mechanism that allows the operator to rebuild learned trust through direct observation.

## Behavioral Metrics for Trust Calibration

Designing for trust calibration is only half the problem. The other half is *measuring* whether calibration is actually occurring. Several validated approaches exist.

**The Jian et al. (2000) Trust in Automated Systems scale** is the most widely used self-report instrument, consisting of 12 items that assess trust and distrust as separate constructs. It is useful for periodic assessments but limited by the standard weaknesses of self-report measures: operators may not accurately report their own trust levels, and the act of measurement may alter the thing being measured.

**Behavioral metrics** are more diagnostic for operational settings:

- **Compliance rate** measures how often the operator follows the AI's recommendation. High compliance (>95%) in a system with known error rates suggests overtrust. Low compliance (<50%) for a well-performing system suggests undertrust.
- **Weight of Advice (WoA)** captures not just whether the operator follows the recommendation but how much they adjust their initial judgment toward it. A WoA of 0 means the operator ignores the AI entirely; a WoA of 1 means they adopt its recommendation without modification.
- **Override rates stratified by confidence level** are the most diagnostic metric available. An operator who overrides the AI at the same rate regardless of whether the system reports 60% or 99% confidence is not calibrated --- they are either ignoring the confidence information or treating it as meaningless. A well-calibrated operator overrides more at lower confidence levels and less at higher ones.

A study using the MIMIC-III clinical dataset with an AI clinical decision support system (AI-CDSS) demonstrated the power of this metric: recommendations at the 90--99% confidence level were overridden at a rate of only 1.7%. This suggests strong calibration --- operators trusted high-confidence recommendations appropriately. The critical question then becomes whether the 1.7% of overrides at high confidence captured genuine system errors, which requires tracking override accuracy over time.

> **Key insight:** A well-calibrated trust relationship means the operator questions the AI exactly when the AI is most likely to be wrong. Measuring this requires correlating override decisions with confidence levels and, ultimately, with outcome correctness.

## Trust Calibration Mechanisms: A Summary

The following table consolidates the mechanisms discussed in this chapter into a reference for implementation:

| Mechanism | What It Does | Evidence | Implementation |
|---|---|---|---|
| First-person uncertainty expression | Decreases operator confidence while increasing decision accuracy | Kim et al. (FAccT 2024, N=404) | Prepend "I'm not sure, but..." when model confidence falls below calibrated threshold |
| Track record dashboards | Enables operators to build learned trust through historical performance review | NWS forecasters study (2024); Hoff & Bashir (2015) learned trust layer | Accuracy by action type, searchable error logs, escalation history, temporal trends |
| Graduated autonomy during onboarding | Accounts for rapid shift from dispositional to learned trust | Merritt & Ilgen (2008): trust shifts in first 3--5 interactions | Start with human-in-the-loop for all actions; expand autonomy based on demonstrated calibration |
| Situational friction injection | Counteracts trust inflation under time pressure | Hoff & Bashir (2015) situational trust layer | Mandatory confirmation steps during high-severity incidents; cannot be bypassed |
| Active trust repair | Accelerates trust recovery after failures through substantive explanation | De Visser et al. (2018); Pak & Rovira (2023) | Self-surfaced errors, root cause explanations, remediation evidence, graduated re-engagement |
| Stratified override tracking | Measures whether operators are actually calibrated | Jian et al. (2000) scale; MIMIC-III AI-CDSS study | Track override rates by confidence band; flag operators who override uniformly regardless of confidence |
| Performance-Process-Purpose transparency | Addresses all three dimensions of trust simultaneously | Lee & See (2004) | Accuracy metrics (Performance), reasoning traces (Process), design documentation (Purpose) |

## Designing for Calibration, Not Maximization

The instinct of many engineering teams is to maximize trust --- to build systems so reliable and so impressive that operators trust them completely. This instinct is wrong. Complete trust is miscalibrated trust. It produces automation bias, complacency, and catastrophic failures when the system inevitably encounters a case outside its competence.

The goal is calibration: a dynamic, context-sensitive relationship in which the operator's trust tracks the system's actual reliability across different task types, confidence levels, and operating conditions. Achieving this requires treating trust not as a marketing problem (how do we make people trust our system?) but as a measurement and control problem (how do we ensure that the operator's trust level matches the system's actual capability in this specific context?).

Every design decision in an AI-augmented operation --- from the phrasing of recommendations to the layout of dashboards to the structure of incident reviews --- either helps or hinders trust calibration. There is no neutral ground. The patterns described in this chapter provide a foundation, but calibration is never finished. It must be monitored, measured, and adjusted continuously, because both the system and the humans who use it are always changing.
