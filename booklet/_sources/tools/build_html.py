#!/usr/bin/env python3
"""Build an interactive single-page HTML booklet from chapter markdown sources."""

import os
import re
import glob
import markdown
import sys
import importlib.util

# Language: default English; `--lang sk` builds the Slovak edition from chapters_sk/ (same filenames;
# section ids are derived from the English chapter titles so anchors stay stable across editions).
LANG = 'sk' if '--lang' in sys.argv and sys.argv[sys.argv.index('--lang') + 1] == 'sk' else 'en'

# AI transparency notice (voluntary, Art 50 EU AI Act) - same wording on every barcik.training publication.
AI_TRANSPARENCY_NOTICE = r'''
<!-- AI transparency notice (Art 50 EU AI Act, voluntary) -->
<aside class="ai-transparency" id="ai-transparency" lang="en" aria-label="AI transparency"><svg class="ait-icon" viewBox="85 96 374 374" aria-hidden="true" focusable="false"><defs><mask id="ait-m-c"><rect width="566.93" height="566.93" fill="#000"/><circle cx="272.03" cy="283.47" r="182.75" fill="#fff"/><path fill="#000" d="M170.79,353.74c-1.08,0-2.05-.43-2.92-1.31-.88-.87-1.31-1.84-1.31-2.92,0-.67.07-1.27.2-1.81l47.34-129.32c.4-1.48,1.24-2.79,2.52-3.93,1.27-1.14,3.05-1.71,5.34-1.71h29.81c2.28,0,4.06.57,5.34,1.71,1.27,1.14,2.11,2.45,2.52,3.93l47.14,129.32c.27.54.4,1.14.4,1.81,0,1.08-.44,2.05-1.31,2.92s-1.91,1.31-3.12,1.31h-24.78c-2.01,0-3.52-.5-4.53-1.51-1.01-1.01-1.65-1.91-1.91-2.72l-7.86-20.55h-53.78l-7.65,20.55c-.27.81-.88,1.71-1.81,2.72-.94,1.01-2.55,1.51-4.83,1.51h-24.78ZM218.13,299.96h37.47l-18.93-53.18-18.53,53.18Z"/><path fill="#000" d="M328.11,353.74c-1.48,0-2.69-.47-3.63-1.41-.94-.94-1.41-2.15-1.41-3.63v-130.93c0-1.48.47-2.68,1.41-3.63s2.15-1.41,3.63-1.41h26.99c1.48,0,2.68.47,3.63,1.41.94.94,1.41,2.15,1.41,3.63v130.93c0,1.48-.47,2.69-1.41,3.63-.94.94-2.15,1.41-3.63,1.41h-26.99Z"/></mask></defs><rect width="566.93" height="566.93" fill="currentColor" opacity=".5" mask="url(#ait-m-c)"/></svg><div><span class="ait-label">AI transparency</span><p>This publication was written with generative AI (Anthropic&rsquo;s Claude) working alongside Robert Barcik. The text went through his review, and he holds editorial responsibility for what is published here (LearningDoe s.r.o.). Where the AI writes in its own voice, the piece says so. Disclosed in the spirit of Article&nbsp;50 of the EU AI Act.</p></div></aside>
<style>
.ai-transparency{display:flex;gap:.9rem;align-items:flex-start;margin:3.5rem 0 1.5rem;padding:1.1rem 0 0;border-top:1px solid;border-color:color-mix(in srgb,currentColor 22%,transparent);opacity:.78;font-size:.82rem;line-height:1.55;font-family:inherit;text-align:left}
.ai-transparency .ait-icon{flex:0 0 auto;width:2.1rem;height:2.1rem;margin-top:.1rem}
.ai-transparency .ait-label{display:block;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;margin-bottom:.3rem}
.ai-transparency p{margin:0;max-width:62ch}
</style>
'''


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters_sk" if LANG == 'sk' else "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "booklet_sk.html" if LANG == 'sk' else "booklet.html")

