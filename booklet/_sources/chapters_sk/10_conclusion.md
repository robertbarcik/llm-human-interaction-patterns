# Kapitola 10: Záver

Najťažšou časťou nasadzovania AI v prevádzke je šev, nie AI.

Šev je hranica, kde sa výstup AI systému stretáva s ľudským úsudkom. Je to miesto, kde sa odporúčanie stáva rozhodnutím, kde sa návrh stáva krokom, kde sa predpoveď stáva záväzkom. Každé zlyhanie skúmané v tejto brožúre (každý prípad automatizačnej zaujatosti, každá ignorovaná výstraha, každá katastrofická strata) sa odohralo na tomto šve. A každé úspešné nasadenie, každý prípad, keď AI skutočne zosilnila ľudskú schopnosť, uspelo preto, že niekto ten šev navrhol s rozvahou.

## Tri princípy

Vzory, rámce a prípadové štúdie predstavené naprieč týmito kapitolami sa zbiehajú do troch princípov. Nie sú nové. V mnohom sú zjavné. Ale dôkazy ukazujú, že sa porušujú častejšie, než dodržiavajú.

### 1. Navrhujte šev, neodstraňujte ho

Hranica medzi človekom a AI nie je nepohodlie, ktoré treba minimalizovať, ale kritický riadiaci povrch celého systému. Každé úsilie urobiť hranicu neviditeľnou (nechať výstup AI hladko tiecť do konania bez trenia, revízie alebo ľudského úsudku) odstraňuje mechanizmus, ktorým sa chytajú chyby, rozpoznávajú hraničné prípady a systém sa prispôsobuje kontextom, pre ktoré nebol navrhnutý.

To neznamená, že každý krok AI vyžaduje ľudské schválenie. Úrovne autonómie a eskalačné rámce diskutované v skorších kapitolách poskytujú spektrum od plnej ľudskej kontroly po monitorovanú autonómiu. Ale na každej úrovni musí byť šev *navrhnutý*: človek musí vedieť, čo AI urobila, prečo to urobila a ako zasiahnuť, ak je niečo zle. Šev musí byť viditeľný, prehľadný a funkčný, nie zakrpatené zaškrtávacie políčko v pracovnom postupe, ktoré sa operátori naučia preskakovať.

### 2. Podporujte ľudské myslenie, nenahrádzajte ho

Hodnota AI v prevádzke nie je v tom, že myslí, aby človek nemusel, ale v tom, že spracúva, vyhľadáva a štruktúruje informácie, aby človek mohol myslieť *lepšie*. Na rozlíšení záleží, lebo režimom zlyhania prvého rámcovania je sebauspokojenie: človek sa odpojí, stratí situačné povedomie a stane sa neschopným chytiť chyby, ktoré AI nevyhnutne urobí. Režimom zlyhania druhého rámcovania je iba neefektivita, čo je problém zásadne inej závažnosti.

Vzory interakcie, ktoré podporujú ľudské myslenie (postupné odhaľovanie s brífingmi štruktúrovanými podľa SBAR, kategorická istota s kalibračnými dátami, prepojenie s dôkazmi podporujúce rozhodovanie založené na rozpoznaní), zdieľajú spoločnú návrhovú filozofiu. Zosilňujú ľudské rozpoznávanie vzorov, intuíciu a kontextové uvažovanie namiesto toho, aby ich obchádzali. Predkladajú informácie vo formátoch, ktoré zodpovedajú tomu, ako expertní operátori naozaj myslia, nie vo formátoch, ktoré je pre AI pohodlné produkovať.

### 3. Stavajte pre zlyhanie, nielen pre úspech

Každý AI agent v niektorom okamihu vyprodukuje nesprávne odporúčania, sfabrikuje informácie, urobí nevhodné kroky alebo sa zachová spôsobmi, ktoré jeho návrhári nepredvídali. Toto nie je dočasné obmedzenie čakajúce na ďalšie vydanie modelu, ale štrukturálna charakteristika systémov, ktoré fungujú v otvorených prostrediach skutočného sveta s neúplnými informáciami a vyvíjajúcimi sa kontextmi.

