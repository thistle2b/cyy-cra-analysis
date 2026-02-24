# CRA a fyzické útoky / výrobní proces – analýza pro WiFi modul

## 1. Fyzické útoky (sundání krytu, připojení na vnitřní sběrnice)

### Závěr: CRA explicitně nepožaduje odolnost vůči fyzickým útokům

CRA je primárně zaměřeno na **kybernetické hrozby** – útoky vedené po síti, přes softwarová rozhraní a digitální komunikační kanály.

### Co CRA říká k relevantním tématům

| Zdroj CRA | Text | Interpretace |
|-----------|------|-------------|
| Bod odůvodnění 9 | Produkty připojené „fyzicky prostřednictvím hardwarových rozhraní" | Funkční připojení, ne fyzické vniknutí |
| Příl. I/I, bod 9 | Minimalizace útočné plochy včetně „externích rozhraní" | Externí = síťové porty, API, ne vnitřní sběrnice za krytem |
| Příl. I/I, bod 3 | Ochrana před neoprávněným přístupem | Digitální přístup (autentizace), ne fyzické zabezpečení |
| Příl. I/I, bod 5 | Ochrana integrity programů před manipulací | Secure boot řeší – i při fyzické záměně FW |

### Mapování na WiFi modul

| Aspekt | Vyžaduje CRA? | Komentář |
|--------|:---:|---------|
| Fyzicky nerozebíratelný kryt (tamper-proof) | ❌ Ne | CRA nepožaduje |
| Tamper detection (detekce otevření krytu) | ❌ Ne | CRA nepožaduje |
| Zalití PCB epoxidem | ❌ Ne | CRA nepožaduje |
| Ochrana JTAG/SWD (zakázání debug portu) | ⚠️ Nepřímo ANO | Minimalizace útočné plochy + bezpečná konfigurace |
| Secure boot | ✅ Ano | Příl. I/I, bod 5 – ochrana integrity |
| Šifrování flash paměti | ⚠️ Doporučeno | Závisí na posouzení rizik |
| Anti-rollback | ✅ Ano | Příl. I/I, bod 5 |
| Secure element pro klíče | ⚠️ Doporučeno | Závisí na posouzení rizik |

### Proč CRA neřeší fyzické útoky

1. CRA je **kybernetický předpis** – zaměřuje se na digitální hrozby šířící se sítí
2. Fyzický přístup = **jiná kategorie rizika** – jiný threat model
3. Fyzická bezpečnost spadá pod **jiné předpisy** (LVD, IEC 62443)

---

## 2. Výrobní proces – flashování FW

### Závěr: CRA se k výrobě vyjadřuje na vysoké úrovni

Klíčová formulace se opakuje v celém nařízení – produkt je **„navržen, vyvinut a vyráběn"** tak, aby zajišťoval kybernetickou bezpečnost. Slovo **„vyráběn"** je záměrné.

### Relevantní články CRA

| Zdroj | Požadavek | Implikace pro výrobu |
|-------|-----------|---------------------|
| Čl. 13(1) | Produkt navržen, vyvinut a **vyráběn** dle přílohy I | Výrobní proces MUSÍ zajistit bezpečnost |
| Příl. I/I, bod 1 | Bez známých zneužitelných zranitelností | Nesmí se flashovat starý FW se známými CVE |
| Příl. I/I, bod 2 | Bezpečná výchozí konfigurace | Z výroby musí vyjít bezpečně nakonfigurované zařízení |
| Příl. I/I, bod 5 | Ochrana integrity programů | Bootloader = program → jeho integrita musí být chráněna |
| Čl. 13(2) | Posouzení rizik ve fázi výroby | Risk assessment MUSÍ pokrývat výrobní provisioning |
| Čl. 31 | Technická dokumentace | Musíte zdokumentovat jak zajišťujete bezpečnost ve výrobě |

### Root of Trust – provisioning ve výrobě

