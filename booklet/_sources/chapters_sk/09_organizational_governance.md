# Kapitola 9: Organizačná governance

Návrh technológie je nutný, ale nie postačujúci. Organizačná governance rozhoduje o tom, či dobrý návrh prežije kontakt s realitou.

Predchádzajúce kapitoly riešili, ako navrhovať vzory interakcie AI a človeka na úrovni rozhrania: ako sa prezentujú informácie, ako sa prideľuje autonómia, ako sa kalibruje dôvera, ako sa zadržiavajú zlyhania. Ale každé z tých návrhových rozhodnutí existuje v organizačnom kontexte, ktorý ho môže buď udržať, alebo erodovať. Dobre navrhnutý vypínač je zbytočný, ak ho nikto nie je oprávnený aktivovať. Starostlivo kalibrovaný prah istoty sa posunie, ak nikto nekontroluje, či stále zodpovedá skutočnému výkonu modelu. Mechanizmus prebitia zakrpatie, ak organizačná kultúra trestá operátorov, ktorí ho používajú. Táto kapitola skúma štruktúry governance, regulačné rámce a modely zrelosti, ktoré rozhodujú o tom, či návrh interakcie AI a človeka prežije nasadenie.

## Vlastníctvo politiky: model troch línií

Najbežnejším zlyhaním governance pri nasadeniach AI je rozptýlené vlastníctvo. Keď za správanie AI systému nezodpovedá jediná osoba alebo tím, každý predpokladá, že sleduje niekto iný. Model troch línií, prevzatý z rámcov riadenia rizík používaných vo finančných službách, poskytuje jasnú štruktúru:

**Prvá línia: aplikačné tímy.** Inžinieri a operátori, ktorí AI systém stavajú, nasadzujú a prevádzkujú. Vlastnia každodenné rozhodnutia: návrh promptov, ladenie prahov, reakciu na incidenty, monitorovanie výkonu. Sú systému najbližšie a najpodrobnejšie rozumejú jeho správaniu.

**Druhá línia: funkcie rizika a súladu.** Tímy, ktoré nastavujú štandardy, kontrolujú návrhy a monitorujú dodržiavanie. Systém nestavajú, ale definujú mantinely, v ktorých musí fungovať: prijateľné úrovne rizika, požadovanú dokumentáciu, povinné testovanie, súlad s platnými predpismi.

**Tretia línia: nezávislý audit.** Interní alebo externí audítori, ktorí periodicky posudzujú, či prvá a druhá línia fungujú, ako majú. Poskytujú vedeniu a prípadne regulátorom uistenie, že rámec governance nie je iba zdokumentovaný, ale skutočne praktizovaný.

Každý AI systém musí mať **pomenovaného vlastníka**: nie tím, nie výbor, ale jednotlivca, ktorý zodpovedá za správanie systému a je oprávnený o ňom rozhodovať, vrátane rozhodnutia ho vypnúť. Tento pomenovaný vlastník zvyčajne sedí v prvej línii, ale má definované eskalačné cesty do druhej a tretej. (Obsadenie a prevádzka tohto dohľadu sa sama stáva servisnou líniou; biznisový prípad pre „dohľad ako službu“ analyzuje [The Token Economics](/token-economics-sk/).)

Dôkazy pre túto štruktúru presahujú teóriu, hoci sú smerové, nie presné: prieskumy odvetvia konzistentne zisťujú, že organizácie s najlepšími výsledkami v AI oveľa pravdepodobnejšie prevádzkujú medzifunkčné orgány governance spájajúce inžinierstvo, riziko, právo a doménovú odbornosť. Rýchlostná výhoda, ktorú takéto prieskumy hlásia, je protiintuitívna, ale konzistentná: jasná governance znižuje nejednoznačnosť, čo skracuje čas cyklu procesov revízie a schvaľovania, ktoré inak nasadenie brzdia.

