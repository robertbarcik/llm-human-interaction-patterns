# Kapitola 4: Psychológia odovzdania

Najnebezpečnejším predpokladom v prevádzke s podporou AI je, že ľudia sa budú pri interakcii s automatizovanými systémami správať racionálne. Nebudú. Nie preto, že by operátori boli nedbanliví alebo nekompetentní, ale preto, že ľudská kognitívna architektúra, ktorá nám tisícročia dobre slúžila, je systematicky nezladená s nárokmi na monitorovanie a prebíjanie automatizovaných systémov. Pochopiť tieto nezladenia nie je voliteľné; je to predpoklad návrhu vzorov interakcie, ktoré naozaj fungujú.

Táto kapitola pokrýva päť kognitívnych javov, ktoré priamo ovplyvňujú kvalitu ľudských rozhodnutí na šve medzi AI a človekom. Každý je rozsiahlo zdokumentovaný v recenzovanom výskume. Každý priniesol zlyhania v skutočnom svete s merateľnými dôsledkami. A každý má návrhové dôsledky, ktoré, ak sa ignorujú, podkopú aj tie najstarostlivejšie navrhnuté štrukturálne vzory z kapitoly 3.

## Automatizačná zaujatosť

Automatizačná zaujatosť je sklon ľudí uprednostňovať návrhy automatizovaných systémov pred protichodnými informáciami z iných zdrojov vrátane vlastných pozorovaní. Nie je to lenivosť, ale dobre zdokumentovaná kognitívna skratka: ľudský mozog berie automatizovaný systém ako autoritu a podľa toho upraví svoje spracovanie.

### Dôkazy

Prelomovou štúdiou je Skitka, Mosier a Burdick (1999), ktorá testovala pilotov aj nepilotov v simulovanom letovom prostredí, kde automatizovaný monitorovací systém občas poskytol nesprávne odporúčania.

Výsledky boli neúprosné:

- **Chyby konania** (vykonanie nesprávneho kroku odporúčaného automatizáciou): **100 % účastníkov** sa dopustilo aspoň jednej chyby konania. Každý jeden účastník vrátane skúsených pilotov sa aspoň raz riadil odporúčaním automatizácie, keď bolo preukázateľne nesprávne.
- **Chyby opomenutia** (nevšimnutie si problémov, ktoré automatizácia prehliadla): **55 % účastníkov** prehliadlo udalosti, ktoré automatizácia neoznačila, aj keď boli na ich prístrojoch jasne viditeľné.

Azda najznepokojivejšie: prítomnosť druhého člena posádky (štandardné zmiernenie ľudskej chyby v letectve) chyby z automatizačnej zaujatosti neznížila (Mosierová a kolegovia spustili tímovú verziu štúdie v roku 1998; miery chýb v dvojčlenných posádkach boli štatisticky nerozlíšiteľné od samostatných operátorov). Prehľad Parasuramana a Manzeya (2010) potvrdil vzor naprieč viacerými doménami a podkladový paradox spoľahlivosti bol zmeraný priamo: v experimentoch Baileyho a Scerba zvýšenie spoľahlivosti automatizácie z 87 % na 98 % posunulo prehliadnutia zlyhaní operátormi zo zhruba tretiny udalostí na takmer polovicu. Čím dôveryhodnejší je záznam automatizácie, tým menej ju človek monitoruje.

### Dôsledky v skutočnom svete

**Prasknutie ropovodu Enbridge (2010)** ukázalo automatizačnú zaujatosť v prevádzkovom rozsahu. Alarmy SCADA indikovali pokles tlaku konzistentný s prasknutím. Operátori velína, kalibrovaní rokmi falošných poplachov, varovania **17 hodín** odmietali, dvakrát ropovod reštartovali a napumpovali do prostredia ďalšiu ropu: do povodia rieky Kalamazoo sa dostalo asi 3,2 milióna litrov (20 082 barelov podľa NTSB). Vyčistenie presiahlo **1 miliardu dolárov**.

**Škandál Horizon britskej pošty** ho ukázal v inštitucionálnom rozsahu. IT systém Horizon obsahoval chyby, ktoré vytvárali fantómové finančné manká. Napriek stovkám vedúcich pobočiek hlásiacich, že čísla systému nesedia so skutočnosťou, pošta systematicky dôverovala počítaču pred ľuďmi, čo viedlo k **736 nezákonným trestným stíhaniam** počas 16 rokov.

