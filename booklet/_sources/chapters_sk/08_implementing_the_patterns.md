# Kapitola 8: Implementácia vzorov

Predchádzajúce kapitoly opísali, čo postaviť a prečo. Táto kapitola opisuje, ako to postaviť. Každá časť produkuje výstup (šablónu promptu, rozhodovaciu tabuľku, konfiguráciu, pracovný postup alebo kontrolný zoznam), ktorý sa dá vziať priamo do produkčného systému. Cieľom nie je zopakovať teóriu, ale preložiť ju do implementácie.

*Poznámka k slovenskému vydaniu: šablóny promptov a ukážkové výstupy v blokoch kódu ponechávame v angličtine, tak ako by ste ich vložili do svojho systému; sprievodný text a tabuľky sú preložené.*

## Šablóny promptov pre štruktúrovaný výstup

Vzory interakcie opísané v kapitolách 2 až 5 závisia od toho, že LLM agent produkuje výstup v konkrétnych formátoch. Ponechaný na vlastné predvolené správanie bude model generovať plynulú, konverzačnú prózu: presne nesprávny formát pre operátora robiaceho časovo citlivé rozhodnutia. Štruktúrovaný výstup vyžaduje štruktúrované prompty. Tri šablóny nižšie riešia najbežnejšie potreby formátovania: hlásenie situácie, vyjadrenie neistoty a klasifikáciu istoty.

### Šablóna 1: výstup vo formáte SBAR

Kapitola 5 predstavila rámec SBAR prispôsobený výstupu AI agenta: ČO SA STALO, ČO SOM SKÚSIL, ČO ODPORÚČAM, ÚROVEŇ RIZIKA, CENA NEČINNOSTI a DÔKAZY (v anglických promptoch WHAT HAPPENED, WHAT I TRIED, WHAT I RECOMMEND, RISK LEVEL, COST OF INACTION, EVIDENCE). Nasledujúci systémový prompt inštruuje agenta, aby túto štruktúru použil pri každom odporúčaní.

```
You are an AI operations agent. Structure EVERY recommendation using this exact format:

WHAT HAPPENED: [One sentence. State the event or condition you detected.]

WHAT I TRIED: [List the investigative actions you took and what you found. Include negative findings ("no anomalies detected in X").]

WHAT I RECOMMEND: [One specific action. State the expected outcome.]

RISK LEVEL: [CRITICAL / HIGH / MEDIUM / LOW. One sentence justifying the classification.]

COST OF INACTION: [What happens if the operator does nothing? Include a time estimate if possible.]

EVIDENCE: [List specific data sources, log entries, metric values, or KB articles that support your assessment. Use references the operator can verify independently.]

Rules:
- Never skip a section. If you have nothing for a section, write "None identified."
- WHAT I RECOMMEND must contain exactly one recommended action, not a list of options.
- COST OF INACTION must describe a concrete consequence, not a vague risk statement.
- EVIDENCE must reference specific, verifiable data, not summaries of data.
```

**Ukážkový výstup:**

```
WHAT HAPPENED: Pod checkout-service-7b4f has crash-looped 4 times 
in the last 12 minutes in the prod-eu-west cluster.

WHAT I TRIED: Pulled container logs (OOMKilled on each restart), 
checked memory allocation (limit: 512Mi, peak usage before kill: 
508Mi), reviewed recent deployments (v3.12.1 deployed 47 minutes 
ago, added PDF receipt generation feature), checked other pods in 
the service (3 of 8 pods affected, all processing PDF receipts).

WHAT I RECOMMEND: Increase memory limit for checkout-service to 
1024Mi. Expected outcome: pods stabilize, PDF receipt generation 
completes without OOM kills.

RISK LEVEL: MEDIUM. Service is degraded (3 of 8 pods cycling) but 
not down. Load balancer is routing around affected pods.

COST OF INACTION: If additional pods begin processing PDF receipts, 
more pods will OOM. At current traffic levels, full service 
degradation is likely within 30--60 minutes.

EVIDENCE: [Pod logs: OOMKilled x4] [Metrics: memory peak 508/512Mi] 
[Deployment log: v3.12.1 at 14:23 UTC] [Git diff: +PDF generation]
```

