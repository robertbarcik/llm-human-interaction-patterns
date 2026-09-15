"""Inline SVG figures for the booklet, with English and Slovak labels.

Each figure is referenced from the chapter markdown by a marker line, e.g.

    <!-- fig:autonomy-ladder -->

and build_html.py replaces the marker with `render(name, lang)`. The same marker sits in
chapters/ and chapters_sk/, so both editions get the same drawing with their own labels.
Figures are drawn for a 760px-wide content column and scale down with the page.
"""

# Palette (matches the booklet CSS)
NAVY, NAVY_L, ACCENT = '#1e3a5f', '#2a5280', '#3b82f6'
TEXT, MUTED, BORDER = '#1e293b', '#64748b', '#cbd5e1'
BLUE_BG, GRAY_BG = '#eff6ff', '#f8fafc'
RED, RED_BG, AMBER, AMBER_BG, GREEN, GREEN_BG = '#dc2626', '#fef2f2', '#d97706', '#fffbeb', '#16a34a', '#f0fdf4'
PURPLE, PURPLE_BG = '#7c3aed', '#f5f3ff'


def _t(lang, en, sk):
    return sk if lang == 'sk' else en


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def box(x, y, w, h, fill=GRAY_BG, stroke=BORDER, r=8, sw=1.5, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def text(x, y, s, size=13, fill=TEXT, weight=400, anchor='middle', italic=False, spacing=''):
    st = ' font-style="italic"' if italic else ''
    ls = f' letter-spacing="{spacing}"' if spacing else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{st}{ls}>{esc(s)}</text>'


def lines(x, y, rows, size=12, fill=TEXT, weight=400, anchor='middle', lh=None):
    lh = lh or size + 4
    return ''.join(text(x, y + i * lh, r, size, fill, weight, anchor) for i, r in enumerate(rows))


def defs():
    m = ''
    for name, color in (('navy', NAVY), ('red', RED), ('gray', MUTED), ('green', GREEN), ('amber', AMBER), ('accent', ACCENT)):
        m += (f'<marker id="ah-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
              f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')
    return f'<defs>{m}</defs>'


def arrow(x1, y1, x2, y2, color='navy', sw=1.8, dash=''):
    col = {'navy': NAVY, 'red': RED, 'gray': MUTED, 'green': GREEN, 'amber': AMBER, 'accent': ACCENT}[color]
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{sw}" marker-end="url(#ah-{color})"{d}/>'


def path_arrow(d, color='navy', sw=1.8, dash=''):
    col = {'navy': NAVY, 'red': RED, 'gray': MUTED, 'green': GREEN, 'amber': AMBER, 'accent': ACCENT}[color]
    dd = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" marker-end="url(#ah-{color})"{dd}/>'


def svg(w, h, body, title):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">'
            f'{defs()}{body}</svg>')


def figure(name, inner, caption):
    return f'<figure class="figure" id="fig-{name}">{inner}<figcaption>{caption}</figcaption></figure>'


# ---------------------------------------------------------------------------
# 1. The declared loop vs. the designed loop (Chapter 2)
# ---------------------------------------------------------------------------
def fig_naive_vs_designed(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    # Left panel
    b += box(10, 10, 355, 285, '#fff', RED_BG, r=12, sw=2)
    b += text(187, 34, t('The declared loop', 'Deklarovaná slučka'), 14, RED, 700)
    cx = 187
    b += box(cx - 70, 50, 140, 36, BLUE_BG, BORDER) + text(cx, 73, t('AI agent', 'AI agent'), 13, NAVY, 600)
    b += arrow(cx, 86, cx, 104)
    b += box(cx - 95, 106, 190, 36, GRAY_BG, BORDER) + text(cx - 10, 129, t('Verdict. Approve?', 'Verdikt. Schváliť?'), 13, TEXT, 600)
    b += box(cx + 50, 111, 38, 26, RED_BG, RED, r=13, sw=1) + text(cx + 69, 128, '30 s', 10, RED, 700)
    b += arrow(cx, 142, cx, 160)
    b += box(cx - 70, 162, 140, 36, GRAY_BG, BORDER) + text(cx, 185, t('Human signs', 'Človek podpíše'), 13, TEXT, 600)
    b += arrow(cx, 198, cx, 216)
    b += box(cx - 70, 218, 140, 36, GRAY_BG, BORDER) + text(cx, 241, t('Action', 'Krok'), 13, TEXT, 600)
    b += path_arrow(f'M{cx + 75},236 C{cx + 150},236 {cx + 150},180 {cx + 75},180', 'red', 2)
    b += lines(cx + 135, 262, [t('blame lands here', 'vina pristane tu'), t('(moral crumple zone)', '(morálna deformačná zóna)')], 10.5, RED, 600)
    # Right panel
    b += box(385, 10, 365, 285, '#fff', GREEN_BG, r=12, sw=2)
    b += text(567, 34, t('The designed loop', 'Navrhnutá slučka'), 14, GREEN, 700)
    rx = 520
    b += box(rx - 85, 50, 170, 36, BLUE_BG, BORDER) + text(rx, 73, t('Facts first (SBAR)', 'Najprv fakty (SBAR)'), 13, NAVY, 600)
    b += arrow(rx, 86, rx, 104)
    b += box(rx - 85, 106, 170, 36, GRAY_BG, BORDER) + text(rx, 129, t('Human forms a view', 'Človek si utvorí názor'), 13, TEXT, 600)
    b += arrow(rx, 142, rx, 160)
    b += box(rx - 105, 162, 210, 36, BLUE_BG, BORDER) + text(rx, 179, t('AI proposes', 'AI navrhne'), 12, NAVY, 600) + text(rx, 193, t('with calibrated confidence', 's kalibrovanou istotou'), 10.5, MUTED)
    b += arrow(rx, 198, rx, 216)
    b += box(rx - 105, 218, 210, 36, GRAY_BG, BORDER) + text(rx, 241, t('Approve, modify or reject', 'Schváliť, upraviť alebo odmietnuť'), 12.5, TEXT, 600)
    # Track record feeding the human
    b += box(645, 100, 96, 44, GRAY_BG, BORDER, dash='4 3') + lines(693, 118, [t('Track record', 'Záznam'), t('by action type', 'o výkone')], 10.5, MUTED, 600)
    b += arrow(645, 122, 607, 124, 'gray', 1.5)
    # Stop button outside
    b += box(650, 215, 90, 40, RED, '#991b1b', r=8, sw=2) + text(695, 240, 'STOP', 14, '#fff', 800)
    b += lines(695, 270, [t('outside the AI,', 'mimo dosahu AI,'), t('no confirmation dialog', 'bez potvrdzovacieho okna')], 10, MUTED)
    inner = svg(760, 300, b, t('The declared loop versus the designed loop', 'Deklarovaná slučka a navrhnutá slučka'))
    cap = t('Figure 2.1 · The same five words, two different systems. Left: a verdict, a timer and a signature, with the blame flowing back to the person. Right: facts before the verdict, calibrated confidence, a track record, and a stop the AI cannot reach.',
            'Obrázok 2.1 · Tie isté slová, dva rôzne systémy. Vľavo: verdikt, časovač a podpis, pričom vina sa vracia k človeku. Vpravo: fakty pred verdiktom, kalibrovaná istota, záznam o výkone a vypínač mimo dosahu AI.')
    return figure('naive-vs-designed', inner, cap)


# ---------------------------------------------------------------------------
# 2. The five patterns on the Sheridan-Verplank scale (Chapter 3)
# ---------------------------------------------------------------------------
def fig_autonomy_ladder(lang):
    t = lambda en, sk: _t(lang, en, sk)
    X0, CW, Y = 40, 68, 158
    b = text(40, 24, t('Sheridan and Verplank, ten levels of automation (1978)', 'Sheridan a Verplank, desať úrovní automatizácie (1978)'), 12.5, MUTED, 600, 'start')

    def band(a, c, y, label, fill, stroke, h=24):
        x = X0 + (a - 1) * CW
        w = (c - a + 1) * CW
        return box(x, y, w, h, fill, stroke, r=6) + text(x + w / 2, y + 16, label, 11.5, TEXT, 700)

    b += band(3, 5, 40, t('Triage & Escalate', 'Triediť a eskalovať'), AMBER_BG, AMBER)
    b += band(4, 5, 70, t('Recommend & Wait', 'Odporučiť a čakať'), BLUE_BG, ACCENT)
    b += band(7, 8, 70, t('Execute & Report', 'Vykonať a hlásiť'), GREEN_BG, GREEN)
    b += band(5, 5, 100, t('Draft & Refine', 'Navrhnúť a doladiť'), PURPLE_BG, PURPLE)
    # graduated autonomy arrow across 2..8
    gx1, gx2 = X0 + 1 * CW + 6, X0 + 8 * CW - 6
    b += f'<line x1="{gx1}" y1="140" x2="{gx2}" y2="140" stroke="{NAVY}" stroke-width="2" marker-end="url(#ah-navy)" marker-start="url(#ah-navy)"/>'
    b += text((gx1 + gx2) / 2, 135, t('Graduated Autonomy: moves between levels, downshifts when unsure', 'Odstupňovaná autonómia: pohybuje sa medzi úrovňami, pri neistote klesá'), 11, NAVY, 700)
    for L in range(1, 11):
        x = X0 + (L - 1) * CW
        fill = NAVY if L >= 9 else (NAVY_L if L >= 6 else ('#93c5fd' if L >= 4 else BLUE_BG))
        col = '#fff' if L >= 4 else NAVY
        b += box(x + 2, Y, CW - 4, 32, fill, 'none', r=5) + text(x + CW / 2, Y + 21, str(L), 14, col, 700)
    b += text(X0, Y + 54, t('Human does everything', 'Človek robí všetko'), 11.5, MUTED, 600, 'start')
    b += text(X0 + 10 * CW, Y + 54, t('Machine decides everything', 'Stroj rozhoduje o všetkom'), 11.5, MUTED, 600, 'end')
    b += text(X0 + 10 * CW, Y + 70, t('(rarely appropriate in operations)', '(v prevádzke zriedka vhodné)'), 10, MUTED, 400, 'end')
    b += text(X0 + 4.5 * CW, Y + 70, t('4 suggests one option · 5 executes it if you approve · 7 acts, then tells you', '4 navrhne jednu možnosť · 5 ju vykoná, ak schválite · 7 koná a potom hlási'), 10, MUTED, 400)
    inner = svg(760, 250, b, t('Five patterns mapped to the Sheridan-Verplank scale', 'Päť vzorov na škále Sheridana a Verplanka'))
    cap = t('Figure 3.1 · Where the five patterns sit on the classic scale. Start at 4 to 5, earn 7 with a track record, and design the movement between levels from day one.',
            'Obrázok 3.1 · Kde na klasickej škále sedí päť vzorov. Začnite na úrovni 4 až 5, úroveň 7 si vyslúžte záznamom o výkone a pohyb medzi úrovňami navrhnite od prvého dňa.')
    return figure('autonomy-ladder', inner, cap)


# ---------------------------------------------------------------------------
# 3. How the five phenomena reinforce each other (Chapter 4)
# ---------------------------------------------------------------------------
def fig_bias_loop(lang):
    t = lambda en, sk: _t(lang, en, sk)
    W, H = 190, 46

    def node(x, y, label, fill=GRAY_BG, stroke=BORDER, col=TEXT):
        return box(x, y, W, H, fill, stroke, r=10) + text(x + W / 2, y + 28, label, 13, col, 700)

    b = ''
    b += node(30, 24, t('Alert fatigue', 'Únava z výstrah'))
    b += node(540, 24, t('Anchoring', 'Ukotvenie'))
    b += node(285, 124, t('Automation bias', 'Automatizačná zaujatosť'), RED_BG, RED, RED)
    b += node(30, 226, t('Diffusion of responsibility', 'Rozptýlenie zodpovednosti'))
    b += node(285, 226, t('Complacency drift', 'Posun k sebauspokojeniu'))
    b += node(540, 226, t('Skill degradation', 'Degradácia zručností'))
    # arrows with verbs
    b += arrow(220, 60, 300, 122, 'red', 2) + text(232, 104, t('increases', 'zosilňuje'), 11, RED, 600, 'start', italic=True)
    b += arrow(540, 60, 460, 122, 'red', 2) + text(528, 104, t('reinforces', 'posilňuje'), 11, RED, 600, 'end', italic=True)
    b += arrow(220, 249, 283, 249, 'navy', 2) + text(252, 240, t('enables', 'umožňuje'), 11, NAVY, 600, italic=True)
    b += arrow(477, 249, 538, 249, 'navy', 2) + text(508, 240, t('accelerates', 'urýchľuje'), 11, NAVY, 600, italic=True)
    b += arrow(380, 172, 380, 224, 'gray', 1.6, '4 3') + text(392, 202, t('same root: a reliable system trains you to stop looking', 'spoločný koreň: spoľahlivý systém vás naučí prestať sa pozerať'), 10.5, MUTED, 400, 'start', italic=True)
    inner = svg(760, 296, b, t('How the cognitive phenomena at the seam reinforce each other', 'Ako sa kognitívne javy na šve navzájom posilňujú'))
    cap = t('Figure 4.1 · Five phenomena, one system. Fatigue and anchoring feed automation bias; diffused responsibility feeds complacency; complacency eats the skills that intervention assumes.',
            'Obrázok 4.1 · Päť javov, jeden systém. Únava a ukotvenie živia automatizačnú zaujatosť; rozptýlená zodpovednosť živí sebauspokojenie; sebauspokojenie požiera zručnosti, s ktorými zásah počíta.')
    return figure('bias-loop', inner, cap)


# ---------------------------------------------------------------------------
# 4. Order of information: verdict first vs. SBAR (Chapter 5)
# ---------------------------------------------------------------------------
def fig_sbar_order(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = text(30, 26, t('Verdict first', 'Najprv verdikt'), 13, RED, 700, 'start')
    # anchor cone
    b += f'<polygon points="176,58 700,30 700,98 176,70" fill="{RED}" opacity="0.08"/>'
    b += box(30, 40, 140, 48, RED_BG, RED) + lines(100, 60, [t('AI verdict', 'Verdikt AI'), t('"database overloaded"', '„databáza je preťažená“')], 11.5, RED, 600)
    b += arrow(170, 64, 212, 64, 'red')
    b += box(214, 40, 150, 48, GRAY_BG, BORDER) + lines(289, 60, [t('Evidence', 'Dôkazy'), t('read to confirm', 'čítané na potvrdenie')], 11.5, TEXT, 600)
    b += arrow(364, 64, 406, 64, 'red')
    b += box(408, 40, 130, 48, GRAY_BG, BORDER) + lines(473, 60, [t('Decision', 'Rozhodnutie'), t('follows the anchor', 'sleduje kotvu')], 11.5, TEXT, 600)
    b += text(560, 60, t('anchor', 'kotva'), 12, RED, 700, 'start', italic=True)
    b += text(560, 76, t('all that follows is read through it', 'všetko ďalšie sa číta cez ňu'), 10.5, RED, 400, 'start', italic=True)

    b += text(30, 140, t('Facts first: SBAR', 'Najprv fakty: SBAR'), 13, GREEN, 700, 'start')
    y = 154
    parts = [
        ('S', t('Situation', 'Situácia'), 30, 104, BLUE_BG, NAVY),
        ('B', t('Background', 'Pozadie'), 142, 104, BLUE_BG, NAVY),
    ]
    for k, lab, x, w, fill, col in parts:
        b += box(x, y, w, 48, fill, BORDER) + text(x + w / 2, y + 20, k, 13, col, 800) + text(x + w / 2, y + 37, lab, 11, col, 600)
    b += arrow(134, y + 24, 140, y + 24, 'navy', 1.5)
    b += arrow(246, y + 24, 260, y + 24, 'navy', 1.5)
    b += box(262, y, 150, 48, GREEN_BG, GREEN, dash='5 3') + lines(337, y + 20, [t('You form a view', 'Utvoríte si názor'), t('before any opinion', 'skôr než príde názor')], 11, GREEN, 600)
    b += arrow(412, y + 24, 426, y + 24, 'navy', 1.5)
    parts2 = [
        ('A', t('Assessment', 'Posúdenie'), 428, 110, GRAY_BG, TEXT),
        ('R', t('Recommendation', 'Odporúčanie'), 546, 116, GRAY_BG, TEXT),
    ]
    for k, lab, x, w, fill, col in parts2:
        b += box(x, y, w, 48, fill, BORDER) + text(x + w / 2, y + 20, k, 13, col, 800) + text(x + w / 2, y + 37, lab, 11, col, 600)
    b += arrow(538, y + 24, 544, y + 24, 'navy', 1.5)
    b += arrow(662, y + 24, 676, y + 24, 'navy', 1.5)
    b += box(678, y, 62, 48, GREEN_BG, GREEN) + lines(709, y + 20, [t('Your', 'Vaše'), t('decision', 'rozhodnutie')], 10.5, GREEN, 700)
    b += text(30, 232, t('The AI\'s opinion arrives last, after the person has seen what it saw. Two extensions for agents: cost of inaction, and links to the evidence.',
                        'Názor AI prichádza posledný, keď človek videl to, čo videla AI. Dve rozšírenia pre agentov: cena nečinnosti a odkazy na dôkazy.'), 11, MUTED, 400, 'start', italic=True)
    inner = svg(760, 246, b, t('Order of information: verdict first versus SBAR', 'Poradie informácií: najprv verdikt alebo SBAR'))
    cap = t('Figure 5.1 · The same facts in two orders. Once the verdict is read, the evidence is scanned for confirmation; in SBAR order the person meets the facts before the opinion.',
            'Obrázok 5.1 · Tie isté fakty v dvoch poradiach. Keď si človek prečíta verdikt, dôkazy už len hľadajú potvrdenie; v poradí SBAR sa s faktami stretne skôr než s názorom.')
    return figure('sbar-order', inner, cap)


# ---------------------------------------------------------------------------
# 5. Progressive disclosure: three layers (Chapter 5)
# ---------------------------------------------------------------------------
def fig_three_layers(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    rows = [
        (240, 280, 24, NAVY, '#fff', t('Layer 1 · 5 seconds', 'Vrstva 1 · 5 sekúnd'), t('severity · one sentence · one action', 'závažnosť · jedna veta · jeden krok'),
         t('Pattern recognition', 'Rozpoznanie vzoru'), t('act, or drill down', 'konať, alebo ísť hlbšie')),
        (150, 460, 90, '#93c5fd', NAVY, t('Layer 2 · 30 seconds', 'Vrstva 2 · 30 sekúnd'), t('SBAR brief · confidence · key metrics · recent changes', 'zadanie SBAR · istota · kľúčové metriky · nedávne zmeny'),
         t('Analytical reasoning', 'Analytické uvažovanie'), t('approve, modify, reject', 'schváliť, upraviť, odmietnuť')),
        (60, 640, 156, BLUE_BG, NAVY, t('Layer 3 · minutes to hours', 'Vrstva 3 · minúty až hodiny'), t('full evidence chain · reasoning · rejected hypotheses · history', 'celý reťazec dôkazov · uvažovanie · zamietnuté hypotézy · história'),
         t('Deep analysis', 'Hĺbková analýza'), t('root cause, post-incident review', 'koreňová príčina, revízia po incidente')),
    ]
    for x, w, y, fill, col, title, sub, mode, act in rows:
        b += box(x, y, w, 50, fill, 'none', r=8)
        b += text(x + w / 2, y + 20, title, 13, col, 700) + text(x + w / 2, y + 38, sub, 10.5, col, 400)
    # side labels
    b += text(20, 14, t('Mode', 'Režim'), 10, MUTED, 700, 'start', spacing='0.08em')
    b += text(740, 14, t('Decision', 'Rozhodnutie'), 10, MUTED, 700, 'end', spacing='0.08em')
    for (x, w, y, fill, col, title, sub, mode, act) in rows:
        b += text(20, y + 30, mode, 10.5, MUTED, 600, 'start')
        b += text(740, y + 30, act, 10.5, MUTED, 600, 'end')
    b += arrow(380, 76, 380, 88, 'gray', 1.4) + arrow(380, 142, 380, 154, 'gray', 1.4)
    inner = svg(760, 222, b, t('Progressive disclosure in three layers', 'Postupné odhaľovanie v troch vrstvách'))
    cap = t('Figure 5.2 · Three layers for three cognitive modes. Experts stop at layer 1 when the pattern is familiar; the deep dive exists for the cases where it is not, and for the review afterwards.',
            'Obrázok 5.2 · Tri vrstvy pre tri režimy myslenia. Expert sa zastaví na prvej vrstve, keď je vzor známy; hĺbková vrstva je pre prípady, keď nie je, a pre revíziu potom.')
    return figure('three-layers', inner, cap)


# ---------------------------------------------------------------------------
# 6. Trust calibration chart (Chapter 6)
# ---------------------------------------------------------------------------
def fig_trust_calibration(lang):
    t = lambda en, sk: _t(lang, en, sk)
    ox, oy, ex, ey = 90, 270, 700, 40
    b = ''
    # regions
    b += f'<polygon points="{ox},{oy} {ox},{ey} {ex},{ey}" fill="{RED}" opacity="0.06"/>'
    b += f'<polygon points="{ox},{oy} {ex},{oy} {ex},{ey}" fill="{AMBER}" opacity="0.08"/>'
    # axes
    b += f'<line x1="{ox}" y1="{oy}" x2="{ex + 20}" y2="{oy}" stroke="{TEXT}" stroke-width="1.5" marker-end="url(#ah-gray)"/>'
    b += f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{ey - 20}" stroke="{TEXT}" stroke-width="1.5" marker-end="url(#ah-gray)"/>'
    b += text((ox + ex) / 2, oy + 28, t('What the system can actually do (per task type)', 'Čo systém naozaj dokáže (podľa typu úlohy)'), 12, TEXT, 600)
    b += f'<text x="{ox - 14}" y="{(oy + ey) / 2}" font-size="12" fill="{TEXT}" font-weight="600" text-anchor="middle" transform="rotate(-90 {ox - 14} {(oy + ey) / 2})">{esc(t("How much the operator trusts it", "Ako veľmi mu operátor dôveruje"))}</text>'
    # diagonal
    b += f'<line x1="{ox}" y1="{oy}" x2="{ex}" y2="{ey}" stroke="{NAVY}" stroke-width="2.5"/>'
    b += f'<text x="560" y="88" font-size="12.5" fill="{NAVY}" font-weight="700" transform="rotate(-20.6 560 88)">{esc(t("Calibrated: trust tracks capability", "Kalibrované: dôvera sleduje schopnosť"))}</text>'
    # labels of regions
    b += lines(200, 80, [t('Overtrust', 'Nadmerná dôvera'), t('automation bias, complacency,', 'automatizačná zaujatosť, sebauspokojenie,'), t('rubber stamps', 'gumové pečiatky')], 12, RED, 700, 'middle', 15)
    b += lines(590, 210, [t('Undertrust', 'Nedostatočná dôvera'), t('disuse, duplicated work,', 'nepoužívanie, dvojitá práca,'), t('value thrown away', 'zahodená hodnota')], 12, AMBER, 700, 'middle', 15)
    # example dots
    b += f'<circle cx="300" cy="100" r="6" fill="{RED}"/>' + text(312, 104, t('"It said 87%, so it must be right"', '„Napísalo 87 %, tak to bude pravda“'), 10.5, RED, 400, 'start', italic=True)
    b += f'<circle cx="520" cy="230" r="6" fill="{AMBER}"/>' + text(508, 234, t('"I re-check everything anyway"', '„Aj tak si všetko prekontrolujem“'), 10.5, AMBER, 400, 'end', italic=True)
    b += f'<circle cx="420" cy="145" r="6" fill="{NAVY}"/>' + text(432, 149, t('verifies at 60%, acts at 99%', 'pri 60 % overuje, pri 99 % koná'), 10.5, NAVY, 600, 'start')
    b += text(ox + 4, ey - 26, t('Trust drops in one failure and rebuilds over many successes. Repair it with explanations, not apologies.', 'Dôvera padne jedným zlyhaním a rastie mnohými úspechmi. Opravujte ju vysvetlením, nie ospravedlnením.'), 10.5, MUTED, 400, 'start', italic=True)
    inner = svg(760, 310, b, t('Trust calibration: trust should track capability', 'Kalibrácia dôvery: dôvera má sledovať schopnosť'))
    cap = t('Figure 6.1 · The goal is the diagonal, not the top. Above it, the operator stops checking; below it, the system is ignored. Both are failure modes, and both are measurable through override rates by confidence band.',
            'Obrázok 6.1 · Cieľom je diagonála, nie vrchol. Nad ňou operátor prestane kontrolovať; pod ňou systém ignoruje. Oboje sú zlyhania a oboje sa dajú merať mierou prepísania podľa pásma istoty.')
    return figure('trust-calibration', inner, cap)


# ---------------------------------------------------------------------------
# 7. Swiss cheese model (Chapter 7)
# ---------------------------------------------------------------------------
def fig_swiss_cheese(lang):
    t = lambda en, sk: _t(lang, en, sk)
    labels = [t('Model', 'Model'), t('Application', 'Aplikácia'), t('Interface', 'Rozhranie'), t('Operator', 'Operátor'), t('Organization', 'Organizácia'), t('Infrastructure', 'Infraštruktúra')]
    subs = [t('alignment, filters', 'zladenie, filtre'), t('RAG checks, thresholds', 'kontroly RAG, prahy'), t('uncertainty, friction', 'neistota, trenie'),
            t('calibrated trust', 'kalibrovaná dôvera'), t('incident review', 'revízia incidentov'), t('kill switch, breakers', 'vypínač, ističe')]
    b = ''
    HY = 150
    for i in range(6):
        x = 70 + i * 108
        b += f'<polygon points="{x},70 {x + 62},50 {x + 62},250 {x},270" fill="#fde68a" stroke="{AMBER}" stroke-width="1.5"/>'
        # decorative holes
        for (hx, hy, r) in ((x + 18, 100, 7), (x + 44, 205, 9), (x + 22, 235, 5)):
            b += f'<circle cx="{hx}" cy="{hy}" r="{r}" fill="#fff" stroke="{AMBER}" stroke-width="1"/>'
        if i < 5:
            b += f'<circle cx="{x + 31}" cy="{HY}" r="11" fill="#fff" stroke="{AMBER}" stroke-width="1"/>'
        b += text(x + 31, 292, labels[i], 11.5, TEXT, 700)
        b += text(x + 31, 306, subs[i], 9.5, MUTED, 400)
    # hazard arrow through aligned holes, stopped at the last slice
    b += f'<line x1="14" y1="{HY}" x2="{70 + 5 * 108 + 2}" y2="{HY}" stroke="{RED}" stroke-width="3" stroke-dasharray="8 5"/>'
    b += text(14, HY - 12, t('hazard', 'hrozba'), 11, RED, 700, 'start')
    hx = 70 + 5 * 108 + 31
    b += f'<circle cx="{hx}" cy="{HY}" r="12" fill="{GREEN}" stroke="#fff" stroke-width="2"/>'
    b += f'<path d="M{hx - 5},{HY} l4,4 l7,-8" fill="none" stroke="#fff" stroke-width="2.5"/>'
    b += text(hx + 26, HY + 4, t('caught', 'zachytené'), 11, GREEN, 700, 'start')
    b += text(30, 30, t('Every layer has holes. An accident needs them all to line up. Never remove a layer because another one "should" catch it.', 'Každá vrstva má diery. Nehoda potrebuje, aby sa všetky zoradili. Nikdy neodstraňujte vrstvu, lebo iná „by to mala“ zachytiť.'), 11.5, MUTED, 400, 'start', italic=True)
    inner = svg(760, 316, b, t('The Swiss cheese model applied to AI operations', 'Model švajčiarskeho syra uplatnený na prevádzku AI'))
    cap = t('Figure 7.1 · Defense in depth. The hazard passes five aligned holes and is stopped by the sixth layer, the one that does not depend on anyone\'s vigilance.',
            'Obrázok 7.1 · Obrana do hĺbky. Hrozba prejde piatimi zoradenými dierami a zastaví ju šiesta vrstva, tá, ktorá nezávisí od ničej ostražitosti.')
    return figure('swiss-cheese', inner, cap)


# ---------------------------------------------------------------------------
# 8. Circuit breaker state machine (Chapters 7 and 8)
# ---------------------------------------------------------------------------
def fig_circuit_breaker(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    states = [(140, 'CLOSED', GREEN, GREEN_BG, t('normal operation', 'bežná prevádzka'), t('failures counted', 'zlyhania sa počítajú')),
              (380, 'OPEN', RED, RED_BG, t('all requests go to', 'všetky požiadavky idú'), t('the fallback path', 'na záložnú cestu')),
              (620, 'HALF_OPEN', AMBER, AMBER_BG, t('one test request', 'jedna testovacia'), t('to the primary path', 'požiadavka na hlavnú cestu'))]
    for x, name, col, bg, s1, s2 in states:
        b += f'<circle cx="{x}" cy="110" r="46" fill="{bg}" stroke="{col}" stroke-width="2.5"/>'
        b += text(x, 115, name, 13, col, 800)
        b += lines(x, 178, [s1, s2], 10.5, MUTED, 400)
    b += path_arrow('M186,90 C240,50 280,50 334,90', 'red', 2) + text(260, 52, t('threshold exceeded', 'prekročený prah'), 11, RED, 600)
    b += path_arrow('M426,90 C480,50 520,50 574,90', 'amber', 2) + text(500, 52, t('timeout elapsed', 'uplynul časový limit'), 11, AMBER, 600)
    b += path_arrow('M574,130 C480,205 280,205 186,130', 'green', 2) + text(380, 224, t('test succeeds: back to normal, counter reset', 'test uspeje: späť do normálu, počítadlo na nulu'), 11, GREEN, 600)
    b += path_arrow('M582,136 C540,175 460,175 424,138', 'red', 1.8, '5 3') + text(503, 172, t('test fails: timeout doubles', 'test zlyhá: limit sa zdvojnásobí'), 10.5, RED, 600)
    inner = svg(760, 236, b, t('Circuit breaker state machine', 'Stavový automat ističa'))
    cap = t('Figure 8.2 · One state machine at three levels: the LLM API, every tool the agent calls, and the quality of the agent\'s own outputs. Only the thresholds and fallbacks differ.',
            'Obrázok 8.2 · Jeden stavový automat na troch úrovniach: API jazykového modelu, každý nástroj, ktorý agent volá, a kvalita jeho vlastných výstupov. Líšia sa len prahy a záložné cesty.')
    return figure('circuit-breaker', inner, cap)


# ---------------------------------------------------------------------------
# 9. Kill switch architecture (Chapter 8)
# ---------------------------------------------------------------------------
def fig_kill_switch_architecture(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    # operator interface
    b += box(120, 16, 520, 76, GRAY_BG, BORDER, r=10)
    b += text(140, 38, t('OPERATOR INTERFACE', 'ROZHRANIE OPERÁTORA'), 10.5, MUTED, 700, 'start', spacing='0.08em')
    b += box(140, 48, 130, 32, RED, '#991b1b', r=6, sw=2) + text(205, 69, 'KILL SWITCH', 12, '#fff', 800)
    b += text(285, 62, t('always visible · no confirmation dialog', 'vždy viditeľný · bez potvrdzovacieho okna'), 11, TEXT, 600, 'start')
    b += text(285, 78, t('one action, audit-logged with who and why', 'jeden úkon, zapísaný do audit logu s kým a prečo'), 10.5, MUTED, 400, 'start')
    b += arrow(380, 92, 380, 118, 'navy', 2) + text(392, 110, t('flips the flag', 'prepne príznak'), 10.5, NAVY, 600, 'start')
    # control plane
    b += box(120, 120, 520, 96, BLUE_BG, ACCENT, r=10)
    b += text(140, 142, t('INFRASTRUCTURE CONTROL PLANE · external to the agent process', 'INFRAŠTRUKTÚRNA RIADIACA VRSTVA · mimo procesu agenta'), 10.5, ACCENT, 700, 'start', spacing='0.06em')
    b += box(140, 154, 200, 46, '#fff', BORDER, r=6) + text(240, 173, 'agent_enabled', 12, NAVY, 700) + text(240, 191, 'true / false', 12, TEXT, 400)
    b += box(360, 154, 260, 46, '#fff', BORDER, r=6) + text(490, 173, t('append-only audit log', 'audit log len na pripisovanie'), 12, NAVY, 700) + text(490, 191, t('every state change: time, operator, reason', 'každá zmena stavu: čas, operátor, dôvod'), 10.5, TEXT, 400)
    b += arrow(240, 216, 240, 244, 'navy', 2) + text(252, 236, t('read only', 'len na čítanie'), 10.5, NAVY, 600, 'start')
    # agent process
    b += box(120, 246, 520, 76, GRAY_BG, BORDER, r=10)
    b += text(140, 268, t('AI AGENT PROCESS', 'PROCES AI AGENTA'), 10.5, MUTED, 700, 'start', spacing='0.08em')
    b += text(140, 288, t('checks agent_enabled before every LLM call and every tool call', 'pred každým volaním modelu a nástroja skontroluje agent_enabled'), 11.5, TEXT, 600, 'start')
    b += text(140, 306, t('cannot write the flag · cannot read or modify the audit log · queued actions are drained on stop', 'nemôže príznak zapísať · nemôže čítať ani meniť audit log · pri zastavení sa fronta vyprázdni'), 10.5, MUTED, 400, 'start')
    # forbidden write path
    b += f'<line x1="560" y1="246" x2="560" y2="218" stroke="{RED}" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#ah-red)"/>'
    b += f'<line x1="548" y1="240" x2="572" y2="224" stroke="{RED}" stroke-width="3"/><line x1="548" y1="224" x2="572" y2="240" stroke="{RED}" stroke-width="3"/>'
    b += text(578, 236, t('no write path', 'žiadna cesta na zápis'), 10.5, RED, 700, 'start')
    inner = svg(760, 334, b, t('Kill switch architecture', 'Architektúra vypínača'))
    cap = t('Figure 8.3 · The flag lives where the agent cannot reach it. The agent reads it before every call; only a person can flip it; the log outlives the agent.',
            'Obrázok 8.3 · Príznak žije tam, kam agent nedosiahne. Agent ho číta pred každým volaním; prepnúť ho môže len človek; log prežije agenta.')
    return figure('kill-switch-architecture', inner, cap)


# ---------------------------------------------------------------------------
# 10. The decision logic: consequence x reversibility (Chapter 8)
# ---------------------------------------------------------------------------
def fig_four_dials(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    cols = [(250, t('Reversible', 'Vratný'), GREEN), (490, t('Irreversible', 'Nevratný'), RED)]
    rows = [(70, t('Low consequence', 'Nízky dôsledok')), (132, t('Medium consequence', 'Stredný dôsledok')), (194, t('High consequence', 'Vysoký dôsledok'))]
    for x, lab, col in cols:
        b += text(x + 115, 52, lab, 12.5, col, 700)
    b += text(140, 52, t('If the action is wrong...', 'Ak je krok nesprávny...'), 11, MUTED, 600)
    for y, lab in rows:
        b += text(232, y + 32, lab, 12, TEXT, 700, 'end')
    cells = {
        (0, 0): (t('Execute & Report', 'Vykonať a hlásiť'), t('level 7, if also time-critical', 'úroveň 7, ak aj časovo kritický'), GREEN_BG, GREEN),
        (0, 1): (t('Recommend & Wait', 'Odporučiť a čakať'), t('level 4', 'úroveň 4'), BLUE_BG, ACCENT),
        (1, 0): (t('Recommend & Wait or Execute & Report', 'Odporučiť a čakať alebo Vykonať a hlásiť'), t('decided by calibrated confidence', 'rozhoduje kalibrovaná istota'), AMBER_BG, AMBER),
        (1, 1): (t('Recommend & Wait', 'Odporučiť a čakať'), t('level 4', 'úroveň 4'), BLUE_BG, ACCENT),
        (2, 0): (t('Recommend & Wait, pre-staged', 'Odporučiť a čakať, s pripraveným krokom'), t('level 5, when time is critical', 'úroveň 5, keď je čas kritický'), BLUE_BG, ACCENT),
        (2, 1): (t('Recommend & Wait, always', 'Odporučiť a čakať, vždy'), t('regardless of time pressure', 'bez ohľadu na časový tlak'), BLUE_BG, NAVY),
    }
    for (r, c), (main, sub, fill, stroke) in cells.items():
        x = cols[c][0]
        y = rows[r][0]
        b += box(x, y, 230, 52, fill, stroke, r=8)
        b += text(x + 115, y + 22, main, 10.2 if len(main) > 30 else 11.5, TEXT, 700) + text(x + 115, y + 40, sub, 10, MUTED, 400)
    b += box(40, 262, 680, 34, RED_BG, RED, r=8)
    b += text(380, 284, t('Low calibrated confidence: Recommend & Wait, whatever the row and column.', 'Nízka kalibrovaná istota: Odporučiť a čakať, nech je riadok a stĺpec akýkoľvek.'), 12, RED, 700)
    inner = svg(760, 308, b, t('Pattern selection by consequence and reversibility', 'Výber vzoru podľa dôsledku a vratnosti'))
    cap = t('Figure 8.1 · Four dials, one table. Consequence and reversibility pick the row and column, time sensitivity moves you within a cell, and low confidence overrides everything.',
            'Obrázok 8.1 · Štyri regulátory, jedna tabuľka. Dôsledok a vratnosť vyberú riadok a stĺpec, časová citlivosť hýbe vnútri bunky a nízka istota prebije všetko.')
    return figure('four-dials', inner, cap)


# ---------------------------------------------------------------------------
# 11. The three-lines model with a named owner (Chapter 9)
# ---------------------------------------------------------------------------
def fig_three_lines(lang):
    t = lambda en, sk: _t(lang, en, sk)
    b = ''
    cols = [
        (40, t('First line', 'Prvá línia'), t('Application teams', 'Aplikačné tímy'), [t('build, deploy, operate', 'stavajú, nasadzujú, prevádzkujú'), t('prompts, thresholds,', 'prompty, prahy,'), t('incident response', 'reakcia na incidenty')], BLUE_BG, ACCENT),
        (275, t('Second line', 'Druhá línia'), t('Risk and compliance', 'Riziká a compliance'), [t('set the standards', 'určujú štandardy'), t('review designs', 'revidujú návrhy'), t('monitor adherence', 'sledujú dodržiavanie')], GRAY_BG, BORDER),
        (510, t('Third line', 'Tretia línia'), t('Independent audit', 'Nezávislý audit'), [t('checks that lines 1 and 2', 'overuje, že línie 1 a 2'), t('actually work,', 'naozaj fungujú,'), t('not just on paper', 'nie len na papieri')], GRAY_BG, BORDER),
    ]
    for x, kicker, title, rows, fill, stroke in cols:
        b += box(x, 60, 210, 118, fill, stroke, r=10)
        b += text(x + 105, 80, kicker, 10, MUTED, 700, spacing='0.08em')
        b += text(x + 105, 100, title, 13.5, NAVY, 800)
        b += lines(x + 105, 122, rows, 11, TEXT, 400, 'middle', 15)
    b += arrow(250, 119, 273, 119, 'navy', 1.8) + arrow(485, 119, 508, 119, 'navy', 1.8)
    b += text(262, 108, t('escalates', 'eskaluje'), 9.5, NAVY, 600) + text(497, 108, t('assures', 'uisťuje'), 9.5, NAVY, 600)
    # named owner badge
    b += box(60, 14, 250, 34, RED_BG, RED, r=17, sw=1.5)
    b += text(185, 36, t('Named owner: one person, can shut it down', 'Pomenovaný vlastník: jeden človek, môže systém vypnúť'), 11.5, RED, 700)
    b += arrow(150, 48, 150, 60, 'red', 1.6)
    # cadence strip
    b += box(40, 196, 680, 34, GREEN_BG, GREEN, r=8)
    b += text(380, 218, t('Cadence: weekly 30-minute triage · monthly metrics and calibration · quarterly risk-tier review, chair rotates', 'Rytmus: týždenná 30-minútová triáž · mesačné metriky a kalibrácia · štvrťročná revízia rizikových úrovní, predseda rotuje'), 11.5, GREEN, 700)
    inner = svg(760, 244, b, t('The three-lines model with a named owner', 'Model troch línií s pomenovaným vlastníkom'))
    cap = t('Figure 9.1 · Diffuse ownership is the most common governance failure. One named person, three lines behind them, and a calendar that keeps the review alive.',
            'Obrázok 9.1 · Rozptýlené vlastníctvo je najčastejšie zlyhanie governance. Jeden pomenovaný človek, tri línie za ním a kalendár, ktorý udrží revíziu pri živote.')
    return figure('three-lines', inner, cap)


FIGURES = {
    'naive-vs-designed': fig_naive_vs_designed,
    'autonomy-ladder': fig_autonomy_ladder,
    'bias-loop': fig_bias_loop,
    'sbar-order': fig_sbar_order,
    'three-layers': fig_three_layers,
    'trust-calibration': fig_trust_calibration,
    'swiss-cheese': fig_swiss_cheese,
    'circuit-breaker': fig_circuit_breaker,
    'kill-switch-architecture': fig_kill_switch_architecture,
    'four-dials': fig_four_dials,
    'three-lines': fig_three_lines,
}


def render(name, lang='en'):
    return FIGURES[name](lang)


if __name__ == '__main__':
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else 'en'
    body = ''.join(f'<h2>{n}</h2>{render(n, lang)}' for n in FIGURES)
    print('<!doctype html><meta charset="utf-8"><style>body{font-family:-apple-system,Helvetica,Arial,sans-serif;max-width:780px;margin:2rem auto}'
          '.figure{margin:1rem 0}.figure svg{width:100%;height:auto}figcaption{font-size:.85rem;color:#64748b}</style>' + body)
