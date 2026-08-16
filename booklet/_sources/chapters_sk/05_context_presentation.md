# Kapitola 5: Prezentácia kontextu

To, ako prezentujete informácie, určuje, čo operátor vidí. A to, čo operátor vidí, určuje, čo rozhodne. Nie je to metafora, ale merateľný, reprodukovateľný jav: tie isté dáta o incidente, prezentované v rôznych formátoch, vedú u tých istých operátorov k rôznym rozhodnutiam so štatisticky významnou konzistenciou.

Kognitívne výzvy opísané v kapitole 4 (automatizačná zaujatosť, ukotvenie, únava z výstrah) sú vlastnosťami interakcie medzi ľudským poznávaním a návrhom informácií, nie pevnými črtami mysle. Dobre navrhnutý prezentačný formát môže ukotvenie znížiť. Zle navrhnutý ho môže zosilniť. Formát je nosným prvkom architektúry systému, nie kozmetickou vrstvou nanesenou po dokončení inžinierstva.

Táto kapitola predstavuje štyri rámce prezentácie kontextu na šve medzi AI a človekom založené na dôkazoch, s konkrétnym usmernením, ako každý uplatniť v prevádzkových AI systémoch.

## Rámec SBAR

SBAR (Situation, Background, Assessment, Recommendation: situácia, pozadie, hodnotenie, odporúčanie) je štruktúrovaný komunikačný rámec široko pripisovaný námornej komunikačnej praxi, hoci zdokumentovaná história začína v **Kaiser Permanente**, ktorého tím pre bezpečnosť pacientov (Leonard, Graham a Bonacum) ho okolo roku 2002 formalizoval pre zdravotníctvo. (Príbeh o pôvode „vyvinuté na jadrových ponorkách“ sa opakuje všade vrátane nemocničných školiacich materiálov, ale žiadny primárny zdroj z námorníctva sa preň nikdy neobjavil; príhodná pripomienka, v kapitole o prezentácii dôkazov, kontrolovať reťazec dôkazov.) Z Kaiseru sa rozšíril do komunikácie pri klinických odovzdaniach v tisíckach nemocníc.

### Dôkazy

Účinok rámca na kvalitu komunikácie je merateľný a veľký. V jednej nedávnej kontrolovanej štúdii (El-Sayed Ghonem a El-Husany, 2023) vzrástol podiel sestier preukazujúcich primeranú komunikáciu pri odovzdaní štruktúrovanú podľa SBAR zo **4,8 % pred štruktúrovaným tréningovým programom na 92,8 % po ňom**. SBAR je aj kľúčovým nástrojom v TeamSTEPPS, kurikule tímovej práce vyvinutom ministerstvom obrany s Agentúrou pre výskum a kvalitu zdravotnej starostlivosti, ktoré nesie vlastnú viacdesaťročnú dôkazovú základňu o tom, že štruktúrovaná komunikácia znižuje klinické chyby.

Veľkosť takýchto zlepšení si žiada vysvetlenie. Informácie dostupné sestrám sa nezmenili. Ich klinické znalosti sa nezmenili. Zmenila sa štruktúra, v ktorej komunikovali. SBAR im dal rámec, ktorý zabezpečil, že zahrnú všetky kritické informácie, predložia ich v predvídateľnom poradí a urobia výslovný rozdiel medzi pozorovaním (situácia, pozadie) a interpretáciou (hodnotenie, odporúčanie).

### SBAR prispôsobený výstupu AI agenta

Rovnaké princípy sa priamo vzťahujú na to, ako AI agent komunikuje s ľudským operátorom. Neštruktúrovaný výstup (stena textu zhŕňajúca vyšetrovanie) núti operátora extrahovať štruktúru, čo je presne ten druh kognitívnej práce, ktorý vedie k prehliadnutým informáciám a ukotveniu na prvom rozpoznanom vzore. Štruktúrovaný výstup znižuje kognitívnu záťaž a zabezpečuje úplnosť.

Pre prevádzkové AI systémy sa SBAR dá prispôsobiť do šesťprvkového rámca:

| Prvok | Ekvivalent v SBAR | Obsah | Účel |
|---------|----------------|---------|---------|
| **ČO SA STALO** | Situácia | Stručné konštatovanie zistenej udalosti alebo stavu | Zorientovať operátora v aktuálnom stave |
| **ČO SOM SKÚSIL** | Pozadie | Kroky, ktoré AI agent urobil počas vyšetrovania alebo prvotnej nápravy | Poskytnúť kontext o tom, čo je už známe a vylúčené |
| **ČO ODPORÚČAM** | Odporúčanie | Konkrétny odporúčaný krok s očakávaným výsledkom | Dať operátorovi jasný rozhodovací bod |
| **ÚROVEŇ RIZIKA** | Hodnotenie | Klasifikácia závažnosti so stručným zdôvodnením | Kalibrovať naliehavosť odpovede operátora |
| **CENA NEČINNOSTI** | (rozšírenie) | Čo sa stane, ak sa neurobí nič, s odhadovaným časovým rámcom | Čeliť skresleniu status quo a vytvoriť naliehavosť tam, kde je opodstatnená |
| **DÔKAZY** | (rozšírenie) | Odkazy na logy, metriky, stopy a články znalostnej bázy | Umožniť nezávislé overenie a hĺbkové vyšetrovanie |

Rozšírenia nad rámec štandardného SBAR (cena nečinnosti a dôkazy) riešia špecifické výzvy interakcie AI a človeka. Cena nečinnosti čelí prirodzenému ľudskému sklonu k nečinnosti tvárou v tvár neistote (skreslenie status quo). Dôkazy riešia automatizačnú zaujatosť tým, že poskytujú surový materiál na nezávislé overenie, namiesto toho, aby operátora žiadali dôverovať iba syntéze AI.

### Praktický príklad

Vezmite AI agenta, ktorý odhalil potenciálny bezpečnostný incident. Tu sú tie isté informácie prezentované v troch formátoch:

**Formát 1: surový výpis**

```
ID výstrahy: SEC-2026-04891. Zdroj: korelačné pravidlo SIEM CR-142.
Časová pečiatka: 2026-04-11T03:42:17Z. Zistené viaceré neúspešné pokusy
o prihlásenie cez SSH z IP 198.51.100.42 na hostiteľov prod-web-01 až
prod-web-08. Celkový počet pokusov: 847 za 23 minút. Geolokácia zdrojovej IP:
São Paulo, Brazília. Žiadne úspešné autentifikácie. Tempo: ~37 pokusov/min.
Vzor konzistentný s credential stuffingom. Spravodajstvo o hrozbách: IP nie je
v známych blokovacích zoznamoch. Predchádzajúca aktivita z tejto IP: žiadna za
posledných 90 dní. Sken zraniteľností hostiteľov (posledných 7 dní):
prod-web-03 má nezáplatované OpenSSH (CVE-2024-6387). Aktuálna konfigurácia
SSH: autentifikácia heslom povolená na všetkých hostiteľoch. Stav fail2ban:
aktívny, prah nastavený na 10 zlyhaní/5 minút, aktuálny zoznam zákazov
neobsahuje zdrojovú IP kvôli rozloženému časovaniu...
```

**Formát 2: štruktúra SBAR**

```
ČO SA STALO: Prebiehajúci útok credential stuffing na 8 produkčných
webových serverov z jedinej IP (198.51.100.42, São Paulo).

ČO SOM SKÚSIL: Dopytoval som spravodajstvo o hrozbách (IP nie je v známych
blokovacích zoznamoch), skontroloval úspešné autentifikácie (žiadne),
prešiel konfigurácie SSH (autentifikácia heslom povolená na všetkých
8 hostiteľoch), skontroloval fail2ban (aktívny, ale nespustený kvôli
rozloženému časovaniu).

ČO ODPORÚČAM: Zablokovať IP 198.51.100.42 na sieťovom firewalle
a vypnúť autentifikáciu SSH heslom na všetkých produkčných hostiteľoch.

ÚROVEŇ RIZIKA: Stredná. Zatiaľ nezistený prienik, ale prod-web-03 má
nezáplatovanú zraniteľnosť OpenSSH (CVE-2024-6387), ktorá by mohla byť
zneužitá, ak útočník zmení taktiku.

CENA NEČINNOSTI: Pokračujúce pokusy hrubou silou s potenciálnym zneužitím
CVE-2024-6387 na prod-web-03. Ak je zraniteľnosť zneužitá, útočník získa
prístup k shellu na produkčnom serveri.

DÔKAZY: [výstraha SIEM] [logy SSH] [správa zo skenu zraniteľností]
[dopyt na spravodajstvo o hrozbách]
```