def _sk_notice():
    """Slovak colophon from the shared generator in the training-ops repo (sibling of this repo)."""
    repos_root = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))  # .../git-repos
    label_py = os.path.join(repos_root, 'training-ops', 'web', 'ai_transparency_label.py')
    spec = importlib.util.spec_from_file_location('ait', label_py)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.colophon('pub_sk', 'sk', uid='c')

T = {
    'en': dict(
        title="LLM-Human Interaction Design Patterns for Operations",
        description="How to design the seam between AI agents and human operators: interaction patterns, trust calibration, SBAR handoffs, kill switches, and governance design.",
        slug="llm-human-interaction-patterns", other_slug="llm-human-interaction-patterns-sk",
        other_label="Čítať po slovensky &rarr;", other_hreflang="sk",
        all_pubs="&larr; All Publications", sidebar_h2="Interaction Design Patterns",
        sidebar_p="Designing the Seam Between AI Agents and Human Operators",
        chapter_word="Chapter", nav_label="Toggle navigation",
    ),
    'sk': dict(
        title="Vzory interakcie LLM a človeka pre prevádzku",
        description="Ako navrhnúť šev medzi AI agentmi a ľudskými operátormi: vzory interakcie, kalibrácia dôvery, odovzdania SBAR, vypínače a návrh governance.",
        slug="llm-human-interaction-patterns-sk", other_slug="llm-human-interaction-patterns",
        other_label="Read in English &rarr;", other_hreflang="en",
        all_pubs="&larr; Všetky publikácie", sidebar_h2="Vzory interakcie",
        sidebar_p="Návrh švu medzi AI agentmi a ľudskými operátormi",
        chapter_word="Kapitola", nav_label="Prepnúť navigáciu",
    ),
}[LANG]