## Model Rady pre agentov od Galileo AI

Štruktúry governance sa musia operacionalizovať pravidelnými rytmami, inak sa rozpadnú na dokumentáciu, ktorú nikto nečíta. Model „Agent Council“ od Galileo AI poskytuje otestovanú šablónu:

**Týždenná triáž (30 minút).** Stále stretnutie, ktoré preberá výkon AI systému za minulý týždeň vrátane incidentov, tesných únikov alebo anomálií. Program je štruktúrovaný: nové incidenty, prebiehajúce vyšetrovania, trendy metrík a nadchádzajúce zmeny. Rozhodnutia sa zaznamenávajú a prideľujú vlastníkom. 30-minútový časový rámec je zámerný: vynucuje priorizáciu a bráni tomu, aby governance spotrebovala čas potrebný na skutočnú prevádzku.

**Mesačné brífingy o metrikách.** Hlbšia revízia výkonnostných dát, analýza trendov a hodnotenie kalibrácie. Tu sa s dátami riešia otázky ako „Je náš prah istoty stále primeraný?“ a „Menia sa miery prebití spôsobom, ktorý naznačuje zlú kalibráciu dôvery?“ Účastníkmi sú vlastníci z prvej línie, zástupcovia rizika z druhej línie a relevantní zainteresovaní.

**Kvartálna rotácia a revízia rizikových úrovní.** Predseda rady rotuje kvartálne a kvartálna revízia prehodnocuje rizikové úrovne a oprávnenia každého AI systému: tu sa robia rozhodnutia o rozšírení alebo zúžení úrovní autonómie, hodnotia sa nové prípady použitia a samotný rámec governance sa aktualizuje podľa poučení. Kvartálny rytmus zabezpečuje, že governance sa vyvíja spolu so systémami, ktoré riadi.

## Revízia AI incidentov

Keď AI systémy produkujú nesprávne, škodlivé alebo neočakávané výstupy, odpoveď organizácie rozhoduje o tom, či sa zlyhanie stane príležitosťou na učenie alebo opakovaným vzorom. Proces revízie AI incidentov rozširuje formát post-mortemu bez hľadania vinníka (známy zo softvérového inžinierstva) o prvky špecifické pre AI.

**Zachytávajte stopy cez korelačné ID.** Každá interakcia AI by mala byť vystopovateľná cez celý svoj životný cyklus: vstup, ktorý ju spustil, uvažovanie modelu (kde je dostupné), vyprodukovaný výstup, odpoveď operátora a konečný výsledok. Korelačné ID, ktoré tieto prvky spájajú, sú dôkazným základom akejkoľvek zmysluplnej revízie, nie voliteľný doplnok.

**Revidujte do 24 – 48 hodín.** Revízie incidentov, ktoré prebehnú týždne po udalosti, trpia vyblednutými spomienkami, racionalizovanými naratívmi a strateným kontextom. Okno 24 – 48 hodín vyvažuje dôkladnosť s čerstvosťou.

**Kategorizujte koreňovú príčinu.** AI incidenty majú charakteristické kategórie koreňových príčin, ktoré sa líšia od tradičných softvérových zlyhaní:

- **Zlyhanie promptu:** Systémový prompt, konštrukcia používateľského promptu alebo few-shot príklady viedli model k nevhodnému výstupu.
- **Medzera v mantineloch:** Výstup porušil politiku alebo obmedzenie, ktoré sa malo vynucovať, ale existujúce mantinely ho nepokrývali.
- **Kvalita dát:** Znalostná báza, vyhľadané dokumenty alebo vstupné dáta obsahovali chyby, medzery alebo zastarané informácie, ktoré model verne reprodukoval.
- **Rozsah oprávnení:** AI systém urobil krok, ktorý nemal byť schopný urobiť, čo indikuje zlyhanie kontroly prístupu alebo hranice schopností.
- **Emergentné multiagentné správanie:** V systémoch s viacerými AI agentmi produkovali interakcie agentov správanie, ktoré by žiadny z nich nevyprodukoval samostatne.

