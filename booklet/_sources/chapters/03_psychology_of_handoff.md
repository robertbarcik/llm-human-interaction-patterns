# Chapter 3: The Psychology of Handoff

The most dangerous assumption in AI-assisted operations is that humans will behave rationally when interacting with automated systems. They will not. Not because operators are careless or incompetent, but because the human cognitive architecture that served us well for millennia is systematically mismatched to the demands of monitoring and overriding automated systems. Understanding these mismatches is not optional -- it is a prerequisite for designing interaction patterns that actually work.

This chapter covers five cognitive phenomena that directly affect the quality of human decisions at the AI-human seam. Each has been extensively documented in peer-reviewed research. Each has produced real-world failures with measurable consequences. And each has design implications that, if ignored, will undermine even the most carefully engineered structural patterns from Chapter 2.

## Automation Bias

Automation bias is the tendency of humans to favor suggestions from automated systems over contradictory information from other sources, including their own observations. It is not a tendency to be lazy. It is a well-documented cognitive shortcut: the human brain treats the automated system as an authority and adjusts its processing accordingly.

### The Evidence

The landmark study is Skitka, Mosier, and Burdick (1999), which tested pilots and non-pilots in a simulated flight environment where an automated monitoring system occasionally provided incorrect recommendations.

The results were stark:

- **Commission errors** (taking an incorrect action recommended by the automation): **100% of participants** committed at least one commission error. Every single participant, including experienced pilots, followed the automation's recommendation at least once when it was demonstrably wrong.
- **Omission errors** (failing to notice problems the automation missed): **55% of participants** missed events that the automation failed to flag, even when clearly visible on their instruments.

Perhaps most troubling: having a second crew member present -- a standard mitigation for human error in aviation -- did not reduce automation bias errors. Parasuraman and Manzey's meta-analysis (2010) confirmed the pattern across multiple domains and added a critical finding: operators of high-reliability systems were **50% less likely to detect automation failures** than operators of less reliable systems. The more trustworthy the automation's track record, the less the human monitors it.

### Real-World Consequences

The **Enbridge pipeline rupture (2010)** demonstrated automation bias at operational scale. SCADA alarms indicated a pressure drop consistent with a rupture. Control room operators, calibrated by years of false alarms, dismissed the warnings for **17 hours**, twice restarting the pipeline and pumping additional oil into the environment. Cleanup exceeded **$1 billion**.

The **UK Post Office Horizon scandal** demonstrated it at institutional scale. The Horizon IT system contained bugs that created phantom financial shortfalls. Despite hundreds of sub-postmasters reporting the system's figures didn't match reality, the Post Office systematically trusted the computer over humans, resulting in **736 wrongful prosecutions** over 16 years.

> **Key insight:** Automation bias is not a character flaw. It is a predictable response to a poorly designed interaction. When a system is right 99% of the time, the rational Bayesian response is to trust it -- and that same rational response will cause the operator to miss the 1% of cases where trust is misplaced. The design must account for this, not the operator.

### Design Implications

Cognitive forcing functions -- interface elements that require the operator to actively engage before accepting the AI's recommendation -- are the primary countermeasure. A Harvard CHI 2021 study demonstrated that requiring operators to state their own assessment before seeing the AI's recommendation significantly reduced automation bias errors. The tradeoff: users found these systems less satisfying to use, creating a direct conflict between safety and usability that designers must navigate explicitly.

## Alert Fatigue

Alert fatigue is the progressive desensitization of operators to alerts as a result of excessive volume, high false positive rates, or both. It is the complement of automation bias: instead of trusting the wrong recommendation, the operator ignores all recommendations because the signal-to-noise ratio has collapsed.

### The Scale of the Problem

The numbers are consistent across industries:

- **Healthcare:** 72-99% of clinical alarms are false (AHRQ, 2020). Clinicians override approximately 90% of medication alerts. ECRI Institute has documented at least 80 fatalities directly attributable to alarm fatigue.
- **Security Operations:** The average SOC receives 2,992 security alerts per day, of which 63% go entirely unaddressed. Sophisticated attackers exploit this through "alert storming" -- generating high volumes of low-priority alerts to mask genuine intrusions.
- **IT Operations:** Similar patterns in infrastructure monitoring, where noisy alerting configurations generate hundreds or thousands of alerts per day, the majority transient or duplicative.

### Evidence-Based Remediation

Alert fatigue is not intractable. Boston Medical Center redesigned its clinical alarm system with threshold adjustments, suppression of non-actionable conditions, and tiered notification routing. Alarm volume dropped from **87,829 per week to 9,967** -- an 89% reduction -- without any increase in adverse patient outcomes.