CSS = """
:root {
    --navy: #1e3a5f;
    --navy-light: #2a5280;
    --accent: #3b82f6;
    --bg: #ffffff;
    --bg-sidebar: #f8fafc;
    --text: #1e293b;
    --text-light: #64748b;
    --border: #e2e8f0;
    --code-bg: #f1f5f9;
    --sidebar-width: 300px;
    --progress-height: 3px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 17px;
    line-height: 1.75;
    color: var(--text);
    background: var(--bg);
}

/* Progress bar */
#progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: var(--progress-height);
    background: var(--accent);
    z-index: 1000;
    transition: width 0.1s;
}

/* Sidebar */
#sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 2rem 0;
    z-index: 100;
    transition: transform 0.3s;
}

#sidebar-header {
    padding: 0 1.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

#sidebar-header .all-pubs-link {
    display: inline-block;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--text-light);
    text-decoration: none;
    margin-bottom: 0.6rem;
    transition: color 0.2s;
}

#sidebar-header .all-pubs-link:hover {
    color: var(--accent);
}
#sidebar-header .lang-link{display:inline-block;margin-top:.6rem;font-size:.78rem;font-weight:600;color:var(--accent);text-decoration:none}
#sidebar-header .lang-link:hover{text-decoration:underline}

#sidebar-header h2 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

#sidebar-header p {
    font-size: 0.78rem;
    color: var(--text-light);
    margin-top: 0.3rem;
    line-height: 1.4;
}

#sidebar nav ul {
    list-style: none;
    padding: 0;
}

#sidebar nav ul li a {
    display: block;
    padding: 0.55rem 1.5rem;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.85rem;
    color: var(--text-light);
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: all 0.2s;
    line-height: 1.4;
}

#sidebar nav ul li a:hover {
    color: var(--navy);
    background: rgba(30, 58, 95, 0.04);
}

#sidebar nav ul li a.active {
    color: var(--navy);
    font-weight: 600;
    border-left-color: var(--accent);
    background: rgba(59, 130, 246, 0.06);
}

/* Hamburger menu */
#menu-toggle {
    display: none;
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 200;
    background: var(--navy);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    font-size: 1.2rem;
    cursor: pointer;
}

/* Main content wrapper */
#content-wrapper {
    margin-left: var(--sidebar-width);
    display: flex;
    justify-content: center;
    padding: 0 2rem;
}

/* Main content */
#content {
    max-width: 780px;
    width: 100%;
    padding: 3rem 1rem 6rem;
}

/* Chapter sections */
.chapter {
    margin-bottom: 5rem;
    padding-top: 1rem;
}

.chapter:first-child {
    margin-bottom: 4rem;
    padding-bottom: 2rem;
    border-bottom: 2px solid var(--border);
}

.chapter-number {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* Typography */
h1 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--navy);
    line-height: 1.2;
    margin-bottom: 1.5rem;
}

h2 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--navy);
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    line-height: 1.3;
}

h3 {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--navy-light);
    margin-top: 2rem;
    margin-bottom: 0.75rem;
}

p {
    margin-bottom: 1.1rem;
}

/* Lists */
ul, ol {
    margin-bottom: 1.1rem;
    padding-left: 1.8rem;
}

li {
    margin-bottom: 0.4rem;
}

/* Strong / emphasis */
strong { font-weight: 700; }
em { font-style: italic; }

/* Code */
code {
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88em;
    background: var(--code-bg);
    padding: 0.15em 0.4em;
    border-radius: 4px;
}

pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem;
    overflow-x: auto;
    margin-bottom: 1.5rem;
    font-size: 0.88rem;
    line-height: 1.6;
}

pre code {
    background: none;
    padding: 0;
    border-radius: 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
    font-size: 0.92rem;
    line-height: 1.5;
}

thead {
    background: var(--navy);
    color: white;
}

th {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 600;
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

td {
    padding: 0.7rem 1rem;
    border-bottom: 1px solid var(--border);
}

tbody tr:nth-child(even) {
    background: var(--bg-sidebar);
}

tbody tr:hover {
    background: rgba(59, 130, 246, 0.04);
}

/* Blockquotes (used for callouts / key takeaways) */
blockquote {
    border-left: 4px solid var(--accent);
    background: rgba(59, 130, 246, 0.04);
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    border-radius: 0 8px 8px 0;
    font-style: normal;
}

blockquote p:last-child {
    margin-bottom: 0;
}

/* "Try it yourself" demo callouts (Human-in-the-Loop Lab) */
.demo-link {
    border: 1px solid #bfdbfe;
    border-left: 4px solid var(--navy);
    background: #eff6ff;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.5rem;
    margin: 1.5rem 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 0.88rem;
    line-height: 1.55;
}
.demo-link .demo-link-label {
    display: block;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.demo-link a {
    font-weight: 600;
}

/* Horizontal rules (chapter dividers) */
hr {
    border: none;
    border-top: 2px solid var(--border);
    margin: 4rem 0;
}

/* Responsive */
@media (max-width: 900px) {
    #sidebar {
        transform: translateX(-100%);
    }
    #sidebar.open {
        transform: translateX(0);
        box-shadow: 4px 0 20px rgba(0,0,0,0.15);
    }
    #menu-toggle {
        display: block;
    }
    #content-wrapper {
        margin-left: 0;
        padding: 0 1rem;
    }
    #content {
        padding: 2rem 0.5rem 4rem;
    }
    h1 { font-size: 1.7rem; }
    h2 { font-size: 1.3rem; }
    table { font-size: 0.82rem; }
    th, td { padding: 0.5rem 0.6rem; }
}

@media (max-width: 600px) {
    #content { padding: 1.5rem 1rem 3rem; }
    body { font-size: 15.5px; }
}

/* Print */
@media print {
    #sidebar, #menu-toggle, #progress-bar { display: none !important; }
    #content-wrapper { margin-left: 0; padding: 0; }
    #content { max-width: 100%; }
    .chapter { page-break-before: always; }
    .chapter:first-child { page-break-before: auto; }
}
"""

