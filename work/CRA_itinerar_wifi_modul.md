# CRA Itinerář pro WiFi modul se secure bootloaderem

> **Kontext:** Praktický itinerář pro dosažení CRA (EU) 2024/2847 compliance
> pro WiFi modul se secure bootloaderem v domácí elektronice (lednice).
> Každá fáze obsahuje tři sekce: co implementovat/review, jaké testy provést, co zapsat do dokumentace.
>
> **Datum:** 2026-02-24

---

## Předpoklady

- **Produkt:** WiFi modul se secure bootloaderem
- **Funkce:** OTA FW upgrade ostatních MCU, předávání logů na cloud
- **Kategorie:** Příloha III, Třída I (důležitý produkt)
- **Itinerář předpokládá:** FW již existuje nebo je ve vývoji → jde o review + doplnění, ne vývoj od nuly

---

## FÁZE 1: Secure Boot & Root of Trust
**⏱ Odhad: 3–5 týdnů** (pokud základ existuje, jinak 6–10 týdnů)

### 🔧 Co implementovat / review

| # | Úkol | Pokud existuje → review | Pokud chybí → implementovat | CRA ref |
|---|------|------------------------|----------------------------|---------|
| 1.1 | Secure boot chain – bootloader ověřuje podpis aplikačního FW | Ověřit algoritmus (min. ECDSA P-256 nebo Ed25519), ověřit že nelze obejít | Implementovat od HW root of trust | Příl. I/I, bod 5 |
| 1.2 | OTP/eFuse provisioning – hash veřejného klíče v HW | Ověřit zda je OTP zapsáno a zamčeno, read-back verifikace | Navrhnout provisioning flow, implementovat v testeru | Příl. I/I, bod 5 |
| 1.3 | Anti-rollback ochrana – monotónní čítač nebo verze v OTP | Ověřit mechanismus, ověřit že nelze downgrade | Implementovat version counter v OTP/NVS | Příl. I/I, bod 5 |
| 1.4 | JTAG/SWD lock v produkci | Ověřit že debug porty jsou zakázané v produkčním buildu | Implementovat JTAG disable v provisioning flow | Příl. I/I, bod 9 |
| 1.5 | Flash encryption (dle risk assessment) | Ověřit algoritmus a key management | Implementovat pokud risk assessment vyžaduje | Příl. I/I, bod 4 |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| Secure boot bypass | Flashnout nepodepsaný FW, ověřit odmítnutí | Modul NESMÍ spustit nepodepsaný kód |
| Anti-rollback | Flashnout starší podepsaný FW | Modul NESMÍ akceptovat starší verzi |
| JTAG lock | Pokus o připojení debuggerem na produkční kus | Debugger NESMÍ navázat spojení |
| Key integrity | Read-back OTP, porovnat s expected hash | Hash MUSÍ odpovídat |
| Boot failure recovery | Korumpovat app FW, ověřit chování | Bootloader MUSÍ zůstat funkční (recovery/brick, ne spuštění koruptu) |

### 📝 Dokumentace (body do CRA tech. dok.)

- Popis Root of Trust architektury (úrovně 0–4)
- Provisioning flow diagram (co se děje ve výrobě krok po kroku)
- Algoritmy a délky klíčů pro podpis FW
- Anti-rollback mechanismus (jak funguje čítač)
- JTAG/SWD lock mechanismus
- Výsledky testů secure boot bypass, anti-rollback, JTAG lock

---

## FÁZE 2: OTA Update Chain
**⏱ Odhad: 3–5 týdnů**

### 🔧 Co implementovat / review