> **Kľúčový postreh:** Automatizačná zaujatosť nie je chyba charakteru, ale predvídateľná reakcia na zle navrhnutú interakciu. Keď má systém pravdu v 99 % prípadov, racionálna bayesovská odpoveď je dôverovať mu, a tá istá racionálna odpoveď spôsobí, že operátor prehliadne to 1 % prípadov, kde je dôvera nemiestna. Počítať s tým musí návrh, nie operátor.

### Návrhové dôsledky

Kognitívne vynucovacie funkcie (prvky rozhrania, ktoré vyžadujú, aby sa operátor aktívne zapojil, kým prijme odporúčanie AI) sú primárnym protiopatrením. Buçinca, Malaya a Gajos (Harvard, publikované na CSCW 2021) ukázali, že požiadavka, aby sa ľudia zaviazali k vlastnému hodnoteniu skôr, než uvidia odporúčanie AI, významne znížila nadmerné spoliehanie sa na nesprávne rady AI. Kompromis: účastníkom sa tieto návrhy páčili najmenej zo všetkého testovaného, čo vytvára priamy konflikt medzi bezpečnosťou a použiteľnosťou, ktorým sa návrhári musia výslovne prepracovať.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/watchlist.html">The Watchlist</a> vás postaví do fronty biometrického overovania s odpočtom a jemne nesprávnymi zhodami od AI; <a href="https://demos.barcik.training/demos/operators-dilemma.html#act1">1. dejstvo The Operator's Dilemma</a> spúšťa tú istú pascu v IT prevádzke. Väčšina ľudí opečiatkuje aspoň jedno nesprávne rozhodnutie. Spočítajte si tie svoje.
</div>

## Únava z výstrah

Únava z výstrah je postupné znecitlivenie operátorov voči výstrahám v dôsledku nadmerného objemu, vysokej miery falošne pozitívnych výsledkov alebo oboch. Je to doplnok automatizačnej zaujatosti: namiesto dôvery v nesprávne odporúčanie operátor ignoruje všetky odporúčania, lebo pomer signálu k šumu sa zrútil.

### Rozsah problému

Čísla sú konzistentné naprieč odvetviami:

- **Zdravotníctvo:** 72 – 99 % klinických alarmov je falošných (AHRQ, 2020). Miery prebitia liekových výstrah sa naprieč štúdiami pohybujú medzi 49 % a 96 %, pričom výstrahy na liekové interakcie sa prebíjajú asi v 90 % prípadov. Sentinel Event Alert Spoločnej komisie o bezpečnosti alarmov (2013) spojil 98 udalostí súvisiacich s alarmami vrátane 80 úmrtí s únavou z alarmov počas štvorročného okna.
- **Bezpečnostná prevádzka:** Priemerné SOC dostáva 2 992 bezpečnostných výstrah denne, z ktorých 63 % ostane úplne neriešených. Sofistikovaní útočníci to zneužívajú cez „búrky výstrah“: generovanie veľkých objemov výstrah s nízkou prioritou na zamaskovanie skutočných prienikov.
- **IT prevádzka:** Podobné vzory v monitorovaní infraštruktúry, kde hlučné konfigurácie výstrah generujú stovky alebo tisíce výstrah denne, väčšinu prechodných alebo duplicitných.

### Náprava založená na dôkazoch

Únava z výstrah nie je neriešiteľná. Boston Medical Center prepracovalo svoj systém klinických alarmov úpravami prahov, potlačením stavov, na ktoré netreba konať, a odstupňovaným smerovaním upozornení. Objem alarmov klesol z **87 823 týždenne na 9 967**: 89-percentné zníženie bez akéhokoľvek nárastu nežiaducich výsledkov u pacientov.

Poučenie: hodnota systému výstrah nie je úmerná jeho citlivosti. Systém, ktorý generuje 3 000 výstrah denne a zachytí 95 % skutočných incidentov, je menej užitočný než ten, ktorý generuje 300 výstrah a zachytí 90 %, lebo prvý systém učí operátorov výstrahy ignorovať.

