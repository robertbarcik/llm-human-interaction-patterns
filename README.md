# LLM-Human Interaction Design Patterns for Operations

Lecture materials for teaching GenAI engineers how to design the seam between AI agents and human operators.

**Live booklet:** [publications.barcik.training/llm-human-interaction-patterns](https://publications.barcik.training/llm-human-interaction-patterns/)
**Live game + demo suite:** [demos.barcik.training](https://demos.barcik.training/) (The Human-in-the-Loop Lab)

## Contents

### Interactive App · "The Operator's Dilemma"

A multi-act browser-based experience that doubles as a screenshare lecture tool and a participant simulation. Five acts cover automation bias, anchoring effects, confidence calibration, graduated autonomy, and interaction pattern design.

**Audience (since 2026-09-15): no IT expertise required.** You play the person on night duty for an online shop; all scenarios use plain office vocabulary (servers, the website, logins, payments, backups). Every wrong AI recommendation contradicts something written in the incident text itself, so catching it is a matter of attention, not domain knowledge. The demo measures attention under pressure: a shrinking timer (30 s down to 12 s), a fatigue strip with a simulated clock and hours awake, chat interruptions that slide in mid-incident (boss, marketing, partner, monitoring bot), optional beeps, and a first-half vs. second-half accuracy comparison in the results and the debrief.

**Theory as slides.** Each act's theory panel is one viewport-sized slide with four fixed slots (the trap, one number, one story, the design answer) and a link to the booklet chapter. **Lecture mode** (header button, persisted, or `?lecture`) enlarges type for a projector. After Act 1 a "show of hands" card lets a room compare results without any backend.

**Run it:** Open `app/index.html` directly in any browser: no server, no build step, no dependencies, no API keys. Everything runs client-side with pre-generated AI responses.

Deep links work per act: `#act1` through `#act5` and `#debrief` (e.g. `index.html#act3`).

The deployed copy lives at [demos.barcik.training/demos/operators-dilemma.html](https://demos.barcik.training/demos/operators-dilemma.html) inside "The Human-in-the-Loop Lab", alongside six sector companion simulations (banking, medical, law enforcement, hiring, border control, justice) whose sources live in the [barcik-training-demos](https://github.com/robertbarcik/barcik-training-demos) repo. `app/index.html` here is the source of truth for the flagship game; copy it over verbatim when it changes.

### HTML Booklet · Reference Takeaway

A ten-chapter guide: the case against the naive human-in-the-loop, five structural interaction patterns, the psychology of handoff, context presentation, trust calibration, failure design (kill switches, circuit breakers), implementation artifacts, and organizational governance. Revised July 2026 with a full fact-check and per-chapter links into the Lab.

**Lecture layer (September 2026):** every chapter opens with an "in one screen" card (claim, key points, the numbers that carry it) and the booklet carries eleven inline SVG figures (both editions, labels translated). The sidebar's **Lecture view** button (or `?skim`) hides the prose and leaves titles, cards and figures, for screensharing during a lecture. Sources: `booklet/_sources/tools/one_screen.py` and `figures.py`; figures are placed with `<!-- fig:NAME -->` markers in the chapter markdown.

**Read it:** Open `booklet/index.html` in a browser, or the live version above.

## Structure

```
app/
  index.html              # Interactive multi-act simulation (source of truth)
booklet/
  index.html              # Generated HTML booklet
  _sources/
    chapters/             # Markdown source files (00-10)
    tools/build_html.py   # Build script (includes SEO head + demo-callout CSS)
    notes.md              # Update log / build facts
```

## Building the booklet from source

```bash
pip install markdown
python3 booklet/_sources/tools/build_html.py            # English
python3 booklet/_sources/tools/build_html.py --lang sk  # Slovak (from chapters_sk/)
cp booklet/_sources/output/booklet.html booklet/index.html
# and copy the same file to barcik-training-publications/llm-human-interaction-patterns/index.html for deployment
```

## Author

Robert Barcik · [barcik.training](https://barcik.training)