| # | Úkol | Review | Implementace | CRA ref |
|---|------|--------|-------------|---------|
| 2.1 | Kryptografický podpis OTA balíčků | Ověřit formát, algoritmus, key management | Build pipeline pro podepisování FW | Příl. I/I, bod 5+12 |
| 2.2 | Šifrovaný kanál pro distribuci (TLS) | Ověřit TLS verzi, cipher suites, cert pinning | Implementovat TLS 1.2+ s vhodným cipher suite | Příl. I/II, bod 7 |
| 2.3 | Rollback ochrana v OTA procesu | Ověřit že OTA nepřijme starší verzi | Svázat s anti-rollback z fáze 1 | Příl. I/I, bod 5 |
| 2.4 | OTA failure recovery | Ověřit chování při přerušení update (výpadek napájení) | A/B partitioning nebo safe rollback | Příl. I/I, bod 7 |
| 2.5 | Notifikace uživatele o dostupné aktualizaci | Ověřit mechanismus (push/pull, cloud notifikace) | Implementovat mechanismus informování | Příl. I/I, bod 12 |
| 2.6 | Autentizace OTA serveru | Ověřit cert validation, pinning | Implementovat server auth | Příl. I/I, bod 3 |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| OTA podpis – valid | Odeslat správně podepsaný FW | Modul akceptuje a nainstaluje |
| OTA podpis – invalid | Odeslat FW s poškozeným podpisem | Modul ODMÍTNE |
| OTA rollback | Odeslat starší podepsaný FW přes OTA | Modul ODMÍTNE |
| OTA power failure | Přerušit update odpojením napájení v průběhu | Modul se MUSÍ zotavit (předchozí FW nebo recovery) |
| OTA MITM | Proxy s vlastním certifikátem | Modul ODMÍTNE spojení / FW |
| OTA channel encryption | Wireshark capture OTA komunikace | Veškerý provoz MUSÍ být šifrovaný |

### 📝 Dokumentace

- Popis OTA architektury (diagram toku aktualizace)
- Formát OTA balíčku (header, podpis, payload)
- Key management pro FW signing (kdo má privátní klíč, kde je uložen, rotace)
- Recovery strategie při selhání update
- Proces vydání bezpečnostní záplaty (od CVE detekce po OTA deploy)
- Mechanismus notifikace uživatelů

---

## FÁZE 3: Komunikace modul ↔ cloud
**⏱ Odhad: 2–4 týdny**

### 🔧 Co implementovat / review

| # | Úkol | Review | Implementace | CRA ref |
|---|------|--------|-------------|---------|
| 3.1 | TLS 1.2+ pro veškerou komunikaci s cloudem | Ověřit verzi, cipher suites, cert validation | Nakonfigurovat TLS stack | Příl. I/I, bod 4+5 |
| 3.2 | mTLS nebo device auth vůči cloud API | Ověřit jak se modul autentizuje | Implementovat klientský certifikát nebo token | Příl. I/I, bod 3 |
| 3.3 | Credential storage na modulu | Ověřit kde jsou uloženy klíče/certifikáty | Secure storage (encrypted NVS, secure element) | Příl. I/I, bod 4 |
| 3.4 | Minimalizace dat v lozích | Ověřit co se loguje a posílá na cloud | Odstranit zbytečné PII/debug data | Příl. I/I, bod 6 |
| 3.5 | Cloud API autorizace (RBAC, scope) | Ověřit že modul nemá víc oprávnění než potřebuje | Least privilege | Příl. I/I, bod 9 |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| TLS version | Wireshark/sslscan na cloud endpoint | Min. TLS 1.2, žádný TLS 1.0/1.1 |
| Cert validation | Podvrhnout self-signed cert | Modul ODMÍTNE spojení |
| Credential extraction | Dump flash, hledat klíče v plaintextu | Klíče NESMÍ být v plaintextu (nebo musí být v secure element) |
| Data minimization | Zachytit a analyzovat obsah logů | Žádné PII, žádné debug data, jen nezbytné informace |
| Auth failure | Odeslat request s neplatným tokenem/cert | Cloud ODMÍTNE |

### 📝 Dokumentace

- Komunikační architektura (diagram modul ↔ cloud)
- TLS konfigurace (verze, cipher suites, cert chain)
- Autentizační mechanismus (mTLS / token / popis)
- Přehled dat odesílaných na cloud (tabulka: typ, účel, minimalizace)
- Credential management (provisioning, rotace, revokace)

---

## FÁZE 4: Bezpečná konfigurace & hardening
**⏱ Odhad: 1–2 týdny**

### 🔧 Co implementovat / review

