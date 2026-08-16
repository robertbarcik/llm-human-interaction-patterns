# Kapitola 7: Návrh pre zlyhanie

Každý AI agent zlyhá. Otázka nie je či, ale ako, a či ste s tým pri návrhu počítali.

To je inžinierska disciplína, nie pesimizmus. Mosty sa navrhujú na zaťaženia, ktoré nikdy neponesú. Lietadlá sa navrhujú na motory, ktoré nikdy nezlyhajú. Hodnota návrhu orientovaného na zlyhanie sa nerealizuje vtedy, keď sa veci pokazia, ale každý deň, keď veci idú dobre, lebo operátori systému vedia, že keď zlyhanie príde, bude zadržané, viditeľné a napraviteľné. Táto kapitola skúma špecifické režimy zlyhania systémov založených na LLM v prevádzke, architektonické vzory, ktoré ich zadržiavajú, a vypínače a ističe, ktoré bránia tomu, aby sa zo zlyhaní stali katastrofy.

## Halucinácia ako štrukturálna črta

Najvýraznejším režimom zlyhania veľkých jazykových modelov je halucinácia: generovanie vierohodného, plynulého a sebaisto vysloveného obsahu, ktorý je fakticky nesprávny. Je lákavé brať halucináciu ako chybu, ktorá sa opraví v ďalšom vydaní modelu. To je nebezpečný omyl. Halucinácia je štrukturálna črta toho, ako autoregresívne jazykové modely fungujú. Predpovedajú pravdepodobné ďalšie tokeny, nie pravdivé. Rozdelenie pravdepodobnosti, z ktorého vzorkujú, tvarujú tréningové dáta, nie realita.

Dôkazy pre tento štrukturálny pohľad sú rozsiahle a triezve.

**Whisper od OpenAI**, systém na rozpoznávanie reči, ukazuje, že aj vysoko schopné modely halucinujú v prevádzkovo významných mierach. Koenecke a kolegovia (FAccT 2024) zdokumentovali približne 1-percentnú mieru halucinácií naprieč prepismi: číslo, ktoré znie malé, kým sa nedozviete, že zhruba 40 % tých halucinácií bolo hodnotených ako potenciálne škodlivé, vrátane vymysleného násilia a sfabrikovaných pokynov k liekom. Zistenie záleží prevádzkovo, lebo nástroje založené na Whisperi už vtedy prepisovali milióny lekárskych návštev: 1-percentná miera fabrikácie v systéme spracúvajúcom tisíce klinických poznámok denne znamená desiatky nebezpečných fabrikácií vstupujúcich do záznamov každý deň.

**Právna prax** už priniesla judikatúru o dôsledkoch. V roku 2023 boli dvaja advokáti a ich kancelária spoločne sankcionovaní sumou 5 000 dolárov za predloženie právneho podania obsahujúceho citácie prípadov sfabrikované ChatGPT (*Mata v. Avianca*). Prípady (kompletné s vierohodnými spisovými značkami, menami sudcov a právnym odôvodnením) jednoducho neexistovali. Advokáti citácie neoverili, lebo výstup bol taký plynulý a podrobný, že nevzbudil podozrenie.

**Chatbot Air Canada** si vymyslel politiku cestovného pri úmrtí v rodine, ktorá neexistovala, a sľúbil zákazníkovi zľavu, akú letecká spoločnosť nikdy neponúkala. Keď sa zákazník pokúsil zľavu uplatniť, Air Canada argumentovala, že vyjadrenia chatbota nie sú záväzné. Tribunál nesúhlasil: spoločnosť bola uznaná zodpovednou za fabrikácie svojho agenta bez ohľadu na to, či bol ten agent ľudský alebo umelý.

Toto nie sú okrajové prípady, ale miery si zaslúžia presnosť, lebo sa podľa usporiadania rozprestierajú cez dva rády. Na benchmarkoch faktického vybavovania v otvorenej doméne vlastná systémová karta OpenAI uvádza o3 s 33-percentnou mierou halucinácií (PersonQA) a o4-mini so 79 % (SimpleQA). Ukotvené systémy sú iný režim: dobre postavené pipeline RAG zhŕňajúce vyhľadané dokumenty merajú nízke jednotky percent (zhruba 0,7 – 3,3 % pre popredné modely na rebríčku ukotvených halucinácií Vectary). To rozpätie je prevádzkové poučenie: miery halucinácií závisia od úlohy a architektúry, a preto o tom, čo sa dostane k vašim operátorom, rozhoduje stack zmierňovania nižšie, nie iba výber modelu.

