# Informacje ogólne

## Metryka

1) Utworzone 18 czerwca 2026, autor: Jerzy Wawro


## Projekty i dokumenty programowe

### Projekty

* Projekt konstytucji: <https://github.com/galicea/konstytucja>

* Projekt nomos: <https://github.com/galicea/nomos>

### Dokumenty programowe

* Aksjoligia dla ludzi i maszyn: https://doi.org/10.5281/zenodo.20744459

* Aksjologicznie Ugruntowana Algorytmizacja Prawa: https://doi.org/10.5281/zenodo.20701271
 

## Architektura techniczna projektu


Aby zminimalizować ryzyko i zapewnić pełną audytowalność, Twoje narzędzia zostaną podzielone na następujące środowiska:

* **GitHub (Główne repozytorium publiczne):** Zgodnie z koncepcją, GitHub jest „magazynem prawdy”. To tutaj znajduje się kod silnika rezolucji w Pythonie, definicje predykatów i raporty z testów. GitHub Actions będzie odpowiadać za CI/CD i automatyczne uruchamianie testów jednostkowych (wymagane pokrycie 100% dla reguł).


* **Forgejo (`code.galicea.org`):** Pełni rolę lustrzanej kopii zapasowej (mirror). Dokument wskazuje na konieczność „utrzymania kopii projektu, aby nie był zależny od GitHub”. Będzie to polskie, suwerenne repozytorium fundacji gwarantujące ciągłość w przypadku problemów z zewnętrznym dostawcą.


* **Taiga (`taiga.galicea.org`):** Centrum operacyjne do zwinnego zarządzania projektem (Agile/Scrum). Posłuży do zarządzania backlogiem zadań, podzielonym na cztery równoległe wątki projektowe: A (Silnik SOK), B (Formalizacja), C (Legislacja), D (Społeczność).


* **Serwer Digital Ocean (`nomos.galicea.org`):** Infrastruktura produkcyjna i testowa dla Fazy 0. Będzie hostować środowisko uruchomieniowe dla silnika w Pythonie, API (FastAPI) udostępniające wyniki wnioskowania, bazę danych (PostgreSQL) dla śladów audytowych (audit trail) oraz publiczny panel demonstracyjny (np. dla testów PoC).


## Organizacja projektu Fazy 0

W wariancie minimalnym (bootstrap/open-source-first), rdzeń operacyjny obsługuje 6–8 osób.

* **Fundacja (1 osoba):** Lider projektu odpowiada za koordynację, pilnowanie licencji open source, organizację finansowania.


* **Zespół Programistyczny (1-3 Devs, 1 DevOps):** Tworzy własny silnik rezolucji w Pythonie oraz mechanizmy CI/CD. DevOps konfiguruje Github/Forgejo i serwer Digital Ocean.


* **Zespół Prawno-Logiczny (1-2 Teoretyków, 1 Legislator):** Odpowiada za przekład przepisów na notację predykatywną oraz tworzenie projektów ustaw konstytucyjnych (od 5 miesiąca).


* **Niezależna Rada Naukowa (2-3 ekspertów):** Zewnętrzny audytor. Recenzuje kluczowe decyzje architektoniczne i aksjologiczne. Ich praca będzie wymagana przed rozpoczęciem modernizacji silnika lub wydania nowej wersji. W fazie 0 będą potrzebni dopiero na zakończenie prac.


* **Kontrybutorzy zewnętrzni:** Zgłaszają błędy na platformie i proponują usprawnienia w modelu open source.


## Plan działania i harmonogram (Kiedy i Jak?)

Faza 0 na najbliższe pół roku wygląda następująco:

**Miesiąc 1: Inicjalizacja (Setup)**

* Konfiguracja Taiga: utworzenie ról, tablic Kanban/Scrum dla wątków A, B, C, D.

* Konfiguracja GitHub i Forgejo: utworzenie repozytoriów, wpięcie otwartej licencji, dodanie instrukcji dla kontrybutorów (README, CONTRIBUTING.md).

* Przygotowanie dokumentacji opisującej cel i założenia projektu oraz jego organizację

**Miesiące 2-3: Budowa Silnika MVP (Wątek A i B)**

* *Dev:* Zbudowanie pierwszego prototypu KOS. Uruchomienie na serwerze do testowania z zapytaniami dotyczącymi projektu.

* *Prawo:* Rozpoczęcie formalizacji projektu Konstytucji na predykaty.

* *Prawo:* Przygotowanie projektów ustaw konstytucyjnych na podstawie obecnych ustaw i obecnej konstytucji. Rozpoczęcie  ich formalizacji.

* *Audyt:* Każdy wprowadzony predykat przechodzi proces `human-in-the-loop`: zatwierdzenie przez eksperta prawa, logika i inżyniera wiedzy.


**Miesiące 3-5: Proof of Concept (PoC)**

* *Dev:* Zbudowanie bazy wiedzy dla systemu aksjologicznego. Uruchomienie na serwerze do testowania.

* Zbudowanie predykatów dla łatwych, deterministycznych ustaw: waloryzacja emerytur, odsetki ustawowe, proste przepisy ordynacji podatkowej.

* Publiczna publikacja raportu PoC na GitHubie z pokazaniem logów z wnioskowania.

* Otwarty nabór do zespołu w środowiskach akademickich.


**Miesiąc 5+: Legislacja (Wątek C)**

* Rozwój silnika KOS (MVP) - testowanie i aktualizacje

* Dobre przetestowanie nowego prawa i całego systemu w warunkach zbliżonych do prawdziwych (test z użyciem person)
  
* Zgłoszenie gotowości systemu. Rozpoczęcie prac analitycznych *Rady Naukowej*. Celem jest potwierdzenie gotowości, zainicjowanie ulepszeń i poprawek.