JS = """
document.addEventListener('DOMContentLoaded', function() {
    // Progress bar
    const progressBar = document.getElementById('progress-bar');
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
        progressBar.style.width = progress + '%';
    });

    // Sidebar navigation highlighting
    const chapters = document.querySelectorAll('.chapter');
    const navLinks = document.querySelectorAll('#sidebar nav a');

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { rootMargin: '-20% 0px -70% 0px' });

    chapters.forEach(function(ch) { observer.observe(ch); });

    // Smooth scrolling
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Close sidebar on mobile
                document.getElementById('sidebar').classList.remove('open');
            }
        });
    });

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('open');
    });

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 900 &&
            !sidebar.contains(e.target) &&
            e.target !== menuToggle) {
            sidebar.classList.remove('open');
        }
    });

    // Mark first nav item as active
    if (navLinks.length > 0) navLinks[0].classList.add('active');
});
"""


def get_chapter_files():
    return sorted(glob.glob(os.path.join(CHAPTERS_DIR, "*.md")))


def extract_title(content):
    for line in content.strip().split("\n"):
        m = re.match(r"^#\s+(.+)", line)
        if m:
            return m.group(1).strip()
        m = re.match(r"^##\s+(.+)", line)
        if m:
            return m.group(1).strip()
    return None


def make_id(title):
    slug = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    return re.sub(r"\s+", "-", slug).strip("-")


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "smarty"],
        output_format="html5"
    )


def build():
    files = get_chapter_files()
    chapters = []

    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        title = extract_title(content) or os.path.basename(f).replace(".md", "").replace("_", " ")
        html_content = md_to_html(content)
        with open(os.path.join(EN_CHAPTERS_DIR, os.path.basename(f)), "r", encoding="utf-8") as fh:
            en_title = extract_title(fh.read().strip()) or title
        ch_id = make_id(en_title)
        chapters.append((title, ch_id, html_content))

    # Build sidebar nav
    nav_items = []
    for i, (title, ch_id, _) in enumerate(chapters):
        label = title
        if i > 0:
            label = f"{i}. {title}"
        nav_items.append(f'<li><a href="#{ch_id}">{label}</a></li>')

    nav_html = "\n".join(nav_items)

    # Build chapter sections
    sections = []
    for i, (title, ch_id, html_content) in enumerate(chapters):
        ch_num = ""
        if i > 0:
            ch_num = f'<div class="chapter-number">{T["chapter_word"]} {i}</div>'
        sections.append(f'''
        <section class="chapter" id="{ch_id}">
            {ch_num}
            {html_content}
        </section>''')

    sections_html = "\n".join(sections)

    # Assemble full HTML
    html = f"""<!DOCTYPE html>
<html lang="{LANG}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{T['title']}</title>
    <meta name="description" content="{T['description']}">
    <link rel="canonical" href="https://publications.barcik.training/{T['slug']}/">
    <link rel="alternate" hreflang="{LANG}" href="https://publications.barcik.training/{T['slug']}/">
    <link rel="alternate" hreflang="{T['other_hreflang']}" href="https://publications.barcik.training/{T['other_slug']}/">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{T['title']}">
    <meta property="og:description" content="{T['description']}">
    <meta property="og:url" content="https://publications.barcik.training/{T['slug']}/">
    <meta property="og:image" content="https://publications.barcik.training/assets/og-card.png">
    <meta name="twitter:card" content="summary_large_image">
    <style>{CSS}</style>
</head>
<body>
    <div id="progress-bar"></div>

    <button id="menu-toggle" aria-label="{T['nav_label']}">&#9776;</button>

    <aside id="sidebar">
        <div id="sidebar-header">
            <a class="all-pubs-link" href="/">{T['all_pubs']}</a>
            <h2>{T['sidebar_h2']}</h2>
            <p>{T['sidebar_p']}</p>
            <a class="lang-link" href="/{T['other_slug']}/">{T['other_label']}</a>
        </div>
        <nav>
            <ul>
                {nav_html}
            </ul>
        </nav>
    </aside>

    <div id="content-wrapper">
        <main id="content">
            {sections_html}
        {AI_TRANSPARENCY_NOTICE if LANG == 'en' else _sk_notice()}
        </main>
    </div>

    <script>{JS}</script>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"Built: {OUTPUT_FILE}")
    print(f"  Chapters: {len(chapters)}")


if __name__ == "__main__":
    build()