**Formát 3: postupné odhaľovanie (podrobne v ďalšej časti)**

```
Vrstva 1 (5-sekundový pohľad):
  🟡 STREDNÉ | Credential stuffing na 8 prod webových serveroch |
  Odporúčanie: zablokovať zdrojovú IP + vypnúť autentifikáciu heslom

Vrstva 2 (30-sekundové hodnotenie):
  [úplný SBAR ako vyššie]

Vrstva 3 (hĺbkový ponor):
  [úplný reťazec dôkazov s výňatkami z logov, detailmi CVE,
  sieťovou topológiou, historickým kontextom]
```

Surový výpis obsahuje všetky tie isté informácie ako formát SBAR, ale núti operátora vykonať kognitívnu prácu ich štruktúrovania. Pod časovým tlakom a objemom výstrah typickým pre bezpečnostnú prevádzku je táto kognitívna práca presne to, čo sa preskočí, a jej vynechanie je to, čo vedie k prehliadnutému kontextu a zlým rozhodnutiam.

## Kleinov model rozhodovania založeného na rozpoznaní

Model rozhodovania založeného na rozpoznaní (Recognition-Primed Decision, RPD) Garyho Kleina, vyvinutý terénnymi štúdiami hasičov, vojenských veliteľov a sestier na jednotkách intenzívnej starostlivosti, zásadne spochybňuje klasický model rozhodovania ako procesu porovnávania alternatív.

### Dôkazy

V Kleinovej pôvodnej štúdii na požiarisku (26 veliteľov, 156 rozhodovacích bodov) **zhruba 80 % expertných rozhodnutí nezahŕňalo vôbec žiadne porovnanie možností**: veliteľ situáciu rozpoznal, vybavil si jediný fungujúci postup a išiel podľa neho. Menej než jedno rozhodnutie z ôsmich zahŕňalo zvažovanie alternatív. Experti negenerovali zoznam možností, nehodnotili každú podľa kritérií a nevyberali najlepšiu. Namiesto toho rozpoznali aktuálnu situáciu ako podobnú predtým zažitému vzoru, vybavili si krok, ktorý v tom vzore fungoval, mentálne simulovali, či by fungoval v aktuálnej situácii, a buď ho vykonali, alebo upravili.

To má priamy a protiintuitívny návrhový dôsledok: **predloženie viacerých možností expertnému operátorovi môže kvalitu rozhodnutia zhoršiť, nie zlepšiť.** Kognitívny proces experta je optimalizovaný na hodnotenie jednej možnosti voči situácii, nie na porovnávanie možností medzi sebou. Systém, ktorý predloží tri možné koreňové príčiny s výhodami a nevýhodami každej, bojuje s prirodzeným rozhodovacím procesom experta. Systém, ktorý predloží jedinú najpravdepodobnejšiu koreňovú príčinu s podpornými dôkazmi a odporúčaným krokom, s ním pracuje.

### Návrhový dôsledok pre AI agentov

Predložte **jediný odporúčaný krok AI ako prvý**, s podpornými dôkazmi. Sprístupnite alternatívne vysvetlenia na požiadanie (postupné odhaľovanie, diskutované nižšie), ale nenúťte experta spracovať ich skôr, než vyhodnotí primárne odporúčanie.

To neznamená alternatívy skrývať. Znamená to štruktúrovať prezentáciu tak, aby prvým kognitívnym zapojením operátora bola najpravdepodobnejšia hypotéza, čo je vzor zapojenia zodpovedajúci tomu, ako experti naozaj premýšľajú. Ak primárne odporúčanie nezodpovedá rozpoznaniu vzoru operátorom (ak niečo pôsobí zle), operátor bude hľadať alternatívy. Systém by mu to mal uľahčiť. Ale nemal by to vynucovať ako predvolenú cestu.

> **Kľúčové rozlíšenie:** Pre operátorov nováčikov môže byť predloženie alternatív cenné, lebo nováčikom chýba knižnica vzorov, ktorá umožňuje rozhodnutia založené na rozpoznaní. Optimálny prezentačný formát závisí od úrovne odbornosti operátora: ďalší argument pre adaptívne rozhrania, ktoré sa prispôsobujú používateľovi.

