# CRA compliance – analýza reálných nákladů a ongoing zátěže pro malé firmy

> **Kontext:** Tento dokument vznikl na základě diskuse o praktických dopadech CRA (EU) 2024/2847
> na malé firmy (startupy, mikropodniky) vyrábějící IoT produkty s WiFi modulem.
> Dokument zachycuje poznatky, korekce chyb a otevřené otázky.
>
> **Datum:** 2026-02-24

---

## 1. Dva zásadně odlišné náklady CRA

Většina diskusí o CRA mluví jen o prvním. Ale ten druhý je ten skutečný problém.

### Náklad 1: „Dostat se do shody" (jednorázový)

- Risk assessment
- Technická dokumentace
- Security by design úpravy
- Penetrační testy
- SBOM
- Posouzení shody
- EU prohlášení o shodě

**Odhad:** 3 měsíce práce konzultanta/vývojáře na první projekt. Dá se naplánovat, dá se odhadnout.

### Náklad 2: „Udržet shodu" (kontinuální, neohraničený)

- Monitoring CVE pro každou komponentu v SBOM
- Reakce na zranitelnosti v RTOS, Wi-Fi stacku, TLS knihovně, cloud SDK
- Vývoj záplat
- Testování záplat (regresní testy!)
- Distribuce záplat (OTA)
- Hlášení ENISA do 24h varování + 72h oznámení
- Aktualizace dokumentace
- Pravidelné bezpečnostní testování
- A to pro KAŽDÝ projekt, KAŽDÝ produkt na trhu

**Odhad:** NELZE odhadnout. Závisí na frekvenci a závažnosti CVE v komponentách.

---

## 2. Problém kumulace projektů

Typický scénář pro malou firmu (konzultant + zákazníci-startupy):

```
Rok 0:  Projekt A – dodáno, CRA compliant
Rok 1:  Projekt B – ve vývoji
Rok 2:  Projekt B – dodáno, Projekt C – ve vývoji
Rok 3:  Projekt C – dodáno, Projekt D – ve vývoji
Rok 4:  Projekt D – dodáno

V roce 4 musíte SOUČASNĚ udržovat CRA compliance pro:
- Projekt A (3 roky na trhu, zbývají 2 roky podpory)
- Projekt B (2 roky na trhu, zbývají 3 roky podpory)
- Projekt C (1 rok na trhu, zbývají 4 roky podpory)
- Projekt D (čerstvě dodaný, zbývá 5 let podpory)

Každý projekt má potenciálně:
- Jiný RTOS (nebo jinou verzi)
- Jiný Wi-Fi stack
- Jiné MCU s jinou HAL
- Jiný cloud SDK
- Jinou TLS knihovnu (nebo jinou verzi)
```

---

## 3. Nepředvídatelnost upgrade stacku

Když přijde CVE v komponentě, možné scénáře:

| Scénář | Náročnost | Časový odhad |
|--------|-----------|-------------|
| **A: Minor patch** (3.4.1 → 3.4.2) – API se nemění, drop-in replacement | Nízká | Hodiny až dny |
| **B: Major update** (3.4 → 4.0) – API breaking changes, přepis integrace, nové regresní testy | Vysoká | Týdny až měsíce |
| **C: Vendor ukončil podporu** – patch neexistuje pro vaši verzi, migrace nebo vlastní patch | Velmi vysoká | Měsíce |
| **D: Vendor zkrachoval / projekt opuštěn** – patch nikdy nebude, alternativa nebo fork | Kritická | Měsíce, potenciálně redesign |

**Nelze předem vědět, která varianta to bude. CRA říká „bez zbytečného prodlení" (příl. I/II, bod 2).**

---

## 4. Strategie pro snížení ongoing nákladů

| Strategie | Efekt | Trade-off |
|-----------|-------|-----------|
| Minimalizace počtu komponent v SBOM | Méně závislostí = méně CVE | Architektonické rozhodnutí na začátku |
| Stejný stack napříč projekty | 1 patch = oprava pro všechny projekty | Omezuje flexibilitu |
| Vendor s LTS podporou | Dostupnost patchů pro starší verze | Může omezit výběr čipu/platformy |
| Abstrakční vrstva nad vendor kódem | Usnadní výměnu komponenty | Více práce na začátku |
| CI/CD + automatické CVE skenování | Rychlejší detekce a reakce | Počáteční investice do infrastruktury |
| Smluvní ošetření s odběratelem | Jasné rozdělení kdo platí ongoing support | Vyjednávání |

---

## 5. Sankce – korekce interpretace

### CHYBNÁ interpretace (opraveno)

Dříve: „Pro firmu s obratem 3M CZK je max. pokuta 3 000 EUR (2,5 % obratu)."

### SPRÁVNÁ interpretace dle čl. 64(2)

> „...až do výše 15 000 000 EUR, nebo dopustí-li se porušení podnik, až do výše 2,5 % jeho celkového ročního obratu celosvětově za předchozí finanční rok **podle toho, která hodnota je VYŠŠÍ**."

