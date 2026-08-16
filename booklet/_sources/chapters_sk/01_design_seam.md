# Kapitola 1: Návrhový šev

Každý AI agent, ktorý interaguje s ľudským operátorom, vytvára šev: hranicu, kde strojové myslenie odovzdáva ľudskému úsudku. Tento šev nie je ani chyba, ktorú treba odstrániť, ani formalita, ktorú treba minimalizovať: je to jediné najzávažnejšie návrhové rozhodnutie v akomkoľvek prevádzkovom systéme s podporou AI, a jeho pokazenie v zdokumentovaných prípadoch stálo miliardy dolárov a stovky životov.

## Prečo na tom záleží práve teraz

Väčšinu histórie veľkých jazykových modelov bol vzor interakcie priamočiary: človek napísal prompt a model vrátil text. Človek bol vždy v slučke, lebo človek bol tou slučkou. Model nemohol konať vo svete; mohol iba navrhovať.

Toto obmedzenie sa rozpustilo. Model Context Protocol (MCP) dáva LLM štruktúrovaný prístup k externým nástrojom a zdrojom dát. Agent Development Kit (ADK) poskytuje frameworky na stavbu autonómnych agentov, ktorí vedia plánovať, vykonávať a iterovať. Volanie funkcií umožňuje LLM vyvolávať API, meniť databázy, reštartovať služby a nasadzovať kód. Z toho, čo bolo kedysi motorom na dopĺňanie textu, je dnes autonómny aktér schopný robiť závažné kroky v produkčných prostrediach.

Tento posun (od LLM ako nástrojov k LLM ako agentom) mení návrhový problém od základu. Keď LLM môže iba odporúčať, zlé odporúčanie nestojí nič, kým podľa neho človek nekoná. Keď LLM môže vykonávať, zlé rozhodnutie stojí všetko v okamihu, keď je urobené. Šev medzi človekom a strojom už nie je príjemný detail používateľského rozhrania. Je to riadiaci povrch.

Čísla naliehavosť potvrdzujú. GitHub Copilot dnes robí 1 z 5 revízií kódu, s vyše 60 miliónmi spracovaných revízií vo viac než 12 000 organizáciách. SRE Agent od PagerDuty vyšetruje produkčné incidenty a pripravuje nápravy na schválenie inžinierom, s autonómnym vykonávaním ako deklarovaným smerom. Agentné SOC od Splunku dáva AI agentov na bezpečnostné vyšetrovania v prvom slede. ServiceNow dodáva vyše 300 vopred postavených zručností a pracovných postupov AI agentov pre správu IT služieb. Sú to produkčné systémy, nie prototypy, a ich výstupy už tvarujú rozhodnutia, ktoré ovplyvňujú dostupnosť, bezpečnosť a tržby vo veľkom. (Poznámka k takýmto číslam: pochádzajú od dodávateľov. Táto brožúra berie prípadové štúdie dodávateľov ako smerový dôkaz o prijatí, nie ako overené dáta o výkone, a kapitola 2 vysvetľuje, prečo na tej disciplíne záleží.)

A napriek tomu dostáva návrh interakcie (šev) často menej pozornosti než architektúra modelu, promptovanie alebo integrácia nástrojov. To je chyba s dobre zdokumentovanými precedensmi.

## Základné napätie

Jadrom výzvy interakcie človeka a AI v prevádzke je napätie, ktoré sa nedá vyriešiť, iba riadiť: priveľa autonómie odstráni ľudský dohľad, ktorý chytá chyby, kým priveľa dohľadu maří účel automatizácie a zavádza vlastné režimy zlyhania.

Toto napätie nie je nové. V roku 1983 publikovala Lisanne Bainbridgeová „Irónie automatizácie“, článok, ktorý sa ukázal takmer prorocky relevantný pre éru AI agentov. Bainbridgeová identifikovala paradox, ktorý sedí v srdci každého návrhového rozhodnutia o automatizácii:

Čím spoľahlivejším sa automatizovaný systém stáva, tým menej často musia ľudia zasahovať. Čím menej často ľudia zasahujú, tým menej praxe získajú. Čím menej praxe majú, tým menej sú schopní účinne zasiahnuť, keď automatizácia zlyhá. A čím spoľahlivejší je systém, tým sebauspokojenejším sa človek stáva, tým menej monitoruje a tým menej pravdepodobne odhalí zlyhanie včas na to, aby konal.

## Čo sa stane, keď šev zlyhá

Dva prípady z letectva ilustrujú dva základné režimy zlyhania a oba sa priamo mapujú na návrh AI agentov.

