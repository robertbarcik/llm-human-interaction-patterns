# LLM-Human Interaction Design Patterns — update log

Working notes for the booklet deployed at `publications.barcik.training/llm-human-interaction-patterns/`. Sources: `chapters/*.md` in this repo, built by `tools/build_html.py` (→ `output/booklet.html`, copied to `booklet/index.html` here AND to `barcik-training-publications/llm-human-interaction-patterns/index.html`). After every rebuild the two copies must be byte-identical (the build script carries the SEO/OG head block since July 2026; no hand-patching).

Build/verify facts:
- Anchors = slugified chapter H1s, filename-sorted; 11 sections (frontmatter + 10 chapters). External links point at the booklet root only, so renumbering is safe.
- Sanctioned dashes: 0 in the built HTML. Ch8's prompt-template code blocks use plain hyphens as separators.
- `.demo-link` callout boxes (raw HTML in markdown, isolated by blank lines) link the Human-in-the-Loop Lab on demos.barcik.training; the flagship game supports `#act1`–`#act5`/`#debrief` hash deep links.

## 2026-07-04 — July 2026 revision (with Claude / Fable 5)

Full editorial + factual overhaul following three independent fact-check passes (of 22 research citations only 6 fully verified; of 27 industry claims 5 hard-wrong).

- **Restructure 9 → 10 chapters.** New Chapter 2 "The Case Against the Naive Loop" (~2,000 words: Vaccaro/Almaatouq/Malone 2024 meta-analysis incl. the AI>human conditional; Green 2022 oversight-policy flaws; Elish 2019 moral crumple zone; Anthropic Feb 2026 approval-fatigue data + MSR "Overseeing Agents Without Constant Oversight"; Article 14 read correctly + Digital Omnibus deferral note). Old Ch6 (implementing) and Ch7 (failure) swapped so concepts precede specs — this also made old Ch6's two broken self-references ("Chapter 6 described...") correct as Chapter 7 refs. File map: 02→03, 03→04, 04→05, 05→06, 06→08, 08→09, 09→10; 07 unchanged; new 02 created.
- **Dedupe:** kill-switch/circuit-breaker content split — Ch7 owns rationale/cases/5 requirements, Ch8 owns specs/state machine/config tables; KILLSWITCH.md spec moved Ch7→Ch8; 737 MAX full treatment lives in Ch1 (load-bearing pairing with AF447), Ch7 compressed to a pointer; Knight Capital full treatment in Ch7 only.
- **Fact corrections (highlights; full ledger in the July 2026 session):** fabricated Bleher & Braun quote → paraphrase; fabricated PagerDuty tier names + "50 approvals" mechanism → real incident-tiers + Review/Autonomous modes; Splunk "90min→60s" was Google Cloud's stat → reattributed/hedged; Dynatrace 56% = IDC AI-guided investigation, not autonomous remediation; SBAR Navy origin marked apocryphal; "4.8%→100%" → El-Sayed Ghonem & El-Husany 2023 (nurses' knowledge, 4.8%→92.8%); Klein "78% under a minute" → real ~80%-no-comparison finding; DARPA XAI $75M dropped; Joint Commission (not ECRI) 80 deaths; CIGI stage "Addiction"; Knight $6.65B/$460M+; Avianca $5,000 total; o3 PersonQA 33% / o4-mini SimpleQA 79% + grounded-RAG 0.7–3.3% contrast; Watson bevacizumab = test case; Zillow $880M; Bard $100B = trigger among factors; Palisade 7/100-vs-79/100 precision + disputed interpretation; AIID ~1,000 (Mar 2025) not 1,400+; "40% faster/60% fewer" governance stat CUT; Gartner 20%/45% kept (verified, cited); Galileo quarterly chair rotation; MiFID "kill functionality"; FDA CDS guidance superseded early 2026 note; AI Act Aug-2026 deadline → Digital Omnibus deferral note (Annex III → Dec 2027).
- **New: "From Levels to Teammates"** (end of Ch3): Dekker & Woods 2002, Klein et al. 2004 ten challenges, NASEM 2022.
- **Cross-links:** 7 `.demo-link` callouts to the Human-in-the-Loop Lab (per-chapter mapping); outbound to `/warden/` (Ch7 multi-agent validation), `/agent-horizon/` (Ch9 Article 14), `/token-economics/` (Ch9 oversight-as-a-service); Ch10 closes with the Lab.
- **Voice sweep:** ~300 double-hyphen dashes in sources → 0 (commas/colons/parens/semicolons; middots in table labels); ~25 "It is not X. It is Y." constructions rewritten; 3 first-person field notes (Ch2 opener, Ch4 workshop story, Ch8 calibration note); frontmatter rewritten around the client-sentence hook with a vendor-numbers honesty note.
- **Build script:** adopted SEO/OG/canonical/favicon head block; added `.demo-link` CSS.

## Game / Human-in-the-Loop Lab (same date)

`app/index.html` (source of truth): OpenRouter/API-key support fully removed (Acts 3+5 use the richer pre-generated responses behind a 1.5s spinner); hash deep links added; header + debrief links to booklet and demos landing; theory-panel fact fixes mirroring the booklet (Skitka, Buçinca CSCW venue, Klein, CSA downshifting, Goddard 30-50% softened); voice sweep (85 → 9 em dashes, the 9 survivors are `'—'` empty-stat placeholders). Deployed copy: `barcik-training-demos/demos/operators-dilemma.html` (byte-identical). Six new sector demos (credit-desk, triage-ward, watchlist, shortlist, border-queue, docket) live in barcik-training-demos only.

## 2026-08-16 — Slovak edition (Vzory interakcie LLM a človeka pre prevádzku)

- `chapters_sk/` (same filenames as `chapters/`), translated entirely by Fable 5, meaning-first, per the
  shared glossary in `barcik-training-publications/_sources/_translation/GLOSSARY_SK.md`.
- `tools/build_html.py --lang sk` → `output/booklet_sk.html`; section ids derived from the English titles
  (stable anchors); Slovak colophon from training-ops; sidebar lang links both ways (EN build gained
  "Čítať po slovensky →" + hreflang alternates, otherwise unchanged).
- Prompt templates and example outputs in Chapter 8's code blocks are kept in English (they are
  copy-paste artifacts); the surrounding prose and tables are translated. Demo links stay EN (demos are English).
- Deployed copies: publications `/llm-human-interaction-patterns-sk/` (+ EN refreshed).
