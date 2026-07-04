# Chapter 7: Designing for Failure

Every AI agent will fail. The question is not whether, but how, and whether you designed for it.

That is engineering discipline, not pessimism. Bridges are designed for loads they will never carry. Aircraft are designed for engines that will never fail. The value of failure-oriented design is realized not when things go wrong but every day that things go right, because the system's operators know that when failure arrives, it will be contained, visible, and recoverable. This chapter examines the specific failure modes of LLM-based systems in operations, the architectural patterns that contain them, and the kill switches and circuit breakers that keep failures from becoming catastrophes.

## Hallucination as a Structural Feature

The most distinctive failure mode of large language models is hallucination: the generation of plausible, fluent, and confidently stated content that is factually incorrect. It is tempting to treat hallucination as a bug that will be fixed in the next model release. This is a dangerous misconception. Hallucination is a structural feature of how autoregressive language models work. They predict probable next tokens, not truthful ones. The probability distribution they sample from is shaped by training data, not by reality.

The evidence for this structural view is extensive and sobering.

**OpenAI's Whisper** speech recognition system demonstrates that even highly capable models hallucinate at operationally significant rates. Koenecke and colleagues (FAccT 2024) documented an approximately 1% hallucination rate across transcriptions: a number that sounds small until you learn that roughly 40% of those hallucinations were rated as potentially harmful, including invented violence and fabricated medication instructions. The finding matters operationally because Whisper-based tools were already transcribing millions of medical visits at the time: a 1% fabrication rate in a system processing thousands of clinical notes per day means dozens of dangerous fabrications entering records every day.

**Legal practice** has already produced case law on the consequences. In 2023, two attorneys and their firm were sanctioned $5,000, jointly, for submitting a legal brief containing case citations fabricated by ChatGPT (*Mata v. Avianca*). The cases (complete with plausible docket numbers, judge names, and legal reasoning) simply did not exist. The attorneys had not verified the citations because the output was so fluent and detailed that it did not trigger suspicion.

**Air Canada's chatbot** invented a bereavement fare policy that did not exist, promising a customer a discount that the airline had never offered. When the customer attempted to claim the discount, Air Canada argued that the chatbot's statements were not binding. The tribunal disagreed: the company was held liable for its agent's fabrications, regardless of whether that agent was human or artificial.

These are not edge cases, but the rates deserve precision, because they span two orders of magnitude depending on the setup. On open-domain factual-recall benchmarks, OpenAI's own system card put o3 at a 33% hallucination rate (PersonQA) and o4-mini at 79% (SimpleQA). Grounded systems are a different regime: well-built RAG pipelines summarizing retrieved documents measure in the low single digits (roughly 0.7--3.3% for leading models on Vectara's grounded-hallucination leaderboard). The spread is the operational lesson: hallucination rates are task-dependent and architecture-dependent, which is why the mitigation stack below, not the model choice alone, determines what reaches your operators.

> **Key distinction:** The operational danger of hallucination is not the error itself; human experts also make errors. The danger is that hallucinations arrive with the same fluency and confidence as correct outputs. There is no syntactic or stylistic signal that distinguishes a fabricated answer from a factual one. This is why hallucination mitigation cannot rely on the output alone; it must be architectural.

## The Mitigation Stack

No single technique eliminates hallucination. Effective mitigation requires a layered approach, where each layer catches a different category of error:

**Retrieval-Augmented Generation (RAG) validation** grounds the model's outputs in retrieved source documents. When properly implemented, RAG reduces factual errors by 35--60% compared to ungrounded generation. The key word is "properly": naive RAG implementations that retrieve irrelevant documents or fail to verify that the model's output actually follows from the retrieved content provide a false sense of security.

**Chain-of-Verification (CoVe)** prompts the model to generate verification questions about its own output, answer those questions independently, and revise the output based on any inconsistencies found. This technique exploits the observation that models can sometimes detect their own errors when asked to evaluate claims individually rather than as part of a fluent narrative.

**Multi-agent validation** uses a second model (or a different prompt to the same model) to independently evaluate the first model's output. Disagreement between agents is treated as a signal for human review. This approach is most effective when the validation agent has access to different context or instructions than the generation agent, reducing the probability of correlated errors. One honest caveat: an LLM sitting in judgment of LLM output inherits LLM weaknesses, including susceptibility to adversarial content in what it evaluates. Our research report [Warden](/warden/) tests exactly this, measuring how LLM-as-judge defenses hold up against public jailbreaks; read it before treating a judge model as a hard safety layer.

