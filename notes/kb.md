# Dokumentacja Systemu Bazy Wiedzy (KB) - Algorytm Rezolucji

## 1. Wstęp i Podstawy Teoretyczne

### Wnioskowanie Algorytmiczne: Reguła Rezolucji
Aplikacja opiera się na **regule rezolucji**, która jest fundamentem programowania logicznego (np. język Prolog). W klasycznym ujęciu, rezolucja służy do dowodzenia twierdzeń poprzez zaprzeczenie (szukanie sprzeczności). W naszej implementacji stosujemy wariant **rezolucji SLD** (Selective Linear Definite clause resolution).

**Główne pojęcia:**
*   **Klauzula (Clause):** Jednostka wiedzy. Może to być fakt (zapisany w bazie danych) lub reguła (definicja).
*   **Unifikacja:** Proces dopasowywania dwóch termów (np. parametrów zapytania do parametrów reguły) tak, aby stały się identyczne poprzez podstawienie wartości pod zmienne.
*   **Nawracanie (Backtracking):** Przeszukiwanie przestrzeni rozwiązań "w głąb". Jeśli jedna ścieżka dowodzenia zawiedzie, algorytm wraca do ostatniego punktu wyboru i próbuje innej alternatywy.

## 2. Implementacja w Pythonie (`backend0`)

Sercem systemu jest `KnowledgeEngine` znajdujący się w `sok/resolution/clause_engine.py`.

### Unifikacja i Zmienne (`UnifyingVariable`)
W przeciwieństwie do prostych zmiennych, `UnifyingVariable` posiada stan (`value`). Podczas unifikacji, jeśli zmienna jest pusta, przyjmuje wartość stałej. Jeśli obie strony mają wartości, są one porównywane.
```python
class UnifyingVariable:
    def unify(self, arg):
        if self.value is not None and self.value != arg:
            return False
        self.value = arg
        return True
```

### Silnik Wnioskowania (`KnowledgeEngine`)
Silnik wykorzystuje **generatory Pythona (`yield`)** do realizacji backtrackingu. Dzięki temu pamięć nie jest obciążona wszystkimi wynikami naraz, a proces "cofania się" w drzewie dowodzenia jest naturalnie obsługiwany przez stos wywołań generatora.

*   **`_execute_base`**: Odpowiada za pobieranie faktów z "bazy" (widoków SQL). Mapuje kolumny widoku na zmienne unifikacyjne.
*   **`_execute_rule`**: Obsługuje rekurencyjne wywoływanie reguł. Tworzy kontekst zmiennych lokalnych dla każdej pod-klauzuli.

### Warstwa Danych (`dbviews.py`)
Silnik nie operuje bezpośrednio na tabelach, lecz na **widokach SQL** zaczynających się od prefiksu `q__`. Pozwala to na pełną separację logiki wnioskowania od fizycznej struktury bazy danych.

## 3. Przewodnik Dewelopera

### Struktura Projektu
*   `backend0/`: Serwer FastAPI + SQLAlchemy.
    *   `resolution/`: Silnik rezolucji.
    *   `models/kb.py`: Definicje struktur klauzul (drzewo wywołań).
*   `frontend0/`: Interfejs Next.js + MUI.
    *   `components/kb/`: Specjalistyczne edytory parametrów i pod-klauzul.

### Instalacja i Uruchomienie

**Backend:**
1. Zainstaluj zależności: `pip install -r requirements.txt`.
2. Uruchom serwer: `python main.py` (domyślnie port 8000).
3. Baza SQLite (`kb.db`) zostanie utworzona automatycznie.

**Frontend:**
1. Zainstaluj paczki: `npm install`.
2. Uruchom dewelopersko: `npm run dev`.

### Rozwijanie Aplikacji

#### Dodawanie nowych typów faktów
Aby dodać nowe źródło faktów, stwórz widok w bazie danych (np. `CREATE VIEW q__pracownicy AS ...`). Następnie w aplikacji zdefiniuj klauzulę o kategorii `baza` i `cl_view_name = 'q__pracownicy'`.

#### Modyfikacja algorytmu rezolucji
Jeśli chcesz dodać operatory logiczne (np. NOT, OR), musisz zmodyfikować funkcję `_execute_rule` w `clause_engine.py`. Obecnie silnik wspiera niejawną koniunkcję (AND) pomiędzy kolejnymi pod-klauzulami.

#### Edycja Frontendu
Główna logika edytora znajduje się w `frontend0/src/pages/kb/editor/[id].tsx`. Wykorzystuje on zagnieżdżone komponenty do obsługi relacji jeden-do-wielu (klauzula -> parametry, klauzula -> pod-klauzule).

### Notatki Programisty - Pułapki
1.  **Backtracking i Stan:** Pamiętaj, że po `yield True` w generatorze należy przywrócić stan zmiennych (`var.set(old_value)`), aby kolejne gałęzie przeszukiwania nie korzystały z "brudnych" danych.
2.  **Unifikacja Kołowa:** Obecna wersja nie sprawdza cykli (occurs check). Unikaj definiowania reguł typu `A :- B. B :- A.`, co doprowadzi do `RecursionError`.
3.  **Wydajność:** Każda klauzula typu `baza` to zapytanie SQL. Silnik stara się optymalizować zapytania poprzez QBE (Query By Example) - parametry z przypisaną wartością są przekazywane do klauzuli `WHERE`.

