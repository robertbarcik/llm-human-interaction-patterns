# LLM-Human Interaction Design Patterns for Operations

Lecture materials for teaching GenAI engineers how to design the seam between AI agents and human operators.

## Contents

### Interactive App — "The Operator's Dilemma"

A multi-act browser-based experience that doubles as a screenshare lecture tool and a participant simulation. Five acts cover automation bias, anchoring effects, confidence calibration, graduated autonomy, and interaction pattern design.

**Run it:** Open `app/index.html` in a browser. Optionally provide an [OpenRouter](https://openrouter.ai/) API key for live LLM interactions in Acts 3 and 5.

### HTML Booklet — Reference Takeaway

A comprehensive guide covering structural interaction patterns, the psychology of handoff, context presentation, trust calibration, failure mode design, and organizational governance.

**Read it:** Open `booklet/index.html` in a browser.

## Structure

```
app/
  index.html              # Interactive multi-act simulation
booklet/
  index.html              # Generated HTML booklet
  _sources/
    chapters/             # Markdown source files
    tools/build_html.py   # Build script
```

## Building the booklet from source

```bash
pip install markdown
python booklet/_sources/tools/build_html.py
cp booklet/_sources/output/booklet.html booklet/index.html
```

## Author

Robert Barcik — [barcik.training](https://barcik.training)