## Časový tlak a kvalita rozhodnutí

Interakcia medzi časovým tlakom a podporou AI je jemnejšia než „rýchlejšie je lepšie“ alebo „pomalšie je bezpečnejšie“. Výskum Swaroopa a kol. na Harvarde (2023) zistil, že rôzne typy podpory AI majú rôzne kompromisy medzi presnosťou a časom a optimálny typ podpory závisí od času dostupného na rozhodnutie.

Pri nízkom časovom tlaku operátori najviac ťažili z podpory AI, ktorá poskytovala vysvetlenia a podporné dôkazy, z toho druhu podpory, ktorý umožňuje analytické uvažovanie a nezávislé overenie. Pri vysokom časovom tlaku operátori najviac ťažili z jednoduchých, priamych odporúčaní, z toho druhu podpory, ktorý podporuje rýchle rozpoznávanie vzorov.

Znepokojivejšie je, že výskum zistil, že pod časovým tlakom **sa rozhodnutia stali rizikovejšími a nadmerné spoliehanie sa na AI vzrástlo**. Operátori pod časovým tlakom skôr prijali odporúčanie AI bez hodnotenia, skôr si vybrali rizikovejšiu možnosť, keď ju AI navrhla, a menej pravdepodobne si všimli chyby v uvažovaní AI.

### Návrhový dôsledok

Prezentačný formát by sa mal prispôsobiť naliehavosti situácie:

- **Nízka naliehavosť (minúty až hodiny):** Predložte úplný SBAR s odkazmi na dôkazy, povzbudzujte nezávislé overenie, uplatnite kognitívne vynucovacie funkcie (pozri kapitolu 4).
- **Stredná naliehavosť (sekundy až minúty):** Predložte zhrnutie SBAR s jediným odporúčaným krokom, dôkazy sprístupnite, ale nevyžadujte ich revíziu.
- **Vysoká naliehavosť (okamžite):** Predložte iba krok a závažnosť, s vykonaním na jedno kliknutie. Rozhodnutie zalogujte na dodatočnú revíziu.

To sa priamo mapuje na rámec postupného odhaľovania diskutovaný nižšie.

## Postupné odhaľovanie

Postupné odhaľovanie je princíp informačnej architektúry, ktorý organizuje obsah do vrstiev rastúcej podrobnosti a dovoľuje používateľovi dostať sa k úrovni detailu, ktorú potrebuje, bez toho, aby ho zahltila úroveň, ktorú nepotrebuje. V prevádzkových AI systémoch je to primárny mechanizmus podpory rýchleho rozpoznávania vzorov u expertov aj dôkladnej analýzy u nováčikov v jedinom rozhraní.

### Tri vrstvy

**Vrstva 1: 5-sekundový pohľad**

To je to, čo operátor vidí, keď sa prvýkrát pozrie na obrazovku, preletí upozornenie alebo mrkne na dashboard. Musí za päť sekúnd alebo menej komunikovať tri veci:

- **Závažnosť** (vizuálny indikátor: farba, ikona alebo kategorický štítok)
- **Zhrnutie** (jedna veta: čo sa stalo a čo je v hre)
- **Odporúčaný krok** (jedna fráza: čo urobiť)

Vrstva 1 podporuje rozhodovací proces experta založený na rozpoznaní. Skúsený operátor prezerajúci vrstvu 1 buď vzor rozpozná a koná, alebo ho nerozpozná a ide hlbšie. Žiadne kognitívne úsilie sa nemrhá na detail, ktorý na prvotné rozpoznanie netreba.

Príklad:
```
🔴 KRITICKÉ | Zistené prepnutie primárnej databázy na záložnú, oneskorenie
replikácie rastie | Odporúčanie: povýšiť repliku db-replica-02 na primárnu
```

**Vrstva 2: 30-sekundové hodnotenie**

To je brífing SBAR s úrovňami istoty. Poskytuje dosť kontextu na to, aby operátor vyhodnotil odporúčanie AI, položil objasňujúce otázky alebo si utvoril alternatívnu hypotézu. Je to vrstva, kde operátor prechádza z rozpoznávania vzorov k analytickému uvažovaniu.