Rozsah tejto výzvy je významný a rastie. AI Incident Database, ktorá sleduje verejne hlásené zlyhania AI, zaznamenala svoj 1 000. incident v marci 2025 a v polovici roka 2026 stojí nad 1 500. Ročný prílev sa zrýchľuje: Stanford AI Index napočítal 233 novo hlásených incidentov v roku 2024, skok o 56,4 % oproti roku 2023, a počet za rok 2025 znovu vzrástol o podobný podiel. Zrýchlenie nie je iba preto, že AI systémy sa zhoršujú; viac AI systémov sa nasadzuje vo viacerých kontextoch a hlásenie sa zlepšuje. Ale trend podčiarkuje potrebu systematickej revízie incidentov namiesto ad hoc reakcií.

## Regulačné rámce

### AI Act EÚ: článok 14

Akt EÚ o umelej inteligencii zakladá najkomplexnejší regulačný rámec ľudského dohľadu nad AI, aký je dnes v platnosti. Článok 14 sa špecificky venuje požiadavkám na ľudský dohľad pri vysokorizikových AI systémoch.

> **Poznámka z júla 2026 k časovej osi.** Vysokorizikové povinnosti sa mali pôvodne uplatňovať od 2. augusta 2026. Zjednodušovací balík „Digitálny omnibus“, finalizovaný v júni 2026, ich odložil: vysokorizikové systémy z prílohy III sa teraz uplatňujú od 2. decembra 2027 a vstavané systémy z prílohy I od augusta 2028. Zakázané praktiky (február 2025) a pravidlá pre AI všeobecného použitia (august 2025) už platia a podstata článku 14 je nezmenená. Potvrďte si aktuálne dátumy so svojím právnym poradcom; táto oblasť sa hýbe.

Článok 14 ods. 4 špecifikuje, že opatrenia ľudského dohľadu majú umožniť osobám vykonávajúcim dohľad:

- **(a)** Plne pochopiť schopnosti a obmedzenia AI systému a byť schopné monitorovať jeho prevádzku.
- **(b)** Byť si vedomé automatizačnej zaujatosti, najmä pri systémoch používaných na poskytovanie informácií alebo odporúčaní pre rozhodnutia fyzických osôb.
- **(c)** Správne interpretovať výstup AI systému s prihliadnutím na charakteristiky systému a dostupné interpretačné nástroje a metódy.
- **(d)** V akejkoľvek konkrétnej situácii rozhodnúť, že AI systém nepoužijú, alebo jeho výstup ignorovať, prebiť či zvrátiť.
- **(e)** Zasiahnuť do prevádzky AI systému alebo systém prerušiť tlačidlom „stop“ alebo podobným postupom.

Praktické dôsledky pre inžinierov GenAI sú priame: dashboardy, ktoré robia správanie systému pozorovateľným (a), školenie a protiopatrenia proti automatizačnej zaujatosti (b), vyjadrenie neistoty a prepojenie s dôkazmi (c), ovládacie prvky prebitia, ktoré sú funkčné a netrestané (d), a vypínače (e) nie sú iba dobré návrhové postupy; pre vysokorizikové systémy na trhoch EÚ sú to právne požiadavky. Ako sa tieto požiadavky na dohľad prekladajú do architektúry agentov na úrovni systému (stacky pozorovateľnosti, smerovanie modelov pre každú interakciu, európska rezidencia dát), mapuje naša sprievodná brožúra [Horizont agentov](/agent-horizon-sk/).

