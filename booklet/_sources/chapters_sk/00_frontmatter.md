# Vzory interakcie LLM a človeka pre prevádzku

## Návrh švu medzi AI agentmi a ľudskými operátormi

---

**Apríl 2026 · revidované júl 2026 · slovenské vydanie august 2026**

*Robert Barcik*

*LearningDoe s.r.o.*

*Kontakt: [robert@barcik.training](mailto:robert@barcik.training)*

---

### O tejto príručke

„Nebojte sa, jednoducho tam dáme človeka do slučky.“ Ak pracujete kdekoľvek v blízkosti prevádzkovej AI, túto vetu ste počuli, pravdepodobne tento mesiac. Ponúka sa ako odpoveď na každý rizikový prípad použitia: klasifikáciu podľa AI Actu, bezpečnostnú revíziu, nepokoj predstavenstva. Táto príručka vychádza z nepríjemného, dobre zdokumentovaného faktu: vo svojej naivnej podobe táto veta opisuje jeden z najlepšie preskúmaných vzorov zlyhania v histórii automatizácie. Ľudia pod tlakom len opečiatkujú automatizované odporúčania, prestanú vnímať záplavy výstrah, ukotvia sa na prvom čísle, ktoré vidia, a zoberú na seba vinu, keď systém, ktorý sotva ovládali, zlyhá.

Otázka, na ktorú táto príručka odpovedá, teda nie je, či kombinovať AI agentov a ľudských operátorov; táto kombinácia už beží vo vašich frontoch tiketov, bezpečnostnej triáži a revíziách kódu. Otázka je, ako navrhnúť odovzdanie, ten *šev*, aby tím človeka a AI skutočne prekonal ktorúkoľvek zložku samostatne, namiesto toho, aby iba vyzeral pod dohľadom.

Materiál čerpá z desaťročí dôkazov z letectva, zdravotníctva, kybernetickej bezpečnosti a priemyselného riadenia: taxonómia automatizácie Sheridana a Verplanka, rámec situačného povedomia Endsleyovej, Kleinov model rozhodovania založený na rozpoznaní, výskum kalibrácie dôvery a moderná literatúra o tímovej spolupráci človeka a AI, plus zdokumentované produkčné nasadenia v GitHube, PagerDuty, Splunku, Dynatrace a ServiceNow. Poznámka k tým nasadeniam: prípadové štúdie dodávateľov sa v celom texte berú ako smerový dôkaz o prijatí, nie ako overené dáta o výkone, a každé výskumné tvrdenie v tejto revízii bolo skontrolované voči primárnemu zdroju.

Táto príručka má praktického spoločníka: **[Laboratórium človeka v slučke](https://demos.barcik.training/)** na demos.barcik.training, sedem krátkych simulácií v prehliadači, ktoré vám dovolia zažiť každý režim zlyhania na vlastnej koži, od úverovej priehradky banky cez policajný zoznam sledovaných osôb po sudcovský rozvrh. Kapitoly pri čítaní odkazujú na príslušnú simuláciu; nič sa neinštaluje, nič sa nekonfiguruje. (Simulácie sú v angličtine.)

*Slovenské vydanie preložil Claude (Fable 5), ktorý sa podieľal aj na júlovej revízii originálu, 16. augusta 2026; prekladané významovo, nie slovo za slovom. Ustálené pojmy z literatúry ostávajú tam, kde je to zvykom, v angličtine s glosou. Pri pochybnostiach platí [anglický originál](/llm-human-interaction-patterns/).*

### Pre koho je táto príručka

- **Inžinieri GenAI**, ktorí stavajú prevádzkové AI systémy so schopnosťou používať nástroje (MCP, agentné frameworky, volanie funkcií) a potrebujú navrhnúť interakčnú vrstvu medzi svojimi agentmi a ľudskými operátormi
- **Manažéri IT prevádzky**, ktorí zavádzajú AI agentov do reakcie na incidenty, monitorovania alebo pracovných postupov service desku a hľadajú usmernenie k úrovniam autonómie založené na dôkazoch
- **Produktoví manažéri**, ktorí navrhujú pracovné postupy s podporou AI a musia vyvážiť efektivitu automatizácie s ľudským dohľadom a zodpovednosťou
- **Profesionáli v bezpečnostnej prevádzke**, ktorí nasadzujú nástroje AI na triáž a vyšetrovanie v prostrediach SOC, kde únava z výstrah a zmeškané detekcie majú skutočné dôsledky
- **Ktokoľvek, kto povedal, alebo komu povedali, „jednoducho tam dáme človeka do slučky“** a chce vedieť, čo naozaj treba na to, aby to bola pravda

### Ako čítať túto príručku

Kapitola 1 definuje návrhový šev a prečo rozhoduje o výsledkoch. Kapitola 2 predkladá argument proti naivnej slučke: dôkazy, že ľudský dohľad, tak ako sa zvyčajne prilepí, zlyháva, a čo namiesto toho regulátori skutočne vyžadujú. Kapitola 3 vám dá päť štrukturálnych vzorov interakcie a taxonómie za nimi a uzatvára sa tým, kam odbor smeruje (tímová spolupráca, nie úrovne). Kapitoly 4 až 6 pokrývajú ľudskú stranu: kognitívne skreslenia, ktoré podkopávajú odovzdania, prezentačné formáty, ktoré im čelia, a to, ako sa dôvera formuje, láme a kalibruje. Kapitola 7 navrhuje pre zlyhanie (zmierňovanie halucinácií, vypínače, ističe); kapitola 8 mení všetko na implementovateľné výstupy (šablóny promptov, rozhodovacie pracovné listy, kalibračné pracovné postupy); kapitola 9 pokrýva organizačnú governance, ktorá udržiava dobrý návrh pri živote. Kapitola 10 uzatvára tromi princípmi a pondelkovým ranným kontrolným zoznamom.

Môžete čítať postupne alebo skočiť na svoju aktuálnu návrhovú výzvu. Každá kapitola je samostatná, s krížovými odkazmi tam, kde pojmy stavajú na skoršom materiáli.

---

### Obsah

1. Návrhový šev
2. Argument proti naivnej slučke
3. Päť štrukturálnych vzorov
4. Psychológia odovzdania
5. Prezentácia kontextu
6. Kalibrácia dôvery
7. Návrh pre zlyhanie
8. Implementácia vzorov
9. Organizačná governance
10. Záver
