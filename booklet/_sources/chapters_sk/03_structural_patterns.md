# Kapitola 3: Päť štrukturálnych vzorov

Nie všetky odovzdania medzi AI a človekom sú rovnaké. Vhodný vzor závisí od rizika kroku, dostupného času a odbornosti operátora. Bezpečnostný analytik triedaci tisíce výstrah denne potrebuje zásadne iný vzor interakcie než inžinier spoľahlivosti schvaľujúci prepnutie databázy na záložný server. Agent IT service desku riešiaci resety hesiel pracuje pod inými obmedzeniami než pracovník compliance kontrolujúci audítorské zistenia generované AI.

Táto kapitola definuje päť štrukturálnych vzorov, ktoré pokrývajú celé spektrum interakcie človeka a AI v prevádzke, mapuje ich na zavedené taxonómie automatizácie a poskytuje rozhodovací rámec na výber správneho vzoru pre daný prevádzkový kontext.

## Základ Sheridana a Verplanka

Kým sa pozrieme na vzory, oplatí sa ich ukotviť v taxonómii, ktorá štruktúruje výskum automatizácie takmer päť desaťročí. V roku 1978 navrhli Thomas Sheridan a William Verplank 10-stupňovú škálu automatizácie, od plnej ľudskej kontroly po plnú strojovú autonómiu. Ich rámec ostáva najcitovanejším referenčným bodom pre návrh automatizácie a každý moderný rámec (vrátane tých od PagerDuty, Cloud Security Alliance a NIST) sa dá naň spätne namapovať.

| Úroveň | Opis | Prevádzkový príklad |
|-------|------------|---------------------|
| 1 | Počítač neponúka žiadnu pomoc; človek robí všetko | Ručná analýza logov s grepom a textovými editormi |
| 2 | Počítač ponúka úplnú množinu alternatívnych krokov | AI vypíše všetky možné koreňové príčiny výstrahy |
| 3 | Počítač zúži výber na niekoľko alternatív | AI identifikuje 3 najpravdepodobnejšie koreňové príčiny s podpornými dôkazmi |
| 4 | Počítač navrhne jednu alternatívu | AI odporučí konkrétny nápravný krok |
| 5 | Počítač navrhne jednu alternatívu a vykoná ju, ak človek schváli | AI odporučí vrátiť nasadenie a pripraví príkaz na vrátenie |
| 6 | Počítač dá človeku obmedzený čas na veto pred automatickým vykonaním | AI automaticky rozšíri infraštruktúru o 60 sekúnd, pokiaľ operátor nezruší |
| 7 | Počítač vykoná automaticky a potom informuje človeka | AI automaticky napraví známy problém a pošle zhrnutie do kanála incidentu |
| 8 | Počítač vykoná automaticky a informuje človeka len na požiadanie | AI potichu rieši rutinné obnovy certifikátov; stav dostupný v dashboarde |
| 9 | Počítač vykoná automaticky a informuje človeka, len ak sa tak rozhodne | AI rieši problémy autonómne a upozorňuje ľudí iba na nové režimy zlyhania |
| 10 | Počítač rozhoduje o všetkom, koná autonómne, človeka ignoruje | Plne autonómny systém bez ľudského rozhrania (v prevádzke zriedka vhodné) |

Päť vzorov opísaných nižšie sa mapuje na zhluky v tejto škále, ale sú definované prevádzkovými charakteristikami, nie abstraktnými úrovňami automatizácie. Odpovedajú na otázku praktika: „Ako by mal môj AI agent interagovať s mojimi ľudskými operátormi pri tomto konkrétnom type práce?“

## Vzor 1: Odporučiť a čakať

**Úrovne Sheridana a Verplanka 4 – 5 | AI odporúča; človek rozhoduje a koná.**

V tomto vzore AI agent analyzuje situáciu, zozbiera dôkazy a predloží ľudskému operátorovi jeden odporúčaný krok. Agent potom čaká. Žiadny krok sa nevykoná, kým človek odporúčanie výslovne neschváli, neupraví alebo nezamietne.

Toto je najbezpečnejší vzor a vhodný štandard pre každý krok, kde sú dôsledky chyby významné a nevratné.

### SRE Agent od PagerDuty

