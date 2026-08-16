# Kapitola 6: Kalibrácia dôvery

Dôvera v AI systém nie je vypínač, ktorý prepnete. Predstavte si ju ako regulátor, ktorý kalibrujete.

Keď inžinier GenAI nasadí AI agenta do prevádzkového prostredia (IT service desk, sieťové operačné centrum, klinický pracovný postup), ústrednou návrhovou výzvou nie je presnosť, latencia, cena za token, ba ani bezpečnosť v abstraktnom zmysle. Ústrednou výzvou je zabezpečiť, aby ľudia, ktorí pracujú po boku agenta, mu dôverovali *presne toľko, koľko si dôveru zaslúži*. Nie viac. Nie menej. Táto kapitola skúma, z čoho dôvera v automatizované systémy naozaj pozostáva, ako sa formuje a láme a ako navrhnúť vzory interakcie, ktoré ju udržia správne kalibrovanú. Všimnite si, že táto kapitola sa venuje kalibrácii *na strane operátora*: ako ľudia interpretujú signály istoty AI a konajú podľa nich. Kalibrácia na strane modelu (či uvádzaná istota modelu zodpovedá skutočnej presnosti) je samostatný inžiniersky problém; kapitola 8 poskytuje praktický pracovný postup na empirickú kalibráciu istoty modelu voči prevádzkovým výsledkom.

## Rámec Leeho a Seeho: výkon, proces, účel

Základný model na pochopenie dôvery v automatizáciu pochádza od Leeho a Seeho (2004), ktorí syntetizovali desaťročia výskumu do trojrozmerného rámca. Dôvera, argumentovali, nie je jediný postoj, ale zloženina troch odlišných úsudkov:

- **Výkon**: *Zvládne to prácu?* Táto dimenzia zachytáva operátorovo hodnotenie kompetencie systému: jeho presnosti, spoľahlivosti a konzistencie naprieč úlohami, ktoré má riešiť.
- **Proces**: *Ako funguje?* Táto dimenzia odráža pochopenie vnútornej logiky systému. Operátor, ktorý si vie utvoriť rozumný mentálny model toho, prečo systém produkuje daný výstup, bude dôveru kalibrovať účinnejšie než ten, kto ho berie ako čiernu skrinku.
- **Účel**: *Prečo bol postavený takto?* Táto dimenzia rieši operátorovo presvedčenie o zámere návrhára. Slúži systém cieľom operátora, alebo optimalizuje niečo iné?

Každá dimenzia sa môže nezávisle zle kalibrovať. Operátor môže dôverovať *výkonu* systému na základe série dobrých výsledkov, pričom nerozumie jeho *procesu*, čo je kombinácia produkujúca krehkú dôveru, náchylnú na zrútenie pri prvom neočakávanom zlyhaní. Naopak, operátor, ktorý dobre rozumie *procesu*, ale nikdy nevidel systém zvládať hraničný prípad, môže dôveru vo výkon kalibrovať privysoko.

> **Kľúčové rozlíšenie:** Nadmerná dôvera vedie k automatizačnej zaujatosti a sebauspokojeniu: operátor prestane kontrolovať prácu systému, prijíma nesprávne odporúčania a stráca situačné povedomie. Nedostatočná dôvera vedie k nepoužívaniu a neefektivite: operátor ignoruje platné odporúčania, duplikuje úsilie a hodnotu systému úplne neguje. Oba režimy zlyhania sú dobre zdokumentované v doménach kritických pre bezpečnosť a oba sú prítomné v každej prevádzke rozšírenej o AI.

Praktický dôsledok pre inžinierov GenAI je, že kalibrácia dôvery vyžaduje zámerný návrh naprieč všetkými tromi dimenziami. Zobrazovanie metrík presnosti rieši výkon. Ukazovanie stôp uvažovania rieši proces. Dokumentovanie návrhových rozhodnutí a optimalizačných cieľov rieši účel. Zanedbanie ktorejkoľvek dimenzie vytvára kalibračnú medzeru.

## Dispozičná, situačná a naučená dôvera

Hoff a Bashir (2015) rozšírili literatúru o dôvere do vrstveného modelu, ktorý vysvetľuje, prečo rôzni operátori reagujú na ten istý systém tak rôzne. Ich rámec identifikuje tri vrstvy dôvery, ktoré pôsobia súčasne:

**Dispozičná dôvera** je východisko. Odráža všeobecný sklon jednotlivca dôverovať alebo nedôverovať automatizovaným systémom, tvarovaný osobnosťou, kultúrou, vekom a predchádzajúcou skúsenosťou s technológiou vo všeobecnosti. Dvadsaťpäťročný inžinier, ktorý vyrástol s odporúčacími algoritmami, prichádza s iným dispozičným východiskom než päťdesiatpäťročný prevádzkový manažér, ktorého kariéra predchádza internet. Ani jedno východisko nie je samo osebe lepšie; obe môžu viesť k zlej kalibrácii.

**Situačná dôvera** závisí od kontextu. Kolíše podľa aktuálneho prevádzkového prostredia: pracovnej záťaže, časového tlaku, vnímaného rizika a dostupnosti alternatív. Operátor pod extrémnym časovým tlakom pri incidente P1 skôr prijme odporúčanie AI bez skúmania, nie preto, že systému v nejakom stabilnom zmysle dôveruje viac, ale preto, že cena overenia mu pripadá vyššia než riziko chyby. Presne vtedy je automatizačná zaujatosť najnebezpečnejšia.

**Naučená dôvera** je vrstva, ktorá sa hromadí priamou skúsenosťou s konkrétnym systémom. Je najsilnejšia a najviac navrhnuteľná. Merritt a Ilgen (2008) ukázali, že len čo ľudia začnú pracovať s konkrétnym systémom, dôvera založená na histórii rýchlo prevládne nad akoukoľvek dispozíciou, s ktorou prišli. Toto zistenie má hlboké návrhové dôsledky: obdobie zaškolenia je obdobie, počas ktorého sa ustanovuje dlhodobá kalibrácia dôvery operátora, nie iba úvod.

Pre inžinierov GenAI tento vrstvený model naznačuje fázový prístup k návrhu dôvery:

1. **Počas zaškolenia** počítajte s dispozičnou variabilitou. Nepredpokladajte jednotný východiskový bod. Niektorí operátori sa budú okamžite nadmerne spoliehať; iní sa budú zapojeniu úplne brániť.
2. **Počas prevádzky pod vysokým tlakom** navrhujte pre situačnú infláciu dôvery. Pridajte trenie (potvrdzovacie kroky, povinnú revíziu uvažovania) presne vtedy, keď sú operátori najviac v pokušení ho preskočiť.
3. **Naprieč prevádzkovým životným cyklom** silno investujte do vrstvy naučenej dôvery. Poskytujte transparentné dáta o výkone. Poctivo ukazujte zlyhania. Urobte záznam systému o výkone viditeľným a prehľadávateľným.

## Vyjadrenie neistoty v prvej osobe

Jedno z najpoužiteľnejších zistení nedávneho výskumu kalibrácie dôvery pochádza od Kimovej a kol. (FAccT 2024, Microsoft Research, N=404). Štúdia skúmala, ako by AI systémy mali komunikovať neistotu, a zistila, že *jazykové rámcovanie* neistoty záleží rovnako ako to, či sa neistota vôbec komunikuje.

Keď AI systém vyjadril neistotu v prvej osobe („Nie som si istý, ale myslím, že tento tiket by mal byť kategorizovaný ako sieťový problém“), účastníci hlásili *zníženú istotu* v odporúčaní systému. Na prvý pohľad to vyzerá ako zlyhanie. Ale kľúčovým zistením bolo, že túto zníženú istotu sprevádzala *zvýšená presnosť rozhodnutí*. Účastníci, ktorí dostali výhradu v prvej osobe, s väčšou pravdepodobnosťou odporúčanie nezávisle vyhodnotili, chytili chyby a dospeli k správnym záverom.

Naproti tomu výhrada zo všeobecnej perspektívy („Toto môže byť sieťový problém“ alebo „V kategorizácii je určitá neistota“) mala slabší účinok. Rámcovanie v prvej osobe zjavne aktivuje iný kognitívny proces: namiesto toho, aby sa neistota brala ako vlastnosť problému (ktorú operátor možno nemá pocit, že vie vyriešiť), rámcovanie v prvej osobe berie neistotu ako vlastnosť *úsudku systému*, ktorú operátor rozpozná ako niečo, čo môže a má vyhodnotiť.

> **Kľúčový postreh:** Navrhnúť AI agenta tak, aby hovoril „Nie som si istý“, nie je priznanie slabosti, ale kalibračný mechanizmus. Cieľom nie je maximalizovať istotu operátora v každom odporúčaní, ale maximalizovať presnosť operátora v rozhodnutiach, ktoré na základe tých odporúčaní robí.