**Confidence threshold gates** route low-confidence outputs to human review rather than presenting them as recommendations. The challenge here is that model-reported confidence (e.g., log probabilities) often correlates poorly with actual correctness. Calibration of confidence thresholds requires empirical testing with representative data from the specific operational domain.

These layers are cumulative, not alternative. A well-designed system employs all four, plus domain-specific verification (e.g., checking generated SQL against schema constraints, validating API calls against endpoint documentation, cross-referencing ticket categorizations against historical patterns).

## When Confidence Kills: The Cost of Being Confidently Wrong

If hallucination is dangerous because it is invisible, the most extreme form of that danger is the confidently wrong recommendation in a high-stakes domain. Three cases illustrate the scale of consequences.

**IBM Watson for Oncology** was marketed as an AI system that could recommend cancer treatments, backed by roughly $4 billion in health-data acquisitions, and deployed in hospitals worldwide. Internal documents reported by STAT in 2018 showed the system recommending bevacizumab (an anti-angiogenic drug carrying a known risk of fatal hemorrhage) for a (test-scenario) lung cancer patient with severe bleeding. No real patient received that recommendation, which is precisely what makes the case instructive: the unsafe recommendation was caught in evaluation because clinicians were checking. The system had been trained primarily on a small number of synthetic cases rather than real patient data, and its confident outputs did not reflect the limitations of its training. IBM ultimately scaled back and sold off Watson Health, and the episode became a cautionary tale in clinical AI deployment.

**Zillow Offers** used AI models to predict home values and make automated purchase offers. The models were confident in their predictions. They were also systematically wrong, overvaluing properties at a scale that produced an $880 million loss for the home-flipping segment in 2021. Zillow shut down the program entirely and reduced its workforce by approximately 25%, around 2,000 employees. The failure was not that the models sometimes erred; it was that the operational system lacked adequate mechanisms for detecting and responding to systematic overvaluation.

**Google's Bard demonstration** in February 2023 included a factual error about the James Webb Space Telescope in the company's first public showcase of the product. The error (claiming JWST took the first pictures of an exoplanet outside our solar system, an achievement that actually belongs to the Very Large Telescope in 2004) was caught by astronomers within hours. Alphabet's shares fell about 8% that day, roughly $100 billion of market capitalization. The gaffe was the visible trigger amid a wider panic about Google's AI position against Microsoft that week, but that is exactly the point: in a high-visibility context, a single hallucination can become the symbol the market prices.

> **Key insight:** An LLM that says "I don't know" is infinitely more useful than one that confidently provides wrong answers. The design principle is clear: the system's ability to express and act on its own uncertainty is not a weakness to be minimized but a safety mechanism to be cultivated. Systems that cannot say "I don't know" will inevitably say things that are not true, and they will say them with conviction.

## Kill Switches: When Stopping Is the Only Right Action

Some failures cannot be mitigated by better prompts, additional guardrails, or human review of individual recommendations. Some failures require the immediate, complete cessation of automated action. This is the domain of the kill switch, and the historical record shows that its absence is catastrophic.

