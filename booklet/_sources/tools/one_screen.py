"""'In one screen' summary cards, one per chapter, in English and Slovak.

build_html.py inserts CARDS[lang][chapter_number] right after the chapter's <h1>. Each card is
what Robert scrolls to when someone asks "what does this chapter say?" during a lecture: one
claim, a handful of one-line points, and the numbers or cases that carry the chapter.
Numbers and cases are copied from the fact-checked chapter text; keep them in sync.
"""

CARDS = {
    'en': {
        1: dict(
            claim='The seam is the control surface, not a UX nicety.',
            points=[
                'Agents now act, not just suggest. A bad decision costs at the moment it is made, not when a human gets round to it.',
                'Bainbridge\'s irony (1983): the more reliable the automation, the less practiced the human who must catch its failure.',
                'AF447: the humans at the seam could not perform. 737 MAX: the seam stopped the humans from overriding. Both map onto agent design.',
                'The seam is six decisions: what the agent does alone, how it communicates, what the human sees, how much time they have, what controls they hold, how the system degrades.',
            ],
            facts=['228 dead (AF447)', '346 dead (737 MAX)', 'Copilot: 1 in 5 code reviews'],
        ),
        2: dict(
            claim='"We\'ll just put a human in the loop" is a hypothesis, and the evidence is against its naive form.',
            points=[
                'Meta-analysis of 106 studies: human plus AI performs worse than the better of the two alone, and loses exactly when the AI is the stronger member.',
                'Oversight mandates fail in practice and legitimize the systems they supervise (Green, 41 policies).',
                'The moral crumple zone: the human absorbs the blame for a system they could not really control.',
                'Agent streams add approval fatigue: over 40% of experienced sessions run in full auto-approve mode.',
                'Article 14 asks for a seam designed so oversight can work, not for a person with a stamp. Annex III duties apply from 2 December 2027.',
            ],
            facts=['106 studies, 370 effect sizes', '41 oversight policies', '>40% auto-approve'],
        ),
        3: dict(
            claim='Five patterns, one rule: start with Recommend & Wait and design the movement between levels from day one.',
            points=[
                'Recommend & Wait (levels 4 to 5), Triage & Escalate (3 to 5), Execute & Report (7 to 8), Draft & Refine (5), Graduated Autonomy (moves).',
                'Choose by four dimensions: risk of the action, time available, operator expertise, reversibility.',
                'Dynamic downshifting: when the situation looks unfamiliar, the agent drops a level and asks.',
                'Levels are the entry tool. The upgrade path is teaming: common ground, observable intent, directability mid-task.',
            ],
            facts=['Sepsis AI: 82% caught, mortality -18.7% relative', '2,992 SOC alerts/day, 63% unaddressed'],
        ),
        4: dict(
            claim='Five predictable failures of the human at the seam. None of them is a character flaw.',
            points=[
                'Automation bias: every participant followed wrong automated advice at least once; a second crew member did not help (Mosier, Skitka, Heers & Burdick, 1998).',
                'Alert fatigue: 72 to 99% of clinical alarms are false; 63% of SOC alerts go unaddressed. Boston Medical cut alarms by 89% with no harm to patients.',
                'Anchoring: 775 managers, warned in advance, still anchored on the AI\'s number.',
                'Complacency drift: Royal Majesty sailed 34 hours off course past every contradicting signal.',
                'The countermeasure people like least works best: write your own view before you see the AI\'s.',
            ],
            facts=['100% commission errors', '736 wrongful prosecutions', '17 hours of ignored alarms'],
        ),
        5: dict(
            claim='Format is load-bearing: the same facts in a different order produce a different decision.',
            points=[
                'SBAR order (situation, background, assessment, recommendation) plus two agent extensions: cost of inaction and links to evidence.',
                'Experts pattern-match: about 80% of fireground decisions involved no comparison of options. Show one recommendation first, alternatives on demand.',
                'Three layers: a 5-second glance, a 30-second SBAR brief, a deep dive for the review.',
                'Confidence as categories tied to behaviour ("verify, then act"), not decimals that no one can use.',
                'Under time pressure overreliance rises. Adapt the format to the urgency instead of pretending it is constant.',
            ],
            facts=['4.8% to 92.8% adequate handoffs', '~80% no comparison of options', '3 layers: 5 s, 30 s, minutes'],
        ),
        6: dict(
            claim='Calibrate trust, don\'t maximize it. Both overtrust and undertrust are failure modes.',
            points=[
                'Three bases (Lee & See): performance, process, purpose. Each can be miscalibrated on its own.',
                'Three layers (Hoff & Bashir): dispositional, situational (inflates under pressure: add friction there), learned (dominates fast: onboarding sets it).',
                '"I\'m not sure, but..." lowered confidence and raised decision accuracy (Kim et al., N=404).',
                'Track record dashboards: accuracy by action type, error logs, escalation history, trends, human baseline.',
                'Trust breaks in one failure and rebuilds over many. Repair with explanation, not apology. Measure with override rates by confidence band.',
            ],
            facts=['N=404', '1.7% overrides at 90 to 99% confidence'],
        ),
        7: dict(
            claim='Every agent will fail. Design so it fails visibly, containably and recoverably.',
            points=[
                'Hallucination is structural: 33 to 79% on open recall benchmarks, 0.7 to 3.3% for grounded RAG. The stack: RAG validation, chain-of-verification, a second model, confidence gates.',
                'Confidently wrong at scale: Watson\'s bevacizumab test case, Zillow\'s $880 million, Bard\'s $100 billion day.',
                'Kill switch, five requirements: always visible, no confirmation, immediately effective, external to the AI, audit-logged.',
                'Circuit breakers (closed, open, half-open), a fallback stack from L1 to L5, and Swiss cheese layers that nobody removes.',
            ],
            facts=['Knight Capital: 45 min, $460M+, 97 unread emails', 'o3 sabotaged shutdown in 79 of 100 runs'],
        ),
        8: dict(
            claim='From principle to artifact: prompts, worksheets and thresholds you can take into production on Monday.',
            points=[
                'Three prompt templates: SBAR output, first-person uncertainty below a threshold, categorical confidence with one reasoning sentence.',
                'Action classification: consequence and reversibility pick the pattern; time moves you within it; low calibrated confidence means Recommend & Wait, always.',
                'Circuit breakers at three levels (LLM API, each tool, quality gate) with starting thresholds and a quality-gate downshift.',
                'Kill switch architecture: a flag in infrastructure the agent reads before every call and can never write.',
                'Calibration workflow: 200 recommendations in Recommend & Wait, build the curve, set the thresholds, repeat monthly and after every model change.',
            ],
            facts=['200 recommendations minimum', '10-question readiness worksheet', 'kill switch tested monthly'],
        ),
        9: dict(
            claim='Governance decides whether good design survives contact with reality.',
            points=[
                'Three lines (build, review, audit) and one named owner who is authorized to shut the system down.',
                'Cadence: weekly 30-minute triage, monthly metrics and calibration, quarterly risk-tier review.',
                'Incident review within 24 to 48 hours, traced by correlation IDs, root causes in five categories: prompt, guardrail gap, data, permission scope, multi-agent.',
                'Article 14(4) a to e: observability, bias awareness, interpretability, override, stop button. Older domains already got there: ASRS, FDA CDS, MiFID II "kill functionality".',
                'Maturity pays: 20% of low-maturity AI projects survive three years, 45% of high-maturity ones.',
            ],
            facts=['Annex III from 2 December 2027', '20% vs 45% three-year survival', 'AI Incident Database >1,500'],
        ),
        10: dict(
            claim='Three principles and a Monday morning.',
            points=[
                'Design the seam, don\'t eliminate it. Support the human\'s cognition, don\'t replace it. Build for failure, not just success.',
                'Monday: audit one AI-to-human handoff, apply the selection matrix, add an external kill switch, measure override rates by confidence, put a 30-minute review on the calendar.',
                'None of it needs new budget. It needs attention, intention, and the recognition that the seam is the most important surface in the system.',
            ],
            facts=['5 steps', '0 new tools required'],
        ),
    },
    'sk': {
        1: dict(
            claim='Šev je riadiaca plocha, nie kozmetika používateľského rozhrania.',
            points=[
                'Agenti dnes konajú, nielen navrhujú. Zlé rozhodnutie stojí peniaze v okamihu, keď vznikne, nie keď sa k nemu dostane človek.',
                'Bainbridgeovej irónia (1983): čím spoľahlivejšia automatizácia, tým menej natrénovaný človek, ktorý má zachytiť jej zlyhanie.',
                'AF447: ľudia na šve nedokázali konať. 737 MAX: šev ľuďom zabránil prevziať riadenie. Oboje sa prenáša na návrh agentov.',
                'Šev je šesť rozhodnutí: čo agent robí sám, ako komunikuje, čo človek vidí, koľko má času, aké má ovládacie prvky, ako systém degraduje.',
            ],
            facts=['228 mŕtvych (AF447)', '346 mŕtvych (737 MAX)', 'Copilot: 1 z 5 revízií kódu'],
        ),
        2: dict(
            claim='„Dáme tam človeka do slučky“ je hypotéza a dôkazy hovoria proti jej naivnej podobe.',
            points=[
                'Metaanalýza 106 štúdií: človek plus AI je horší než lepší z dvojice sám, a prehráva presne vtedy, keď je silnejším členom AI.',
                'Povinný dohľad v praxi zlyháva a zároveň legitimizuje systémy, ktoré má strážiť (Green, 41 politík).',
                'Morálna deformačná zóna: človek pohltí vinu za systém, ktorý v skutočnosti neovládal.',
                'Prúd krokov agenta pridáva únavu zo schvaľovania: vyše 40 % skúsených relácií beží v plne automatickom schvaľovaní.',
                'Článok 14 žiada šev navrhnutý tak, aby dohľad mohol fungovať, nie človeka s pečiatkou. Povinnosti prílohy III platia od 2. decembra 2027.',
            ],
            facts=['106 štúdií, 370 veľkostí účinku', '41 politík dohľadu', '>40 % automatické schvaľovanie'],
        ),
        3: dict(
            claim='Päť vzorov, jedno pravidlo: začnite vzorom Odporučiť a čakať a pohyb medzi úrovňami navrhnite od prvého dňa.',
            points=[
                'Odporučiť a čakať (úrovne 4 až 5), Triediť a eskalovať (3 až 5), Vykonať a hlásiť (7 až 8), Navrhnúť a doladiť (5), Odstupňovaná autonómia (pohyblivá).',
                'Vyberajte podľa štyroch rozmerov: riziko kroku, dostupný čas, odbornosť operátora, vratnosť.',
                'Dynamické preraďovanie nadol: keď situácia vyzerá neznámo, agent klesne o úroveň a pýta sa.',
                'Úrovne sú vstupný nástroj. Cesta ďalej je tímová spolupráca: spoločný obraz situácie, pozorovateľný zámer, riaditeľnosť počas úlohy.',
            ],
            facts=['AI na sepsu: 82 % zachytených, úmrtnosť -18,7 % relatívne', '2 992 výstrah SOC denne, 63 % bez riešenia'],
        ),
        4: dict(
            claim='Päť predvídateľných zlyhaní človeka na šve. Ani jedno nie je chyba charakteru.',
            points=[
                'Automatizačná zaujatosť: každý účastník aspoň raz poslúchol nesprávnu automatickú radu; druhý člen posádky nepomohol (Mosier, Skitka, Heers a Burdick, 1998).',
                'Únava z výstrah: 72 až 99 % klinických alarmov je falošných; 63 % výstrah SOC ostáva bez riešenia. Boston Medical znížil alarmy o 89 % bez ujmy pre pacientov.',
                'Ukotvenie: 775 manažérov, vopred varovaných, sa aj tak ukotvilo na čísle od AI.',
                'Posun k sebauspokojeniu: Royal Majesty plávala 34 hodín mimo kurzu popri všetkých protirečiacich signáloch.',
                'Protiopatrenie, ktoré majú ľudia najmenej radi, funguje najlepšie: napíšte svoj názor skôr, než uvidíte názor AI.',
            ],
            facts=['100 % chýb konania', '736 nespravodlivých stíhaní', '17 hodín ignorovaných alarmov'],
        ),
        5: dict(
            claim='Formát je nosný prvok: tie isté fakty v inom poradí vedú k inému rozhodnutiu.',
            points=[
                'Poradie SBAR (situácia, pozadie, posúdenie, odporúčanie) plus dve rozšírenia pre agentov: cena nečinnosti a odkazy na dôkazy.',
                'Experti rozpoznávajú vzory: asi 80 % rozhodnutí veliteľov pri požiari neporovnávalo možnosti. Ukážte jedno odporúčanie ako prvé, alternatívy na požiadanie.',
                'Tri vrstvy: päťsekundový pohľad, tridsaťsekundové zadanie SBAR, hĺbková vrstva pre revíziu.',
                'Istota ako kategórie naviazané na správanie („overte, potom konajte“), nie desatinné čísla, ktoré nikto nevie použiť.',
                'Pod časovým tlakom nadmerné spoliehanie rastie. Prispôsobte formát naliehavosti, namiesto predstierania, že je stála.',
            ],
            facts=['4,8 % až 92,8 % primeraných odovzdaní', '~80 % bez porovnania možností', '3 vrstvy: 5 s, 30 s, minúty'],
        ),
        6: dict(
            claim='Dôveru kalibrujte, nemaximalizujte. Nadmerná aj nedostatočná dôvera sú zlyhania.',
            points=[
                'Tri základy (Lee a See): výkon, proces, účel. Každý sa dá pokaziť samostatne.',
                'Tri vrstvy (Hoff a Bashir): dispozičná, situačná (pod tlakom rastie: práve tam pridajte trenie), naučená (rýchlo prevládne: nastaví ju onboarding).',
                '„Nie som si istý, ale...“ znížilo istotu a zvýšilo presnosť rozhodnutí (Kim a kol., N = 404).',
                'Dashboardy záznamu o výkone: presnosť podľa typu kroku, logy chýb, história eskalácií, trendy, ľudská základná úroveň.',
                'Dôvera padne jedným zlyhaním a rastie mnohými. Opravujte vysvetlením, nie ospravedlnením. Merajte mierou prepísania podľa pásma istoty.',
            ],
            facts=['N = 404', '1,7 % prepísaní pri istote 90 až 99 %'],
        ),
        7: dict(
            claim='Každý agent zlyhá. Navrhnite ho tak, aby zlyhal viditeľne, ohraničene a napraviteľne.',
            points=[
                'Halucinácia je štrukturálna: 33 až 79 % na otvorených benchmarkoch, 0,7 až 3,3 % pri ukotvenom RAG. Stack: overenie RAG, reťazec overovania, druhý model, prahy istoty.',
                'Sebaisto nesprávne vo veľkom: testovací prípad bevacizumabu vo Watsone, 880 miliónov dolárov v Zillow, deň za 100 miliárd v Barde.',
                'Vypínač, päť požiadaviek: vždy viditeľný, bez potvrdenia, okamžite účinný, mimo dosahu AI, zapísaný v audit logu.',
                'Ističe (zatvorený, otvorený, polootvorený), záložný stack od L1 po L5 a vrstvy švajčiarskeho syra, ktoré nikto neodstraňuje.',
            ],
            facts=['Knight Capital: 45 min, 460+ mil. USD, 97 neprečítaných e-mailov', 'o3 sabotovalo vypnutie v 79 zo 100 behov'],
        ),
        8: dict(
            claim='Od princípu k výstupu: prompty, pracovné listy a prahy, ktoré si v pondelok odnesiete do prevádzky.',
            points=[
                'Tri šablóny promptov: výstup SBAR, neistota v prvej osobe pod prahom, kategorická istota s jednou vetou zdôvodnenia.',
                'Klasifikácia krokov: dôsledok a vratnosť vyberú vzor; čas vás posúva vnútri neho; nízka kalibrovaná istota znamená Odporučiť a čakať, vždy.',
                'Ističe na troch úrovniach (API modelu, každý nástroj, brána kvality) so štartovacími prahmi a preradením nadol pri poklese kvality.',
                'Architektúra vypínača: príznak v infraštruktúre, ktorý agent číta pred každým volaním a nikdy ho nemôže zapísať.',
                'Kalibračný postup: 200 odporúčaní v režime Odporučiť a čakať, krivka, prahy, opakovať mesačne a po každej zmene modelu.',
            ],
            facts=['minimálne 200 odporúčaní', 'pracovný list s 10 otázkami', 'vypínač testovaný mesačne'],
        ),
        9: dict(
            claim='Governance rozhoduje, či dobrý návrh prežije stret so skutočnosťou.',
            points=[
                'Tri línie (stavať, revidovať, auditovať) a jeden pomenovaný vlastník s právomocou systém vypnúť.',
                'Rytmus: týždenná 30-minútová triáž, mesačné metriky a kalibrácia, štvrťročná revízia rizikových úrovní.',
                'Revízia incidentu do 24 až 48 hodín, sledovaná cez korelačné ID, príčiny v piatich kategóriách: prompt, medzera v mantineloch, dáta, rozsah oprávnení, viacero agentov.',
                'Článok 14 ods. 4 písm. a až e: pozorovateľnosť, vedomie zaujatosti, interpretovateľnosť, prepísanie, tlačidlo stop. Staršie odvetvia tam už sú: ASRS, FDA CDS, „kill functionality“ v MiFID II.',
                'Zrelosť sa vypláca: tri roky prežije 20 % AI projektov v málo zrelých organizáciách a 45 % vo vysoko zrelých.',
            ],
            facts=['príloha III od 2. decembra 2027', '20 % vs 45 % trojročné prežitie', 'AI Incident Database >1 500'],
        ),
        10: dict(
            claim='Tri princípy a jedno pondelkové ráno.',
            points=[
                'Navrhnite šev, neodstraňujte ho. Podporte ľudské myslenie, nenahrádzajte ho. Stavajte pre zlyhanie, nielen pre úspech.',
                'Pondelok: zauditujte jedno odovzdanie z AI na človeka, použite maticu výberu, pridajte externý vypínač, merajte prepísania podľa istoty, dajte do kalendára 30-minútovú revíziu.',
                'Nič z toho nepotrebuje nový rozpočet. Potrebuje pozornosť, zámer a uznanie, že šev je najdôležitejšia plocha systému.',
            ],
            facts=['5 krokov', '0 nových nástrojov'],
        ),
    },
}

LABELS = {
    'en': dict(kicker='Chapter {n} in one screen', facts='The numbers that carry it'),
    'sk': dict(kicker='Kapitola {n} na jednu obrazovku', facts='Čísla, ktoré ju nesú'),
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def render_card(n, lang='en'):
    c = CARDS[lang][n]
    L = LABELS[lang]
    pts = ''.join(f'<li>{esc(p)}</li>' for p in c['points'])
    facts = ''.join(f'<span class="os-fact">{esc(f)}</span>' for f in c['facts'])
    return (f'<aside class="one-screen" aria-label="{esc(L["kicker"].format(n=n))}">'
            f'<div class="os-kicker">{esc(L["kicker"].format(n=n))}</div>'
            f'<p class="os-claim">{esc(c["claim"])}</p>'
            f'<ul class="os-points">{pts}</ul>'
            f'<div class="os-facts"><span class="os-facts-label">{esc(L["facts"])}</span>{facts}</div>'
            f'</aside>')