Klíčové slovo: **VYŠŠÍ** (ne nižší).

Pro firmu s obratem 120 000 EUR:
- 2,5 % obratu = 3 000 EUR
- Fixní strop = 15 000 000 EUR
- **Vyšší = 15 000 000 EUR** → toto je maximální pokuta

| Obrat firmy | Max. pokuta | Poměr k obratu |
|-------------|-------------|----------------|
| 120 000 EUR (3M CZK) | 15 000 000 EUR | 12 500 % |
| 1 000 000 EUR | 15 000 000 EUR | 1 500 % |
| 10 000 000 EUR | 15 000 000 EUR | 150 % |
| 600 000 000 EUR | 15 000 000 EUR | 2,5 % |
| 1 000 000 000 EUR | 25 000 000 EUR | 2,5 % |

**Poznámka:** Maximum není automatická sazba. Ale samotná existence tohoto stropu představuje pro mikropodniky teoreticky likvidační riziko.

---

## 6. CRA jako bariéra vstupu – riziko konkurenčního boje

### Reálný scénář pro startupy

Startup vstupuje na trh zavedeného výrobce (Bosch, Whirlpool...).

Zavedený výrobce:
- Má regulatory tým
- CRA compliance = položka v rozpočtu
- Může podat podnět dozoru nad trhem na konkurenta
- „Ten startup nemá řádnou technickou dokumentaci" → legální, legitimní, účinné

Toto se **DĚJE** v jiných regulovaných odvětvích (medtech, automotive, chemie) **rutinně**.

Podání podnětu dozoru nad trhem na konkurenta je legální a běžné. Dozor MUSÍ reagovat na podnět.

---

## 7. Timing – proč nelze čekat na harmonizované normy

```
Vývojový projekt:        ~18 měsíců
CRA prvotní compliance:  ~3 měsíce práce (v rámci projektu)
Harmonizované normy:     publikace 2026-2027 (přesné datum neznámé)
Plná účinnost CRA:       11.12.2027

PROBLÉM:
- Nikdo nechce zastavit 18měsíční projekt na konci,
  protože zjistí, že nesplňuje CRA
- CRA požadavky musí být jasné NA ZAČÁTKU projektu
- Ale harmonizované normy ještě neexistují
- → Musíte pracovat s textem nařízení a nejlepším odhadem
- → Riziko, že normy přinesou překvapení
```

---

## 8. Co říct zákazníkům (startupům)

### Upřímná verze

> „CRA compliance pro IoT produkt bude stát řádově miliony korun rozložené do 5+ let.
> Přesný odhad dnes nikdo nemá – harmonizované normy neexistují, enforcement praxe neexistuje.
>
> Toto MUSÍTE započítat do:
> - Ceny produktu
> - Business plánu
> - Fundraisingu
>
> CRA NENÍ důvod nepodnikat. CRA JE důvod:
> - Započítat regulatory náklady do business plánu od začátku
> - Navrhovat produkt CRA-compliant od začátku
> - Nezačínat s technickým dluhem v bezpečnosti
> - Vědět, že 5 let povinné podpory = 5 let nákladů
>
> Nevím kolik to přesně bude stát. Nikdo to dnes neví.
> A kdo tvrdí, že to ví, lže."

---

## 9. Otevřené otázky (k únoru 2026)

| Otázka | Stav | Dopad |
|--------|------|-------|
| Jak budou vypadat harmonizované normy? | Neznámé – publikace 2026-2027 | Zásadní – určí konkrétní požadavky |
| Jak přísně bude dozor interpretovat požadavky? | Neznámé – žádná praxe | Zásadní |
| Bude CRA zneužíváno v konkurenčním boji? | Pravděpodobné (analogie s jinými regulacemi) | Vysoký pro startupy |
| Co znamená „bez zbytečného prodlení"? | Nevyloženo | Zásadní pro ongoing náklady |
| Jak budou dozorové orgány přistupovat k mikropodnikům? | Neznámé | Zásadní |
| Kolik CVE ročně přijde pro typický embedded stack? | Závisí na stacku, nelze predikovat | Určuje ongoing náklady |
| Bude Modul A (self-assessment) dostupný pro Třídu I? | Podmíněno existencí harmonizované normy | Zásadní pro náklady |

---

## 10. Závěr

CRA je regulace navržená primárně s ohledem na velké výrobce, která dopadá neproporcionálně na malé firmy a startupy. To neznamená, že je špatná – bezpečnost IoT produktů je legitimní cíl. Ale je třeba být realistický o nákladech a rizicích.

**Pro konzultanta:** Vaše hodnota je v tom, že rozumíte technické stránce CRA a umíte implementovat compliance efektivně. Ale musíte být upřímný k zákazníkům o tom, co je čeká – včetně nejistot.

**Pro startupy:** CRA je reálný náklad. Neignorujte ho. Nezlevňujte ho. Započítejte ho do business plánu. A hlavně – navrhujte produkt CRA-compliant od prvního dne, ne na konci projektu.