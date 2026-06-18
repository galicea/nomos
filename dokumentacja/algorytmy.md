# Algorytmy

## 1. Ochrona przed halucynacjami - deterministyczna sztuczna inteligencja

SOK będzie wykorzystywał sztuczną inteligencję, w tym duże modele językowe (LLM). Największym wyzwaniem z tym związanym jest zjawisko generowania fałszywych informacji (halucynacji) oraz problem semantyki referencyjnej (ugruntowania symboli, *Symbol Grounding Problem*). Poleganie wyłącznie na sieciach neuronowych czy standardowych systemach RAG  *Retrieval-Augmented Generation*) tworzy ryzykowną „czarną
skrzynkę\".

Aby zapewnić pewność i odtwarzalność wyników (audytowalność), SOK opiera się na **Deterministycznym Algorytmie Sztucznej Inteligencji** - hybrydowej architekturze neuro-symbolicznej opisanej w artykule „*Deterministic Artificial Intelligence Algorithm: a hybrid neuro-symbolic architecture based on semantic fields, fuzzy logic, and predicative notation*\"[^1]. Algorytm ten został wdrożony w praktyce i potwierdził swoją skuteczność.

Architektura przyjęta w algorytmie zmienia rolę LLM w czterech
warstwach:
-   **Notacja predykatywna:** prawo zapisywane jest w postaci predykatów określających podmiot, obiekty i atrybuty (np. PRED(A1, A2, ATTR)). Predykaty te stanowią nienaruszalne „kotwice faktograficzne\" (*factual anchors*).

-   **Analiza semantyczna:** na podstawie opisu sprawy następuje wybór predykatów przy użyciu pola semantycznego opisywanego w logice rozmytej (*fuzzy logic*). Pole semantyczne zmienia się w trakcie dialogu - dlatego ten etap nie jest w pełni deterministyczny. Odpowiada to realnym sytuacjom negocjowania znaczenia między stronami postępowania.

-   **Fundament logiczny:** wnioskowanie w oparciu o uzyskany zbiór predykatów i struktury przepisów prawa jest mechanizmem **w pełni deterministycznym**. Realizowane jest przez własny silnik rezolucji napisany w Pythonie (szczegóły w sekcji 5.3.1).

-   **Rola LLM:** rola modelu językowego zostaje zredukowana wyłącznie do warstwy generatywnej i interpretacyjnej - model działa jako zaawansowany translator z języka predykatów na naturalny i **nie ma prawa modyfikacji logiki**.

Dzięki temu system eliminuje zarówno swobodne halucynacje generatywne, jak i błędy semantyczne na etapie mapowania tekstu na logikę.

## 2. Silnik rezolucji w Pythonie

Silnik wnioskowania SOK jest zaimplementowany jako **własna biblioteka Pythona**, realizująca reguły rezolucji bezpośrednio w kodzie. Decyzja o rezygnacji z zewnętrznych środowisk logiki (takich jak SWI-Prolog czy miniKanren) jest podyktowana czterema argumentami:

1.  **Dostępność kompetencji.** Python jest językiem powszechnie znanym przez polskich programistów, matematyków i informatyków. Obniża to próg wejścia dla wolontariuszy i kontrybutorów open source, co ma krytyczne znaczenie w fazie 0.

2.  **Integralność ekosystemu.** Cały stos technologiczny (pola semantyczne, interfejs API, testy, CI/CD, panel audytowy) może być utrzymywany w jednym języku i jednym repozytorium.

3.  **Pełna audytowalność.** Reguły rezolucji zapisane explicite w Pythonie są czytelne dla każdego programisty bez znajomości składni Prologa. Każdy krok wnioskowania może być zalogowany i odtworzony.

4.  **Kontrola nad defeasible reasoning.** Własna implementacja pozwala precyzyjnie sterować obsługą wyjątków, hierarchią norm i kolizjami reguł - bez zależności od semantyki zewnętrznego interpretera.

Każde wywołanie resolve() zwraca zarówno wynik (predykat konkluzji lub kategorię „wymaga sędziego\"), jak i pełny ślad kroków wnioskowania w formacie JSON - niemodyfikowalny, sygnowany przez silnik. Testy jednostkowe pokrywają każdą regułę osobno; testy integracyjne symulują pełne przypadki z polskiego prawa.

## 3. Rola człowieka w translacji przepisów (human-in-the-loop)

Sztuczna inteligencja pełni w SOK rolę wspomagającą. Proces weryfikacji i translacji języka naturalnego na predykaty odbywa się z obowiązkowym udziałem człowieka. Rozróżniamy trzy sytuacje użycia algorytmu:

1.  **Testowanie nowych zapisów prawa:** osoba testująca otrzymuje parafrazę testowanych tez wygenerowaną na podstawie ustalonych predykatów. Po zatwierdzeniu parafrazy pojawia się wynik wnioskowania.

2.  **Akceptacja nowych przepisów:** poza akceptacją parafrazy przez ekspertów wymagane są testy oparte o opis różnych przypadków. Wyniki testów podlegają weryfikacji przez zespół ekspertów. Badane są nie tylko wyniki, ale też sposób ich uzyskania - w tym użycie właściwych predykatów i reguł rezolucji.

3.  **Automatyzacja wyroku:** parafraza pierwotnych zapisów jest akceptowana przez strony postępowania, co oznacza zgodę na sformułowanie wyroku przez automat. W sprawach trudnych parafraza opisu może zależeć od parametrów ustawianych przez sędziego.

Każdy predykat wchodzący do bazy SOK wymaga zatwierdzenia. Szczególowe zasady - do ustalenia (np. wymaganie **trzech niezależnych recenzji**: eksperta prawa, logika i programisty-inżyniera wiedzy). Historia zatwierdzeń jest rejestrowana w repozytorium - wraz z uzasadnieniami.