Vrstva 2 zahŕňa:
- Úplnú štruktúru SBAR (čo sa stalo, čo som skúsil, čo odporúčam, úroveň rizika, cena nečinnosti)
- Úroveň istoty AI (diskutovanú v ďalšej časti)
- Kľúčové metriky a ich trendy
- Relevantné nedávne zmeny alebo udalosti

**Vrstva 3: hĺbkový ponor**

To je úplný reťazec dôkazov: surové logy, časové rady metrík, rozdiely konfigurácií, články znalostnej bázy, historické záznamy incidentov a reťazec uvažovania AI. Používa sa na revíziu po incidente, v prípadoch, keď operátor nesúhlasí s hodnotením AI, alebo pri nových situáciách, ktoré nezodpovedajú žiadnemu známemu vzoru.

Vrstva 3 je aj miestom, kde prepojenie s dôkazmi (diskutované nižšie) prináša svoju hodnotu, lebo dovoľuje operátorovi vystopovať závery AI späť ku konkrétnym dátovým bodom.

### Prečo tri vrstvy

Tri nie sú ľubovoľné. Výskum kognitívnej záťaže konzistentne ukazuje, že ľudia dokážu efektívne spracovať 3 – 5 kusov informácií naraz (Miller, 1956; Cowan, 2001). Tri vrstvy sa mapujú na tri odlišné kognitívne režimy:

| Vrstva | Čas | Kognitívny režim | Typ rozhodnutia | Stav používateľa |
|-------|------|----------------|---------------|------------|
| Vrstva 1 | 5 sekúnd | Rozpoznávanie vzorov | Konať alebo vyšetrovať ďalej | Prezeranie, triáž |
| Vrstva 2 | 30 sekúnd | Analytické uvažovanie | Schváliť, upraviť alebo zamietnuť odporúčanie | Sústredené hodnotenie |
| Vrstva 3 | Minúty až hodiny | Hĺbková analýza | Vyšetrovanie koreňovej príčiny, revízia po incidente | Zámerné vyšetrovanie |

## Komunikácia istoty

To, ako AI agent komunikuje svoju istotu v odporúčaní, je jedným z najzávažnejších a najčastejšie zle zvládnutých aspektov prezentácie kontextu.

### Problém so surovými pravdepodobnosťami

Intuitívny prístup (predloženie číselnej pravdepodobnosti („87 % istota, že ide o útok credential stuffing“)) je pre väčšinu operátorov horší než zbytočný. Výskum konzistentne ukazuje, že:

- Ľudia pravdepodobnosti zle kalibrujú, preceňujú nízke a podceňujú vysoké (Kahneman a Tversky, 1979).
- Číselné pravdepodobnosti vytvárajú falošnú presnosť. „87 % istota“ naznačuje úroveň kalibrácie, akú žiadny súčasný LLM nemá.
- Rôzni operátori interpretujú tú istú pravdepodobnosť rôzne. „87 %“ môže jednému operátorovi pripadať takmer isté a inému nepríjemne neisté.

### Kategorická istota s kalibráciou

Účinnejší prístup používa kategorické štítky namapované na definované rozsahy pravdepodobnosti a prevádzkové dôsledky:

| Kategória | Rozsah pravdepodobnosti | Prevádzkový dôsledok |
|----------|------------------|------------------------|
| **Potvrdené** | >95 % | Dôkazy sú presvedčivé; pokračujte odporúčaným krokom |
| **Vysoká istota** | 80 – 95 % | Silné dôkazy; odporúčanie je pravdepodobne správne, ale overte kľúčové predpoklady |
| **Stredná istota** | 60 – 80 % | Podporné dôkazy existujú, ale alternatívne vysvetlenia sú vierohodné; pred konaním vyšetrite |
| **Nízka istota** | 40 – 60 % | Dôkazy sú nejednoznačné; berte ako stopu na vyšetrovanie, nie ako základ konania |
| **Špekulatívne** | <40 % | Nedostatočné dôkazy; pred akýmkoľvek krokom je potrebné ďalšie vyšetrovanie |

Hodnota kategorických štítkov nespočíva v presnosti, ale v kalibrácii správania operátora. „Vysoká istota“ komunikuje nielen pravdepodobnosť, ale aj očakávanú reakciu: overte kľúčové predpoklady, potom konajte. „Nízka istota“ komunikuje inú očakávanú reakciu: vyšetrujte ďalej. Štítok vedie správanie spôsobom, akým číslo nie.