Implementačný vzor je priamočiary, ale vyžaduje disciplínu:

- Keď je istota modelu pod definovaným prahom (kalibrovaným pre konkrétny prípad použitia), predraďte odporúčaniu značky neistoty v prvej osobe.
- Používajte konkrétny jazyk: „Nie som si istý týmto hodnotením“, nie neurčitú výhradu ako „Toto by potenciálne mohlo byť...“
- Spárujte vyjadrenie neistoty s uvažovaním systému, aby operátor vedel, *v čom* si systém nie je istý, a mohol podľa toho sústrediť svoje overovanie.

## Dashboardy záznamu o výkone

Štúdia z roku 2024 o predpovedateľoch Národnej meteorologickej služby (NWS), ktorí integrovali nástroje AI na predpovedanie do svojho pracovného postupu, zistila pozoruhodný konsenzus: všetci predpovedatelia považovali za nevyhnutné preskúmať predpovede AI pre minulé prípady skôr, než začnú dôverovať aktuálnemu výstupu systému. Nechceli hodnotiť AI na jedinej predpovedi. Chceli vidieť jej záznam o výkone, najmä jej zlyhania.

Toto zistenie sa zhoduje s vrstvou naučenej dôvery v rámci Hoffa a Bashira a ukazuje na konkrétnu návrhovú požiadavku: **dashboardy záznamu o výkone**. Nie sú to jednoduché percentá presnosti, ale prehľadávateľné histórie, ktoré dovoľujú operátorom budovať kalibrované mentálne modely toho, kde systém uspieva a kde zlyháva.

Účinný dashboard záznamu o výkone pre prevádzku rozšírenú o AI by mal zahŕňať:

- **Presnosť podľa typu kroku.** AI agent, ktorý správne vyrieši 94 % tiketov na reset hesla, ale iba 61 % problémov s konfiguráciou VPN, potrebuje tie čísla zobrazené osobitne. Zmiešaná metrika presnosti skrýva variabilitu, ktorú operátori na kalibráciu potrebujú.
- **Logy chýb s kontextom.** Keď sa systém mýlil, v čom sa mýlil a prečo? Prehľadávateľné, kategorizované histórie chýb dovoľujú operátorom vyvinúť rozpoznávanie vzorov pre režimy zlyhania systému.
- **História eskalácií.** Ako často systém eskaluje na človeka a čo sa deje po eskalácii? Systém, ktorý eskaluje 40 % prípadov, môže byť dobre kalibrovaný; systém, ktorý eskaluje 2 % prípadov, môže byť nebezpečne presebavedomý.
- **Časové trendy.** Zlepšuje sa systém, zhoršuje, alebo je stabilný? Operátori, ktorí vidia výkonnostné trendy, vyvinú sofistikovanejšie modely dôvery než tí, ktorí vidia iba aktuálne snímky.
- **Porovnanie s ľudským východiskom.** Tam, kde je dostupné, ukážte, ako sa výkon AI porovnáva s výkonom človeka bez podpory pri rovnakých typoch úloh. To ukotví kalibráciu v prevádzkovej realite, nie v abstraktných očakávaniach.

## Oprava dôvery po zlyhaniach

Dôvera v automatizované systémy, raz poškodená, sleduje asymetrickú trajektóriu, s ktorou musí každý inžinier GenAI počítať: po zlyhaní klesá rýchlo (často v jedinej udalosti), ale zotavuje sa pomaly, počas viacerých úspešných interakcií. Asymetria medzi tým, ako sa dôvera ničí a ako sa znovu buduje, je dlhodobé zistenie v literatúre o riziku a De Visser, Pak a Shaw (2018) na ňom postavili rámec opravy dôvery pre interakciu človeka a stroja. Jediné vysoko viditeľné zlyhanie môže vymazať týždne alebo mesiace získanej dôvery.

Táto asymetria vytvára návrhový imperatív: oprava dôvery musí byť aktívny, navrhnutý proces, nie pasívny dôsledok obnoveného dobrého výkonu. Jednoducho pokračovať v správnej prevádzke po zlyhaní nestačí. Systém (a organizácia okolo neho) musí urobiť výslovné opravné kroky.