**Let Air France 447 (2009)** ukázal zlyhanie vykonania odovzdania. Keď sa nad Atlantikom kvôli nespoľahlivým údajom o rýchlosti odpojil autopilot, piloti (ktorí strávili drvivú väčšinu letových hodín monitorovaním automatizácie) museli zrazu riadiť lietadlo ručne v zhoršených podmienkach. Ich zručnosti ručného pilotovania a schopnosti interpretovať prístroje zakrpateli nepoužívaním. Piloti aerodynamické prepadnutie nikdy nediagnostikovali. Zahynulo všetkých 228 ľudí na palube. Vyšetrovanie zistilo, že spoľahlivosť automatizácie erodovala práve tie zručnosti, ktoré boli potrebné, keď automatizácia zlyhala.

**Boeing 737 MAX (2018 – 2019)** ukázal zlyhanie návrhu odovzdania. Systém MCAS sa spoliehal na jediný snímač uhla nábehu, nebol spomenutý vo výcvikových materiáloch pilotov, a keď sa chybne aktivoval, postup na jeho potlačenie nebol ani zjavný, ani dobre nacvičený. Piloti bojovali s automatizáciou, ale nedokázali ju účinne prebiť. Tristoštyridsaťšesť ľudí zahynulo pri dvoch haváriách, lebo šev bol navrhnutý tak, že účinný ľudský zásah bol takmer nemožný.

> **Kľúčové rozlíšenie:** AF447 bolo zlyhanie človeka na šve (automatizácia fungovala správne tým, že sa odpojila, ale ľudia nedokázali podať výkon). Boeing 737 MAX bolo zlyhanie samotného švu: automatizácia zabránila účinnému ľudskému dohľadu. Oba režimy zlyhania sú priamo relevantné pre návrh AI agentov: vašim operátorom môžu chýbať zručnosti na prebitie vášho agenta (AF447), alebo váš agent môže byť navrhnutý tak, že prebitie je nepraktické (737 MAX).

## Situačné povedomie na šve

Model situačného povedomia Micy Endsleyovej (1995) vysvetľuje, prečo sú tieto zlyhania predvídateľné. Situačné povedomie funguje na troch úrovniach: **vnímanie** (vidieť dáta), **porozumenie** (chápať, čo znamenajú) a **projekcia** (predvídať, čo sa stane ďalej). Najzákernejší účinok automatizácie je na porozumenie: operátori vidia výstupy, ale strácajú kontextové porozumenie, ktoré tým výstupom dáva zmysel.

To je priamo relevantné pre AI agentov. LLM agent, ktorý autonómne vyšetrí incident a predloží zhrnutie, žiada operátora, aby vykonal projekciu a rozhodnutie bez toho, aby prešiel vnímaním a porozumením. Operátor musí rozhodnúť na základe zhrnutia, ktoré nezostavil, s kontextom, ktorý nezozbieral, o stave systému, ktorý nepozoroval. Bez zámernej návrhovej podpory operátor skĺzne buď k opečiatkovaniu (automatizačná zaujatosť), alebo k spochybňovaniu všetkého (nedôvera k automatizácii).

## Definícia návrhového švu

Návrhový šev je úplná množina rozhodnutí, ktoré riadia, ako AI agent a ľudský operátor interagujú na svojej hranici:

- **Čo agent robí autonómne** a čo postúpi človeku
- **Ako agent komunikuje** svoje zistenia, odporúčania a úrovne istoty
- **Aké informácie človek dostane** na vyhodnotenie výstupu agenta
- **Koľko času má človek** na rozhodnutie
- **Aké ovládacie prvky má človek** na prebitie, úpravu alebo vrátenie krokov agenta
- **Ako systém degraduje**, keď agent zlyhá, človek sa pomýli alebo sa preruší komunikácia

Každé z týchto rozhodnutí tvaruje interakciu spôsobmi, ktoré sa časom úročia. Systém, ktorý predkladá odporúčania bez úrovní istoty, učí operátorov dôverovať alebo nedôverovať plošne. Systém, ktorý dovoľuje autonómne konanie bez mechanizmov vrátenia, vytvára nevratné dôsledky z vratných chýb. Systém, ktorý predkladá priveľa informácií na jedno rozhodnutie, vytvára kognitívne preťaženie, ktoré vedie k únave z výstrah a opečiatkovaniu.

> **Kľúčový postreh:** Cieľom nie je šev odstrániť, ale navrhnúť ho tak, aby tím človeka a AI prekonal ktorúkoľvek zložku samostatne. To vyžaduje brať šev nie ako technické rozhranie, ale ako sociotechnický systém, v ktorom interaguje ľudské poznávanie, organizačný kontext a architektúra systému.

Kým šev navrhneme, jedna vec je nevyhnutná: rozobrať pohodlnú predstavu, že stačí ho iba obsadiť. Ďalšia kapitola sa púšťa do vety, ktorú každý AI projekt nakoniec počuje, „jednoducho tam dáme človeka do slučky“, a kapitola 3 potom predstaví päť štrukturálnych vzorov, ktoré definujú, ako si AI agenti a ľudskí operátori delia zodpovednosť v prevádzkových pracovných postupoch.
