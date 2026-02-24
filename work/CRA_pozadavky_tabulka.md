# Kompletní tabulka požadavků CRA (EU) 2024/2847 pro WiFi modul se secure bootloaderem

## Profil zařízení

| Parametr | Hodnota |
|----------|---------|
| **Produkt** | WiFi modul se secure bootloaderem |
| **Funkce** | OTA FW upgrade ostatních MCU, předávání logů na cloud |
| **Prostředí** | Domácí elektronika (lednice) |
| **Kategorie CRA** | Příloha III, Třída I (důležitý produkt) |
| **Cloud** | Ano – řešení pro zpracování dat na dálku (bod odůvodnění 11, 12) |

---

## A. ZÁKLADNÍ POŽADAVKY NA KYBERNETICKOU BEZPEČNOST – Příloha I, Část I

| # | Požadavek | Zdroj CRA | Relevance | Implementace |
|---|-----------|-----------|-----------|--------------|
| 1 | Odpovídající úroveň kybernetické bezpečnosti na základě posouzení rizik | Příl. I/I, bod 1 | Kritická | Posouzení rizik: WiFi stack, OTA řetězec, cloud |
| 2 | Bez známých zneužitelných zranitelností | Příl. I/I, bod 1 | Kritická | Sken zranitelností před každým release |
| 3 | Bezpečná výchozí konfigurace, možnost factory reset | Příl. I/I, bod 2 | Kritická | Žádná výchozí hesla, factory reset funkce |
| 4 | Ochrana před neoprávněným přístupem | Příl. I/I, bod 3 | Kritická | Autentizace OTA, mTLS vůči cloudu, ochrana debug portů |
| 5 | Ochrana důvěrnosti dat šifrováním | Příl. I/I, bod 4 | Kritická | TLS 1.2+, šifrování credentials |
| 6 | Ochrana integrity dat, programů a konfigurace | Příl. I/I, bod 5 | Kritická | Secure boot, podpis FW, ochrana proti MITM |
| 7 | Minimalizace zpracovávaných dat | Příl. I/I, bod 6 | Střední | Logy jen nezbytné informace |
| 8 | Ochrana dostupnosti, odolnost proti DoS | Příl. I/I, bod 7 | Kritická | Odolnost Wi-Fi stacku, watchdog |
| 9 | Minimalizace negativního dopadu na jiná zařízení | Příl. I/I, bod 8 | Střední | Žádný broadcast storm, ARP flood |
| 10 | Minimalizace útočné plochy | Příl. I/I, bod 9 | Kritická | Žádné zbytečné porty, zakázaný debug v produkci |
| 11 | Omezení dopadu bezpečnostního incidentu | Příl. I/I, bod 10 | Kritická | Izolace OTA, oddělení oprávnění |
| 12 | Logování bezpečnostních událostí | Příl. I/I, bod 11 | Střední | Log přihlášení, OTA operací, anomálií |
| 13 | Řešení zranitelností přes bezpečnostní aktualizace | Příl. I/I, bod 12 | Kritická | OTA mechanismus, notifikace uživatelů |

## B. POŽADAVKY NA ŘEŠENÍ ZRANITELNOSTÍ – Příloha I, Část II

| # | Požadavek | Zdroj CRA | Relevance | Implementace |
|---|-----------|-----------|-----------|--------------|
| 14 | SBOM – identifikace a dokumentace komponent | Příl. I/II, bod 1 | Kritická | SBOM: Wi-Fi driver, RTOS, TLS, OTA, cloud SDK |
| 15 | Bezpečnostní opravy bez zbytečného prodlení | Příl. I/II, bod 2 | Kritická | Rychlý release záplat, OTA distribuce |
| 16 | Pravidelné testování bezpečnosti | Příl. I/II, bod 3 | Kritická | Pentest, fuzz testing, SAST/DAST |
| 17 | Zveřejnění informací o opravených zranitelnostech | Příl. I/II, bod 4 | Střední | Security advisory, CVE, changelog |
| 18 | Politika koordinovaného zveřejňování zranitelností | Příl. I/II, bod 5 | Kritická | Politika na webu, kontakt, doba odpovědi |
| 19 | Sdílení informací o potenciálních zranitelnostech | Příl. I/II, bod 6 | Střední | security@, security.txt |
| 20 | Bezpečná distribuce aktualizací | Příl. I/II, bod 7 | Kritická | Podepsané OTA balíčky, rollback ochrana |
| 21 | Bezplatné šíření bezpečnostních oprav | Příl. I/II, bod 8 | Kritická | Bezplatná OTA po celou dobu podpory |