### Návrhové dôsledky

Pre AI agentov fungujúcich vo vzore Triediť a eskalovať je únava z výstrah primárnym režimom zlyhania. Protiopatrenia:

- **Agresívna deduplikácia a korelácia:** Zoskupujte súvisiace výstrahy do incidentov.
- **Filtrovanie podľa istoty:** Potlačte výstrahy pod prahom istoty a prijmite občasné prehliadnutia, aby ste zachovali pozornosť operátora.
- **Adaptívne prahy:** Upravujte podľa kontextu (denná doba, nedávne zmeny, aktuálna záťaž incidentmi).
- **Rozpočty výstrah:** Zastropujte celkové denné eskalácie a prinúťte systém priorizovať.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/triage-ward.html">The Triage Ward</a>: odpracujte nočnú zmenu s frontou alarmov, kde záleží na jednom z osemnástich, a potom tú istú noc po prepracovaní v štýle Boston Medical. Ten rozdiel je celý argument tejto časti.
</div>

## Efekt ukotvenia

Ukotvenie je kognitívne skreslenie identifikované Tverskym a Kahnemanom (1974), pri ktorom počiatočná informácia neúmerne ovplyvňuje následné úsudky, aj keď je kotva ľubovoľná alebo irelevantná. V interakcii AI a človeka slúži prvotné odporúčanie AI ako silná kotva.

Štúdia 775 manažérov z roku 2025 potvrdila, že efekty ukotvenia pretrvávajú aj u skúsených profesionálov v ich oblasti odbornosti a aj keď boli účastníci pred úsudkom výslovne varovaní pred skreslením ukotvenia. Skúsenosť a povedomie ukotvenie znižujú, ale neodstraňujú.

Návrhový dôsledok je priamy: keď AI agent predloží odporúčanie ako prvé, následné vyšetrovanie operátora je tvarované týmto rámcovaním. Skôr bude hľadať potvrdzujúce dôkazy a menej pravdepodobne bude sledovať alternatívne hypotézy.

### Návrhové dôsledky

- **Zvážte opak:** Výslovne vyzvite operátorov, aby zvážili alternatívne vysvetlenia, kým prijmú odporúčanie AI.
- **Dáta pred odporúčaním:** Predložte surové dáta a kontext skôr, než odhalíte odporúčanie AI, čím dáte operátorovi príležitosť utvoriť si nezávislé hodnotenie. Drahšie na čase operátora, ale významne znižuje ukotvenie.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/credit-desk.html">The Credit Desk</a> spustí experiment s poradím na vás naprieč šiestimi žiadosťami o úver (dve zo skóre AI sú zámerne zle kalibrované); <a href="https://demos.barcik.training/demos/operators-dilemma.html#act2">2. dejstvo The Operator's Dilemma</a> to robí s produkčným incidentom.
</div>

## Posun k sebauspokojeniu

Posun k sebauspokojeniu je postupná erózia bdelosti, ku ktorej dochádza, keď automatizovaný systém dlhší čas spoľahlivo funguje. Na rozdiel od automatizačnej zaujatosti (ktorá pôsobí pri jednotlivých rozhodnutiach) pôsobí posun k sebauspokojeniu na úrovni trvalého monitorovacieho správania a vytvára rozširujúcu sa medzeru medzi poskytovaným dohľadom a predpokladaným dohľadom.

### M/V Royal Majesty (1995)

Výletná loď M/V Royal Majesty najazdila na plytčinu pri Nantuckete s 1 509 ľuďmi na palube, lebo kábel antény GPS lode sa odpojil, čo spôsobilo, že GPS prešiel na výpočet polohy odhadom. Systém zobrazoval varovný indikátor. Tím na mostíku si ho nevšimol. Loď **34 hodín** plávala po čoraz odchýlenejšom kurze a odchýlila sa **17 námorných míľ** od trasy. Viaceré nezávislé ukazovatele (radar, meranie hĺbky, vizuálne pozorovania) protirečili polohe podľa GPS, ale posádka prestala krížovo kontrolovať.