The lesson: the value of an alerting system is not proportional to its sensitivity. A system that generates 3,000 alerts per day and catches 95% of real incidents is less useful than one that generates 300 alerts and catches 90%, because the first system trains operators to ignore alerts.

### Design Implications

For AI agents operating in the Triage and Escalate pattern, alert fatigue is the primary failure mode. Countermeasures:

- **Aggressive deduplication and correlation:** Group related alerts into incidents.
- **Confidence-based filtering:** Suppress alerts below a confidence threshold, accepting occasional misses to preserve operator attention.
- **Adaptive thresholds:** Adjust based on context (time of day, recent changes, current incident load).
- **Alert budgets:** Cap total daily escalations, forcing the system to prioritize.

## The Anchoring Effect

Anchoring is the cognitive bias identified by Tversky and Kahneman (1974) in which an initial piece of information disproportionately influences subsequent judgments, even when the anchor is arbitrary or irrelevant. In AI-human interaction, the AI's initial recommendation serves as a powerful anchor.

A 2025 study of 775 managers confirmed that anchoring effects persist even among experienced professionals in their domain of expertise, and even when participants were explicitly warned about anchoring bias before making their judgments. Experience and awareness reduce anchoring but do not eliminate it.

The design implication is direct: when an AI agent presents a recommendation first, the operator's subsequent investigation is shaped by that framing. They are more likely to seek confirming evidence and less likely to pursue alternative hypotheses.

### Design Implications

- **Consider-the-opposite:** Explicitly prompt operators to consider alternative explanations before accepting the AI's recommendation.
- **Data before recommendation:** Present the raw data and context before revealing the AI's recommendation, giving the operator an opportunity to form an independent assessment. More expensive in operator time but significantly reduces anchoring.

## Complacency Drift

Complacency drift is the gradual erosion of vigilance that occurs when an automated system performs reliably over an extended period. Unlike automation bias (which operates at individual decisions), complacency drift operates at the level of sustained monitoring behavior, creating a widening gap between the oversight provided and the oversight assumed.

### M/V Royal Majesty (1995)

The cruise ship M/V Royal Majesty ran aground near Nantucket with 1,509 people aboard because the ship's GPS antenna cable had detached, causing the GPS to switch to dead reckoning. The system displayed a warning indicator. The bridge team did not notice -- for **34 hours**, the ship sailed on a progressively divergent course, drifting **17 nautical miles** off track. Multiple independent indicators -- radar, depth soundings, visual observations -- contradicted the GPS position, but the crew had stopped cross-checking.

Closely related is **skill degradation**: the FAA has documented that **60% of aviation accidents** involving pilot error included a lack of manual flying proficiency -- skills that atrophied because autopilot handled the flying. In IT operations, this manifests when AI agents handle investigation and resolution for extended periods, and operators lose the diagnostic skills that escalation assumes they have.

### The CIGI Agency Decay Model

The Centre for International Governance Innovation describes a four-stage organizational pattern: **Experimentation** (AI supplements human work) → **Integration** (AI becomes standard, independent analysis declines) → **Reliance** (AI is primary input, skills atrophy, new staff trained to work with AI, not without it) → **Dependency** (organization cannot function without AI, no fallback).

> **Key distinction:** Complacency drift is not about individual operators making bad decisions. It is about organizational systems gradually losing their capacity for independent judgment. Countering it requires organizational interventions: periodic mandatory manual operation, challenge tickets with known outcomes, tracking approval-without-review rates, and simulation-based skill maintenance.

## Bringing It Together

These five phenomena -- automation bias, alert fatigue, anchoring, complacency drift, and skill degradation -- are not independent. They interact and reinforce each other:

- **Alert fatigue** increases **automation bias** (overwhelmed operators accept AI recommendations without scrutiny).
- **Complacency drift** accelerates **skill degradation** (operators who stop monitoring closely also stop practicing the skills needed for effective monitoring).
- **Anchoring** reinforces **automation bias** (the AI's recommendation shapes thinking, making independent evaluation harder).
- **Diffusion of responsibility** between human and AI enables **complacency drift** -- as Bleher and Braun (2022) observed, "the human says 'I followed the system' and the vendor says 'the human made the final call.'" When no one feels individually accountable, there is less motivation to maintain vigilance.

The structural patterns from Chapter 2 provide the skeleton of effective human-AI interaction. The cognitive phenomena in this chapter determine whether that skeleton supports a functional system or an empty one. A Recommend and Wait pattern that presents its recommendations in a way that anchors the operator and provides no forcing function for independent evaluation is, in practice, an Execute and Report pattern with extra steps.

The next chapter examines how to present information at the seam -- the specific communication formats and disclosure strategies that support good human decision-making in the face of these cognitive challenges.