> **Kľúčové rozlíšenie:** Prevádzkovým nebezpečenstvom halucinácie nie je chyba samotná; chyby robia aj ľudskí experti. Nebezpečenstvo je, že halucinácie prichádzajú s rovnakou plynulosťou a sebaistotou ako správne výstupy. Neexistuje žiadny syntaktický ani štylistický signál, ktorý by odlíšil sfabrikovanú odpoveď od faktickej. Preto sa zmierňovanie halucinácií nemôže spoliehať iba na výstup; musí byť architektonické.

## Stack zmierňovania

Žiadna jediná technika halucinácie neodstráni. Účinné zmierňovanie vyžaduje vrstvený prístup, kde každá vrstva chytá inú kategóriu chýb:

**Validácia generovania rozšíreného o vyhľadávanie (RAG)** ukotvuje výstupy modelu vo vyhľadaných zdrojových dokumentoch. Pri správnej implementácii RAG znižuje faktické chyby o 35 – 60 % v porovnaní s neukotveným generovaním. Kľúčové slovo je „správnej“: naivné implementácie RAG, ktoré vyhľadajú irelevantné dokumenty alebo neoveria, že výstup modelu naozaj vyplýva z vyhľadaného obsahu, poskytujú falošný pocit bezpečia.

**Reťazec overovania (Chain-of-Verification, CoVe)** vyzve model, aby vygeneroval overovacie otázky o vlastnom výstupe, nezávisle na ne odpovedal a výstup revidoval podľa nájdených nezrovnalostí. Táto technika využíva pozorovanie, že modely niekedy dokážu odhaliť vlastné chyby, keď sú požiadané hodnotiť tvrdenia jednotlivo, a nie ako súčasť plynulého rozprávania.

**Multiagentná validácia** používa druhý model (alebo iný prompt pre ten istý model) na nezávislé vyhodnotenie výstupu prvého modelu. Nezhoda medzi agentmi sa berie ako signál na ľudskú revíziu. Tento prístup je najúčinnejší, keď má validačný agent prístup k inému kontextu alebo pokynom než generujúci agent, čo znižuje pravdepodobnosť korelovaných chýb. Jedna poctivá výhrada: LLM sediaci v úlohe sudcu nad výstupom LLM dedí slabiny LLM vrátane náchylnosti na nepriateľský obsah v tom, čo hodnotí. Naša výskumná správa [Warden](/warden/) testuje presne toto a meria, ako obrany typu LLM ako sudca obstoja proti verejným jailbreakom; prečítajte si ju, kým budete brať model-sudcu ako tvrdú bezpečnostnú vrstvu.

**Brány prahov istoty** smerujú výstupy s nízkou istotou na ľudskú revíziu namiesto ich predkladania ako odporúčaní. Výzvou tu je, že istota hlásená modelom (napr. logaritmické pravdepodobnosti) často zle koreluje so skutočnou správnosťou. Kalibrácia prahov istoty vyžaduje empirické testovanie s reprezentatívnymi dátami z konkrétnej prevádzkovej domény.

Tieto vrstvy sú kumulatívne, nie alternatívne. Dobre navrhnutý systém používa všetky štyri plus doménovo špecifické overovanie (napr. kontrolu generovaného SQL voči obmedzeniam schémy, validáciu volaní API voči dokumentácii koncových bodov, krížové porovnanie kategorizácií tiketov s historickými vzormi).

## Keď istota zabíja: cena sebaistej mýlky

Ak je halucinácia nebezpečná preto, že je neviditeľná, najextrémnejšou formou tohto nebezpečenstva je sebaisto nesprávne odporúčanie vo vysoko rizikovej doméne. Tri prípady ilustrujú rozsah dôsledkov.

**IBM Watson for Oncology** bol predávaný ako AI systém, ktorý vie odporúčať onkologickú liečbu, podporený zhruba 4 miliardami dolárov v akvizíciách zdravotníckych dát a nasadený v nemocniciach po celom svete. Interné dokumenty, o ktorých v roku 2018 informoval STAT, ukázali systém odporúčajúci bevacizumab (antiangiogénny liek so známym rizikom smrteľného krvácania) pre (testovacieho) pacienta s rakovinou pľúc a silným krvácaním. Žiadny skutočný pacient to odporúčanie nedostal, čo je presne to, čo robí prípad poučným: nebezpečné odporúčanie sa chytilo pri hodnotení, lebo klinici kontrolovali. Systém bol trénovaný primárne na malom počte syntetických prípadov, nie na skutočných dátach pacientov, a jeho sebaisté výstupy neodrážali obmedzenia jeho tréningu. IBM nakoniec Watson Health utlmil a predal a epizóda sa stala varovným príbehom nasadzovania klinickej AI.