| # | Úkol | CRA ref |
|---|------|---------|
| 4.1 | Žádná výchozí hesla / shared secrets v FW | Příl. I/I, bod 2 |
| 4.2 | Factory reset funkce – návrat do bezpečného stavu | Příl. I/I, bod 2 |
| 4.3 | Žádné zbytečné otevřené porty / služby | Příl. I/I, bod 9 |
| 4.4 | Debug výpisy zakázané v produkčním buildu | Příl. I/I, bod 9 |
| 4.5 | Watchdog pro obnovu po pádech / zacyklení | Příl. I/I, bod 7 |
| 4.6 | Rate limiting / ochrana proti Wi-Fi DoS | Příl. I/I, bod 7 |
| 4.7 | Izolace OTA procesu od běžného provozu (privilege separation) | Příl. I/I, bod 10 |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| Default credentials | Sken FW binary na hardcoded hesla/klíče | Žádné nalezené |
| Factory reset | Provést reset, ověřit stav | Návrat do bezpečné výchozí konfigurace |
| Port scan | nmap scan modulu | Pouze nezbytné porty otevřené |
| Debug output | Monitor UART/log v produkčním buildu | Žádné debug výpisy |
| Watchdog | Vyvolat hang (infinite loop inject) | Modul se MUSÍ restartovat |
| Wi-Fi DoS | Deauth flood, beacon flood | Modul se MUSÍ zotavit |

### 📝 Dokumentace

- Výchozí konfigurace modulu (tabulka parametrů)
- Popis factory reset funkce a chování
- Seznam otevřených portů / služeb s odůvodněním
- Watchdog konfigurace
- Privilege separation model

---

## FÁZE 5: Logování bezpečnostních událostí
**⏱ Odhad: 1–2 týdny**

### 🔧 Co implementovat / review

| # | Úkol | CRA ref |
|---|------|---------|
| 5.1 | Logování OTA událostí (start, úspěch, selhání, odmítnutý podpis) | Příl. I/I, bod 11 |
| 5.2 | Logování autentizačních událostí (cloud connect, cert errors) | Příl. I/I, bod 11 |
| 5.3 | Logování anomálií (watchdog reset, unexpected reboot, flash errors) | Příl. I/I, bod 11 |
| 5.4 | Ochrana integrity logů (nelze smazat/modifikovat) | Příl. I/I, bod 5 |
| 5.5 | Mechanismus předávání logů na cloud (pokud je to součástí produktu) | — |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| OTA event log | Provést úspěšný a neúspěšný OTA | Oba události zaznamenány |
| Auth failure log | Simulovat cert error | Událost zaznamenána |
| Log integrity | Pokus o modifikaci logu z aplikační vrstvy | Log NESMÍ být modifikovatelný aplikací |
| Log overflow | Zaplnit log storage | Definované chování (circular buffer / upload) |

### 📝 Dokumentace

- Seznam logovaných bezpečnostních událostí (tabulka: událost, severity, formát)
- Mechanismus ukládání a ochrany logů
- Retenční politika (jak dlouho, kde)

---

## FÁZE 6: SBOM & CVE skenování
**⏱ Odhad: 1–2 týdny**

### 🔧 Co udělat

| # | Úkol | CRA ref |
|---|------|---------|
| 6.1 | Vytvořit SBOM – všechny SW komponenty s verzemi | Příl. I/II, bod 1; Čl. 31(7) |
| 6.2 | Skenovat SBOM proti NVD/CVE databázím | Příl. I/I, bod 1 |
| 6.3 | Vyřešit nalezené CVE (patch/mitigate/accept+document) | Příl. I/I, bod 1 |
| 6.4 | Nastavit ongoing CVE monitoring (automatizace) | Příl. I/II, bod 2 |
| 6.5 | Audit open-source licencí a due diligence | Čl. 13(5) |

### Typické komponenty v SBOM pro WiFi modul