Úzko súvisí **degradácia zručností**: FAA zdokumentovala, že **60 % leteckých nehôd** zahŕňajúcich chybu pilota obsahovalo nedostatok zručnosti v ručnom pilotovaní: zručnosti, ktoré zakrpateli, lebo lietanie riešil autopilot. V IT prevádzke sa to prejavuje, keď AI agenti dlhší čas riešia vyšetrovanie a nápravu a operátori strácajú diagnostické zručnosti, ktoré eskalácia predpokladá, že majú.

### Model úpadku konania podľa CIGI

Centre for International Governance Innovation opisuje štvorstupňový organizačný vzor: **Experimentovanie** (AI dopĺňa ľudskú prácu) → **Integrácia** (AI sa stáva štandardom, nezávislá analýza klesá) → **Spoliehanie** (AI je primárny vstup, zručnosti krpatejú, noví ľudia sú školení pracovať s AI, nie bez nej) → **Závislosť** (organizácia nedokáže fungovať bez AI, žiadny záložný plán).

> **Kľúčové rozlíšenie:** Posun k sebauspokojeniu nie je o jednotlivých operátoroch robiacich zlé rozhodnutia, ale o organizačných systémoch, ktoré postupne strácajú schopnosť nezávislého úsudku. Čeliť mu vyžaduje organizačné zásahy: pravidelnú povinnú manuálnu prevádzku, kontrolné tikety so známymi výsledkami, sledovanie mier schválenia bez revízie a udržiavanie zručností pomocou simulácií.

> **Poznámka z terénu od autora.** Tieto javy púšťam na svojich workshopoch ako živú simuláciu (cvičenie nakoniec vyrástlo do hry The Operator's Dilemma, na ktorú táto kapitola stále odkazuje). Okamih, keď som prestal potrebovať slajdy, nastal, keď bezpečnostný inžinier, hlboko v časovanom kole triáže, schválil odporúčanie, ktoré protirečilo dátam na jeho vlastnej obrazovke, zdvihol zrak a povedal: „Vedel som, že niečo nesedí, ale bežal časovač.“ Nikto sa nezasmial. Polovica miestnosti urobila to isté o pár incidentov skôr. O automatizačnej zaujatosti môžete prednášať hodinu a ľudia zdvorilo prikyvujú. Deväťdesiat sekúnd odpočtu ich obráti.

## Zhrnutie

Týchto päť javov (automatizačná zaujatosť, únava z výstrah, ukotvenie, posun k sebauspokojeniu a degradácia zručností) nie je nezávislých. Interagujú a navzájom sa posilňujú:

- **Únava z výstrah** zvyšuje **automatizačnú zaujatosť** (preťažení operátori prijímajú odporúčania AI bez skúmania).
- **Posun k sebauspokojeniu** zrýchľuje **degradáciu zručností** (operátori, ktorí prestanú pozorne monitorovať, prestanú aj cvičiť zručnosti potrebné na účinné monitorovanie).
- **Ukotvenie** posilňuje **automatizačnú zaujatosť** (odporúčanie AI tvaruje myslenie a sťažuje nezávislé hodnotenie).
- **Rozptýlenie zodpovednosti** medzi človekom a AI umožňuje **posun k sebauspokojeniu**: Bleher a Braun (2022) opisujú výslednú medzeru v zodpovednosti: operátor môže ukázať na to, že sa riadil systémom, kým dodávateľ môže ukázať na to, že konečné rozhodnutie urobil človek. Keď sa nikto necíti individuálne zodpovedný, je menej motivácie udržiavať bdelosť.

Štrukturálne vzory z kapitoly 3 poskytujú kostru účinnej interakcie človeka a AI. Kognitívne javy v tejto kapitole určujú, či táto kostra podopiera funkčný systém alebo prázdny. Vzor Odporučiť a čakať, ktorý predkladá svoje odporúčania spôsobom, ktorý operátora ukotví a neposkytne žiadnu vynucovaciu funkciu pre nezávislé hodnotenie, je v praxi vzor Vykonať a hlásiť s krokmi navyše.

Ďalšia kapitola skúma, ako prezentovať informácie na šve: konkrétne komunikačné formáty a stratégie zverejňovania, ktoré podporujú dobré ľudské rozhodovanie tvárou v tvár týmto kognitívnym výzvam.