## C. POVINNOSTI VÝROBCE – Články 13-16

| # | Povinnost | Zdroj | Lhůta/Detail |
|---|-----------|-------|--------------|
| 22 | Produkt navržen, vyvinut a vyráběn dle přílohy I | Čl. 13(1) | Povinné |
| 23 | Posouzení kybernetických bezpečnostních rizik | Čl. 13(2) | Povinné – celý životní cyklus |
| 24 | Náležitá péče u komponent třetích stran | Čl. 13(5) | Povinné – audit open-source |
| 25 | Nápravná opatření při zjištění zranitelnosti | Čl. 13(6) | Neprodleně |
| 26 | Postup posuzování shody | Čl. 13(7) | Modul A/B+C/H |
| 27 | Technická dokumentace | Čl. 13(8) | Povinné |
| 28 | EU prohlášení o shodě | Čl. 13(12) | Povinné |
| 29 | Označení CE | Čl. 13(13) | Povinné |
| 30 | Doba podpory min. 5 let | Čl. 13(8) | Povinné |
| 31 | Uchování dokumentace min. 10 let | Čl. 13(9) | Povinné |
| 32 | Identifikace výrobce na produktu/obalu | Čl. 13(15) | Povinné |
| 33 | Jednotné kontaktní místo pro zranitelnosti | Čl. 13(16) | Povinné |
| 34 | Hlášení aktivně zneužívané zranitelnosti – varování | Čl. 14(2)(a) | 24 hodin |
| 35 | Hlášení aktivně zneužívané zranitelnosti – oznámení | Čl. 14(2)(b) | 72 hodin |
| 36 | Hlášení aktivně zneužívané zranitelnosti – zpráva | Čl. 14(2)(c) | 14 dní po opravě |
| 37 | Hlášení závažného incidentu | Čl. 14(3) | 24h/72h/1 měsíc |
| 38 | Informování uživatelů o zranitelnosti | Čl. 14(8) | Bez zbytečného odkladu |
| 39 | Dobrovolné hlášení jakékoli zranitelnosti | Čl. 15 | Dobrovolné |
| 40 | Hlášení přes jednotnou platformu ENISA | Čl. 16 | Povinné |

## D. INFORMACE PRO UŽIVATELE – Příloha II

| # | Informace | Zdroj | Forma |
|---|-----------|-------|-------|
| 41 | Jméno/název výrobce, adresa, e-mail/URL | Příl. II, bod 1 | Produkt/dokumentace |
| 42 | Kontaktní místo pro hlášení zranitelností | Příl. II, bod 2 | Produkt/dokumentace/web |
| 43 | Identifikace produktu (typ, sériové číslo) | Příl. II, bod 3 | Produkt/dokumentace |
| 44 | Zamýšlený účel produktu | Příl. II, bod 4 | Dokumentace |
| 45 | Okolnosti vedoucí k bezpečnostním rizikům | Příl. II, bod 5 | Dokumentace |
| 46 | Odkaz na EU prohlášení o shodě | Příl. II, bod 6 | Dokumentace |
| 47 | Typ podpory a datum konce podpory | Příl. II, bod 7 | Dokumentace/obal |
| 48 | Pokyny k instalaci, provozu a údržbě | Příl. II, bod 8 | Návod |
| 49 | Pokyny k bezpečné počáteční konfiguraci | Příl. II, bod 8 | Návod |
| 50 | Popis instalace bezpečnostních aktualizací | Příl. II, bod 8 | Návod |
| 51 | SBOM – alespoň top-level závislosti | Příl. II, bod 9 | Na žádost dozoru |