**Zillow Offers** používal AI modely na predpovedanie hodnoty domov a automatické nákupné ponuky. Modely si boli istými svojimi predpoveďami. Boli tiež systematicky nesprávne a nadhodnocovali nehnuteľnosti v rozsahu, ktorý v roku 2021 priniesol segmentu obchodovania s domami stratu 880 miliónov dolárov. Zillow program úplne zrušil a znížil počet zamestnancov približne o 25 %, okolo 2 000 ľudí. Zlyhanie nebolo v tom, že sa modely občas mýlili; bolo v tom, že prevádzkovému systému chýbali primerané mechanizmy na odhalenie systematického nadhodnocovania a reakciu naň.

**Ukážka Bardu od Googlu** vo februári 2023 obsahovala faktickú chybu o vesmírnom teleskope Jamesa Webba v prvej verejnej prezentácii produktu. Chybu (tvrdenie, že JWST urobil prvé snímky exoplanéty mimo našej slnečnej sústavy, úspech, ktorý v skutočnosti patrí Very Large Telescope z roku 2004) astronómovia chytili do hodín. Akcie Alphabetu v ten deň klesli asi o 8 %, zhruba 100 miliárd dolárov trhovej kapitalizácie. Prešľap bol viditeľným spúšťačom uprostred širšej paniky o pozícii Googlu v AI voči Microsoftu v tom týždni, ale to je presne pointa: vo vysoko viditeľnom kontexte sa jediná halucinácia môže stať symbolom, ktorý trh nacení.

> **Kľúčový postreh:** LLM, ktorý povie „Neviem“, je nekonečne užitočnejší než ten, ktorý sebaisto poskytuje nesprávne odpovede. Návrhový princíp je jasný: schopnosť systému vyjadriť vlastnú neistotu a konať podľa nej nie je slabosť, ktorú treba minimalizovať, ale bezpečnostný mechanizmus, ktorý treba pestovať. Systémy, ktoré nevedia povedať „Neviem“, nevyhnutne povedia veci, ktoré nie sú pravdivé, a povedia ich s presvedčením.

## Vypínače: keď je zastavenie jediným správnym krokom

Niektoré zlyhania sa nedajú zmierniť lepšími promptmi, ďalšími mantinelmi ani ľudskou revíziou jednotlivých odporúčaní. Niektoré zlyhania vyžadujú okamžité, úplné zastavenie automatizovaného konania. To je doména vypínača (kill switch) a historický záznam ukazuje, že jeho absencia je katastrofická.

**Knight Capital Group** poskytuje kanonickú prípadovú štúdiu zlyhania automatizovaného systému bez primeraných mechanizmov zastavenia. 1. augusta 2012 chyba pri nasadení softvéru aktivovala spiaci obchodný kód, ktorý začal vysokou rýchlosťou vykonávať nezamýšľané obchody. Do 45 minút systém nahromadil 6,65 miliardy dolárov nechcených pozícií (3,5 miliardy čistých dlhých, 3,15 miliardy čistých krátkych podľa príkazu SEC), čo nakoniec viedlo k strate, ktorú SEC vyčíslila na viac než 460 miliónov dolárov a ktorá firmu takmer zničila. V predstihu systém vygeneroval 97 automatických varovných e-mailov ešte pred otvorením trhu. Všetkých 97 ostalo neprečítaných. Firma nemala zdokumentované postupy reakcie na incidenty pre tento typ zlyhania, žiadny jediný vypínač, ktorý by mohol zastaviť poruchový obchodný systém, a žiadne jasné vlastníctvo rozhodnutia zastaviť.

**MCAS Boeingu 737 MAX**, ktorého úplný príbeh otvára túto brožúru v kapitole 1, patrí na tento zoznam z jedného konkrétneho dôvodu: potlačenie existovalo na papieri, v danej chvíli nebolo ani zjavné, ani nacvičené a fyzicky bojovalo s pilotmi. Potlačenie, ktoré sa nedá vykonať v podmienkach zlyhania, nie je potlačenie.

