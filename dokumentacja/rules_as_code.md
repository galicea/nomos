# Architektura silnika formalnej weryfikacji prawa (Rules as Code)
### Opis proponowanego rozwiązania, uzasadnienie wyboru i przegląd alternatyw

## 1. Kontekst problemu

Celem projektu jest formalizacja prawa polskiego  jako bazy predykatów logicznych, zgodnie z podejściem **Rules as Code** (RaC) — prawo powstaje równolegle w języku naturalnym i w języku logiki formalnej, a cykl tłumaczenia tekst → predykaty → tekst pozwala wykrywać niejednoznaczności już na etapie legislacji, a nie podczas sporu sądowego. System ma operować na własnym, pisanym w Pythonie silniku rezolucji działającym bezpośrednio na klauzulach logicznych, wspomaganym mechanizmem obliczeniowym do obsługi wyrażeń matematycznych (kwoty, terminy, progi podatkowe) wbudowanych w treść przepisów.

Najważniejsze pytanie: czy do tego zadania należy sięgnąć po istniejące, „ciężkie" systemy dowodzenia matematycznego — Mizar, Coq, Lean 4, Isabelle/HOL — czy też lepiej zbudować rozwiązanie lżejsze, dopasowane do specyfiki rezolucji na klauzulach prawnych.

## 2. Proponowane rozwiązanie

Finalna architektura, do której doprowadziła analiza, **nie korzysta z żadnego z dużych asystentów dowodów** (Mizar, Coq, Lean 4, Isabelle/HOL) jako centralnego komponentu. Składa się z czterech warstw.

**Warstwa języka.** Istniejący parser tekstowy izoluje strukturę logiczną klauzuli oraz — jako odrębne fragmenty — wyrażenia matematyczne (np. `D > 5000 + 200 * W`), które dla silnika rezolucji są jedynie nieprzezroczystymi literałami teorii (*theory literals*).

**Warstwa semantyki.** Przed trafieniem do bazy klauzul każda zmienna przechodzi przez słownik pojęć (ontologię), który ujednolica synonimy (np. „zarobek", „pensja") do jednego, systemowego identyfikatora. Wdrożenie dopuszcza dwie ścieżki wprowadzania przepisów: ścieżkę A — dedykowany frontend/edytor z podpowiadaniem nazw wymuszający poprawne identyfikatory już w trakcie pisania, oraz ścieżkę B — import wolnego tekstu (Word/Markdown), w którym moduł sugestii semantycznych (prosty algorytm tekstowy lub lokalny model językowy) prosi legislatora o przypisanie nieznanego pojęcia do istniejącego wpisu w słowniku lub o zgłoszenie nowego. Obie ścieżki zasilają ten sam parser, więc do silnika rezolucji trafiają już tylko ujednolicone klauzule.

**Warstwa weryfikacji logicznej.** Klasyczna rezolucja działa na klauzulach tekstowych — bez tłumaczenia ich na obiekty innego paradygmatu (typy w Lean/Coq czy meta-logikę Isabelle). To ona odpowiada za wykrywanie sprzeczności między przepisami (wyprowadzenie klauzuli pustej), wykrywanie przepisów redundantnych (sprawdzenie, czy stare prawo już implikuje nowy przepis) oraz odrzucanie zapisów, których parser nie potrafi przełożyć na klauzule.

**Warstwa obliczeniowa (Theory Resolution).** Wyrażenia matematyczne nie są dowodzone rezolucją czysto logiczną (co prowadziłoby do eksplozji kombinatorycznej przy próbie wyprowadzenia aksjomatów arytmetyki), lecz przekazywane jako gotowe stringi do zewnętrznego solvera SMT (Z3) traktowanego jak czarna skrzynka. Zalecana strategia wywołania to wariant hybrydowy: funkcja pomocnicza (`KALKULATOR()`) milczy (zwraca `True`) tak długo, jak na danej ścieżce przeszukiwania występuje tylko jedno ograniczenie matematyczne dla danej zmiennej, i odpytuje Z3 tylko wtedy, gdy rezolucja nałoży na tę samą zmienną drugie, potencjalnie sprzeczne ograniczenie (np. próg podatkowy z dwóch różnych artykułów). To podejście „leniwe z bramkowaniem przy unifikacji" minimalizuje liczbę kosztownych wywołań solvera, jednocześnie odcinając ślepe gałęzie drzewa rezolucji tam, gdzie to się opłaca.

## 3. Uzasadnienie: dlaczego takie rozwiązanie, a nie inne

Decyzja o pozostaniu przy własnym silniku rezolucji, z Z3 jako jedynym zewnętrznym komponentem, wynika z trzech powodów:

**Brak wspólnego paradygmatu.** Lean 4, Coq i Isabelle/HOL nie przyjmują na wejściu „surowej" logiki pierwszego rzędu — wymagają własnej składni opartej na teorii typów (Lean/Coq) lub na meta-logice HOL (Isabelle). Podłączenie ich do systemu, który już teraz jest samodzielnym silnikiem rezolucyjnym operującym na czystych klauzulach FOL, oznaczałoby budowę kosztownego kompilatora tłumaczącego klauzule na termy i typy, a następnie parsowanie wyniku z powrotem — czyli dokładnie tę warstwę translacyjną, którą architektura miała unikać.

**Niedopasowanie fundamentu logicznego Mizara.** Mizar był rozważany jako kandydat szczególnie obiecujący, bo opiera się na klasycznej teorii mnogości i logice pierwszego rzędu — czyli, przynajmniej na pierwszy rzut oka, na tym samym języku co silnik rezolucyjny. W praktyce okazuje się to złudne z trzech powodów: (1) niemal każdy obiekt w Mizarze jest definiowany jako zbiór w teorii Tarskiego–Grothendiecka, więc wprowadzenie tych aksjomatów do silnika rezolucyjnego wywołuje eksplozję kombinatoryczną nieistotnych tautologii o należeniu do zbiorów; (2) „miękkie typowanie" Mizara oraz powszechne w MML schematy (np. schemat indukcji) są de facto logiką drugiego rzędu, więc wymagają głębokiej, nietrywialnej transformacji do czystego FOL; (3) Mizar nie ma wbudowanego silnika obliczeniowego — każdy krok arytmetyczny musi być wyprowadzony jawnie, co dla problemów liczbowych (typowych w prawie podatkowym) jest wyjątkowo nieefektywne. Projekt **MPTP** (Mizar Problems for Theorem Proving), który tłumaczy MML do formatu TPTP używanego przez solwery rezolucyjne takie jak Vampire czy E, faktycznie pokazał, że automatyczne dowodzenie bez podpowiedzi premis radzi sobie z mniej więcej 40% średnio zaawansowanych twierdzeń z biblioteki — liczba w dialogu podana poprawnie i zgodna z opublikowanymi wynikami (zob. sekcja weryfikacji poniżej).

**Konflikt ról, nie przewaga funkcjonalna.** Argument, że Lean 4 czy Coq „mają przewagę" nad Mizarem dzięki teorii typów, izomorfizmowi Curry’ego–Howarda i wbudowanym mechanizmom obliczeniowym, jest słuszny — ale dotyczy scenariusza, w którym system *od podstaw* budowany jest jako asystent dowodów, a nie scenariusza, w którym własny silnik rezolucyjny już istnieje i ma działać na klauzulach tekstowych. W tym drugim przypadku dołożenie drugiego weryfikatora opartego na zupełnie innym paradygmacie nie zwiększa mocy systemu, a tylko dodaje warstwę tłumaczenia i potencjalnych błędów (tzw. *semantic gap*). Innymi słowy: to nie jest pytanie „który system dowodzenia jest lepszy", lecz „czy w ogóle potrzebny jest drugi system dowodzenia" — a odpowiedź, przy istniejącej architekturze, jest negatywna.

Mechanizm, który faktycznie był potrzebny — obsługa arytmetyki w klauzulach logicznych bez ich pełnej formalizacji — ma własną, dobrze ugruntowaną nazwę w literaturze: **Theory Resolution**, wprowadzoną przez Marka Stickela w 1985 roku, będącą jednym z konceptualnych poprzedników dzisiejszych solwerów SMT (Satisfiability Modulo Theories). To rozwiązanie węższe i lżejsze niż jakikolwiek asystent dowodów, a jednocześnie precyzyjnie adresujące rzeczywisty problem: literały matematyczne traktowane jako czarna skrzynka, odpytywana tylko wtedy, gdy rezolucja nagromadzi na tej samej zmiennej więcej niż jedno ograniczenie.

## 4. Przegląd rozważanych alternatyw