| Komponenta | Příklad | Typický zdroj CVE |
|------------|---------|-------------------|
| RTOS | FreeRTOS, Zephyr, ThreadX | Nízký–střední |
| Wi-Fi driver/stack | Vendor SDK (ESP-IDF, CYW, …) | Střední–vysoký |
| TLS knihovna | mbedTLS, wolfSSL | Střední |
| OTA klient | Vlastní / vendor SDK | Závisí |
| Cloud SDK | AWS IoT SDK, Azure SDK | Střední |
| Kryptografická knihovna | mbedCrypto, tinycrypt | Střední |
| Bootloader | MCUboot, vendor | Nízký |
| HAL / CMSIS | Vendor | Nízký |

### 📝 Dokumentace

- SBOM v strojově čitelném formátu (CycloneDX nebo SPDX)
- Výsledky CVE skenu s rozhodnutím (patch / mitigate / accept)
- Proces ongoing CVE monitoringu (kdo, jak často, jaký tooling)
- Due diligence záznam pro open-source komponenty

---

## FÁZE 7: Výrobní proces & provisioning
**⏱ Odhad: 2–3 týdny**

### 🔧 Co implementovat / review

| # | Úkol | CRA ref |
|---|------|---------|
| 7.1 | Provisioning flow v testeru (OTP zápis → bootloader → app → lock) | Čl. 13(1) |
| 7.2 | Verifikace po lock-down (read-back secure boot, JTAG, FW verze) | Příl. I/I, bod 5 |
| 7.3 | Logování výrobního procesu (S/N, FW verze, hash, PASS/FAIL, datum) | Čl. 13(9) |
| 7.4 | Ochrana FW/klíčů v testeru (šifrované úložiště) | Čl. 13(1) |
| 7.5 | Proces aktualizace FW v testeru (kdo, jak, záznam) | Čl. 31 |
| 7.6 | Bezpečná výchozí konfigurace z výroby | Příl. I/I, bod 2 |

### 🧪 Testy

| Test | Metoda | PASS kritérium |
|------|--------|---------------|
| Provisioning kompletní flow | Provést na prázdném čipu | Všechny kroky PASS, log kompletní |
| Verifikace po provisioning | Read-back všechny security fuses | Odpovídá expected hodnotám |
| FW verze z výroby | Ověřit že se flashuje aktuální release | Žádné staré FW se známými CVE |
| Tester FW update | Aktualizovat FW v testeru, provést provisioning | Nový FW korektně flashován |

### 📝 Dokumentace

- Provisioning flow diagram (sekvenční diagram)
- Popis výrobního testeru (HW, SW, bezpečnostní opatření)
- Seznam verifikačních kroků s PASS/FAIL kritérii
- Logování a traceabilita (co se loguje, doba uchování min. 10 let)
- Risk assessment výrobního procesu

---

## FÁZE 8: Penetrační test & bezpečnostní testování
**⏱ Odhad: 2–4 týdny** (závisí na rozsahu, interní vs. externí pentest)

### 🧪 Testy

| Oblast | Testy | Metoda |
|--------|-------|--------|
| Wi-Fi stack | Deauth attacks, rogue AP, evil twin, KRACK | Aircrack-ng, hostapd, custom scripts |
| OTA chain | MITM, replay, downgrade, corrupted package | mitmproxy, custom fuzzer |
| Cloud komunikace | Cert spoofing, token theft, API abuse | Burp Suite, custom scripts |
| FW binary | Reverse engineering, hardcoded secrets | Ghidra/IDA, binwalk, strings |
| Fuzz testing | Malformed packets na všechna rozhraní | AFL, libFuzzer, custom harness |
| SAST | Statická analýza zdrojového kódu | Coverity, SonarQube, cppcheck |

### 📝 Dokumentace

- Pentest report s nalezenými zranitelnostmi, severity, doporučení
- Fuzz testing report (coverage, nalezené crashes)
- SAST report (nalezená issues, řešení)
- Záznam o nápravných opatřeních pro nalezené problémy

---

## FÁZE 9: Formální dokumentace & compliance
**⏱ Odhad: 3–5 týdnů**

### 📝 Dokumenty k vytvoření