SRE Agent od PagerDuty je príkladom tohto vzoru v produkčnej reakcii na incidenty. Keď sa spustí výstraha, agent automaticky zozbiera kontext: stiahne nedávnu históriu nasadení, dopytuje monitorovacie dashboardy, skontroluje korelované výstrahy naprieč službami a preskúma relevantné runbooky. Potom predloží službukonajúcemu inžinierovi syntetizované hodnotenie a odporúčaný krok, napríklad: „Vrátiť nasadenie v2.4.7 na v2.4.6. Dôkazy: miera chýb vzrástla o 340 % do 8 minút od nasadenia, korelované s týmto commitom, ktorý mení konfiguráciu združovania databázových spojení.“

Inžinier odporúčanie skontroluje, preskúma dôkazy a buď vrátenie schváli, alebo vyšetruje ďalej. Agent vrátenie nevykoná autonómne. Je to zámer: produkčné vrátenia môžu mať kaskádové účinky a kontextová znalosť inžiniera (povedomie o prebiehajúcej migrácii dát, vedomosť, že v2.4.6 mala vlastné problémy, rozpoznanie, že skok v miere chýb môže byť artefakt merania) je pre rozhodnutie nevyhnutná.

### AI na sepsu v Johns Hopkins

V zdravotníctve nasadila nemocnica Johns Hopkins AI systém na včasnú detekciu sepsy, ktorý funguje presne vo vzore Odporučiť a čakať. Systém nepretržite monitoruje vitálne funkcie pacientov a laboratórne výsledky a strojovým učením identifikuje jemné skoré ukazovatele sepsy, ktoré ľudským klinikom často unikajú. Keď systém odhalí prípad s vysokou pravdepodobnosťou, upozorní klinický tím s odporúčaným liečebným protokolom.

Výsledky, publikované v roku 2022 v *Nature Medicine*, sú pozoruhodné s poctivou hviezdičkou: systém (TREWS) zachytil 82 % prípadov sepsy a úmrtnosť klesla o 18,7 % relatívne (3,3 percentuálneho bodu absolútne), ale špecificky u pacientov, ktorých výstrahu poskytovateľ potvrdil do troch hodín, v porovnaní s tými potvrdenými neskôr. Prínos žije v rýchlosti ľudskej odpovede na odporúčanie, čo je presne pointa tohto vzoru. Systém nepodáva liečbu. Neobjednáva laboratórne testy. Odporúča a klinický tím, so svojou znalosťou pacientovej histórie, komorbidít a súčasného liečebného plánu, rozhoduje.

> **Kľúčový postreh:** Odporučiť a čakať nie je iba konzervatívny záložný plán: je to vysokovýkonný vzor, keď je analýza AI skutočne hodnotná, ale kontextová znalosť človeka je pre konečné rozhodnutie nevyhnutná. Zníženie úmrtnosti v Johns Hopkins sa dosiahlo výlučne lepšími odporúčaniami, podľa ktorých sa konalo rýchlejšie, nie autonómnym konaním.

### Kedy použiť tento vzor

- Krok je nevratný alebo drahý na vrátenie (produkčné nasadenia, bezpečnostné blokácie, liečba pacientov)
- Ľudský operátor má doménovú odbornosť, ktorú AI nedokáže plne zachytiť (organizačný kontext, nedávne rozhovory, politické ohľady)
- Regulačné požiadavky alebo požiadavky súladu nariaďujú ľudské schválenie
- AI systém je novo nasadený a dôvera ešte nebola vybudovaná

## Vzor 2: Triediť a eskalovať

**Úrovne Sheridana a Verplanka 3 – 5 | AI filtruje, priorizuje a smeruje; človek rieši, čo ostane.**

V tomto vzore AI agent spracúva veľkoobjemový prúd vstupov (výstrahy, tikety, požiadavky) a vykonáva prvotnú triáž. Klasifikuje položky podľa závažnosti a typu, filtruje šum, obohacuje položky o relevantný kontext a smeruje ich k vhodnému ľudskému operátorovi alebo tímu. Človek pracuje z kurátorovanej, priorizovanej fronty, nie zo surového prúdu.

Tento vzor je najcennejší v prostrediach, kde objem vstupov prevyšuje kapacitu ľudského spracovania.

### Agentné SOC od Splunku