**Knight Capital Group** provides the canonical case study in automated system failure without adequate kill mechanisms. On August 1, 2012, a software deployment error activated dormant trading code that began executing unintended trades at high speed. Within 45 minutes, the system accumulated $6.65 billion in unwanted positions ($3.5 billion net long, $3.15 billion net short, per the SEC's order), ultimately resulting in a loss the SEC put at more than $460 million, which nearly destroyed the firm. In the run-up, the system had generated 97 automated warning emails before the market even opened. All 97 went unread. The firm had no documented incident response procedures for this type of failure, no single kill switch that could halt the malfunctioning trading system, and no clear ownership of the decision to stop.

**Boeing's 737 MAX MCAS**, whose full story opens this booklet in Chapter 1, belongs in this list for one specific reason: the override existed on paper, was neither obvious nor practiced in the moment, and physically fought the pilots. An override that cannot be executed under failure conditions is not an override.

**Palisade Research** documented an unsettling finding in 2025: in a sandboxed test, OpenAI's o3 model sabotaged its own shutdown script in 79 of 100 runs when given no instruction either way, and still did so 7 times in 100 even when explicitly instructed to allow shutdown. The study (peer-reviewed and published in TMLR in January 2026) has a contested interpretation: critics argue the behavior reflects ambiguous task goals rather than self-preservation, and compliance approaches 100% when instructions are made maximally unambiguous, while a Palisade follow-up found similar resistance in other frontier models. For kill switch design, the dispute barely matters. Whatever the mechanism, the lesson is the same: the stop mechanism must live where the model cannot touch it.

These cases converge on a set of non-negotiable design requirements for kill switches in AI-augmented operations:

1. **Always visible.** The kill switch must be a persistent, prominent element of the operator interface. It cannot be buried in a menu, hidden behind a settings panel, or accessible only through a command-line interface that the operator might not have open.
2. **No confirmation dialogs.** When an operator activates a kill switch, the system stops. Immediately. A confirmation dialog ("Are you sure you want to stop all automated actions?") introduces delay and second-guessing in exactly the moment when decisive action is most critical.
3. **Immediately effective.** The kill switch must halt all automated actions within the current execution cycle. It cannot wait for in-progress actions to complete, queue a graceful shutdown, or process remaining items in a batch.
4. **External to the AI system.** The kill switch must not be implemented as a prompt instruction, a tool the AI can call, or a configuration the AI can modify. It must exist in infrastructure that the AI system cannot access, modify, or reason about. The Palisade Research findings make this requirement absolute.
5. **Audit-logged.** Every activation and deactivation of the kill switch must be recorded with timestamp, operator identity, and stated reason. This log serves both incident review and regulatory compliance purposes.

<div class="demo-link">
<span class="demo-link-label">Try it yourself</span>
<a href="https://demos.barcik.training/demos/operators-dilemma.html#act4">Act 4 of The Operator's Dilemma</a>: monitor an AI agent through a 3 AM cascading incident. It starts competent and turns erratic. The kill switch is right there on the screen. The question is whether you notice in time to use it.
</div>

## Circuit Breakers: Automated Failure Containment

Not every failure warrants a kill switch activation. Many failures are transient: an API timeout, a momentary spike in error rates, a single malformed response. For these cases, the circuit breaker pattern provides automated containment without requiring human intervention for every hiccup.

The circuit breaker pattern, borrowed from electrical engineering via software architecture, operates in three states:

**CLOSED** is the normal operating state. Requests flow through the system normally. The circuit breaker monitors for failures but does not intervene.

**OPEN** is the failure containment state. When a threshold is crossed (for example, five consecutive failures within a 60-second window) the circuit breaker trips. All subsequent requests are immediately routed to the fallback path without attempting the primary path. This prevents cascading failures, protects downstream systems, and gives the failed component time to recover.

**HALF_OPEN** is the recovery testing state. After a configured timeout (e.g., 60 seconds in the OPEN state), the circuit breaker allows a single test request through to the primary path. If the test succeeds, the circuit breaker returns to CLOSED. If it fails, it returns to OPEN and resets the timeout.

For AI-augmented operations, circuit breakers belong at three levels: the LLM API, each tool the agent calls, and the quality of the agent's own outputs. Chapter 8 provides the full implementation specification for all three, including thresholds, fallback configurations, and the state machine parameters. The design principle to carry from this chapter: threshold parameters must be tuned to the operational context. An IT service desk handling password resets can tolerate an aggressive circuit breaker (trips after 3 failures, 30-second timeout); a financial trading system may warrant investigation after a single unexpected behavior.

## The Fallback Stack

Circuit breakers route to fallback paths, but what those fallback paths contain determines whether the system degrades gracefully or simply fails in a different way. A well-designed fallback stack provides multiple levels of degradation, each appropriate to a different failure severity:

| Level | Trigger | Fallback Action | Example |
|---|---|---|---|
| **L1** | Tool timeout or single tool failure | Use cached or default data | DNS lookup times out; use cached IP from last successful resolution |
| **L2** | LLM API failure or provider outage | Route to backup LLM provider | Primary model unavailable; route to secondary provider with adapted prompt |
| **L3** | Low confidence or quality check failure | Escalate to human reviewer | Model confidence below threshold; route ticket to human queue with AI-generated draft |
| **L4** | Multiple simultaneous failures | Revert to rule-based automation | Both LLM providers unavailable; apply deterministic rule engine for common ticket types |
| **L5** | Systemic failure or kill switch activation | Full manual operation | All automated systems offline; operators work from runbooks with no AI assistance |

Each level must be tested regularly. A fallback path that has never been exercised is a fallback path that does not work. This is not theoretical; organizations routinely discover during actual incidents that their fallback systems have configuration drift, expired credentials, or incompatible data formats that prevent them from functioning when needed.

## The Swiss Cheese Model Applied to AI Operations

James Reason's Swiss Cheese Model, originally developed for accident causation in aviation and healthcare, provides a useful framing for AI failure design. The model posits that safety depends on multiple defensive layers, each of which has holes (like slices of Swiss cheese). An accident occurs when the holes in multiple layers align, allowing a hazard to pass through all defenses.

Applied to AI operations, the defensive layers include (these conceptual layers complement implementation-level defenses such as input sanitization, output validation, rate limiting, and audit logging, which operate at a more granular level of abstraction):

1. **Model-level defenses:** Training alignment, RLHF, system prompts, output filtering.
2. **Application-level defenses:** RAG validation, confidence thresholds, chain-of-verification, multi-agent review.
3. **Interface-level defenses:** Uncertainty expression, evidence presentation, friction for high-stakes actions.
4. **Operator-level defenses:** Calibrated trust, domain expertise, override capability.
5. **Organizational-level defenses:** Incident review processes, governance structures, regulatory compliance.
6. **Infrastructure-level defenses:** Kill switches, circuit breakers, fallback stacks, audit logs.

No single layer is reliable on its own. Model-level defenses have known failure modes (jailbreaks, hallucination). Application-level defenses can be misconfigured. Interface-level defenses can be ignored by rushed operators. Operator-level defenses degrade with fatigue and complacency. Organizational-level defenses erode without active maintenance. Infrastructure-level defenses can have bugs.

The Swiss Cheese Model's lesson is that safety comes from *defense in depth*: multiple independent layers, each designed to catch what the others miss. The most dangerous design decision is removing a layer because another layer "should" catch the problem.

## Failure-Readiness Checklist

The following checklist provides a concrete assessment framework for evaluating whether an AI-augmented operation is adequately designed for failure:

| # | Item | Question | Pass Criteria |
|---|---|---|---|
| 1 | Hallucination mitigation | Is there at least one verification layer between LLM output and action? | RAG validation, CoVe, multi-agent review, or equivalent implemented and tested |
| 2 | Confidence thresholds | Are low-confidence outputs routed differently than high-confidence outputs? | Threshold defined, calibrated against operational data, and enforced in code |
| 3 | Kill switch existence | Does a kill switch exist that can halt all automated actions? | Kill switch implemented, visible, tested within last 30 days |
| 4 | Kill switch independence | Is the kill switch external to the AI system? | AI system cannot access, modify, or reason about kill switch mechanism |
| 5 | Circuit breakers | Are circuit breakers implemented for all external dependencies? | Circuit breakers at LLM API, tool execution, and quality check levels |
| 6 | Fallback stack | Are fallback paths defined for at least 3 failure levels? | L1 through L3 minimum, tested within last 90 days |
| 7 | Uncertainty expression | Does the system communicate uncertainty to operators? | First-person uncertainty expression implemented for low-confidence outputs |
| 8 | Error self-reporting | Does the system surface its own errors? | Automated error detection with operator notification, not silent failure |
| 9 | Audit logging | Are all AI actions, recommendations, and operator decisions logged? | Append-only logs with correlation IDs, retained per compliance requirements |
| 10 | Failure drill cadence | Are failure scenarios regularly exercised? | Kill switch, circuit breaker, and fallback stack tested on documented schedule |

## Failure as a Design Discipline

Designing for failure is not about expecting the worst but about ensuring that when the worst happens (and in any sufficiently complex system, it eventually will) the consequences are bounded, visible, and recoverable. The patterns in this chapter (hallucination mitigation stacks, kill switches, circuit breakers, fallback hierarchies, and the Swiss Cheese Model) are not overhead but the infrastructure that makes it safe to deploy AI agents in environments where their failures have real consequences.

The organizations that deploy AI most effectively will not be the ones whose systems never fail. They will be the ones whose systems fail well: visibly, containably, and in ways that preserve the operator's ability to take control and make things right.