| System | Fundament logiczny | Mocna strona | Dlaczego odrzucony w tym projekcie |
| --- | --- | --- | --- |
| **Mizar** | Teoria mnogości Tarskiego–Grothendiecka + logika I rzędu | Czytelny dla matematyków zapis dowodów; ogromna biblioteka MML | Mimo wspólnego języka FOL, aksjomaty teorii mnogości wywołują eksplozję kombinatoryczną w silniku rezolucyjnym; brak wbudowanej arytmetyki; schematy to skrycie logika II rzędu |
| **Coq** | Rachunek Konstrukcji Indukcyjnych (CIC), teoria typów | Dowody jako programy (Curry–Howard), zaawansowane języki taktyk (Ltac) | Wymaga pełnej translacji klauzul na termy/typy; nieprzystosowany do pracy na płaskich klauzulach FOL |
| **Lean 4** | Teoria typów zbliżona do CIC, z natywnym, wydajnym językiem programowania | Kompiluje się do C, FFI, metaprogramowanie, duże wsparcie społeczności AI/ML (np. Liquid Tensor Experiment) | Ten sam problem translacyjny jak Coq; sensowny dopiero przy modelowaniu logiki deontycznej, hierarchii norм czy *defeasible reasoning* wykraczających poza FOL |
| **Isabelle/HOL** | Logika wyższego rzędu (HOL), moduł Sledgehammer tłumaczący do FOL dla zewnętrznych ATP | Sledgehammer automatycznie korzysta z E, Vampire, SPASS, CVC4, Z3; bogata historia formalizacji systemów normatywnych | Komunikacja Python ↔ Isabelle (Poly/ML + Scala) wymaga ciężkiego procesu w tle (PIDE/LSP); nadmiarowe, gdy własny silnik już działa na czystym FOL |
| **Z3 / SMT (wybrane)** | Logika pierwszego rzędu + teorie (arytmetyka, tablice itd.) | Naturalny binding do Pythona, format tekstowy SMT-LIB, błyskawiczne sprawdzanie `sat`/`unsat` | — (przyjęty jako jedyny zewnętrzny komponent, wyłącznie jako „czarna skrzynka" do arytmetyki) |
| **ASP / Clingo** | Programowanie ze zbiorami odpowiedzi | Naturalna obsługa wnioskowania niemonotonicznego, dobre wsparcie dla reguł z wyjątkami | Wspomniany jako alternatywa dla samej weryfikacji niesprzeczności bazy przepisów, jeśli predykaty zamykają się w logice zdań/FOL — nie był jednak potrzebny, bo własny silnik rezolucji już to realizuje |

Warto odnotować, że ocena „dlaczego odrzucony" dotyczy *tego konkretnego* projektu — silnika rezolucji działającego natywnie na klauzulach tekstowych. W innym kontekście (np. budowa systemu od zera, bez istniejącego silnika, lub potrzeba modelowania logiki deontycznej czy hierarchii aktów prawnych jako niezmienników) Lean 4 lub Isabelle/HOL mogłyby być uzasadnionym wyborem —  ze wskazaniem na Lean 4 (dzięki kompilacji do C i integracji FFI) jako lepszego kandydata niż Isabelle, gdyby taka potrzeba faktycznie się zmaterializowała.

## 5. Pozostałe kluczowe decyzje projektowe

**Eager vs. lazy theory resolution.** Sprawdzanie spójności matematycznej „w locie" (przy każdym węźle drzewa rezolucji) generuje duży narzut komunikacji Python ↔ Z3, a w prawie kontynentalnym arytmetyka pojawia się zwykle na końcu długich łańcuchów warunków logicznych (np. najpierw trzeba dowieść, że ktoś jest „przedsiębiorcą" i „rezydentem", zanim w ogóle dojdzie do liczenia podatku). Stąd ogólna reguła: podejście leniwe (sprawdzanie po znalezieniu kandydata na dowód) jest efektywniejsze dla prostych, sekwencyjnych wzorów (np. subwencje oświatowe) i dla klasyfikacji towarowej w VAT, gdzie matematyka to tylko końcowe przemnożenie stawki. Podejście „w locie" zachowuje przewagę tam, gdzie ten sam typ zmiennej (np. dochód, wiek) jest wielokrotnie ograniczany w różnych przepisach — typowo w progresywnych skalach podatkowych — bo tam wczesne odcięcie sprzecznej gałęzi chroni przed dalszą, bezużyteczną analizą szczegółowych ulg. Finalna rekomendacja to hybryda bramkowana liczbą ograniczeń na tej samej zmiennej, opisana w punkcie 2.

**Rygor semantyczny (słownik pojęć / ontologia).** Bez ujednolicenia nazewnictwa zmiennych ten sam fakt prawny może być zakodowany pod różnymi etykietami w różnych aktach, co uniemożliwi solverowi wykrycie realnej sprzeczności. Rozwiązaniem jest słownik pojęć (odpowiednik prostej ontologii) wpięty jako krok pośredni istniejącego parsera — bez tworzenia nowych klas, zgodnie z przyjętą zasadą minimalizacji liczby typów obiektów w systemie. W skali międzynarodowej odpowiednikiem takiego podejścia jest standard **Akoma Ntoso / LegalDocML**, wspierany m.in. przez instytucje UE, który pozwala tagować fragmenty tekstu prawnego jawnymi identyfikatorami semantycznymi niezależnie od użytych słów.

**Standaryzacja zapisu klauzul.** Skoro predykaty są zapisywane jako czysty tekst logiczny,  **TPTP** (Thousands of Problems for Theorem Provers) jest gotowym, globalnym standardem zapisu problemów dla silników rezolucyjnych pierwszego rzędu — co potencjalnie umożliwia benchmarkowanie własnego silnika względem narzędzi takich jak Vampire czy E.

## 6.Dodatkowe informacji

* System Mizar został stworzony przez Andrzeja Trybulca na Uniwersytecie w Białymstoku, a prace nad nim rozpoczęły się w latach 70.  Biblioteka działa w oparciu o MML oraz teorii mnogości Tarskiego–Grothendiecka.

* Wynik MPTP — automatyczne dowodzenie bez podpowiedzi człowieka radzące sobie z około 40% twierdzeń z MML — jest dobrze potwierdzony w literaturze: pierwsza wersja translatora MPTP pozwoliła udowodnić 11 222 z 27 449 problemów, czyli 41%, a późniejsze udoskonalenia premis i translacji podniosły ten wynik do ponad 61% na standardowym benchmarku MPTP2078. Liczba „40%" podana w rozmowie jest więc trafna jako wynik wczesnych eksperymentów, choć nowsze metody (uczenie maszynowe do selekcji przesłanek, hammering) znacząco ją poprawiły.

* Licencje: Lean 4 i biblioteka Mathlib są dystrybuowane na licencji Apache 2.0. Isabelle jest dystrybuowana na zmodyfikowanej (3-klauzulowej) licencji BSD — Isabelle jest wolnym oprogramowaniem wydanym na zmodyfikowanej licencji BSD, choć dokładniej należałoby mówić o „BSD-3-Clause" niż ogólnie o „licencji typu BSD".

* Teoria rezolucji teorii (Theory Resolution) Stickela z 1985 roku może być używana  z architekturą SMT, choć trzeba zaznaczyć, że bezpośrednią architekturą stojącą za większością nowoczesnych solwerów SMT jest framework DPLL(T) (Nieuwenhuis, Oliveras, Tinelli), dla którego prace Stickela są istotnym, ale nie jedynym, źródłem inspiracji.

* Projekt Liquid Tensor Experiment, formalizujący wynik Petera Scholzego w Lean, jest  przedsięwzięciem społeczności Lean — ukończonym w 2022 roku.

* Z3 jest dystrybuowany na licencji MIT.

* Standard Akoma Ntoso (LegalDocML) jest używanym w praktyce standardem XML do reprezentacji dokumentów parlamentarnych i prawnych, rozwijanym pod patronatem OASIS i wykorzystywanym w niektórych projektach instytucji UE. Skala faktycznego wdrożenia bywa różna w różnych jurysdykcjach.

## 7. Źródła

- [Mizar Home Page](https://mizar.uwb.edu.pl/)
- [System Mizar – Wikipedia](https://pl.wikipedia.org/wiki/System_Mizar)
- [Mizar Mathematical Library](https://mizar.uwb.edu.pl/library/)
- [Translating Mizar for First Order Theorem Provers (Urban)](https://www.researchgate.net/publication/220915884_Translating_Mizar_for_First_Order_Theorem_Provers)
- [Miztype – soft typing w Mizarze (Wiedijk)](https://www.cs.ru.nl/~freek/mizar/miztype.pdf)
- [MPTP – TPTP Seminar overview](https://tptp.org/Seminars/ATP/Applications/MPTP.html)
- [Lean 4 – strona projektu](https://lean-lang.org/theorem_proving_in_lean4/Introduction/)
- [Lean 4 dokumentacja](https://lean4.dev/)
- [Isabelle/HOL – strona projektu](https://isabelle.in.tum.de/)
- [Isabelle (proof assistant) – Wikipedia](https://en.wikipedia.org/wiki/Isabelle_%28proof_assistant%29)
- [Liquid Tensor Experiment – blog Lean Community](https://leanprover-community.github.io/blog/posts/lte-final/)
- [Z3 Theorem Prover – repozytorium GitHub](https://github.com/Z3Prover/z3)
- [Clingo / Potassco (Answer Set Programming)](https://potassco.org/clingo/)
- [Stickel, „Automated deduction by theory resolution" (1985)](https://www.ijcai.org/Proceedings/85-2/Papers/101.pdf)
- [A Tutorial on Satisfiability Modulo Theories](https://scispace.com/pdf/a-tutorial-on-satisfiability-modulo-theories-oj18lj9pz2.pdf)
- [Isabelle vs. Lean – nieformalne porównanie](https://mrkeks.net/should-i-switch-from-isabelle-hol-to-lean/)