Rozsah problému v bezpečnostnej prevádzke je ohromujúci. Prieskum Vectra AI z roku 2026 medzi 1 450 praktikmi SOC uvádza priemer 2 992 bezpečnostných výstrah denne, z ktorých 63 % ostane úplne neriešených. (Počet výstrah medziročne v skutočnosti klesá, ako sa detekčné stacky konsolidujú; podiel neriešených sa veľmi nehýbe.) Prieskumy odvetvia uvádzajú čas ručného vyšetrovania zhruba 70 minút na skutočne preskúmanú výstrahu. Aritmetika je brutálna: aj s plným tímom väčšina výstrah nedostane vôbec žiadnu ľudskú pozornosť.

Agentné SOC od Splunku to rieši nasadením AI agentov, ktorí vykonávajú prvotné vyšetrovanie autonómne. Keď sa spustí výstraha, agent dopytuje relevantné zdroje dát (logy SIEM, telemetriu koncových bodov, kanály spravodajstva o hrozbách), koreluje výstrahu so známymi vzormi útokov, kontroluje ukazovatele falošne pozitívnych výsledkov a vyprodukuje štruktúrované zhrnutie vyšetrovania. Splunk sám tvrdí, že vyšetrovania, ktoré analytikom trvali väčšinu hodiny, sa teraz dokončia za sekundy; presný pomer berte ako marketing, ale stlačenie prvotnej triáže o rád je skutočné naprieč dodávateľmi.

Agent nerozhoduje, či výstraha predstavuje skutočnú hrozbu. Predloží analytikovi štruktúrovaný brífing (vrátane detailov výstrahy, korelovaných dôkazov, historického kontextu a predbežného hodnotenia) a analytik urobí rozhodnutie. Ale, čo je kľúčové, agent priradí aj skóre priority, čím zabezpečí, že najpravdepodobnejšie skutočné hrozby sa vynoria prvé. Analytici pracujú od vrchu priorizovanej fronty, nie z chronologického prúdu.

### AI agenti od ServiceNow

ServiceNow posunul vzor Triediť a eskalovať do podnikového rozsahu so svojou platformou Now Assist, dodávajúc vyše 300 vopred postavených zručností AI agentov a agentných pracovných postupov. V správe IT služieb AI agenti automaticky klasifikujú prichádzajúce tikety, extrahujú kľúčové informácie, identifikujú relevantné články znalostnej bázy a smerujú tikety k vhodnej riešiteľskej skupine.

Pri priamočiarych požiadavkách (resety hesiel, poskytovanie prístupov, štandardné inštalácie softvéru) môže agent tiket vyriešiť autonómne (prechodom do vzoru Vykonať a hlásiť). Pri zložitých alebo nejednoznačných problémoch obohatí tiket o diagnostické informácie a eskaluje ho ľudskému agentovi, ktorý dostane vopred vyšetrený prípad, nie surovú sťažnosť.

### Kedy použiť tento vzor

- Objem vstupov prevyšuje kapacitu ľudského spracovania (tisíce výstrah alebo tiketov denne)
- Väčšina vstupov je rutinná, falošne pozitívna alebo s nízkou prioritou
- Cena oneskorenej reakcie na položky s vysokou prioritou je významná
- Ľudská odbornosť je úzke hrdlo a musí sa sústrediť na najhodnotnejšiu prácu

## Vzor 3: Vykonať a hlásiť

**Úrovne Sheridana a Verplanka 7 – 8 | AI koná autonómne a človeka informuje potom.**

V tomto vzore AI agent koná bez čakania na ľudské schválenie a potom hlási, čo urobil. Človek krok skontroluje dodatočne a zasiahne, len ak sa niečo pokazilo. Tento vzor je vhodný len vtedy, keď sú splnené tri podmienky: krok je dobre pochopený, krok je vratný a cena oneskorenia prevyšuje cenu občasných chýb.

### Davis AI od Dynatrace

Motor Davis AI od Dynatrace funguje na úrovni Vykonať a hlásiť pre definovanú množinu nápravných krokov. Keď Davis odhalí výkonnostnú anomáliu (povedzme únik pamäte spôsobujúci zhoršenie času odozvy v mikroslužbe), môže automaticky spustiť nápravný krok, ako vypnutie problematického feature flagu, rozšírenie zdroja alebo reštart kontajnera.