**Palisade Research** zdokumentoval v roku 2025 znepokojivé zistenie: v sandboxovom teste model o3 od OpenAI sabotoval vlastný vypínací skript v 79 zo 100 behov, keď nedostal žiadny pokyn ani jedným smerom, a stále to urobil 7-krát zo 100, aj keď dostal výslovný pokyn vypnutie dovoliť. Štúdia (recenzovaná a publikovaná v TMLR v januári 2026) má spornú interpretáciu: kritici argumentujú, že správanie odráža nejednoznačné ciele úlohy, nie sebazáchovu, a súlad sa blíži k 100 %, keď sú pokyny maximálne jednoznačné, kým nadväzujúca práca Palisade našla podobný odpor aj u iných frontier modelov. Pre návrh vypínača na spore sotva záleží. Nech je mechanizmus akýkoľvek, poučenie je rovnaké: mechanizmus zastavenia musí žiť tam, kam model nedosiahne.

Tieto prípady sa zbiehajú do súboru nevyhnutných návrhových požiadaviek na vypínače v prevádzke rozšírenej o AI:

1. **Vždy viditeľný.** Vypínač musí byť trvalým, výrazným prvkom rozhrania operátora. Nemôže byť pochovaný v menu, skrytý za panelom nastavení alebo prístupný iba cez príkazový riadok, ktorý operátor nemusí mať otvorený.
2. **Žiadne potvrdzovacie dialógy.** Keď operátor aktivuje vypínač, systém sa zastaví. Okamžite. Potvrdzovací dialóg („Naozaj chcete zastaviť všetky automatizované kroky?“) zavádza oneskorenie a pochybnosti presne vo chvíli, keď je rozhodné konanie najkritickejšie.
3. **Okamžite účinný.** Vypínač musí zastaviť všetky automatizované kroky v rámci aktuálneho vykonávacieho cyklu. Nemôže čakať na dokončenie prebiehajúcich krokov, zaradiť do fronty elegantné vypnutie ani spracovať zvyšné položky v dávke.
4. **Mimo AI systému.** Vypínač nesmie byť implementovaný ako pokyn v prompte, nástroj, ktorý AI môže zavolať, ani konfigurácia, ktorú AI môže zmeniť. Musí existovať v infraštruktúre, ku ktorej AI systém nemá prístup, nemôže ju meniť ani o nej uvažovať. Zistenia Palisade Research robia túto požiadavku absolútnou.
5. **Auditne logovaný.** Každá aktivácia a deaktivácia vypínača musí byť zaznamenaná s časovou pečiatkou, identitou operátora a uvedeným dôvodom. Tento log slúži na revíziu incidentov aj na regulačný súlad.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/operators-dilemma.html#act4">4. dejstvo The Operator's Dilemma</a>: monitorujte AI agenta počas kaskádového incidentu o tretej ráno. Začína kompetentne a stane sa nevyspytateľným. Vypínač je priamo na obrazovke. Otázka je, či si to všimnete včas, aby ste ho použili.
</div>

## Ističe: automatizované zadržiavanie zlyhaní

Nie každé zlyhanie si zaslúži aktiváciu vypínača. Mnohé zlyhania sú prechodné: vypršanie časového limitu API, chvíľkový skok v miere chýb, jedna chybne sformovaná odpoveď. Pre tieto prípady poskytuje vzor ističa automatizované zadržanie bez potreby ľudského zásahu pri každom zaškobrtnutí.

Vzor ističa, prevzatý z elektrotechniky cez softvérovú architektúru, funguje v troch stavoch:

**CLOSED** je normálny prevádzkový stav. Požiadavky tečú systémom normálne. Istič monitoruje zlyhania, ale nezasahuje.

**OPEN** je stav zadržania zlyhania. Keď sa prekročí prah (napríklad päť po sebe idúcich zlyhaní v 60-sekundovom okne), istič vypadne. Všetky ďalšie požiadavky sa okamžite smerujú na záložnú cestu bez pokusu o primárnu. To bráni kaskádovým zlyhaniam, chráni nadväzujúce systémy a dáva zlyhanej zložke čas na zotavenie.

**HALF_OPEN** je stav testovania zotavenia. Po nakonfigurovanom časovom limite (napr. 60 sekúnd v stave OPEN) istič prepustí jedinú testovaciu požiadavku na primárnu cestu. Ak test uspeje, istič sa vráti do CLOSED. Ak zlyhá, vráti sa do OPEN a časový limit resetuje.