Dôsledok: návrh pre zlyhanie je súčasťou jadra systému, nie druhoradou starosťou, ktorá sa rieši, keď zvyšok funguje. Každý autonómny krok potrebuje externý vypínač, ktorý AI nedokáže obísť. Každý automatizovaný pracovný postup potrebuje otestovanú záložnú cestu, ktorú operátori precvičili. Každý AI systém potrebuje pomenovaného ľudského vlastníka, ktorý je splnomocnený a oprávnený ho vypnúť.

## Dôkazy, syntetizované

Výskum a prípadové štúdie predstavené naprieč týmito kapitolami rozprávajú konzistentný príbeh o tom, čo sa stane, keď sa tieto princípy porušia:

- **Automatizačná zaujatosť** produkuje v laboratórnych podmienkach miery chýb konania blížiace sa 100 %: operátori sa riadia preukázateľne nesprávnymi odporúčaniami AI, lebo akt spochybnenia systému vyžaduje viac kognitívneho úsilia než prijatie jeho výstupu.
- **Únava z výstrah** necháva 63 % bezpečnostných výstrah neriešených, nie preto, že by operátori boli nedbanliví, ale preto, že objem výstrah prevyšuje kapacitu ľudského spracovania a návrh rozhrania nepodporuje účinnú triáž.
- **Posun k sebauspokojeniu** môže ostať dlho neodhalený: v jednom zdokumentovanom prípade prešlo 34 hodín nesprávneho správania automatizovaného systému bez ľudského odhalenia, lebo monitorovacie rozhrania neboli navrhnuté tak, aby ukázali postupnú degradáciu.
- **45-minútová strata Knight Capital vyše 460 miliónov dolárov** nastala po tom, čo 97 automatických varovných e-mailov ostalo neprečítaných, lebo nikto nebol poverený ich sledovať, žiadny prah nespustil eskaláciu a neexistoval vypínač na zastavenie poruchového systému.
- **Systém MCAS Boeingu 737 MAX**, spoliehajúci sa na jediný snímač uhla nábehu s postupom potlačenia, ktorý nebol ani zjavný, ani primerane nacvičený, prispel k 346 úmrtiam pri dvoch haváriách.

Toto sú zlyhania návrhu švu, nie zlyhania AI technológie. V každom prípade technický systém robil to, na čo bol postavený. Zlyhanie bolo na hranici medzi systémom a ľuďmi, ktorí nad ním mali dohliadať.

## Vynárajúci sa štandard

Naprieč rámcami skúmanými v tejto brožúre sa formuje vynárajúci sa štandard návrhu interakcie AI a človeka. Šesťúrovňový rámec autonómie CSA (od plnej ľudskej kontroly cez monitorovanú autonómiu po plnú automatizáciu) s dynamickým preradením nadol podľa kontextu, istoty a dôsledkov predstavuje štrukturálny základ. Kľúčovou inováciou nie sú úrovne samotné, ale princíp *dynamického pohybu* medzi nimi: systém, ktorý funguje na úrovni autonómie 4 pri rutinných úlohách, ale automaticky sa preradí na úroveň 2, keď istota klesne alebo vzrastú stávky.

Informačná architektúra švu je rovnako kritická. Postupné odhaľovanie s brífingmi štruktúrovanými podľa SBAR zabezpečuje, že operátori dostanú správne informácie v správnom čase. Kategorická istota s kalibračnými dátami zabezpečuje, že neistota sa komunikuje v pojmoch, podľa ktorých sa dá konať. Prepojenie s dôkazmi podporuje vlastný proces uvažovania operátora namiesto vyžadovania slepej dôvery.

Architektúra zlyhania (vypínače mimo AI, ističe pri každej závislosti, záložné stacky testované podľa harmonogramu a filozofia obrany do hĺbky modelu švajčiarskeho syra) zabezpečuje, že keď k zlyhaniam dôjde, sú ohraničené, viditeľné a napraviteľné.