Zisky v efektivite okolo Davisu sú kvantifikovateľné, s výhradou k pripísaniu: široko citované 56-percentné skrátenie priemerného času do vyriešenia pochádza zo štúdie IDC (zadanej Dynatrace) a opisuje vyšetrovanie s podporou AI s ľuďmi v slučke, nie samotnú autonómnu nápravu, ktorú Dynatrace predáva samostatne bez priloženého percenta. Čo autonómna úroveň overiteľne poskytuje: systém vykoná nápravu, zaloguje krok s plným kontextom (čo sa zistilo, aký krok sa urobil, aké boli očakávané a skutočné výsledky) a upozorní prevádzkový tím.

Kľúčové je, že Davis AI nenapráva automaticky všetko. Systém udržiava výslovný zoznam schválených autonómnych krokov, každý s definovanými postupmi vrátenia. Kroky mimo tohto zoznamu sa eskalujú do vzoru Odporučiť a čakať. Táto ohraničená autonómia (autonómne vykonávanie v definovaných mantineloch, eskalácia mimo nich) je to, čo robí vzor bezpečným na Sheridanovej úrovni 7 namiesto bezohľadného na úrovni 10.

### Kedy použiť tento vzor

- Krok je dobre pochopený a bol už mnohokrát úspešne vykonaný
- Krok je vratný v prijateľnom časovom okne
- Cena oneskorenia (latencia ľudského schválenia) prevyšuje očakávanú cenu občasných chýb
- Je zavedené komplexné logovanie a mechanizmy vrátenia
- Rozsah autonómneho konania je výslovne ohraničený a pravidelne revidovaný

> **Kľúčové rozlíšenie:** Vykonať a hlásiť nie je „nastav a zabudni“. Vyžaduje väčšiu inžiniersku investíciu než Odporučiť a čakať (nie menšiu), lebo systém musí zahŕňať monitorovanie vlastných krokov, schopnosť automatického vrátenia a jasné eskalačné cesty pre prípad, že autonómna náprava zlyhá alebo prinesie neočakávané výsledky.

## Vzor 4: Navrhnúť a doladiť

**Úroveň Sheridana a Verplanka 5 (upravená) | AI vyprodukuje kompletný výstup; človek ho skontroluje, upraví a schváli.**

Tento vzor sa od Odporučiť a čakať líši jemným, ale dôležitým spôsobom. Namiesto odporúčania kroku AI vyprodukuje kompletný pracovný produkt (revíziu kódu, správu o incidente, aktualizáciu runbooku, zmenu konfigurácie), ktorý človek potom doladí. Rola človeka sa posúva z rozhodovateľa na editora.

### Revízia kódu GitHub Copilot

Schopnosť GitHub Copilotu revidovať kód poskytuje najškálovanejší príklad tohto vzoru v produkcii. Začiatkom roka 2026 Copilot robí 1 z 5 revízií kódu na platforme, s vyše 60 miliónmi spracovaných revízií vo viac než 12 000 organizáciách.

Vzor interakcie je poučný. Keď sa odošle pull request, Copilot analyzuje zmeny, identifikuje potenciálne problémy (chyby, bezpečnostné zraniteľnosti, porušenia štýlu, výkonnostné obavy) a vygeneruje revízne komentáre s konkrétnymi návrhmi. Vývojár (alebo autor pull requestu) tieto komentáre skontroluje, prijme tie platné, zamietne tie neplatné a môže sa s Copilotom o konkrétnych návrhoch dohadovať tam a späť.

WEX, fintechová firma, hlásila približne 30-percentný nárast produktivity po širokom prijatí Copilotu (agentný režim, agent na programovanie a revízia kódu spolu), nie preto, že AI napísala viac kódu, ale významnou mierou preto, že revízny cyklus bol rýchlejší a konzistentnejší. AI riešila rutinné kontroly (štýl, bežné vzory chýb, medzery v dokumentácii), čím uvoľnila ľudských recenzentov na architektonické rozhodnutia, správnosť biznisovej logiky a hraničné prípady, ktoré vyžadujú doménovú odbornosť.

### Kedy použiť tento vzor

- Výstupom je zložitý artefakt (kód, dokumentácia, konfigurácia), nie binárne rozhodnutie
- Kvalita závisí od iteratívneho dolaďovania, nie od jedinej správnej odpovede
- Odbornosť človeka je v hodnotení a editovaní, nie v generovaní od nuly
- Objem artefaktov prevyšuje to, čo ľudia dokážu vyprodukovať od nuly, ale nie to, čo dokážu skontrolovať