| # | Dokument | CRA ref | Obsah |
|---|----------|---------|-------|
| 9.1 | **Risk Assessment** | Čl. 13(2); Čl. 31(3) | Hrozby, zranitelnosti, dopady, opatření – pro WiFi stack, OTA, cloud, výrobu |
| 9.2 | **Technická dokumentace** | Čl. 31 | Obecný popis, návrh/vývoj, SDLC, rizika, normy, testy, SBOM |
| 9.3 | **SBOM** | Čl. 31(7); Příl. II, bod 9 | CycloneDX/SPDX formát + human-readable verze |
| 9.4 | **EU prohlášení o shodě** | Čl. 13(12); Čl. 31(8) | Formální dokument dle šablony |
| 9.5 | **Uživatelská dokumentace** | Příloha II | Bezpečná konfigurace, instalace, OTA pokyny, výrobce kontakt |
| 9.6 | **Vulnerability disclosure policy** | Příl. I/II, bod 5 | Politika na webu, security@, security.txt, SLA odpovědi |
| 9.7 | **EOL / support plan** | Čl. 31(4); Příl. II, bod 7 | Datum konce podpory (min. 5 let), typ podpory |
| 9.8 | **Incident response plán** | Čl. 14 | Postup při zranitelnosti: 24h varování → 72h oznámení → 14d zpráva |

---

## FÁZE 10: Posouzení shody
**⏱ Odhad: 2–8 týdnů** (závisí na zvoleném modulu)

| Modul | Podmínka | Náročnost | Odhad |
|-------|----------|-----------|-------|
| **Modul A** (self-assessment) | Existuje harmonizovaná norma a výrobce ji pokryl | Nízká | 2 týdny |
| **Modul B+C** (EU-type examination + conformity to type) | Notifikovaný orgán posuzuje typ | Střední–vysoká | 4–8 týdnů + čekání na NB |
| **Modul H** (full quality assurance) | Kompletní QMS, audit NB | Vysoká | 6–8 týdnů + čekání na NB |

> **Poznámka:** K únoru 2026 harmonizované normy pro CRA ještě neexistují → Modul A pravděpodobně zatím není dostupný pro Třídu I. Nutno sledovat publikaci norem.

---

## Celkový časový odhad

| Fáze | Rozsah | Odhad (pokud základ existuje) | Odhad (od nuly) |
|------|--------|-------------------------------|-----------------|
| 1. Secure Boot & Root of Trust | HW/FW | 3–5 týdnů | 6–10 týdnů |
| 2. OTA Update Chain | FW | 3–5 týdnů | 5–8 týdnů |
| 3. Komunikace modul ↔ cloud | FW + cloud | 2–4 týdny | 4–6 týdnů |
| 4. Bezpečná konfigurace & hardening | FW review | 1–2 týdny | 2–4 týdny |
| 5. Logování | FW | 1–2 týdny | 2–3 týdny |
| 6. SBOM & CVE | Tooling + analýza | 1–2 týdny | 1–2 týdny |
| 7. Výrobní proces | HW tester + flow | 2–3 týdny | 4–6 týdnů |
| 8. Penetrační test | Security testing | 2–4 týdny | 2–4 týdny |
| 9. Formální dokumentace | Dokumenty | 3–5 týdnů | 4–6 týdnů |
| 10. Posouzení shody | Compliance | 2–8 týdnů | 2–8 týdnů |
| **CELKEM** | | **20–40 týdnů** | **32–57 týdnů** |

### Důležité poznámky k odhadům

1. **Fáze se překrývají** – reálně běží paralelně (dokumentace průběžně, SBOM od začátku). Realistický elapsed time je cca **60–70 % součtu**.
2. **Odhad „pokud základ existuje"** = FW má secure boot, TLS, OTA, ale nebylo to dělané s ohledem na CRA → review + doplnění + dokumentace.
3. **Odhad „od nuly"** = čistý čip bez jakékoliv security implementace.
4. **Fáze 8 (pentest)** lze paralelizovat s dokumentací.
5. **Fáze 10 (posouzení shody)** závisí na dostupnosti notifikovaných orgánů a harmonizovaných norem.
6. **Ongoing náklady po dokončení** – viz `CRA_analyza_naklady_ongoing.md` – toto je jen prvotní compliance, ne celkový lifetime cost.