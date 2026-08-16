# Kapitola 2: Argument proti naivnej slučke

> **Poznámka z terénu od autora.** Učím inžinierstvo GenAI a je jedna veta, ktorú počujem takmer na každom firemnom workshope, zvyčajne asi po štyridsiatich minútach, keď sa dostaneme k rizikovým prípadom použitia. Niekto seniorný sa oprie a povie: „S týmto si nerobte starosti. Je to vysoké riziko, jasné, ale jednoducho tam dáme človeka do slučky.“ A miestnosť sa uvoľní. Otázka súladu je vybavená, architektonická revízia ide ďalej a nikto sa nespýta človeka, ktorý tým človekom naozaj *bude*, ako bude vyzerať jeho utorkové popoludnie. Táto kapitola existuje kvôli tej vete. Napísal som ju, aby ste nabudúce, keď ju budete počuť alebo hovoriť, presne vedeli, koľko práce sa za tými pár slovami skrýva.

„Jednoducho tam dáme človeka do slučky“ je najpohodlnejšia odpoveď v prevádzkovej AI. Znie obozretne, uspokojuje audítorov a na prvé prečítanie sa zdá byť tým, čo regulátori vyžadujú. Vo svojej naivnej podobe je to zároveň jeden z najlepšie zdokumentovaných vzorov zlyhania v celej literatúre o automatizácii. Táto kapitola predkladá ten argument s dôkazmi, kým zvyšok brožúry postaví alternatívu: slučku, ktorá je *navrhnutá*, nie iba vyhlásená.

## Čo hovoria dôkazy o kombináciách človeka a AI

Začnite najpriamejšou otázkou: keď spárujete človeka s AI systémom, prekoná kombinácia svoje časti?