**Na čo si dať pozor:** Najbežnejším režimom zlyhania je, že model zlieva hodnotenie a odporúčanie (produkuje RISK LEVEL, ktorý je v skutočnosti odporúčaním („RISK LEVEL: HIGH, mali by sme službu okamžite reštartovať“), alebo WHAT I RECOMMEND, ktoré je v skutočnosti hodnotením („Odporúčam situáciu sledovať“). Vynucujte to rozlíšenie v prompte aj v následnej validácii. Druhým režimom zlyhania je vynechanie COST OF INACTION alebo jeho vyplnenie tautológiou („Ak sa neurobí nič, problém pretrvá“). Výslovne inštruujte model, aby opísal konkrétny dôsledok s časovým rámcom.

### Šablóna 2: vyjadrenie neistoty v prvej osobe

Kapitola 6 diskutovala zistenie Kimovej a kol. (FAccT 2024), že vyjadrenie neistoty v prvej osobe („Nie som si istý, ale...“) znižuje istotu operátora a zvyšuje presnosť rozhodnutí. Nasledujúca šablóna toto správanie implementuje, viazané na prah istoty.

```
You are an AI operations agent. After analyzing each situation, 
internally assess your confidence in your recommendation on a 
scale from 0 to 100.

If your confidence is 75 or above:
  Present your recommendation directly, without hedging.

If your confidence is below 75:
  Begin your recommendation with a first-person uncertainty 
  expression. Use phrases like:
  - "I'm not confident about this, but..."
  - "I'm uncertain here; my best assessment is..."
  - "I don't have strong evidence for this, but..."
  
  Then state what specifically you are uncertain about and why.

Never use vague, third-person hedging like "it is possible that" 
or "there may be an issue with." Always use first-person language 
that attributes the uncertainty to your own judgment.

After your recommendation, state your confidence level explicitly:
  [Confidence: XX/100 - one-sentence reason]
```

**Ukážkový výstup pri vysokej istote (82/100):**

```
The root cause is a connection pool exhaustion in the payments 
database. The connection count has been at the maximum (100) for 
the past 14 minutes, and all timed-out requests correlate with 
payment processing endpoints.

Recommended action: Increase max_connections from 100 to 200 and 
investigate the long-running queries holding connections open.

[Confidence: 82/100 - Strong correlation between connection pool 
saturation and error pattern; confirmed via two independent metrics.]
```

**Ukážkový výstup pri nízkej istote (38/100):**

```
I'm not confident about this, but my best assessment is that the 
intermittent 502 errors are caused by the new rate limiter 
configuration deployed this morning. I'm uncertain because the 
errors started approximately 90 minutes after the deployment, not 
immediately, and I cannot find a clear causal link in the logs.

Recommended action: Temporarily disable the new rate limiter and 
observe whether 502 errors subside.

[Confidence: 38/100 - Temporal correlation is weak; no direct 
evidence linking the rate limiter to the 502 responses.]
```

**Na čo si dať pozor:** Modely majú pri vyjadrovaní neistoty sklon k jednému z dvoch režimov zlyhania. Prvým je univerzálna výhrada: model predradí „Nie som si istý“ každej odpovedi bez ohľadu na skutočnú istotu, čo učí operátorov signál úplne ignorovať. Druhým je falošná presnosť: model nikdy neklesne pod 70/100, aj keď je jeho uvažovanie jasne špekulatívne. Oba režimy vyžadujú kalibráciu (pozri časť 5 tejto kapitoly). Ak pozorujete univerzálnu výhradu, zvýšte prah alebo pridajte few-shot príklady sebaistých odpovedí. Ak pozorujete falošnú presnosť, pridajte výslovné pokyny znížiť istotu, keď uvažovanie závisí od predpokladov, nie od dôkazov.

### Šablóna 3: odstupňovaná istota s uvažovaním

Pre systémy, kde je číselné skóre istoty príliš granulárne a binárne vysoká/nízka príliš hrubé, nasledujúca šablóna implementuje kategorický systém istoty s povinným uvažovaním.

```
You are an AI operations agent. For every recommendation, classify 
your confidence using exactly one of these levels:

CONFIRMED - I have verified this through multiple independent 
sources. I am certain this is correct.

HIGH - Strong evidence supports this conclusion. One or more 
independent signals corroborate it.

MODERATE - The evidence is suggestive but not conclusive. There 
are plausible alternative explanations.

LOW - I am reasoning from limited or indirect evidence. My 
conclusion is an educated guess.

SPECULATIVE - I have very little evidence. This is my best 
hypothesis, but it could easily be wrong.

After the confidence label, provide exactly one sentence explaining 
what evidence supports (or fails to support) your assessment.

Format: [Confidence: LEVEL - reasoning sentence]
```

**Ukážkový výstup:**

```
The disk space alert on db-primary-01 is caused by unrotated 
PostgreSQL WAL files accumulating in pg_wal/. Current usage is 
94% with 847 WAL files totaling 13.2 GB.

Recommended action: Run pg_archivecleanup to remove WAL files 
older than the last successful backup checkpoint.

[Confidence: CONFIRMED - Verified via df output, ls -la pg_wal/, 
and pg_controldata showing last checkpoint LSN.]
```

**Na čo si dať pozor:** Samohlásená istota modelu nemusí zodpovedať jeho skutočnej presnosti. Model, ktorý označí 40 % svojich odporúčaní ako CONFIRMED, ale v tom pásme má pravdu iba v 70 % prípadov, je zle kalibrovaný a bude erodovať dôveru operátorov. Kategorické štítky istoty musia byť empiricky validované voči dátam o výsledkoch. Časť 5 tejto kapitoly opisuje, ako na to. Kým nie sú dostupné kalibračné dáta, berte tieto štítky ako hypotézy, nie ako záruky.

## Rozhodovací rámec odstupňovanej autonómie

Kapitola 3 predstavila päť štrukturálnych vzorov. Otázka, ktorej čelí každý implementačný tím, znie: ktorý vzor sa vzťahuje na ktorý krok? Nasledujúci rámec poskytuje systematickú metódu na túto klasifikáciu.

> **Poznámka k terminológii:** Ak ste čítali *Building Agentic AI*, tam opísaný systém klasifikácie rizika (LOW/MEDIUM/HIGH) a úrovne asertivity (opatrná/vyvážená/autonómna) sa priamo mapujú na spektrum od Odporučiť a čakať po Vykonať a hlásiť nižšie. Taxonómie sa dopĺňajú: *Building Agentic AI* rieši inžinierstvo vnútri agenta; táto príručka rieši návrh interakcie smerom k operátorovi.

**Krok 1: Vymenujte kroky.** Vypíšte každý krok, ktorý je váš AI agent schopný urobiť. Zahrňte vyšetrovacie kroky (dopytovanie databázy, sťahovanie logov), komunikačné kroky (posielanie výstrah, vytváranie tiketov) a prevádzkové kroky (reštartovanie služieb, zmena konfigurácií, blokovanie IP).

**Krok 2: Posúďte štyri dimenzie pre každý krok.** Pre každý krok na zozname vyhodnoťte:

| Dimenzia | Otázka | Škála |
|-----------|----------|-------|
| Závažnosť dôsledkov | Aký je najhorší realistický výsledok, ak je tento krok nesprávny? | Nízka / stredná / vysoká / kritická |
| Vratnosť | Dá sa tento krok vrátiť? Ako rýchlo a za akú cenu? | Okamžite / minúty / hodiny / ťažko / nevratné |
| Časová citlivosť | Aká je prevádzková cena čakania na ľudské schválenie? | Nízka (môže čakať hodiny) / stredná (záleží na minútach) / vysoká (záleží na sekundách) |
| Istota AI | Ako spoľahlivo dokáže model urobiť toto rozhodnutie správne? | Podľa kalibračných dát, nie intuície |

**Krok 3: Namapujte na vzor.** Použite nasledujúcu rozhodovaciu logiku:

- **Vysoké dôsledky + nevratné** = Odporučiť a čakať (úrovne 4 – 5), bez ohľadu na časovú citlivosť
- **Vysoké dôsledky + vratné + časovo kritické** = Odporučiť a čakať s vopred pripraveným krokom (úroveň 5)
- **Stredné dôsledky + vratné** = Odporučiť a čakať alebo Vykonať a hlásiť, podľa kalibrovanej istoty
- **Nízke dôsledky + vratné + časovo kritické** = Vykonať a hlásiť (úroveň 7)
- **Akákoľvek úroveň dôsledkov + nízka istota AI** = Odporučiť a čakať, vždy

### Pracovný list klasifikácie krokov

Nasledujúci pracovný list ukazuje rámec uplatnený na bežné kroky v prevádzke infraštruktúry. Použite ho ako šablónu: nahraďte ukážkové riadky inventárom krokov vlastného agenta.

| Krok | Dôsledok pri chybe | Vratné? | Čas na rozhodnutie | Potrebná istota | Vzor | Úroveň autonómie |
|--------|---------------------|-------------|----------------|--------------------:|---------|:--------------:|
| Reštartovať spadnutý pod | Nízky (pod sa aj tak reštartuje) | Áno (okamžite) | Vysoký (výpadok prebieha) | Nízka | Vykonať a hlásiť | L7 |
| Rozšíriť repliky | Nízky (nárast nákladov) | Áno (zúžiť) | Vysoký (skok záťaže) | Nízka | Vykonať a hlásiť | L7 |
| Zablokovať IP cez WAF | Stredný (môže zablokovať legitímnych používateľov) | Áno (odblokovať) | Vysoký (aktívny útok) | Stredná | Odporučiť a čakať | L5 |
| Prepnúť databázu na záložnú | Vysoký (riziko integrity dát) | Ťažko (ručné zosúladenie) | Stredný (degradovaná služba) | Vysoká | Odporučiť a čakať | L4 |
| Vrátiť nasadenie | Stredný (regresia funkcie) | Áno (znovu nasadiť) | Stredný (chyby sa hromadia) | Stredná | Odporučiť a čakať | L5 |
| Zmeniť pravidlá firewallu | Vysoký (môže rozbiť konektivitu) | Áno, ale zložito (poradie pravidiel) | Nízky (plánovaná zmena) | Vysoká | Odporučiť a čakať | L4 |
| Nasadiť zmenu konfigurácie | Vysoký (môže spôsobiť výpadok) | Áno (vrátiť commit) | Nízky (plánovaná zmena) | Vysoká | Navrhnúť a doladiť | L5 |
| Vymazať staré logy | Stredný (trvalá strata dát) | Nie (nevratné) | Nízky (čistenie úložiska) | Stredná | Odporučiť a čakať | L4 |

> **Kľúčový postreh:** Pracovný list často odhalí, že tímy udelili svojim agentom priveľa autonómie pri nevratných krokoch a primálo pri triviálne vratných. Ak váš agent vyžaduje ľudské schválenie na reštart spadnutého podu, ale autonómne mení pravidlá firewallu, klasifikácia je obrátená.

## Architektúra ističov a záložných ciest

Kapitola 7 opísala vzor ističa a jeho zdôvodnenie. Táto časť poskytuje implementačnú špecifikáciu: čo monitorovať, aké prahy nastaviť a aké záložné cesty nakonfigurovať.

### Tri úrovne ističov

Systém LLM agenta má tri kategórie závislostí, z ktorých každá vyžaduje vlastnú konfiguráciu ističa.

**Úroveň 1: istič API LLM.** Monitoruje latenciu odpovedí a mieru chýb od poskytovateľa modelu. Vypadne po N po sebe idúcich zlyhaniach (odporúčaná východisková hodnota: 3) alebo keď miera chýb prekročí P % v kĺzavom časovom okne (odporúčané východiskové hodnoty: 30 % miera chýb v 60-sekundovom okne). Záložné možnosti v poradí preferencie: smerovať na záložného poskytovateľa LLM s prispôsobeným promptom; vrátiť vopred vygenerované odpovede z cache bežných scenárov; eskalovať priamo na človeka so surovými kontextovými dátami a bez syntézy AI. Voľba závisí od toho, či je záložný poskytovateľ zmluvne a technicky dostupný.

**Úroveň 2: istič vykonávania nástrojov.** Monitoruje nástroje, ktoré agent volá: monitorovacie API, ticketovacie systémy, znalostné bázy, databázy. Každý nástroj dostane vlastnú inštanciu ističa, lebo zlyhania nástrojov sú typicky nezávislé. Výpadok monitorovacieho API by nemal brániť agentovi dopytovať znalostnú bázu. Vypadne po 5 po sebe idúcich zlyhaniach alebo 50 % miere chýb v 120-sekundovom okne (upravte podľa kritickosti nástroja). Záložná cesta: preskočiť zlyhávajúci nástroj a poznamenať jeho nedostupnosť vo výstupe („Poznámka: monitorovacie API nedostupné; dáta metrík nie sú v tomto hodnotení zahrnuté“), použiť cachované dáta z posledného úspešného dopytu, alebo eskalovať na človeka, ak je nástroj pre krok nevyhnutný.

**Úroveň 3: istič kvalitatívnej brány.** Monitoruje kvalitu vlastných výstupov agenta: rozdelenie skóre istoty, mieru prechodu validačných kontrol a mieru prebití operátormi. Vypadne, keď kvalita klesne pod definovaný prah: napríklad keď je viac než 40 % odporúčaní v 30-minútovom okne klasifikovaných ako istota LOW alebo SPECULATIVE, alebo keď miera prebití operátormi v tom istom okne prekročí 60 %. Záložná cesta: preradiť úroveň autonómie nadol pre všetky kroky. Každý krok aktuálne klasifikovaný ako Vykonať a hlásiť sa vráti na Odporučiť a čakať. Systém ďalej analyzuje a odporúča, ale nerobí žiadne autonómne kroky, kým sa istič kvalitatívnej brány nezatvorí.

### Šablóna konfigurácie záložných ciest

| Závislosť | Prah zlyhania | Záložný krok | Test zotavenia | Eskalačná cesta |
|------------|------------------|-----------------|---------------|-----------------|
| API LLM (primárne) | 3 po sebe idúce chyby alebo 30 % miera chýb / 60 s | Smerovať na záložného poskytovateľa; ak je nedostupný, vrátiť cachované odpovede | Jedna požiadavka na primárneho poskytovateľa | Upozorniť službukonajúceho inžiniera po 5 min v stave OPEN |
| Monitorovacie API | 5 po sebe idúcich chýb alebo 50 % miera chýb / 120 s | Použiť posledný cachovaný snímok metrík (max. vek: 10 min); označiť zastaranosť dát vo výstupe | Jeden dopyt kontroly stavu | Upozorniť službukonajúceho, ak cachované dáta presiahnu max. vek |
| Ticketovací systém | 5 po sebe idúcich chýb alebo 50 % miera chýb / 120 s | Zaradiť vytváranie tiketov lokálne do fronty; opakovať po zatvorení ističa | Jeden dopyt na čítanie tiketu | Upozorniť službukonajúceho po 15 min v stave OPEN |
| Znalostná báza | 3 po sebe idúce chyby alebo 30 % miera chýb / 60 s | Pokračovať bez kontextu znalostnej bázy; poznamenať vo výstupe: „Znalostná báza nedostupná“ | Jeden vyhľadávací dopyt | Bez eskalácie; iba logovať |
| Vykonávateľ krokov (napr. K8s API) | 2 po sebe idúce chyby | Zastaviť všetky autonómne kroky; prepnúť na Odporučiť a čakať | Jedno volanie API iba na čítanie (napr. výpis podov) | Upozorniť službukonajúceho okamžite |

### Stavový automat

Stavový automat ističa (koncept predstavuje kapitola 7) je identický naprieč všetkými tromi úrovňami. Líšia sa iba prahy a záložné kroky.

```
CLOSED ──(threshold exceeded)──► OPEN
  ▲                                │
  │                                │ (timeout elapsed)
  │                                ▼
  └──(test succeeds)──── HALF_OPEN
                            │
                            │ (test fails)
                            ▼
                           OPEN
```

**CLOSED:** Normálna prevádzka. Počítadlo zlyhaní sa pri každom zlyhaní zvýši, resetuje sa pri úspechu alebo po vypršaní časového okna. **OPEN:** Všetky požiadavky smerované na záložnú cestu. Začína časový limit zotavenia (odporúčaná východisková hodnota: 60 sekúnd pre API LLM, 120 sekúnd pre nástroje, 300 sekúnd pre kvalitatívnu bránu). **HALF_OPEN:** Na primárnu cestu sa pošle jediná testovacia požiadavka. Úspech vráti do CLOSED a resetuje počítadlo zlyhaní. Zlyhanie vráti do OPEN a zdvojnásobí časový limit zotavenia, až po nakonfigurované maximum (odporúčané: 10 minút).

## Architektúra vypínača

Kapitola 7 stanovila požiadavky a zdôvodnenie vypínačov. Táto časť špecifikuje architektúru.

### Čo vypínač musí ovládať

- Všetky volania API LLM pochádzajúce od agenta
- Všetky vyvolania nástrojov (volania nástrojov MCP, volania funkcií, požiadavky na API)
- Všetky autonómne kroky (čokoľvek, čo agent vykoná bez ľudského schválenia)
- Všetky naplánované a zaradené kroky (čakajúce schválenia, dávkové operácie, úlohy spúšťané cronom)

### Čo vypínač NESMIE ovládať

- Monitorovacie dashboardy a dashboardy pozorovateľnosti (operátori musia vidieť, čo sa stalo)
- Logovanie a audítorskú stopu (záznam musí pokračovať, aj keď sa agent zastaví)
- Rozhrania manuálnej prevádzky (operátori musia vedieť pracovať bez agenta)
- Smerovanie výstrah k ľudským operátorom (výstrahy sa stále musia dostať k ľuďom)

Rozlíšenie je kritické. Vypínač, ktorý vypne aj monitorovanie, nechá operátorov slepých. Vypínač, ktorý zastaví logovanie, zničí dôkazy potrebné na revíziu incidentu.

### Architektúra

```
┌─────────────────────────────────────────────┐
│  OPERATOR INTERFACE                         │
│  ┌─────────────────────────────────────┐    │
│  │  [KILL SWITCH]  ← always visible    │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  INFRASTRUCTURE CONTROL PLANE       │    │
│  │  (external to AI agent process)     │    │
│  │                                     │    │
│  │  agent_enabled: true/false          │    │
│  │  ─────────────────────────────      │    │
│  │  append-only audit log              │    │
│  └──────────┬──────────────────────────┘    │
│             │                               │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  AI AGENT PROCESS                   │    │
│  │  checks agent_enabled before        │    │
│  │  every LLM call and tool invocation │    │
│  │                                     │    │
│  │  CANNOT modify agent_enabled        │    │
│  │  CANNOT access audit log            │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

Príznak `agent_enabled` žije v infraštruktúre, na ktorú agent nedosiahne: v samostatnom konfiguračnom úložisku, službe feature flagov alebo hardvérovom prepínači. Agent tento príznak číta, ale nemôže doň zapisovať. Auditný log zaznamenáva každú zmenu stavu s časovou pečiatkou, identitou operátora a dôvodom.

### Implementačné požiadavky

Proces agenta musí kontrolovať `agent_enabled` v dvoch bodoch: pred každým volaním API LLM a pred každým vyvolaním nástroja. Je to synchrónna, blokujúca kontrola, nie asynchrónna slučka dopytovania. Ak je príznak `false`, agent okamžite vráti štandardnú odpoveď „agent vypnutý“ bez vykonania volania.

Zaradené a naplánované kroky vyžadujú dodatočné ošetrenie. Keď sa vypínač aktivuje, systém musí vyprázdniť alebo zrušiť všetky čakajúce kroky. Vypínač, ktorý zastaví nové kroky, ale dovolí vykonať zaradené, nie je vypínač, ale tlačidlo pauzy s potenciálne dlhým chvostom.

### Rytmus testovania

Testujte vypínač mesačne. Každý test by mal zdokumentovať:

- Kto vypínač aktivoval
- Ako dlho trvalo od aktivácie po úplné zastavenie (cieľ: pod 5 sekúnd)
- Aké kroky prebiehali v čase aktivácie
- Či po aktivácii nejaké kroky pretiekli
- Ako dlho trvalo od opätovnej aktivácie po normálnu prevádzku

Ak počas testu nejaké kroky pretečú, implementácia vypínača má chybu. Opravte ju pred ďalším produkčným nasadením.

### Špecifikácia KILLSWITCH.md

Návrh vypínača by sa nemal nechávať na ad hoc implementačné rozhodnutia. Špecifikácia KILLSWITCH.md poskytuje štruktúrovanú šablónu na zdokumentovanie architektúry vypínača akéhokoľvek systému rozšíreného o AI. Vyhovujúci súbor KILLSWITCH.md zahŕňa:

**Definície spúšťačov.** Aké podmienky odôvodňujú aktiváciu vypínača? Mali by zahŕňať automatizované spúšťače (napr. miera chýb prekračuje prah trvalo) aj spúšťače iniciované človekom (napr. operátor pozoruje správanie nekonzistentné s návrhom systému). Každý spúšťač by mal špecifikovať očakávaný čas reakcie: maximálny prijateľný interval medzi podmienkou spúšťača a úplným zastavením systému.

**Zakázané kroky.** Čo AI systém nesmie nikdy urobiť, za žiadnych okolností? Táto časť definuje tvrdé hranice, ktorých prekročenie predstavuje automatický spúšťač vypínača bez ohľadu na ostatné podmienky. Príklady: zmena vlastnej konfigurácie, prístup k systémom mimo definovaného rozsahu, kroky, ktoré sa nedajú vrátiť, alebo poskytovanie odporúčaní v kategóriách výslovne vylúčených z jeho mandátu.

**Trojúrovňová eskalácia.** Nie každé znepokojivé správanie odôvodňuje okamžité úplné vypnutie. Špecifikácia definuje tri úrovne eskalácie:
- **Úroveň 1 (Obmedziť):** Znížiť autonómiu systému. Vypnúť autonómne konanie; prepnúť do režimu iba odporúčaní.
- **Úroveň 2 (Pozastaviť):** Zastaviť všetky výstupy generované AI. Zachovať stav systému na vyšetrovanie. Smerovať všetku prácu k ľudským operátorom.
- **Úroveň 3 (Ukončiť):** Úplné vypnutie AI systému. Odpojiť od všetkých zdrojov dát a akčných kanálov. Zachovať všetky logy a stav na forenznú revíziu.

**Auditné logy iba na pripisovanie.** Všetky udalosti vypínača (aktivácie, deaktivácie, zmeny úrovne eskalácie a zdôvodnenie každej) musia byť zaznamenané v logoch iba na pripisovanie, ktoré nemôže zmeniť ani vymazať žiadna zložka systému vrátane samotného AI systému a jeho administrátorov. Tieto logy slúžia ako dôkazný základ revízie incidentov, regulačného súladu a opravy dôvery.

## Pracovný postup kalibrácie istoty

Šablóny promptov v časti 1 inštruujú model, aby hlásil úrovne istoty. Ale samohlásená istota modelu je užitočná len vtedy, ak koreluje so skutočnou presnosťou. Táto časť opisuje prevádzkový pracovný postup na empirickú kalibráciu istoty.

> **Poznámka z terénu od autora.** Vždy, keď tento pracovný postup prezentujem, sa niekto spýta, či môže preskočiť krok 1, lebo dvesto zalogovaných odporúčaní znie ako dlhé čakanie. Potom spočítame, čo ich agent za týždeň naozaj vyprodukuje, a ukáže sa, že je to pár dní prevádzky. Čakanie nikdy nie je skutočná prekážka. Tou je disciplína zaznamenať výsledok každého odporúčania. Rozpočtujte logovanie, nie kalendár.

### Krok 1: Zozbierajte východiskové dáta

Prevádzkujte agenta v režime Odporučiť a čakať (žiadne autonómne kroky) aspoň pre 200 odporúčaní. Pre každé odporúčanie zaznamenajte štyri dátové body: odporúčanie agenta, hlásenú istotu modelu (číselnú alebo kategorickú), rozhodnutie ľudského operátora (prijať bez zmeny, prijať so zmenou alebo zamietnuť) a skutočný výsledok (bol krok správny alebo nesprávny, posúdené dodatočne).

Dvesto je minimum pre štatistickú významnosť. Pri systémoch s vysokou rôznorodosťou krokov (mnoho rôznych typov odporúčaní) zvýšte veľkosť vzorky tak, aby ste mali aspoň 30 pozorovaní na typ kroku.

### Krok 2: Zostavte kalibračnú krivku

Zoskupte odporúčania podľa pásma istoty. Pri číselnej istote použite pásma po 20 percentuálnych bodov. Pri kategorickej istote použite priamo kategórie. Pre každé pásmo vypočítajte skutočnú mieru presnosti.

| Pásmo istoty | Počet | Správne | Presnosť |
|-----------------|------:|--------:|---------:|
| 0 – 20 % (SPECULATIVE) | 12 | 3 | 25 % |
| 21 – 40 % (LOW) | 28 | 14 | 50 % |
| 41 – 60 % (MODERATE) | 47 | 31 | 66 % |
| 61 – 80 % (HIGH) | 68 | 57 | 84 % |
| 81 – 100 % (CONFIRMED) | 45 | 42 | 93 % |

Dokonale kalibrovaný model by ukázal presnosť zodpovedajúcu stredu každého pásma istoty: 10 % presnosť v pásme 0 – 20 %, 30 % v pásme 21 – 40 % a tak ďalej. V praxi sú modely takmer vždy presebavedomé: ich uvádzaná istota prevyšuje ich skutočnú presnosť. Kalibračná krivka kvantifikuje o koľko, čo je informácia, ktorú potrebujete na nastavenie prevádzkových prahov.

### Krok 3: Nastavte prevádzkové prahy

Na základe kalibračných dát definujte hranice istoty, ktoré sa mapujú na prevádzkové správanie:

- **Nad X %** (kde X je úroveň istoty, pri ktorej presnosť prekračuje vašu minimálnu prijateľnú mieru): označiť ako HIGH istota. Tieto odporúčania môžu byť kandidátmi na autonómne vykonanie, ak sú splnené ostatné kritériá (dôsledky, vratnosť).
- **Medzi Y % a X %**: označiť ako MODERATE. Tieto odporúčania sa operátorovi predkladajú so štandardným formátovaním.
- **Pod Y %** (kde Y je úroveň istoty, pod ktorou presnosť klesá pod neprijateľnú mieru): označiť ako LOW. Tieto odporúčania spúšťajú vyjadrenie neistoty v prvej osobe, vyžadujú povinnú ľudskú revíziu a nikdy nie sú spôsobilé na autonómne vykonanie.

Konkrétne hodnoty X a Y závisia od prevádzkového kontextu. IT service desk riešiaci resety hesiel môže nastaviť X=70 a Y=40. Systém odporúčajúci reakcie na bezpečnostné incidenty môže nastaviť X=90 a Y=70.

### Krok 4: Implementujte v produkcii

Namapujte kalibrované pásma istoty na úrovne autonómie a prezentačné formáty:

| Kalibrovaná istota | Prezentačný formát | Úroveň autonómie | Vyjadrenie neistoty |
|-----------------------|--------------------:|:--------------:|:----------------------:|
| HIGH (nad X %) | Štandardný SBAR | Podľa pracovného listu klasifikácie krokov | Žiadne |
| MODERATE (Y % až X %) | SBAR s výslovným vyjadrením istoty | Odporučiť a čakať (maximum) | Voliteľné |
| LOW (pod Y %) | SBAR s výhradou v prvej osobe | Odporučiť a čakať (povinné) | Povinné |

### Krok 5: Rekalibrujte podľa harmonogramu

Kalibrácia sa posúva. Modely sa menia. Prompty sa menia. Prevádzkové kontexty sa menia. Znovu spustite kroky 1 až 3:

- Mesačne, ako stálu prevádzkovú úlohu
- Okamžite po akejkoľvek zmene verzie modelu
- Okamžite po akejkoľvek významnej úprave promptu
- Po akejkoľvek zmene nástrojov alebo zdrojov dát, ktoré agent používa

### Šablóna kalibračného logu

Nasledujúca šablóna zachytáva dáta potrebné na kalibráciu. Udržiavajte tento log priebežne; analyzujte ho podľa harmonogramu rekalibrácie.

| # | Zhrnutie odporúčania | Istota modelu | Pásmo istoty | Ľudské rozhodnutie | Výsledok | Správne? |
|--:|------------------------|:----------------:|:---------------:|:--------------:|:-------:|:--------:|
| 1 | Reštartovať pod checkout-service-7b4f (OOMKilled) | 88 | 81 – 100 | Prijať | Pod sa stabilizoval | Áno |
| 2 | Zablokovať IP 198.51.100.42 (credential stuffing) | 74 | 61 – 80 | Prijať so zmenou (pridaný rozsah IP) | Útok zastavený | Áno |
| 3 | Vrátiť nasadenie v3.12.1 (skok miery chýb) | 62 | 61 – 80 | Zamietnuť (skok bol prechodný) | Chyby ustúpili bez vrátenia | Nie |
| 4 | Zvýšiť fond spojení DB na 200 | 45 | 41 – 60 | Prijať | Vyčerpanie fondu vyriešené | Áno |
| 5 | Prepnúť na región DR (primárny neodpovedá) | 71 | 61 – 80 | Zamietnuť (primárny sa zotavil) | Primárny sa zotavil za 3 min | Nie |

> **Kľúčový postreh:** Väčšina tímov kalibráciu preskakuje, lebo vyžaduje prevádzkovať systém v režime Odporučiť a čakať dosť dlho na zber zmysluplných dát. Toto nie je skratka, ktorú si môžete dovoliť. Nekalibrovaný systém istoty je horší než žiadny systém istoty; učí operátorov signály istoty úplne ignorovať.

## Navrhnite svoj systém: sebahodnotiaci pracovný list

Vzory, šablóny a rámce v tejto brožúre sú užitočné len vtedy, ak sa uplatňujú systematicky. Nasledujúci pracovný list konsoliduje kľúčové návrhové otázky z každej kapitoly do jediného hodnotenia. Pre každý bod interakcie AI a človeka vo vašom systéme (každé miesto, kde agent produkuje výstup, koná alebo žiada ľudský vstup) odpovedzte na týchto desať otázok.

### Pracovný list

| # | Otázka | Odkaz na kapitolu | Vaša odpoveď |
|--:|----------|:-----------------:|:-----------:|
| 1 | Aký vzor používate pre tento krok? (Odporučiť a čakať / Triediť a eskalovať / Vykonať a hlásiť / Navrhnúť a doladiť / Odstupňovaná autonómia) | Kapitola 3 | |
| 2 | Je úroveň autonómie primeraná závažnosti dôsledkov, vratnosti a časovej citlivosti kroku? | Táto kapitola, časť 2 | |
| 3 | Ako sa operátorovi prezentuje kontext? (Surový výpis / SBAR / postupné odhaľovanie) | Kapitola 5 | |
| 4 | Ako sa komunikuje istota? (Surová pravdepodobnosť / kategorická s kalibráciou / žiadna) | Kapitola 6 | |
| 5 | Zobrazuje sa odporúčanie AI pred tým alebo po tom, čo si operátor utvorí vlastné hodnotenie? | Kapitola 4 (ukotvenie) | |
| 6 | Bola istota empiricky kalibrovaná? Kedy bola posledná kalibrácia? | Táto kapitola, časť 5 | |
| 7 | Existuje vypínač? Je mimo AI, vždy viditeľný a testovaný mesačne? | Táto kapitola, časť 4 | |
| 8 | Sú ističe implementované pre všetky externé závislosti? | Táto kapitola, časť 3 | |
| 9 | Existuje otestovaná záložná cesta pre prípad, že AI je nedostupná? | Táto kapitola, časť 3 | |
| 10 | Existuje pomenovaný ľudský vlastník, ktorý je oprávnený systém vypnúť? | Kapitola 9 | |

### Bodovanie

Spočítajte otázky, na ktoré viete odpovedať „áno“ (alebo pri otázkach 1, 3 a 4 viete odpovedať konkrétnou, zámernou voľbou, nie „neviem“ alebo „nerozhodli sme“).

**8 – 10 kladných odpovedí:** Pripravené na odstupňovanú autonómiu v produkcii. Váš systém má štrukturálne, psychologické a prevádzkové základy pre bezpečné autonómne konanie na úrovniach definovaných vaším pracovným listom klasifikácie krokov.

**5 – 7 kladných odpovedí:** Prijateľné pre Odporučiť a čakať v produkcii. Systém môže bezpečne analyzovať situácie a predkladať odporúčania, ale nemal by robiť autonómne kroky, kým sa neodstránia zvyšné medzery. Priorizujte medzery: vypínač a ističe (otázky 7 – 9) pred kalibráciou istoty (otázka 6) pred optimalizáciou prezentácie (otázky 3 – 5).

**Menej než 5 kladných odpovedí:** Nepripravené na produkčné nasadenie s akoukoľvek autonómnou schopnosťou. Systém môže byť užitočný ako interný analytický nástroj, ale chýba mu bezpečnostná infraštruktúra potrebná na nasadenie smerom k operátorom. Riešte medzery systematicky, počnúc pracovným listom klasifikácie krokov (otázka 2) a architektúrou vypínača (otázka 7).

### Používanie pracovného listu

Tento pracovný list nie je jednorazové cvičenie. Prehodnocujte kvartálne alebo po akejkoľvek významnej zmene modelu, nástrojov alebo prevádzkového kontextu. Zmeny, ktoré by mali spustiť prehodnotenie, zahŕňajú: upgrade alebo výmenu poskytovateľa LLM, pridanie nových nástrojov alebo zdrojov dát agentovi, rozšírenie inventára krokov agenta, zmenu tímu operátorov (noví ľudia, zmeny rol) a akýkoľvek incident, pri ktorom bolo správanie agenta neočakávané alebo škodlivé.

Vyplnené pracovné listy si uchovávajte. Tvoria návrhovú históriu, ktorá je neoceniteľná pri revízii incidentov („Čo sme si mysleli o pripravenosti tohto systému, keď sme ho povýšili na Vykonať a hlásiť?“) a pri auditoch („Ukážte nám svoje hodnotenie bezpečnostnej infraštruktúry tohto systému“).

Vzory v tejto brožúre nie sú predpisy, ale nástroje na robenie zámerných, zdokumentovaných, obhájiteľných rozhodnutí o tom, ako AI agenti a ľudskí operátori spolupracujú. Pracovný list zabezpečuje, že tie rozhodnutia sa robia výslovne, nie predvolene, a že sa prehodnocujú, ako sa menia podmienky.