Ako však argumentovala právna vedkyňa Melanie Finková, samotný ľudský dohľad bez ochrán na úrovni systému nestačí. Požiadavka na dohľad, ktorá kladie celé bremeno na ľudských operátorov (bez toho, aby vyžadovala, aby bol systém sám navrhnutý pre bezpečné zlyhanie), vytvára regulačnú medzeru. Táto kritika posilňuje prístup obrany do hĺbky opísaný v kapitole 7: ľudský dohľad je jedna vrstva, nie celá bezpečnostná architektúra.

### Rámec riadenia rizík AI od NIST

Národný inštitút pre štandardy a technológie (NIST) publikoval Rámec riadenia rizík AI (AI RMF 1.0) ako dobrovoľné usmernenie pre riadenie rizík AI. Rámec je organizovaný okolo štyroch kľúčových funkcií:

- **GOVERN:** Ustanoviť a udržiavať politiky, procesy a štruktúry zodpovednosti pre riadenie rizík AI.
- **MAP:** Identifikovať a kategorizovať kontexty, schopnosti a potenciálne dopady AI systémov.
- **MEASURE:** Posudzovať a sledovať riziká AI kvantitatívnymi a kvalitatívnymi metódami.
- **MANAGE:** Priorizovať identifikované riziká a konať proti nim zmierňovaním, monitorovaním a komunikáciou.

NIST následne publikoval Profil generatívnej AI (NIST AI 600-1), ktorý mapuje špecifické riziká systémov generatívnej AI (vrátane halucinácií, konfabulácie, súkromia dát a environmentálneho dopadu) na štruktúru AI RMF. Pre inžinierov GenAI poskytuje AI 600-1 štruktúrovaný kontrolný zoznam rizík na posúdenie a zmiernenie, organizovaný podľa tej istej taxonómie GOVERN-MAP-MEASURE-MANAGE.

### ISO/IEC 42001:2023

ISO/IEC 42001:2023 predstavuje prvý medzinárodne certifikovateľný štandard systému riadenia špecificky pre umelú inteligenciu. Modelovaný podľa štruktúry ISO 27001 (informačná bezpečnosť) a ISO 9001 (riadenie kvality) poskytuje rámec na ustanovenie, implementáciu, udržiavanie a neustále zlepšovanie systému riadenia AI v organizácii.

Pre organizácie pôsobiace naprieč jurisdikciami poskytuje certifikácia ISO 42001 preukázateľný, auditovateľný rámec governance AI, ktorý môže súčasne uspokojiť viaceré regulačné požiadavky. Štandard nepredpisuje konkrétne technické implementácie, ale vyžaduje zdokumentované politiky, hodnotenia rizík a procesy neustáleho zlepšovania pre AI systémy.

## Model zrelosti AI od Gartnera

Model zrelosti AI od Gartnera poskytuje päťúrovňový rámec na posúdenie pripravenosti organizácie nasadzovať a udržiavať AI systémy:

| Úroveň | Názov | Charakteristiky |
|---|---|---|
| 1 | **Povedomie** | AI skúmaná v ad hoc pilotoch; žiadna formálna governance; prijímanie poháňa nadšenie jednotlivcov |
| 2 | **Aktívna** | Viacero AI projektov beží; niektoré štruktúry governance sa vynárajú; roztrieštené nástroje a postupy |
| 3 | **Prevádzková** | AI systémy v produkcii s definovaným vlastníctvom; procesy governance ustanovené; metriky sledované |
| 4 | **Systémová** | Governance AI integrovaná do podnikového riadenia rizík; medzifunkčná koordinácia; znovupoužiteľné platformy |
| 5 | **Transformačná** | AI zabudovaná v kľúčových biznisových procesoch; priebežné učiace sa slučky; governance poháňa inovácie namiesto ich obmedzovania |