V priemere nie. [Vaccaro, Almaatouq a Malone](https://www.nature.com/articles/s41562-024-02024-1) publikovali v roku 2024 v *Nature Human Behaviour* predregistrovanú metaanalýzu pokrývajúcu 106 experimentálnych štúdií a 370 veľkostí účinku. Kombinácie človeka a AI podali významne *horší* výkon než lepší z dvojice človek alebo AI samostatne. Synergia, kde tím porazí oboch svojich členov, bola výnimkou, nie pravidlom.

Detail, na ktorom pre prevádzku najviac záleží, je podmienka pochovaná v tom výsledku. Kombinácie priniesli zisky, keď človek sám prekonával AI samotnú: nadradený úsudok človeka, doplnený strojom, niečo pridal. Ale keď AI sama prekonávala človeka samotného, pridanie človeka výsledky zhoršilo. Zásahy človeka uberali hodnotu, prebíjali správne výstupy a mávali rukou nad nesprávnymi.

Teraz si všimnite, ktorý prípad je vaše nasadenie. Ak dávate AI systém do triáže tiketov, vyšetrovania výstrah alebo preverovania dokumentov práve preto, že v tej úlohe prekonáva vašich ľudí, potom je metaanalytické očakávanie pre „človeka v slučke“ ako naivný doplnok záporné. Konfigurácia, po ktorej všetci siahajú ako po bezpečnostnom opatrení, je štatisticky konfigurácia, v ktorej človek prispieva najmenej.

Nič z toho neargumentuje za odstránenie ľudí. Tá istá metaanalýza našla zisky pri úlohách tvorby obsahu a v usporiadaniach, kde deľba práce hrala na silné stránky každej strany. Argument je užší a užitočnejší: *predvolená* slučka, jeden človek schvaľujúci prúd výstupov AI, ktoré nevyprodukoval, o situáciách, ktoré nevyšetril, zlyháva, pokiaľ niečo v návrhu neurobí príspevok človeka skutočným. Kapitoly 3 až 6 sú o tom, čo to niečo je.

## Dohľad ako politické divadlo

Druhý súbor dôkazov pochádza od ľudí, ktorí študujú požiadavky na dohľad po tom, čo sa stanú politikou.

[Ben Green](https://doi.org/10.1016/j.clsr.2022.105681) preskúmal 41 politík, ktoré nariaďujú ľudský dohľad nad vládnymi algoritmami, od rozhodnutí o dávkach po policajné nástroje. Jeho záver, publikovaný v roku 2022 v *Computer Law & Security Review*, má dve časti a obe by mali byť nepríjemné pre kohokoľvek, kto píše dokument o governance AI. Po prvé, dohľad zlyháva: desaťročia výskumu ľudských faktorov (dôkazy o automatizačnej zaujatosti a sebauspokojení, ktoré táto brožúra pokrýva v kapitole 4) ukazujú, že ľudia sú systematicky nevhodní na rolu, ktorú im tieto politiky prideľujú, monitorovať väčšinou správny systém a chytať jeho zriedkavé chyby. Po druhé, a horšie, požiadavka na dohľad nasadenie *legitimizuje*. Algoritmus sa dostane do vysoko rizikového kontextu, z ktorého by inak mohol byť vylúčený, lebo „každé rozhodnutie kontroluje človek“ je v zázname. Človek sa stáva dôvodom, prečo chybný systém smie bežať.

Greenova navrhovaná alternatíva je inštitucionálna: agentúry by mali pred nasadením s dôkazmi zdôvodniť, že ich ľudský dohľad naozaj funguje, namiesto toho, aby to tvrdili. Podržte si tú myšlienku; kalibračný pracovný postup v kapitole 8 a behaviorálne metriky v kapitole 6 sú presne ten druh dôkazov, o ktoré žiada, uplatnený na podnik.

Pre to, čo sa stane s človekom vnútri nepreskúmanej slučky, existuje meno. [Madeleine Clare Elishová](https://doi.org/10.17351/ests2019.260) to nazvala **morálna deformačná zóna**: vo vysoko automatizovanom systéme sa právna a morálna zodpovednosť presúva na najbližšieho ľudského operátora, ktorý mal nad výsledkom obmedzenú skutočnú kontrolu, tak ako deformačná zóna auta pohltí náraz, aby ochránila to, čo je vnútri. Piloti lietadla riadeného takmer úplne automatizáciou, bezpečnostný vodič v autonómnom testovacom vozidle, rádiológ, ktorý „potvrdil“ čítanie modelu: keď systém zlyhá, vyšetrovanie nájde človeka, lebo človek sa dá nájsť. Dodávateľ ukáže na vyhlásenie, že výstup bol poradný. Organizácia ukáže na schvaľovací log s menom operátora.

Prečítajte si klientsku vetu znovu v tomto svetle. „Jednoducho tam dáme človeka do slučky“ často neznamená „pridáme bezpečnostný mechanizmus“. Prevádzkovo to znamená „rozhodli sme, kto ponesie vinu“. Ak človek nedokáže zmysluplne vyhodnotiť výstup AI (žiadny čas, žiadny kontext, žiadny kalibrovaný signál istoty, žiadna nacvičená zručnosť), potom slučka poskytuje divadlo zodpovednosti pre nasadenie a expozíciu voči zodpovednosti pre človeka. Nikto v architektonickej revízii to nezamýšľa. Naivná verzia to aj tak prináša.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/docket.html">The Docket</a>: sadnite si ako sudca do simulácie predsúdneho konania s podporou AI a pocíťte, ako sa deformačná zóna zatvára okolo vášho podpisu. Obe vetvy. Trvá to osem minút.
</div>

## Problém špecifický pre agentov

Všetko vyššie pochádza z klasickej literatúry o automatizácii, študovanej na pilotoch, klinikoch a operátoroch velínov. LLM agenti pridávajú zvrat, s ktorým sa klasici nemuseli vyrovnávať: slučka nie je jedno rozhodnutie, je to prúd.

Agent pracujúci na tikete, incidente alebo kódovej základni vyprodukuje za sedenie desiatky krokov, každý nominálne podliehajúci schváleniu. Ekonomika pozornosti je pri tomto tempe brutálna a rané dáta z terénu ukazujú presne ten posun, aký by ste predpovedali. [Analýza skutočného používania agentov](https://www.anthropic.com/research/measuring-agent-autonomy) od Anthropicu (február 2026, čerpajúca zo sedení Claude Code) zistila, že noví používatelia schvaľujú kroky agenta krok za krokom, ale okolo 750 sedení skúsenosti už viac než 40 percent sedení beží v režime plného automatického schvaľovania, oproti zhruba 20 percentám u nováčikov. Dohľad migruje z kontroly krokov na kontrolu plánov a u skúsených používateľov sa veľká časť z neho jednoducho vypne. Microsoft Research dospel k doplňujúcemu záveru vo svojej práci o dohľade nad agentmi z roku 2026 (názov hovorí za všetko: „Overseeing Agents Without Constant Oversight“): neustála revízia každého kroku neprežije kontakt so skutočnými záťažami a praktickou otázkou sa stáva, ako navrhnúť *prerušovaný* dohľad, ktorý stále chytí to, na čom záleží.

Schvaľovacia výzva má, inými slovami, rovnakú krivku únavy ako klinický alarm (kapitola 4 vám dá čísla). Akýkoľvek návrh dohľadu, ktorý predpokladá, že človek pozorne skontroluje štyridsiaty siedmy krok dnešného tristého sedenia agenta, predpokladá človeka, ktorý neexistuje. To nerobí dohľad nad agentmi nemožným. Robí nemožnou naivnú verziu a zvyšuje hodnotu každej techniky v tejto brožúre, ktorá sústreďuje ľudskú pozornosť tam, kde mení výsledky: schvaľovanie odstupňované podľa rizika (kapitola 3), smerovanie podľa kalibrovanej istoty (kapitoly 6 a 8) a zadržiavanie zlyhaní, ktoré vôbec nezávisí od bdelosti (kapitola 7).

## Regulačný motív, čítaný správne

Reflex za klientskou vetou je zvyčajne regulačný a v EÚ má konkrétnu adresu: článok 14 AI Actu, „Ľudský dohľad“. Oplatí sa prečítať, čo článok skutočne vyžaduje, lebo je oveľa náročnejší, než reflex naznačuje.

Článok 14 nehovorí „človek má byť v slučke“. Hovorí, že vysokorizikové AI systémy musia byť navrhnuté tak, aby fyzické osoby, ktoré nad nimi vykonávajú dohľad, *mohli*: pochopiť schopnosti a obmedzenia systému a monitorovať jeho prevádzku; byť si vedomé automatizačnej zaujatosti, presne týmito slovami; správne interpretovať výstup systému s ohľadom na dostupné interpretačné nástroje; rozhodnúť sa systém nepoužiť alebo jeho výstup ignorovať, prebiť či zvrátiť; a zasiahnuť do prevádzky systému alebo ju prerušiť tlačidlom stop či podobným postupom.

To nie je personálna požiadavka. To je *návrhová špecifikácia švu* a číta sa ako obsah tejto brožúry: transparentnosť schopností a záznamy o výkone (kapitola 6), protiopatrenia proti automatizačnej zaujatosti (kapitola 4), interpretovateľný výstup a kalibrovaná istota (kapitola 5), funkčné prebitie, ktoré sa netrestá (kapitoly 3 a 9), a skutočný mechanizmus zastavenia (kapitola 7). Nasadzujúci subjekt, ktorý najme kontrolóra a na systéme nezmení nič, článok 14 nesplnil; obsadil deformačnú zónu. Právna vedkyňa [Melanie Finková](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5147196) hovorí ostrejšiu pointu: dohľad nie je zázračný liek a brať človeka ako záchrannú sieť, ktorá ospravedlňuje slabšie záruky inde, obracia logiku článku naruby. Systém musí byť postavený tak, aby dohľad mohol fungovať; človek nerobí nebezpečný systém bezpečným tým, že sa naň pozerá.

> **Poznámka z júla 2026 k načasovaniu.** Vysokorizikové povinnosti AI Actu sa mali pôvodne uplatňovať od 2. augusta 2026. Zjednodušovací balík „Digitálny omnibus“, finalizovaný v júni 2026, ich odložil: prípady použitia z prílohy III (zoznam, ktorý zahŕňa úverové skórovanie, nábor a väčšinu prevádzkových scenárov v demách tejto brožúry) sa teraz uplatňujú od 2. decembra 2027 a vstavané systémy z prílohy I od augusta 2028. Podstata článku 14 je nezmenená. Ak vás odklad láka odložiť návrh dohľadu o rok, všimnite si, že každý režim zlyhania v tejto kapitole funguje bez ohľadu na dátumy vynucovania a dodatočné prerábanie švu je oveľa drahšie než jeho návrh. Ako vždy pri právnych otázkach: berte to so štipkou soli a potvrďte si dátumy a povinnosti so svojím právnym poradcom.

## Čo táto kapitola nehovorí

Tri nesprávne čítania stojí za to uzavrieť.

Po prvé, toto nie je argument za plnú autonómiu. Tie isté dôkazy, ktoré usvedčujú naivnú slučku, usvedčujú automatizáciu bez dohľadu ešte silnejšie; katastrofy v kapitole 7 sú väčšinou systémy, ktoré sa nedali zastaviť. Skutočná voľba je medzi vyhlásenou slučkou a navrhnutou, nie medzi opečiatkovaním a žiadnym človekom.

Po druhé, toto nie je tvrdenie, že ľudský úsudok je bezcenný. Metaanalytické straty sa sústreďujú tam, kde človek nedostane žiadny základ pre úsudok: žiadny kontext, žiadna kalibrácia, žiadny čas, holý výstup a tlačidlo schváliť. Tam, kde návrh dá človeku skutočný materiál na prácu, kombinácia vyhráva. To je vlastnosť švu, nie druhu.

Po tretie, toto nie je rada v oblasti súladu proti ľuďom v slučke. Článok 14 vyžaduje ľudský dohľad nad vysokorizikovými systémami, a mal by. Argument je, že požiadavka pomenúva inžiniersky výsledok, dohľad, ktorý *funguje*, a zvyšok tejto brožúry je to inžinierstvo.

<div class="demo-link">
<span class="demo-link-label">Vyskúšajte si sami</span>
<a href="https://demos.barcik.training/demos/operators-dilemma.html">The Operator's Dilemma</a>: päť dejstiev v úlohe človeka v slučke, od opečiatkovania pod časomierou po rozhodnutie, kedy stlačiť vypínač. Ak z tejto brožúry spustíte jednu interaktívnu vec, spustite túto.
</div>

> **Kľúčové posolstvo:** „Jednoducho tam dáme človeka do slučky“ je hypotéza a dôkazy hovoria proti jej naivnej podobe: kombinácie človeka a AI v priemere zaostávajú za lepším zo svojich členov a prehrávajú presne vtedy, keď je AI silnejším členom; mandáty dohľadu empiricky zlyhávajú a zároveň legitimizujú systémy, nad ktorými dohliadajú; človek v nenavrhnutej slučke funguje ako morálna deformačná zóna, ktorá pohlcuje vinu bez toho, aby vykonávala kontrolu; a agentné pracovné postupy pridávajú krivku únavy zo schvaľovania, ktorá revíziu každého kroku porazí do mesiacov. Článok 14 AI Actu EÚ, čítaný pozorne, už súhlasí: vyžaduje šev navrhnutý tak, aby dohľad mohol uspieť. Vyhlásiť slučku je začiatok práce, nie jej koniec.