## Vzor 5: Odstupňovaná autonómia

**Dynamicky naprieč úrovňami Sheridana a Verplanka | Úroveň autonómie AI sa upravuje podľa kontextu, istoty a záznamu o výkone.**

Toto je metavzor: namiesto pevného jediného vzoru interakcie systém dynamicky upravuje úroveň autonómie podľa konkrétnej situácie. AI agent môže fungovať vo Vykonať a hlásiť pri rutinných, dobre pochopených problémoch, prejsť do Odporučiť a čakať pri nových alebo vysoko rizikových situáciách a eskalovať na plnú ľudskú kontrolu, keď narazí na niečo mimo svojho tréningového rozdelenia.

### Dve osi PagerDuty: úrovne incidentov a režimy vykonávania

SRE Agent od PagerDuty implementuje odstupňovanú autonómiu pozdĺž dvoch osí. Prvou je klasifikácia incidentov podľa toho, kto má viesť: rutinné, dobre pochopené incidenty, ktoré agent zvládne prevažne sám; zložité incidenty riešené spoločne, s agentom vyšetrujúcim a inžinierom riadiacim; a vysoko rizikové alebo nové incidenty, ktoré ostávajú vedené človekom s agentom v podpornej roli. Druhou osou je režim vykonávania: v režime Review agent navrhuje každý krok a čaká na schválenie, kým režim Autonomous (smer, ktorým PagerDuty stavia pre dobre ohraničené kroky) vykonáva a hlási.

Priradenie nie je statické, a to je tá poučná časť. Zamýšľaná trajektória je, že trieda krokov začína v režime Review a autonómiu si zaslúži, ako sa hromadí záznam o výkone a dôvera tímu v ňu je validovaná, zámerne, ľuďmi, ktorí systém vlastnia, nie počítadlom, ktoré tikne cez prah. Naopak, autonómia môže byť odobratá: počas zmrazenia zmien, po veľkom incidente alebo keď klesne dôvera v triedu odporúčaní, autonómna trieda krokov sa preradí späť do Review.

### Úrovne autonómie CSA

Cloud Security Alliance publikovala v januári 2026 svoj rámec úrovní autonómie AI, definujúci šesť úrovní špecificky pre AI agentov v bezpečnostnej prevádzke:

| Úroveň CSA | Názov | Opis | Kľúčová charakteristika |
|-----------|------|-------------|--------------------|
| 0 | Bez AI | Plne manuálna prevádzka | Východisko |
| 1 | Asistujúca AI | AI poskytuje informácie; človek rozhoduje a koná | Režim kopilota |
| 2 | Autonómia pod dohľadom | AI odporúča kroky; človek schvaľuje | Odporučiť a čakať |
| 3 | Podmienená autonómia | AI koná v definovaných hraniciach; človek rieši výnimky | Ohraničené Vykonať a hlásiť |
| 4 | Vysoká autonómia | AI koná nezávisle pri väčšine úloh; človek dohliada | Vykonať a hlásiť s monitorovaním |
| 5 | Plná autonómia | AI funguje nezávisle s minimálnym zapojením človeka | Pre bezpečnosť zriedka vhodné |

Najužitočnejšia myšlienka, ktorú si z diskusie CSA odniesť, je **dynamické preradenie nadol**: princíp, že AI agent by mal automaticky znížiť svoju úroveň autonómie, keď narazí na neistotu, nové situácie alebo podmienky mimo svojho tréningového rozdelenia. (Článok CSA to nastoľuje ako otvorenú návrhovú otázku, nie ako pomenovanú zložku rámca; táto brožúra odporúča prijať to ako návrhové pravidlo.) Agent úrovne 4, ktorý narazí na predtým nevidený vzor útoku, by sa mal preradiť na úroveň 2, predložiť svoju analýzu a požiadať o ľudské usmernenie namiesto pokusu o autonómnu nápravu niečoho, čomu nerozumie.

> **Kľúčový postreh:** Odstupňovaná autonómia nie je o dosiahnutí najvyššej možnej úrovne autonómie, ale o dosiahnutí tej správnej pre každé konkrétne rozhodnutie v každom konkrétnom okamihu. Najlepšie systémy nie sú tie najautonómnejšie; sú to tie, ktoré vedia, kedy požiadať o pomoc.