Pak a Rovira (2023) modelovali, ktoré opravné kroky by sa mali ukázať ako najtrvanlivejšie (empirický záznam o oprave dôvery je skutočne zmiešaný, čo ich model motivovalo): ich predpoveď, ukotvená v teórii presviedčania, je, že **vecné vysvetlenia prinášajú trvanlivejšiu opravu než emocionálne ospravedlnenia**, lebo vysvetlenie zapája operátorovo uvažovanie o systéme, nie jeho pocity z udalosti. Ospravedlnenie, ktoré nesie vysvetľujúci obsah, môže fungovať tiež; ospravedlnenie bez neho vyprchá. Inžinierom bude predpoveď pripadať neprekvapivá a má priame dôsledky pre návrh komunikácie o incidentoch.

Účinné stratégie opravy dôvery zahŕňajú:

1. **Okamžité priznanie.** Systém by mal svoje zlyhania sám ukázať, namiesto čakania, kým ich operátor objaví. Systém, ktorý povie „V predchádzajúcom odporúčaní som urobil chybu; tu je, čo som pokazil“, zachová viac dôvery než ten, ktorého chyby sa objavia nezávisle.
2. **Vysvetlenie koreňovej príčiny.** Poskytnite technicky poctivé vysvetlenie, prečo k zlyhaniu došlo, na úrovni detailu primeranej operátorovi. „Vyhalucinoval som neexistujúci koncový bod API, lebo tréningové dáta obsahovali zastaranú dokumentáciu“ opravuje účinnejšie než „Došlo k chybe.“
3. **Dôkaz o náprave.** Keď je to možné, ukážte, čo sa zmenilo. Ak pribudol mantinel, doladil sa prompt alebo sa aktualizovala znalostná báza, komunikujte to konkrétne.
4. **Odstupňované opätovné zapojenie.** Po významnom zlyhaní dočasne zvýšte úroveň ľudského dohľadu. Je to kalibračný mechanizmus, nie trest: dovolí operátorovi znovu vybudovať naučenú dôveru priamym pozorovaním.

## Behaviorálne metriky kalibrácie dôvery

Navrhovať pre kalibráciu dôvery je len polovica problému. Druhá polovica je *merať*, či ku kalibrácii naozaj dochádza. Existuje viacero validovaných prístupov.

**Škála dôvery v automatizované systémy Jiana a kol. (2000)** je najpoužívanejší sebahodnotiaci nástroj, pozostávajúci z 12 položiek, ktoré hodnotia dôveru a nedôveru ako samostatné konštrukty. Je užitočná na periodické hodnotenia, ale obmedzená štandardnými slabinami sebahodnotiacich meraní: operátori nemusia presne hlásiť vlastnú úroveň dôvery a samotný akt merania môže meranú vec zmeniť.

**Behaviorálne metriky** sú pre prevádzkové prostredia diagnostickejšie:

- **Miera súladu** meria, ako často sa operátor riadi odporúčaním AI. Vysoký súlad (>95 %) v systéme so známymi mierami chýb naznačuje nadmernú dôveru. Nízky súlad (<50 %) pri dobre fungujúcom systéme naznačuje nedostatočnú dôveru.
- **Váha rady (Weight of Advice, WoA)** zachytáva nielen to, či sa operátor riadi odporúčaním, ale aj to, o koľko k nemu posunie svoj pôvodný úsudok. WoA 0 znamená, že operátor AI úplne ignoruje; WoA 1 znamená, že prijme jej odporúčanie bez zmeny.
- **Miery prebitia rozvrstvené podľa úrovne istoty** sú najdiagnostickejšia dostupná metrika. Operátor, ktorý AI prebíja rovnakou mierou bez ohľadu na to, či systém hlási 60 % alebo 99 % istotu, nie je kalibrovaný; buď informáciu o istote ignoruje, alebo ju berie ako bezvýznamnú. Dobre kalibrovaný operátor prebíja viac pri nižších úrovniach istoty a menej pri vyšších.

Retrospektívna štúdia s klinickou dátovou sadou MIMIC-III a AI systémom na podporu klinického rozhodovania metriku ilustruje: odporúčania na úrovni istoty 90 – 99 % boli prebité iba v 1,7 % prípadov. (Jedna simulovaná štúdia v jednej doméne; berte číslo ako ilustráciu meracieho prístupu, nie ako benchmark.) Kritickou otázkou sa potom stáva, či prebitia, ku ktorým pri vysokej istote dochádza, zachytávajú skutočné chyby systému, čo vyžaduje sledovať presnosť prebití v čase.