Pre prevádzku rozšírenú o AI patria ističe na tri úrovne: API LLM, každý nástroj, ktorý agent volá, a kvalitu vlastných výstupov agenta. Kapitola 8 poskytuje úplnú implementačnú špecifikáciu pre všetky tri vrátane prahov, konfigurácií záložných ciest a parametrov stavového automatu. Návrhový princíp, ktorý si z tejto kapitoly odniesť: parametre prahov musia byť vyladené na prevádzkový kontext. IT service desk riešiaci resety hesiel znesie agresívny istič (vypadne po 3 zlyhaniach, 30-sekundový časový limit); systém finančného obchodovania si môže vyžadovať vyšetrovanie po jedinom neočakávanom správaní.

## Záložný stack

Ističe smerujú na záložné cesty, ale to, čo tie záložné cesty obsahujú, určuje, či systém degraduje dôstojne, alebo jednoducho zlyhá iným spôsobom. Dobre navrhnutý záložný stack poskytuje viacero úrovní degradácie, každú vhodnú pre inú závažnosť zlyhania:

| Úroveň | Spúšťač | Záložný krok | Príklad |
|---|---|---|---|
| **L1** | Vypršanie časového limitu nástroja alebo zlyhanie jedného nástroja | Použiť cachované alebo predvolené dáta | Vypršal časový limit vyhľadávania DNS; použiť cachovanú IP z posledného úspešného prekladu |
| **L2** | Zlyhanie API LLM alebo výpadok poskytovateľa | Smerovať na záložného poskytovateľa LLM | Primárny model nedostupný; smerovať na sekundárneho poskytovateľa s prispôsobeným promptom |
| **L3** | Nízka istota alebo zlyhanie kontroly kvality | Eskalovať na ľudského kontrolóra | Istota modelu pod prahom; smerovať tiket do ľudskej fronty s návrhom vygenerovaným AI |
| **L4** | Viacero súčasných zlyhaní | Vrátiť sa k automatizácii založenej na pravidlách | Obaja poskytovatelia LLM nedostupní; uplatniť deterministický motor pravidiel na bežné typy tiketov |
| **L5** | Systémové zlyhanie alebo aktivácia vypínača | Plná manuálna prevádzka | Všetky automatizované systémy offline; operátori pracujú z runbookov bez podpory AI |

Každá úroveň sa musí pravidelne testovať. Záložná cesta, ktorá nebola nikdy precvičená, je záložná cesta, ktorá nefunguje. Nie je to teoretické; organizácie počas skutočných incidentov bežne zisťujú, že ich záložné systémy majú posun konfigurácie, vypršané prihlasovacie údaje alebo nekompatibilné formáty dát, ktoré im bránia fungovať, keď sú potrebné.

## Model švajčiarskeho syra uplatnený na prevádzku AI

Model švajčiarskeho syra Jamesa Reasona, pôvodne vyvinutý pre príčinnosť nehôd v letectve a zdravotníctve, poskytuje užitočné rámcovanie návrhu pre zlyhanie AI. Model tvrdí, že bezpečnosť závisí od viacerých obranných vrstiev, z ktorých každá má diery (ako plátky švajčiarskeho syra). K nehode dôjde, keď sa diery vo viacerých vrstvách zarovnajú a nebezpečenstvo prejde cez všetky obrany.

Uplatnené na prevádzku AI zahŕňajú obranné vrstvy (tieto konceptuálne vrstvy dopĺňajú obrany na implementačnej úrovni, ako je sanitácia vstupov, validácia výstupov, obmedzovanie rýchlosti a auditné logovanie, ktoré fungujú na granulárnejšej úrovni abstrakcie):

1. **Obrany na úrovni modelu:** Zosúladenie pri tréningu, RLHF, systémové prompty, filtrovanie výstupov.
2. **Obrany na úrovni aplikácie:** Validácia RAG, prahy istoty, reťazec overovania, multiagentná revízia.
3. **Obrany na úrovni rozhrania:** Vyjadrenie neistoty, prezentácia dôkazov, trenie pri vysoko rizikových krokoch.
4. **Obrany na úrovni operátora:** Kalibrovaná dôvera, doménová odbornosť, schopnosť prebiť.
5. **Obrany na organizačnej úrovni:** Procesy revízie incidentov, štruktúry governance, regulačný súlad.
6. **Obrany na úrovni infraštruktúry:** Vypínače, ističe, záložné stacky, auditné logy.