## E. TECHNICKÁ DOKUMENTACE – Článek 31

| # | Obsah | Zdroj | Detail |
|---|-------|-------|--------|
| 52 | Obecný popis produktu | Čl. 31(1) | Popis modulu, funkcí, HW |
| 53 | Popis návrhu a vývoje | Čl. 31(2) | SDLC, nástroje, verzování |
| 54 | Posouzení kybernetických rizik | Čl. 31(3) | Risk assessment dokument |
| 55 | Životní cyklus, doba podpory | Čl. 31(4) | EOL plán |
| 56 | Seznam použitých norem | Čl. 31(5) | EN 18031, IEC 62443, ETSI EN 303 645 |
| 57 | Výsledky testů | Čl. 31(6) | Pentesty, fuzz testy |
| 58 | SBOM | Čl. 31(7) | Kompletní seznam SW komponent |
| 59 | EU prohlášení o shodě | Čl. 31(8) | Formální dokument |

## F. POSOUZENÍ SHODY – Článek 32

| # | Požadavek | Zdroj | Poznámka |
|---|-----------|-------|----------|
| 60 | Třída I – postup posuzování shody | Čl. 32(2) | Povinné |
| 60a | Modul A (pokud existuje harmonizovaná norma) | Čl. 32(2)(a) | Podmíněně |
| 60b | Modul B+C | Čl. 32(2)(b) | Alternativně |
| 60c | Modul H | Čl. 32(2)(c) | Alternativně |

## G. OZNAČENÍ – Článek 30

| # | Požadavek | Zdroj |
|---|-----------|-------|
| 61 | Označení CE | Čl. 30 |
| 62 | ID notifikovaného orgánu (při modulu B+C nebo H) | Čl. 30 |

## H. CLOUD BACKEND

| # | Požadavek | Zdroj |
|---|-----------|-------|
| 63 | Cloud spadá pod CRA jako řešení pro zpracování dat na dálku | Bod odůvodnění 11 |
| 64 | Šifrování komunikace modul-cloud | Příl. I/I, bod 4+5 |
| 65 | Autentizace cloud API | Příl. I/I, bod 3 |
| 66 | Bezpečnostní aktualizace cloud komponent | Příl. I/II, bod 2 |
| 67 | SBOM cloud komponent | Příl. I/II, bod 1 |
| 68 | Hlášení zranitelností cloud komponent | Čl. 14 |

## I. OTA UPDATE CHAIN

| # | Požadavek | Zdroj |
|---|-----------|-------|
| 69 | Kryptografické podpisy FW balíčků | Příl. I/I, bod 5+12 |
| 70 | Anti-rollback ochrana | Příl. I/I, bod 5 |
| 71 | Šifrovaný kanál pro distribuci | Příl. I/II, bod 7 |
| 72 | Informování uživatelů o aktualizacích | Příl. I/I, bod 12 |
| 73 | Bezplatné bezpečnostní aktualizace | Příl. I/II, bod 8 |
| 74 | Aktualizace bez zbytečného prodlení | Příl. I/II, bod 2 |

## J. SANKCE – Článek 64

| # | Typ porušení | Sankce |
|---|-------------|--------|
| 75 | Nesplnění přílohy I nebo čl. 13, 14 | Až 15 000 000 EUR / 2,5 % obratu |
| 76 | Porušení jiných povinností | Až 10 000 000 EUR / 2 % obratu |
| 77 | Nepřesné/zavádějící informace | Až 5 000 000 EUR / 1 % obratu |

## K. ČASOVÁ OSA

| # | Datum | Milník |
|---|-------|--------|
| 78 | 10.12.2024 | Vstup CRA v platnost |
| 79 | 11.9.2026 | Hlášení zranitelností (čl. 14) |
| 80 | 11.12.2027 | Plná použitelnost všech požadavků |