> **Kľúčový postreh:** Dobre kalibrovaný vzťah dôvery znamená, že operátor spochybňuje AI presne vtedy, keď sa AI najpravdepodobnejšie mýli. Merať to vyžaduje korelovať rozhodnutia o prebití s úrovňami istoty a nakoniec so správnosťou výsledku.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/shortlist.html">The Shortlist</a> vypočíta vaše vlastné skóre váhy rady: skontrolujte užší výber kandidátov zoradený AI (dve z poradí sú nesprávne z dôvodov, ktoré odhalia len úplné spisy) a pozrite sa, koľko z konečného poradia bolo naozaj vaše.
</div>

## Mechanizmy kalibrácie dôvery: zhrnutie

Nasledujúca tabuľka konsoliduje mechanizmy diskutované v tejto kapitole do referencie na implementáciu:

| Mechanizmus | Čo robí | Dôkazy | Implementácia |
|---|---|---|---|
| Vyjadrenie neistoty v prvej osobe | Znižuje istotu operátora a zvyšuje presnosť rozhodnutí | Kim a kol. (FAccT 2024, N=404) | Predradiť „Nie som si istý, ale...“, keď istota modelu klesne pod kalibrovaný prah |
| Dashboardy záznamu o výkone | Umožňujú operátorom budovať naučenú dôveru revíziou historického výkonu | Štúdia predpovedateľov NWS (2024); vrstva naučenej dôvery Hoffa a Bashira (2015) | Presnosť podľa typu kroku, prehľadávateľné logy chýb, história eskalácií, časové trendy |
| Odstupňovaná autonómia počas zaškolenia | Počíta s rýchlym posunom z dispozičnej na naučenú dôveru | Merritt a Ilgen (2008): dôvera založená na histórii skoro prevládne | Začať s človekom v slučke pri všetkých krokoch; rozširovať autonómiu podľa preukázanej kalibrácie |
| Vkladanie situačného trenia | Čelí inflácii dôvery pod časovým tlakom | Vrstva situačnej dôvery Hoffa a Bashira (2015) | Povinné potvrdzovacie kroky pri incidentoch vysokej závažnosti; nedajú sa obísť |
| Aktívna oprava dôvery | Zrýchľuje zotavenie dôvery po zlyhaniach vecným vysvetlením | De Visser a kol. (2018); Pak a Rovira (2023) | Samostatne ukázané chyby, vysvetlenia koreňovej príčiny, dôkaz o náprave, odstupňované opätovné zapojenie |
| Rozvrstvené sledovanie prebití | Meria, či sú operátori naozaj kalibrovaní | Škála Jiana a kol. (2000); štúdia AI-CDSS na MIMIC-III | Sledovať miery prebitia podľa pásma istoty; označiť operátorov, ktorí prebíjajú jednotne bez ohľadu na istotu |
| Transparentnosť výkon–proces–účel | Rieši všetky tri dimenzie dôvery súčasne | Lee a See (2004) | Metriky presnosti (výkon), stopy uvažovania (proces), návrhová dokumentácia (účel) |

## Navrhovať pre kalibráciu, nie pre maximalizáciu

Inštinkt mnohých inžinierskych tímov je dôveru maximalizovať: postaviť systémy tak spoľahlivé a tak pôsobivé, že im operátori úplne dôverujú. Tento inštinkt je nesprávny. Úplná dôvera je zle kalibrovaná dôvera. Produkuje automatizačnú zaujatosť, sebauspokojenie a katastrofické zlyhania, keď systém nevyhnutne narazí na prípad mimo svojej kompetencie.

Cieľom je kalibrácia: dynamický, kontextovo citlivý vzťah, v ktorom dôvera operátora sleduje skutočnú spoľahlivosť systému naprieč rôznymi typmi úloh, úrovňami istoty a prevádzkovými podmienkami. Dosiahnuť to vyžaduje brať dôveru nie ako marketingový problém (ako prinútiť ľudí dôverovať nášmu systému?), ale ako problém merania a riadenia (ako zabezpečiť, aby úroveň dôvery operátora zodpovedala skutočnej schopnosti systému v tomto konkrétnom kontexte?).

Každé návrhové rozhodnutie v prevádzke rozšírenej o AI (od formulácie odporúčaní cez rozloženie dashboardov po štruktúru revízií incidentov) kalibrácii dôvery buď pomáha, alebo bráni. Neexistuje neutrálna pôda. Vzory opísané v tejto kapitole poskytujú základ, ale kalibrácia nie je nikdy hotová. Musí sa monitorovať, merať a upravovať priebežne, lebo systém aj ľudia, ktorí ho používajú, sa stále menia.