```
Úroveň 0 (HW):     OTP/eFuse v čipu – jednou zapsané, nelze změnit
                    └── Hash veřejného klíče výrobce
Úroveň 1 (klíč):   Veřejný klíč uložen v OTP
                    └── Nikdo ho nemůže změnit
Úroveň 2 (boot):   Secure bootloader podepsaný vaším klíčem
                    └── Ověřen proti klíči v OTP při každém startu
Úroveň 3 (app):    Aplikační FW podepsaný vaším klíčem
                    └── Ověřen bootloaderem
Úroveň 4 (OTA):    Aktualizace podepsané vaším klíčem
                    └── Ověřeny bootloaderem/aplikací

KRITICKÝ MOMENT: Zápis úrovně 0 a 1 probíhá VE VÝROBĚ
na „otevřeném" čipu. PO zápisu je řetězec důvěry uzavřen.
```

---

## 3. Kufříkový tester s jehlovým polem

### Závěr: Z pohledu CRA vynikající řešení ✅

Uzavřený kufr s jehlovým polem a tlačítkem START:
- Automatizuje celý provisioning proces
- Eliminuje lidský faktor (dělník nemůže ovlivnit co se flashuje)
- Vynucuje všechny kroky v pořadí

### Hodnocení

| Aspekt | Hodnocení |
|--------|-----------|
| Automatizace procesu | ✅ VÝBORNÉ |
| Eliminace lidského faktoru | ✅ VÝBORNÉ |
| Fyzické oddělení (uzavřený kufr) | ✅ VÝBORNÉ |
| Jednoduchá obsluha (1 tlačítko) | ✅ VÝBORNÉ |

### Doporučení k doplnění

1. **Verifikace po lock-down** – read-back ověření secure boot, JTAG lock, FW verze
2. **Logování** – sériové číslo, FW verze, hash bootloaderu, PASS/FAIL, datum/čas
3. **Ochrana FW/klíčů v testeru** – šifrované úložiště, aktualizace jen autorizovanou osobou
4. **Proces aktualizace FW v testeru** – kdo, jak, záznam o změně

---

## 4. Insider threat (sabotáž testeru, USB port)

### Závěr: CRA toto neřeší – je to interní záležitost výrobce

**CRA se vztahuje na PRODUKTY UVÁDĚNÉ NA TRH, ne na výrobní nástroje.**

| Co CRA řeší | Co CRA neřeší |
|-------------|---------------|
| ✅ Produkt (WiFi modul) vycházející z výroby | ❌ Výrobní nástroje (tester) |
| ✅ Že má aktivní secure boot | ❌ Jak vypadá tester uvnitř |
| ✅ Že má správný FW | ❌ Jaké porty má tester |
| ✅ Že je to zdokumentováno | ❌ Zabezpečení testeru proti insider threat |
| ✅ Odpovědnost výrobce za shodu | ❌ Organizace výroby |

### Scénáře mimo scope CRA

- Dělník rozšroubuje kufr a upraví SD kartu → interní bezpečnost firmy
- USB port na testeru pro tiskárnu → interní bezpečnost firmy
- Kompromitace provisioning klíčů → interní bezpečnost firmy

### ALE: Odpovědnost zůstává na výrobci

Pokud sabotáž vede k neshodnému produktu na trhu, **odpovědný je vždy výrobce** (čl. 13). CRA nezajímá PROČ produkt nesplňuje požadavky.

### Praktické doporučení (nad rámec CRA)

Pro extra jistotu stačí jedno opatření: **nezávislá verifikace hotového produktu** – jednoduchý druhý tester (read-only), který ověří secure boot, JTAG lock, FW verzi. Je nezávislý na kufru → sabotáž kufru neovlivní verifikaci.

---

## 5. Co zapsat do technické dokumentace CRA

Pro čl. 31 doporučená struktura kapitoly o výrobním procesu:

1. Popis výrobního testeru (uzavřený kufr, jehlové pole)
2. Provisioning flow (sekvenční diagram všech kroků)
3. Bezpečnostní opatření (ochrana klíčů, omezení přístupu)
4. Verifikační kroky (seznam kontrol, PASS/FAIL kritéria)
5. Logování a traceabilita (co se loguje, doba uchování min. 10 let)
6. Risk assessment výrobního procesu (rizika + opatření)