Model zrelosti je prediktívny, nie iba opisný. Prieskum Gartnera z roku 2025 (432 respondentov, publikovaný v júni 2025) zistil, že iba 20 % organizácií na nízkych úrovniach zrelosti (1 – 2) udrží svoje AI projekty v prevádzke dlhšie než tri roky, oproti 45 % organizácií na vysokých úrovniach zrelosti (4 – 5). Medzera nie je primárne o kvalite technológie; je o udržateľnosti governance. Organizácie s nízkou zrelosťou spúšťajú AI projekty s nadšením, ale chýbajú im štruktúry na ich udržiavanie, monitorovanie a prispôsobovanie v čase. Výsledkom je vzor množenia pilotov nasledovaný tichým opustením.

> **Kľúčový postreh:** Model zrelosti odhaľuje vzor, ktorý by mal znepokojiť každého inžiniera GenAI: infraštruktúra governance opísaná v tejto kapitole nie je réžia, ktorá spomaľuje nasadenie, ale štrukturálny základ, ktorý rozhoduje o tom, či nasadené systémy ostanú v prevádzke dosť dlho na to, aby priniesli trvalú hodnotu. Tímy, ktoré preskočia governance, aby sa hýbali rýchlejšie, štatisticky stavajú systémy, ktoré neprežijú svoj prvý rok.

## Poučenia naprieč doménami

Výzva riadiť interakciu človeka a AI nie je jedinečná pre GenAI. Viaceré zrelé odvetvia strávili desaťročia vývojom rámcov governance pre automatizované systémy, nad ktorými musia ľudia dohliadať. Ich zbiehajúce sa zistenia sú poučné.

**Letectvo** bolo priekopníkom systematického hlásenia incidentov so systémom NASA Aviation Safety Reporting System (ASRS), ktorý poskytuje dôverné, netrestajúce hlásenie bezpečnostných obáv. Národná rada pre bezpečnosť dopravy (NTSB) vedie nezávislé vyšetrovania nehôd, ktoré prinášajú záväzné bezpečnostné odporúčania. Bezpečnostný záznam leteckého odvetvia (miery úmrtnosti v komerčnom letectve klesli za desaťročia o rády) sa nepripisuje žiadnej jednotlivej technológii, ale ekosystému governance okolo nej: povinnému hláseniu, nezávislému vyšetrovaniu, priebežnému výcviku a kultúre, kde sa spochybňovanie automatizovaných systémov očakáva, nie trestá.

**Zdravotníctvo** vyvinulo špecifické regulačné rámce pre podporu klinického rozhodovania (CDS) cez FDA. Usmernenie agentúry rozlišuje medzi CDS, ktorá fakticky nahrádza klinický úsudok (regulovaná ako zdravotnícka pomôcka), a CDS, ktorú môže klinik pred konaním nezávisle skontrolovať a vyhodnotiť (potenciálne vyňatá z regulácie pomôcok). Čiara sa nedávno posunula: revidované konečné usmernenie zo začiatku roka 2026 uvoľnilo pozíciu z roku 2022 a dovoľuje aj nástrojom s jediným odporúčaním kvalifikovať sa ako CDS mimo pomôcok, keď klinik môže nezávisle skontrolovať základ odporúčania. Jadrový princíp revíziu prežil a priamo sa mapuje na úrovne autonómie diskutované v skorších kapitolách: požiadavky governance závisia od toho, koľko skutočného ľudského zapojenia má systém navrhnuté.

**Finančné služby** poskytujú azda najpriamejšie použiteľný precedens cez MiFID II a jeho vykonávacie nariadenie RTS 6, ktoré upravuje algoritmické obchodovanie. Požiadavky zahŕňajú: kontroly pred obchodom, ktoré bránia príkazom mimo definovaných parametrov, monitorovanie všetkej algoritmickej aktivity v reálnom čase, „funkciu zabitia“ (vlastný termín nariadenia pre vypínač) schopnú okamžite zrušiť všetky nevybavené príkazy a ročné sebahodnotenie systémov algoritmického obchodovania. Tieto požiadavky vzišli priamo z incidentov ako Knight Capital a kodifikujú návrhové vzory diskutované v kapitole 7 do regulačných mandátov.

