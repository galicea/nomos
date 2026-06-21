# Dokumentacja Systemu Semantycznego (LT) - Spreading Activation i Integracja z LLM

## 1. Wstęp i Podstawy Teoretyczne

### Kognitywne Wyszukiwanie Semantyczne: Spreading Activation
System LT opiera się na **algorytmie rozchodzenia się pobudzenia (Spreading Activation)**. Służy on do modelowania pamięci semantycznej jako grafu pojęć i wyszukiwania kontekstu powiązanego z pytaniem użytkownika.

**Główne pojęcia:**
*   **Węzeł (Node):** Reprezentuje element wiedzy semantycznej. Może to być pojedyncze słowo (`NODE_WORD`), archetyp pytania/frazy (`NODE_PHRASE_ARCHETYPE`), archetyp semantyczny (`NODE_SEMANTIC_ARCHETYPE`) lub predykat (`NODE_PREDICATE_ARCHETYPE`).
*   **Krawędź (Edge):** Reprezentuje relację skojarzeniową między węzłami z przypisaną wagą ($w$).
*   **Aktywacja (Activation):** Poziom pobudzenia węzła ($\mu_i$). Początkowo pobudzane są słowa występujące w zapytaniu użytkownika (bottom-up), a następnie pobudzenie propaguje się wzdłuż krawędzi do sąsiadujących węzłów.
*   **Globalny Kontekst i Zanikanie (Decay):** Mechanizm pamięci krótkotrwałej. Aktywacje węzłów stopniowo wygasają z czasem, co pozwala na modelowanie historii i kontekstu konwersacji bez przeciążenia pamięci.

---

## 2. Implementacja w Pythonie (`backend0`)

Sercem systemu jest klasa `CognitiveProcessor` oraz `SemanticMemory` zlokalizowane w `sok/services/lt_engine.py`.

### Pamięć Semantyczna (`SemanticMemory`)
Zarządza ładowaniem grafu z trwałej bazy danych do pamięci RAM oraz synchronizacją zmian (zapis cache z RAM do DB za pomocą `flush_to_db`).

```python
class SemanticMemory:
    def _load_cache(self):
        # Ładowanie węzłów i krawędzi z bazy SQLite/Postgres do pamięci RAM
        for node in self.session.scalars(select(SemanticNode)):
            ...
```

### Silnik Wnioskowania Semantycznego (`CognitiveProcessor`)
Implementuje matematyczny model rozchodzenia się pobudzenia w krokach czasowych ($t$):
$$\mu_i(t+1) = \mu_i(t) \cdot \delta + \sum_{j \in N_{in}(i)} w_{ji} \cdot \mu_j(t) + \text{boost}_i(t)$$
gdzie:
*   $\delta$ (`DECAY_COEFFICIENT` = 0.8) to współczynnik zanikania,
*   $w_{ji}$ to waga krawędzi z węzła $j$ do $i$,
*   $\text{boost}_i(t)$ to zewnętrzne pobudzenie (np. słowa wpisane przez użytkownika).

```python
class CognitiveProcessor_new:
    def process(self, text: str, boost: Optional[Dict[int, float]] = None, propagation_steps: int = 2) -> Dict:
        # 1. Pobudzenie bezpośrednie słów kluczowych
        # 2. Iteracyjna propagacja pobudzenia
        # 3. Wybór najbardziej aktywnych archetypów i predykatów
        # 4. Aktualizacja globalnego kontekstu (merge_activations)
```

### Integracja z LLM (`PromptBuilder`)
Odpowiada za zrzut aktywnych predykatów z bazy do szablonu promptu dla modelu językowego (LLM). Wzbogaca prompt o logikę i odpowiedzi pomocnicze przypisane do zidentyfikowanych predykatów biznesowych.

---

## 3. Przewodnik Dewelopera

### Struktura Projektu
*   `sok/`: Główny katalog aplikacji.
    *   `services/lt_engine.py`: Silnik semantyczny, pamięć RAM/DB i orkiestrator.
    *   `api/lt.py`: Endpointy dla zapytań semantycznych i ofert (`/query`, `/offer/{slug}`).
    *   `api/gemini.py`: Moduł integracji z Gemini API (używający `requests`).
    *   `models/lt.py`: Trwałe tabele bazodanowe dla grafu semantycznego, pytań i predykatów.
    *   `schemas/lt_schemas.py`: Schematy Pydantic (`QuestionPost`).

### Instalacja i Uruchomienie
1. Zainstaluj wymagane zależności z `requirements.txt`.
2. Uruchom serwer FastAPI za pomocą: `PYTHONPATH=. python3 main.py`.
3. Port domyślny: `8000`.

### Rozwijanie Aplikacji

#### Dodawanie nowych relacji semantycznych
Możesz dodać nowe powiązania bezpośrednio w bazie danych w tabelach `semantic_node` i `semantic_edge` lub poprzez procedurę zasilania pytań (`QuestionSeeder`), która automatycznie tokenizuje pytania i mapuje je na predykaty.

#### Uruchomienie Zasilania (Seeding)
Możesz zasilić bazę z pytań testowych uruchamiając skrypt bezpośrednio:
```bash
PYTHONPATH=. python3 services/lt_engine.py
```
To zmapuje rekordy z tabeli `Question` i `QuestionPredicateMapping` na graf w pamięci semantycznej.

---

### Notatki Programisty - Pułapki

1.  **Stan Globalnego Kontekstu:** Pamięć podręczna w tle (`GlobalContext`) jest wątkowo bezpieczna dzięki blokadzie `threading.Lock`. Jednak przy braku aktywności należy cyklicznie wywoływać metodę `decay()`, aby zapobiec utrzymywaniu starych tematów w pamięci konwersacji.
2.  **API Key dla Gemini:** Upewnij się, że zmienna środowiskowa `GEMINI_API_KEY` jest ustawiona w systemie. W przeciwnym wypadku silnik zaloguje ostrzeżenie i zwróci odpowiedź symulowaną (mock) z pełnym podglądem wygenerowanego promptu.
3.  **Tymczasowe ID:** Węzły dodawane do `SemanticMemory` w trakcie sesji otrzymują ujemne, tymczasowe identyfikatory (np. -1, -2). Dopiero wywołanie `flush_to_db()` zapisuje je i mapuje na prawdziwe auto-inkrementowane ID z SQLite/Postgres.