### Vizualizácia neistoty

Výskum Reyesa a kol. (2025) zistil, že predloženie vizualizácií neistoty (grafických zobrazení rozdelenia istoty AI namiesto jediného bodového odhadu) **zvýšilo dôveru u 58 % účastníkov, ktorí prišli s negatívnymi postojmi k AI** (štvrtina vzorky; účinok sa sústredil presne tam, kde je oprava dôvery najťažšia). Vizualizácia neistoty je kalibračná páka, nie univerzálna.

Doplňujúca štúdia na ACM FAccT (2025) zistila, že **skóre istoty založené na vzdialenosti** (metriky, ktoré komunikujú, ako podobná je aktuálna situácia tréningovým dátam, na ktorých bola AI kalibrovaná) priniesli **o 8,2 % viac správnych rozhodnutí** v porovnaní s tradičnými skóre istoty, v malej medicínskej štúdii delegovania úloh (29 účastníkov; berte to ako sľubné, nie uzavreté). Skóre založené na vzdialenosti pomáhajú operátorom pochopiť nielen to, aká istá si je AI, ale aj to, aká relevantná je jej kalibrácia istoty pre aktuálnu situáciu.

> **Kľúčový postreh:** Cieľom komunikácie istoty nie je presne sprostredkovať vnútorný stav AI, ale primerane kalibrovať správanie operátora. Formát istoty, ktorý spôsobí, že operátori overujú odporúčania s vysokou istotou a vyšetrujú tie s nízkou, uspieva, bez ohľadu na to, ako presne sa mapuje na skutočné rozdelenie pravdepodobnosti modelu.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/border-queue.html">The Border Queue</a> vám ukáže tie isté hodnotenia rizika v troch rámcovaniach (surové desatinné čísla, kalibrované kategórie, holé verdikty) a zmeria, čo každé robí s vašimi postúpeniami a vašou istotou; <a href="https://demos.barcik.training/demos/operators-dilemma.html#act3">3. dejstvo The Operator's Dilemma</a> spúšťa experiment s rámcovaním na diagnostike jedného incidentu.
</div>

## Prepojenie s dôkazmi a vysvetliteľnosť

Poslednou zložkou prezentácie kontextu je prepojenie s dôkazmi: spojenie záverov a odporúčaní AI s konkrétnymi dátovými bodmi, ktoré ich podporujú. Slúži dvom funkciám: umožňuje nezávislé overenie (čelí automatizačnej zaujatosti) a poskytuje surový materiál na to, aby si operátor vybudoval vlastné situačné povedomie namiesto úplného spoliehania sa na syntézu AI.

### Citácie RAG a vložené odkazy

Pre AI agentov používajúcich generovanie rozšírené o vyhľadávanie (RAG) je najpriamočiarejšou formou prepojenia s dôkazmi vložená citácia: označenie každého tvrdenia vo výstupe AI odkazom na zdrojový dokument, záznam logu alebo metriku, ktorá ho podporuje. Je to rovnaký prístup ako v akademickom písaní, prispôsobený prevádzkovému kontextu.

Príklad:
```
Hodnotenie koreňovej príčiny: Vyčerpanie fondu spojení na db-primary-01
[1] spustilo nasadenie v2.4.7 o 14:32 UTC [2], ktoré zaviedlo únik
spojení v module autentifikácie používateľov [3]. Počet spojení vzrástol
zo základných 45 na maximum 500 za 23 minút [4], čo spôsobilo kaskádové
vypršania časových limitov v nadväzujúcich službách [5].

Zdroje:
[1] Metrika CloudWatch: aktívne spojenia db-primary-01 (14:00 – 15:00 UTC)
[2] Log nasadenia: záznam o vydaní v2.4.7
[3] Git diff: commit a3f7c2e, súbor auth/connection_pool.py, riadky 142 – 158
[4] Dashboard metrík fondu spojení (odkaz)
[5] Mapa závislostí služieb so stopou šírenia chýb (odkaz)
```

### Postupné odhaľovanie reťazca uvažovania

Pri zložitejších analýzach sa dá pomocou postupného odhaľovania prezentovať aj samotný reťazec uvažovania AI:

- **Vrstva 1:** Záver a odporúčaný krok (bez uvažovania).
- **Vrstva 2:** Kľúčové kroky uvažovania: 3 – 4 najdôležitejšie logické spojenia medzi dôkazmi a záverom.
- **Vrstva 3:** Úplný reťazec uvažovania vrátane hypotéz, ktoré boli zvážené a zamietnuté, s dôkazmi pre a proti každej.

Tento prístup rešpektuje rozhodovací proces experta založený na rozpoznaní (vrstva 1 stačí, ak je vzor známy) a zároveň poskytuje úplnú audítorskú stopu pre prípady, ktoré vyžadujú hlbšiu analýzu alebo revíziu po incidente.

### Program DARPA XAI

Agentúra ministerstva obrany pre pokročilé výskumné projekty (DARPA) viedla svoj program vysvetliteľnej AI (XAI) v rokoch 2017 až 2021 a financovala okolo tucta výskumných tímov na testovanie prístupov, ako urobiť uvažovanie AI systémov transparentným pre ľudských operátorov. Medzi prístupmi, ktoré retrospektívy programu vyzdvihujú, vynikajú **vysvetlenia založené na príkladoch** ako obzvlášť účinné pre prevádzkové rozhodovanie (program nevyhlásil jediného univerzálneho víťaza; ktorý štýl vysvetlenia pomáha, závisí od úlohy).

Namiesto vysvetľovania vnútornej logiky AI („neurónová sieť priradila váhu 0,73 príznaku X“) vysvetlenia založené na príkladoch predkladajú podobné prípady z minulosti a ich výsledky: „Táto situácia je podobná incidentu INC-2025-3847, ktorý spôsobila nesprávna konfigurácia DNS a vyriešilo ho vyprázdnenie cache DNS. Riešenie trvalo 12 minút a nebol hlásený žiadny dopad na zákazníkov.“

Vysvetlenia založené na príkladoch fungujú, lebo sa zhodujú s modelom rozhodovania založeného na rozpoznaní: pomáhajú operátorovi priradiť aktuálnu situáciu k známemu vzoru, čo je kognitívny proces, ktorý experti naozaj používajú.

## Spojenie do celku

Účinná prezentácia kontextu na šve medzi AI a človekom integruje všetky štyri rámce:

1. **Štruktúrujte** výstup pomocou SBAR, aby ste zabezpečili úplnosť a predvídateľnosť.
2. **Priorizujte** odporúčaný krok ako prvý, v súlade s modelom RPD, a alternatívy sprístupnite na požiadanie.
3. **Vrstvite** informácie pomocou postupného odhaľovania, aby sa každý operátor mohol zapojiť v hĺbke primeranej jeho odbornosti a naliehavosti situácie.
4. **Kalibrujte** komunikáciu istoty pomocou kategorických štítkov s prevádzkovými dôsledkami, nie surových pravdepodobností.
5. **Prepájajte** závery s dôkazmi pomocou vložených citácií a vysvetlení založených na príkladoch.

Nie sú to nezávislé návrhové voľby. Interagujú: SBAR poskytuje štruktúru pre vrstvu 2. Model RPD určuje, čo ide do vrstvy 1. Komunikácia istoty určuje, ako sa operátor zapája do vrstiev 1 a 2. Prepojenie s dôkazmi napĺňa vrstvu 3.

Výsledkom, ak sa implementuje súdržne, je prezentačný formát, ktorý:

- Podporuje rýchle rozpoznávanie vzorov u skúsených operátorov (vrstva 1, zosúladenie s RPD)
- Umožňuje analytické hodnotenie, keď je potrebné (vrstva 2, štruktúra SBAR)
- Poskytuje úplnú audítorskú stopu na dodatočnú revíziu a učenie (vrstva 3, prepojenie s dôkazmi)
- Primerane kalibruje dôveru operátora (komunikácia istoty)
- Znižuje automatizačnú zaujatosť tým, že uľahčuje nezávislé overenie (prepojenie s dôkazmi)
- Znižuje ukotvenie tým, že predkladá dáta pred interpretáciou, keď to čas dovolí (poradie SBAR)

Ďalšia kapitola skúma, ako sa dôvera medzi ľudskými operátormi a AI agentmi vyvíja, kalibruje a (keď sa zle riadi) rúca.