> **Kľúčový postreh:** Každá zrelá doména, ktorá integrovala automatizované rozhodovanie do vysoko rizikovej prevádzky, sa nezávisle zblížila na tých istých jadrových princípoch: povinná schopnosť ľudského dohľadu, nezávislé vyšetrovanie incidentov, systematické hlásenie, požiadavky na vypínač a štruktúry governance, ktoré sa auditujú, nie iba dokumentujú. Prevádzka GenAI z týchto princípov nie je vyňatá; je jednoducho najnovšou doménou, ktorá sa s nimi stretáva.

## Model zrelosti interakcie AI a človeka

Syntézou rámcov governance, regulačných požiadaviek a poučení naprieč doménami diskutovaných v tejto kapitole poskytuje nasledujúci model zrelosti sebahodnotiaci rámec pre governance interakcie AI a človeka:

| Úroveň | Governance | Riadenie incidentov | Regulačný postoj | Kalibrácia dôvery | Návrh pre zlyhanie |
|---|---|---|---|---|---|
| **1 &middot; Ad hoc** | Žiadne formálne vlastníctvo; AI systémy nasadzujú jednotlivé tímy | Žiadna štruktúrovaná revízia; zlyhania riešené reaktívne | Nevedomosť o platných požiadavkách | Žiadne systematické meranie | Vypínač chýba alebo je netestovaný |
| **2 &middot; Vznikajúca** | Pomenovaní vlastníci veľkých systémov; neformálna governance | Hlásenia o incidentoch sa podávajú, ale systematicky nerevidujú | Požiadavky identifikované, ale zatiaľ neriešené | Sledované základné metriky presnosti | Vypínač existuje; záložný stack čiastočný |
| **3 &middot; Definovaná** | Model troch línií implementovaný; pravidelný rytmus governance | Post-mortemy bez hľadania vinníka s kategorizáciou koreňových príčin | Plán súladu zdokumentovaný a prebieha | Sledované miery prebití a kalibrácia istoty | Ističe a plný záložný stack otestované |
| **4 &middot; Riadená** | Medzifunkčná rada pre AI; governance integrovaná s podnikovým rizikom | Príspevky do AI Incident Database; analýza trendov poháňa zlepšenia | Certifikovaná alebo nezávisle auditovaná voči platným štandardom | Behaviorálne metriky dôvery poháňajú iteráciu návrhu | Uplatnený model švajčiarskeho syra; cvičenia zlyhania podľa harmonogramu |
| **5 &middot; Optimalizujúca** | Governance poháňa inovácie; priebežné slučky zlepšovania | Prediktívna analytika incidentov; program tesných únikov v prevádzke | Aktívna účasť na tvorbe štandardov | Kalibrácia dôvery je priebežný, meraný proces | Návrh pre zlyhanie je kľúčová kompetencia, nie dodatočná myšlienka |

Organizácia nemusí dosiahnuť úroveň 5, aby nasadzovala AI systémy zodpovedne. Ale organizácia na úrovni 1, ktorá nasadzuje autonómnych AI agentov v produkcii, pracuje s dlhom governance, ktorý sa bude časom úročiť, a výskum naznačuje, že zložený úrok z dlhu governance je strmý.

## Od návrhu k trvanlivosti

Štruktúry governance opísané v tejto kapitole sú spojivovým tkanivom medzi návrhovým zámerom a prevádzkovou realitou. Bez nich sú vzory interakcie zo skorších kapitol ašpiračnou dokumentáciou. S nimi sa tie vzory stávajú živými systémami, ktoré sa prispôsobujú meniacim sa modelom, meniacim sa predpisom, meniacim sa operátorom a meniacim sa prevádzkovým kontextom. Technológia sa bude ďalej rýchlo vyvíjať. Otázka governance znie, či sa s ňou dokáže vyvíjať aj organizácia.