A architektúra governance (pomenovaní vlastníci, zodpovednosť troch línií, revízie v pravidelnom rytme, post-mortemy incidentov bez hľadania vinníka a zosúladenie s regulačnými rámcami ako AI Act EÚ a NIST AI RMF) zabezpečuje, že všetko vyššie pretrvá aj po prvotnom nasadení.

## Čo urobiť v pondelok ráno

Pre inžiniera GenAI, ktorý toto číta v nedeľu večer a rozmýšľa, kde začať, tu je päť konkrétnych krokov (kapitola 8 poskytuje šablóny a pracovné listy na ich vykonanie):

1. **Auditujte jednu existujúcu interakciu AI a človeka.** Vyberte jediný bod vo svojom súčasnom systéme, kde sa výstup AI dostane k ľudskému operátorovi. Zmapujte ho: Aké informácie operátor dostane? Čo s nimi môže urobiť? Ako by vedel, že sú nesprávne? Ako by to zastavil?

2. **Uplatnite maticu výberu vzoru.** Pre tú interakciu určte primeranú úroveň autonómie podľa závažnosti dôsledkov, vratnosti rozhodnutia, časových obmedzení a istoty AI. Je súčasná úroveň primeraná? Ak nie, čo by sa muselo zmeniť?

3. **Pridajte vypínač.** Ak váš AI systém môže robiť autonómne kroky a nemá mechanizmus na okamžité zastavenie všetkých takých krokov (taký, ktorý je mimo AI, vždy viditeľný a nevyžaduje potvrdzovací dialóg), postavte ho. Otestujte ho. Zdokumentujte ho.

4. **Merajte miery prebití.** Začnite sledovať, ako často operátori odporúčania AI prijímajú, upravujú alebo zamietajú, rozvrstvené podľa hlásenej úrovne istoty AI. Táto jediná metrika vám o kalibrácii dôvery povie viac než akýkoľvek prieskum alebo rozhovor.

5. **Naplánujte revíziu interakcie s AI.** Dajte si do kalendára opakujúce sa 30-minútové stretnutie (týždenne alebo raz za dva týždne) na revíziu výkonu AI systému, incidentov a tesných únikov. Pozvite inžinierstvo, prevádzku a aspoň jedného človeka mimo bezprostredného tímu. Držte sa formátu post-mortemu bez hľadania vinníka. Urobte to skôr, než to budete potrebovať.

Žiadny z týchto krokov nevyžaduje novú technológiu, nový rozpočet ani organizačné schválenie. Vyžadujú pozornosť, zámer a uznanie, že šev medzi AI a človekom je najdôležitejší návrhový povrch vo vašom systéme.

A ak chcete, aby váš tím *pocítil*, prečo na tom všetkom záleží, kým ho požiadate, aby to postavil, pošlite ho do [Laboratória človeka v slučke](https://demos.barcik.training/): sedem krátkych simulácií (sprievodná sada tejto brožúry), ktoré ľuďom dovolia zažiť automatizačnú zaujatosť, únavu z výstrah, ukotvenie a morálnu deformačnú zónu na vlastnej koži, od úverovej priehradky banky cez nočnú zmenu na nemocničnom oddelení po sudcovský rozvrh. Dvadsať minút v Laboratóriu obráti viac skeptikov než akákoľvek prezentácia.

## Na záver

Organizácie, ktoré to zvládnu správne, nebudú tie s najsofistikovanejšou AI. Budú to tie s najpremyslenejšie navrhnutými švami.

Modely sa budú ďalej zlepšovať. Kontextové okná porastú. Schopnosti uvažovania sa prehĺbia. Náklady klesnú. Ale základná výzva (zabezpečiť, aby pravdepodobnostný systém a ľudský operátor účinne spolupracovali v neistote, pod časovým tlakom a s dôsledkami v skutočnom svete) ostane. Je to návrhový problém, problém governance a nakoniec ľudský problém. Vzory v tejto brožúre sú východiskový bod, nie cieľ. Cieľom je prevádzka, kde AI robí ľudských expertov schopnejšími, informovanejšími a účinnejšími, bez toho, aby ich kedy urobila menej bdelými.
