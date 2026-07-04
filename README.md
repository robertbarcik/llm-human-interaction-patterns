# LLM-Human Interaction Design Patterns for Operations

Lecture materials for teaching GenAI engineers how to design the seam between AI agents and human operators.

**Live booklet:** [publications.barcik.training/llm-human-interaction-patterns](https://publications.barcik.training/llm-human-interaction-patterns/)
**Live game + demo suite:** [demos.barcik.training](https://demos.barcik.training/) (The Human-in-the-Loop Lab)

## Contents

### Interactive App · "The Operator's Dilemma"

A multi-act browser-based experience that doubles as a screenshare lecture tool and a participant simulation. Five acts cover automation bias, anchoring effects, confidence calibration, graduated autonomy, and interaction pattern design.

**Run it:** Open `app/index.html` directly in any browser: no server, no build step, no dependencies, no API keys. Everything runs client-side with pre-generated AI responses.

Deep links work per act: `#act1` through `#act5` and `#debrief` (e.g. `index.html#act3`).

The deployed copy lives at [demos.barcik.training/demos/operators-dilemma.html](https://demos.barcik.training/demos/operators-dilemma.html) inside "The Human-in-the-Loop Lab", alongside six sector companion simulations (banking, medical, law enforcement, hiring, border control, justice) whose sources live in the [barcik-training-demos](https://github.com/robertbarcik/barcik-training-demos) repo. `app/index.html` here is the source of truth for the flagship game; copy it over verbatim when it changes.

### HTML Booklet · Reference Takeaway

A ten-chapter guide: the case against the naive human-in-the-loop, five structural interaction patterns, the psychology of handoff, context presentation, trust calibration, failure design (kill switches, circuit breakers), implementation artifacts, and organizational governance. Revised July 2026 with a full fact-check and per-chapter links into the Lab.

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
python booklet/_sources/tools/build_html.py
cp booklet/_sources/output/booklet.html booklet/index.html
# and copy the same file to barcik-training-publications/llm-human-interaction-patterns/index.html for deployment
```

## Author

Robert Barcik · [barcik.training](https://barcik.training)