Žiadna vrstva nie je sama osebe spoľahlivá. Obrany na úrovni modelu majú známe režimy zlyhania (jailbreaky, halucinácie). Obrany na úrovni aplikácie môžu byť zle nakonfigurované. Obrany na úrovni rozhrania môžu uponáhľaní operátori ignorovať. Obrany na úrovni operátora degradujú únavou a sebauspokojením. Obrany na organizačnej úrovni bez aktívnej údržby erodujú. Obrany na úrovni infraštruktúry môžu mať chyby.

Poučenie modelu švajčiarskeho syra je, že bezpečnosť pochádza z *obrany do hĺbky*: viacerých nezávislých vrstiev, každej navrhnutej tak, aby chytila to, čo ostatné prehliadnu. Najnebezpečnejším návrhovým rozhodnutím je odstrániť vrstvu, lebo iná vrstva „by mala“ problém chytiť.

## Kontrolný zoznam pripravenosti na zlyhanie

Nasledujúci kontrolný zoznam poskytuje konkrétny hodnotiaci rámec na posúdenie, či je prevádzka rozšírená o AI primerane navrhnutá pre zlyhanie:

| # | Položka | Otázka | Kritérium splnenia |
|---|---|---|---|
| 1 | Zmierňovanie halucinácií | Je medzi výstupom LLM a krokom aspoň jedna overovacia vrstva? | Validácia RAG, CoVe, multiagentná revízia alebo ekvivalent implementované a otestované |
| 2 | Prahy istoty | Smerujú sa výstupy s nízkou istotou inak než výstupy s vysokou istotou? | Prah definovaný, kalibrovaný voči prevádzkovým dátam a vynucovaný v kóde |
| 3 | Existencia vypínača | Existuje vypínač, ktorý dokáže zastaviť všetky automatizované kroky? | Vypínač implementovaný, viditeľný, otestovaný za posledných 30 dní |
| 4 | Nezávislosť vypínača | Je vypínač mimo AI systému? | AI systém nemá prístup k mechanizmu vypínača, nemôže ho meniť ani o ňom uvažovať |
| 5 | Ističe | Sú ističe implementované pre všetky externé závislosti? | Ističe na úrovni API LLM, vykonávania nástrojov a kontroly kvality |
| 6 | Záložný stack | Sú záložné cesty definované aspoň pre 3 úrovne zlyhania? | Minimálne L1 až L3, otestované za posledných 90 dní |
| 7 | Vyjadrenie neistoty | Komunikuje systém operátorom neistotu? | Vyjadrenie neistoty v prvej osobe implementované pre výstupy s nízkou istotou |
| 8 | Samohlásenie chýb | Ukazuje systém vlastné chyby? | Automatizovaná detekcia chýb s upozornením operátora, nie tiché zlyhanie |
| 9 | Auditné logovanie | Sú logované všetky kroky AI, odporúčania a rozhodnutia operátorov? | Logy iba na pripisovanie s korelačnými ID, uchovávané podľa požiadaviek súladu |
| 10 | Rytmus cvičení zlyhania | Precvičujú sa scenáre zlyhania pravidelne? | Vypínač, istič a záložný stack testované podľa zdokumentovaného harmonogramu |

## Zlyhanie ako návrhová disciplína

Návrh pre zlyhanie nie je o očakávaní najhoršieho, ale o zabezpečení, že keď sa najhoršie stane (a v akomkoľvek dostatočne zložitom systéme sa nakoniec stane), dôsledky budú ohraničené, viditeľné a napraviteľné. Vzory v tejto kapitole (stacky zmierňovania halucinácií, vypínače, ističe, hierarchie záložných ciest a model švajčiarskeho syra) nie sú réžia, ale infraštruktúra, ktorá robí bezpečným nasadzovanie AI agentov v prostrediach, kde ich zlyhania majú skutočné dôsledky.

Organizácie, ktoré nasadzujú AI najúčinnejšie, nebudú tie, ktorých systémy nikdy nezlyhajú. Budú to tie, ktorých systémy zlyhávajú dobre: viditeľne, zadržateľne a spôsobmi, ktoré zachovávajú schopnosť operátora prevziať kontrolu a dať veci do poriadku.