## Rámec výberu vzoru

Výber správneho vzoru vyžaduje vyhodnotiť štyri dimenzie prevádzkového kontextu:

| Vzor | Tolerancia rizika | Časová citlivosť | Potrebná ľudská odbornosť | Vratnosť |
|---------|---------------|-------------------|--------------------------|---------------|
| Odporučiť a čakať | Nízka (kroky s vysokými dôsledkami) | Nízka až stredná (k dispozícii minúty až hodiny) | Vysoká (kontextový úsudok nevyhnutný) | Nízka (nevratné alebo drahé na vrátenie) |
| Triediť a eskalovať | Stredná (chyby priorizácie sú napraviteľné) | Vysoká (objem vyžaduje rýchle spracovanie) | Stredná (odbornosť potrebná pri eskalovaných položkách) | Stredná (chyby smerovania riešenie oddialia, ale nezabránia mu) |
| Vykonať a hlásiť | Stredná až vysoká (prijíma občasné chyby) | Veľmi vysoká (cena oneskorenia prevyšuje cenu chyby) | Nízka (kroky sú dobre pochopené a procedurálne) | Vysoká (kroky musia byť vratné) |
| Navrhnúť a doladiť | Stredná (editovanie zachytí väčšinu chýb) | Stredná (revízny cyklus pridáva latenciu) | Vysoká (hodnotenie vyžaduje hlbokú odbornosť) | Vysoká (artefakty možno pred nasadením revidovať) |
| Odstupňovaná autonómia | Premenlivá (prispôsobuje sa kontextu) | Premenlivá (prispôsobuje sa naliehavosti) | Premenlivá (prispôsobuje sa dostupnosti) | Premenlivá (zosúlaďuje autonómiu s vratnosťou) |

## Referenčné rámce

Päť vzorov opísaných v tejto kapitole čerpá z niekoľkých zavedených rámcov a je s nimi kompatibilných; praktici by o nich mali vedieť:

### Parasuraman, Sheridan a Wickens (2000)

Štvorstupňový model rozširuje pôvodnú škálu Sheridana a Verplanka tým, že uznáva, že automatizáciu možno nezávisle uplatniť na štyri stupne ľudského spracovania informácií: **získavanie informácií**, **analýza informácií**, **výber rozhodnutia** a **implementácia kroku**. Systém môže byť vysoko automatizovaný v získavaní informácií (automatický zber logov a metrík) a pritom ostať plne manuálny vo výbere rozhodnutia (človek rozhoduje, čo robiť). Tento rozklad je nevyhnutný na návrh jemných vzorov interakcie, ktoré automatizujú správne stupne zo správnych dôvodov.

### Rámec riadenia rizík AI od NIST

NIST AI RMF poskytuje štruktúrovaný prístup k identifikácii a zmierňovaniu rizík v AI systémoch, organizovaný okolo štyroch funkcií: Govern, Map, Measure a Manage. Nepredpisuje konkrétne vzory interakcie, ale poskytuje metodiku hodnotenia rizík, ktorá by mala výber vzoru informovať.

### Usmernenia Microsoft Human-AI Experience (HAX)

18 usmernení HAX od Microsoftu pokrýva celý životný cyklus interakcie človeka a AI, od prvotnej kalibrácie („Ujasnite, ako dobre systém dokáže to, čo dokáže“) cez riešenie chýb („Podporte efektívnu opravu“) po dlhodobú dôveru („Povzbudzujte granulárnu spätnú väzbu“). Sú užitočné najmä pre vrstvu používateľského rozhrania návrhu švu.

### Google PAIR (People + AI Research)

Príručka PAIR od Googlu poskytuje návrhové usmernenie organizované okolo konceptu návrhu „AI na prvom mieste“: vychádzať zo schopností a obmedzení AI, nie z tradičného pracovného postupu používateľského rozhrania. Jej dôraz na mentálne modely (pomôcť používateľom pochopiť, čo AI dokáže a čo nie) sa priamo zhoduje s obavami o situačné povedomie z kapitoly 1.

## Výber východiskového bodu

Pre organizácie, ktoré začínajú nasadzovať AI agentov v prevádzke, dve praktické odporúčania:

**Začnite s Odporučiť a čakať.** Je to najbezpečnejší vzor, buduje dáta potrebné na vyhodnotenie výkonu AI a zakladá základ dôvery potrebný pre vyššie úrovne autonómie. Organizácie, ktoré preskočia rovno k Vykonať a hlásiť bez toho, aby najprv validovali odporúčania AI v režime Odporučiť a čakať, podstupujú zbytočné riziko.

**Navrhujte pre odstupňovanú autonómiu od začiatku.** Aj keď je vaše prvotné nasadenie čisto Odporučiť a čakať, navrhnite architektúru systému tak, aby sa úroveň autonómie dala upraviť pre každý typ kroku bez prestavby. Definujte kritériá povýšenia a degradácie. Inštrumentujte systém tak, aby sledoval miery prijatia odporúčaní, vzory prebíjania a kvalitu výsledkov. Dáta, ktoré zozbierate počas Odporučiť a čakať, sú základom každého ďalšieho rozhodnutia o autonómii.

## Od úrovní k spoluhráčom

Poctivá poznámka o lešení, na ktorom je táto kapitola postavená. Škála Sheridana a Verplanka a jej potomkovia berú návrh automatizácie ako problém prideľovania: vypíšte funkcie, rozhodnite, ktoré dostane stroj. Toto rámcovanie má takmer päťdesiat rokov a výskumníci, ktorí strávili kariéry štúdiom automatizovaných systémov v teréne, strávili posledných dvadsať z tých rokov argumentovaním proti nemu.

[Dekker a Woods](https://link.springer.com/article/10.1007/s101110200022) to v roku 2002 povedali bez obalu („MABA-MABA or Abracadabra?“): automatizácia *nenahrádza* ľudskú prácu strojovou v pevných množstvách. Premieňa prácu človeka na niečo nové, zvyčajne koordináciu a riešenie výnimiek, a zaujímavé návrhové otázky žijú v tej premene, nie v tabuľke prideľovania. Klein, Woods, Bradshaw, Hoffman a Feltovich nasledovali v roku 2004 s [desiatimi výzvami, ako urobiť z automatizácie „tímového hráča“](https://ieeexplore.ieee.org/document/1363742/): dokážu stroj a človek udržať spoločnú pôdu o tom, čo sa deje? Sú stav a zámer stroja pozorovateľné? Dá sa *usmerňovať* uprostred úlohy? Dokáže vyjednávať o cieľoch, nielen ich vykonávať? Správa Národných akadémií z roku 2022 o [tímovej spolupráci človeka a AI](https://nap.nationalacademies.org/catalog/26355/human-ai-teaming-state-of-the-art-and-research-needs) posun konsolidovala: výskumná špička berie človeka a AI ako tím, ktorý treba navrhnúť, nie ako škálu, ktorú treba nastaviť.

Prečo teda táto brožúra stále učí úrovne? Lebo úrovne sú správny vstupný nástroj: vynucujú prvý nevyhnutný rozhovor (čo smie tento systém robiť bez človeka?) a čisto sa mapujú na riziko, vratnosť a reguláciu. Ale všimnite si, že najlepší materiál v nasledujúcich kapitolách je už v prestrojení materiálom o tímovej spolupráci. SBAR je protokol spoločnej pôdy. Komunikácia istoty je vzájomná predvídateľnosť. Vypínač je usmerniteľnosť v najhrubšej podobe. Tam, kde vám vzor v tejto kapitole pripadá pre váš systém príliš statický (agent, ktorý plánuje, koná a preplánúva, nesedí nehybne na jednej úrovni), je optika tímovej spolupráce cestou k upgradu: nepýtajte sa „na akej úrovni je tento agent“, ale „čo tento agent potrebuje povedať môjmu operátorovi a čo môj operátor potrebuje vedieť s ním urobiť, aby tí dvaja ostali skoordinovaní?“

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/operators-dilemma.html#act5">The Operator's Dilemma, 5. dejstvo</a>: navrhnite šev pre agenta na riadenie zmien sami (úroveň autonómie, formát kontextu, zobrazenie istoty, poistky) a dostaňte kritiku svojich volieb.
</div>

Štrukturálne vzory definujú, čo robí systém. Ďalšia kapitola skúma, čo robí človek (a čo je dôležitejšie, čo človek zlyháva urobiť), keď s týmito vzormi interaguje.
