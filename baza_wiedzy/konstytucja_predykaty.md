W przypadku zapisów o charakterze stricte aksjologicznym lub deklaratywnym, dla których pełna formalizacja matematyczna jest niemożliwa lub bezcelowa, dodano stosowną adnotację wraz z przybliżoną metaregułą.


# Preambuła

My, Naród Polski - wszyscy obywatele Rzeczypospolitej, zarówno wierzący w Boga będącego źródłem prawdy, sprawiedliwości, dobra i piękna, jak i nie podzielający tej wiary, a te uniwersalne wartości wywodzący z innych źródeł, równi w prawach i w powinnościach wobec dobra wspólnego ustanawiamy Konstytucję Rzeczypospolitej Polskiej jako prawa podstawowe dla naszego państwa.

**Predykaty logiczne:**
*Zapis o charakterze deklaratywnym. Definiuje podmiot stanowiący prawo:*


$$\text{ŹródłoPrawa}(\text{Konstytucja}) = \text{NaródPolski}$$

Propagujemy postawy integrujące: miłości, braterstwa i solidarności i szacunku dla godności człowieka.

**Predykaty logiczne:**
*Zapis aksjologiczny (deklaracja kierunkowa):*


$$\forall x (\text{Postawa}(x) \land \text{Integrująca}(x) \to \text{Zalecana}(x))$$

# Rozdział I

## **Prawa i obowiązki podstawowe.**

1.0. Osobą w rozumieniu niniejszej Konstytucji jest każda istota ludzka od chwili poczęcia do naturalnej śmierci.

**Predykaty logiczne:**


$$\forall x (\text{IstotaLudzka}(x) \land \text{Czas}(x) \ge \text{Poczęcie} \land \text{Czas}(x) \le \text{ŚmierćNaturalna} \to \text{Osoba}(x))$$

1.1. Uznajemy, że każdej osobie przysługują takie same fundamentalne prawa, które są niezbywalne: prawo do życia i poszanowania godności człowieka jako osoby. Prawa te są ważniejsze niż dobro struktur organizacyjnych w jakich funkcjonujemy.

**Predykaty logiczne:**


$$\forall x (\text{Osoba}(x) \to \text{MaPrawoNiezbywalne}(x, \text{Życie}) \land \text{MaPrawoNiezbywalne}(x, \text{Godność}))$$

$$\forall s (\text{StrukturaOrganizacyjna}(s) \to \text{Nadrzędność}(\text{PrawaPodstawowe}, \text{Dobro}(s)))$$

1.2. Ustanawiamy państwo Rzeczpospolita Polska jako republikę dbającą o warunki indywidualnego i społecznego rozwoju swych obywateli.

**Predykaty logiczne:**


$$\text{ZobowiązanieCelowe}(\text{RP}, \text{RozwójObywateli})$$

1.3. Każda osoba przebywająca na terytorium Rzeczpospolitej Polskiej ma prawo dobrowolnego uczestniczenia we wspólnotach – czyli strukturach zbudowanych w oparciu o zasady troski o dobro wspólne. Dobro wspólne należy rozumieć jako warunki osobistego rozwoju dla wszystkich członków wspólnoty. Uznajemy, że tego typu wspólnotami są przede wszystkim rodziny rozumiane jako trwały związek kobiety i mężczyzny oraz naród. Te wspólnoty są pod ochroną i opieką państwa.

**Predykaty logiczne:**


$$\forall x (\text{Osoba}(x) \land \text{Terytorium}(x, \text{RP}) \to \text{PrawoDo}(\text{Uczestnictwo}(\text{Wspólnota})))$$

$$\forall w (\text{Wspólnota}(w) \to \text{OchronaPaństwa}(w))$$

$$\forall r (\text{TrwałyZwiązekKobietyIMężczyzny}(r) \to \text{Rodzina}(r) \land \text{Wspólnota}(r))$$

1.4. Uznajemy istnienie hierarchii wartości podstawowych:

1. Godność osoby jest wartością nieredukowalną. Zabrania się stanowienia prawa, które uzasadnia celowe naruszenie praw fundamentalnych jakiejkolwiek jednostki korzyścią ogółu. Żaden człowiek nie może stanowić wyłącznie środka do osiągnięcia celów państwa lub społeczeństwa.



**Predykaty logiczne:**


$$\forall x (\text{Osoba}(x) \to \text{Nieredukowalna}(\text{Godność}(x)))$$

$$\forall p (\text{Prawo}(p) \to \neg \text{Uzasadnia}(p, \text{NaruszeniePraw}(\text{Jednostka}, \text{KorzyśćOgółu})))$$

2. Szacunek dla prawdy - oznacza bezwzględny nakaz stosowania wyłącznie tych praw i decyzji administracyjnych, które stanowią logiczną, niesprzeczną konsekwencję udowodnionych faktów i praw wyższego rzędu, co podlega weryfikacji przez system o którym mowa w paragrafie 5.3.



**Predykaty logiczne:**


$$\forall d (\text{Decyzja}(d) \lor \text{Prawo}(d) \to \text{KonsekwencjaLogiczna}(d, \text{Fakty} \land \text{PrawaWyższe}) \land \text{Weryfikowalne}(d, \text{DSK}))$$

3. Dobro wspólnot – czyli prawo i obowiązek troski o wspólnoty będące pod ochroną i opieką państwa. Z troski o wspólnotę wynika konieczność stanowienia praw strzegących przyjęty system wartości.



**Predykaty logiczne:**


$$\forall w (\text{Wspólnota}(w) \land \text{PodOchroną}(w) \to \text{ObowiązekTroski}(\text{Obywatel}, w))$$

4. Sprawiedliwość, czyli stała i niezmienna wola przyznania każdemu należnych mu praw.



**Predykaty logiczne:**


$$\forall x \forall p (\text{NależnePrawo}(p, x) \to \text{Zagwarantowane}(p, x))$$

5. Wolność i tolerancja. Swoboda działania i głoszenia odmiennych poglądów – o ile nie podważa się w ten sposób fundamentalnych wartości chronionych niniejszą Konstytucją.



**Predykaty logiczne:**


$$\forall a (\text{Działanie}(a) \lor \text{GłoszeniePoglądów}(a)) \land \neg \text{Podważa}(a, \text{PrawaFundamentalne}) \to \text{Dozwolone}(a)$$

6. Swoboda zrzeszania się. Obywatele mają prawo powoływać do życia różne organizacje życia społecznego, które pozwalają na lepsze współdziałanie. Jednak działalność tych organizacji nie może naruszać przyjętego systemu wartości.



**Predykaty logiczne:**


$$\forall o (\text{Organizacja}(o) \land \neg \text{Narusza}(o, \text{SystemWartości}) \to \text{PrawoZrzeszania}(\text{Obywatel}, o))$$

7. Zasada pomocniczości. Oznacza to, że wsparcie działań osób poprzez struktury państwa jest niezbędne dopiero w sytuacji, gdy te osoby nie mogą poradzić sobie samodzielnie. Interwencja państwa następuje wyłącznie po spełnieniu obiektywnych, mierzalnych kryteriów niemożności zaspokojenia potrzeb podstawowych (np. brak dochodu minimalnego, orzeczona trwała niezdolność do pracy), których katalog określa ustawa o randze konstytucyjnej o ustroju gospodarczym



**Predykaty logiczne:**


$$\forall i (\text{InterwencjaPaństwa}(i, \text{Osoba}) \to \text{SpełniaKryteriaNiemożności}(\text{Osoba}, \text{UstawaGospodarcza}))$$

8. Prawo własności. Poszanowanie prywatnej własności jest podstawą ustroju państwa. Własność ta jednak nie może być gromadzona i utrzymywana z naruszeniem praw innych obywateli.



**Predykaty logiczne:**


$$\forall w (\text{WłasnośćPrywatna}(w) \land \neg \text{NaruszaPrawaInnych}(w) \to \text{Chroniona}(w))$$

1.5. Zmiany w prawach podstawowych są możliwe jedynie przy zachowaniu dwukadencyjności z potwierdzeniem w referendum:

1. Głosowanie inicjujące: Odchodzący parlament uchwala wniosek o zawieszeniu statusu "prawa podstawowego" z określonego zapisu oraz zakres możliwych zmian w następnym parlamencie. Zakres możliwych zmian nie może wykraczać poza obszar wskazanego przepisu i musi być logicznie spójny z pozostałymi prawami podstawowymi. Na tym etapie sam przepis nie ulega zmianie i nadal obowiązuje.


2. W dniu kolejnych wyborów do parlamentu obywatele otrzymują dodatkową kartę referendalną. Rozstrzygają na niej wyłącznie kwestię formalną: czy zatwierdzają propozycje odchodzącego parlamentu dotyczące konkretnie wskazanego przepisu.


3. Jeśli naród zagłosuje na "TAK" (i frekwencja przekroczy 60%), nowo wybrany parlament zyskuje swobodę – może zmienić ten przepis w trybie przewidzianym dla niższych aktów prawnych. Jeśli parlament nie przegłosuje zmian, albo naród zagłosuje na "NIE", przepis natychmiast odzyskuje swoją nienaruszalność i nowy parlament nie może go zmienić.



**Predykaty logiczne:**


$$\text{Zmiana}(\text{PrawoPodstawowe}) \leftrightarrow (\text{Wniosek}(\text{Parlament1}) \land \text{ZgodnośćZakresu}(\text{Wniosek}) \land \text{Referendum}(\text{Frekwencja} > 0.6 \land \text{Wynik} = \text{TAK}) \land \text{Zatwierdzenie}(\text{Parlament2}))$$

1.6. Państwo ma obowiązek powstrzymywania zła moralnego i fizycznego, z zachowaniem absolutnego szacunku dla każdej osoby. Użycie siły przez aparat państwowy jest legalne wyłącznie w celu powstrzymania naruszeń praw podstawowych i nie może prowadzić do celowego zniszczenia osoby ani traktowania jej podmiotowości jako rzeczy. Zakres użytej siły musi być proporcjonalny do aktualnego zagrożenia i ustaje wraz z jego ustaniem.

**Predykaty logiczne:**


$$\forall s (\text{UżycieSiły}(s) \to \text{Cel}(s, \text{PowstrzymanieNaruszeń}) \land \text{Proporcjonalne}(s, \text{Zagrożenie}) \land \neg \text{CeloweZniszczenie}(s, \text{Osoba}))$$

1.7. Państwo dąży do absolutnej niesprzeczności prawa. Każdy akt prawny nakładający obowiązki obywatelskie musi posiadać formalne, logiczne uzasadnienie wywiedzione z praw podstawowych, podlegające deterministycznej weryfikacji. Stanowienie praw nie spełniających wymogu rygorystycznej spójności logicznej jest zakazane.

**Predykaty logiczne:**


$$\forall p (\text{Prawo}(p) \to \text{DowódZgodności}(p, \text{PrawaPodstawowe}) \land \text{Weryfikowalne}(p, \text{DSK}))$$

# Rozdział II

## **Jak rozumieć prawa podstawowe.**

**Państwo**

2.1. Państwo nie jest jedynie strukturą lub aparatem ucisku. Wierzymy, że tworzą go ludzie kierujący się wspólnymi celami i wartościami. Dlatego należy w pierwszym rzędzie brać pod uwagę dobro tworzących wspólnotę obywateli. Celem państwa jest ochrona warunków rozwoju poprzez pracę z zachowaniem wolności, solidarności i tolerancji. Celem współpracy jest stałe doskonalenie istniejącego ładu w taki sposób, by wszyscy mogli w nim uczestniczyć w zgodzie z własnymi przekonaniami.

**Predykaty logiczne:**
*Zapis opisowy/metacelowy:*


$$\text{CelNadrzędny}(\text{Państwo}, \text{DobroObywateli}) \land \text{OchronaWarunków}(\text{Państwo}, \text{Rozwój})$$

**Wolność**

2.2. Suwerenność państwa uznajemy za wartość tak dużą, że dla jej obrony może nastąpić ograniczanie wolności (np. mobilizacja). Ograniczenia te mogą być jednak ustanawiane tylko wtedy, gdy są konieczne w demokratycznym państwie dla jego bezpieczeństwa lub porządku publicznego i są współmierne do zagrożenia, nie naruszając istoty praw fundamentalnych.

**Predykaty logiczne:**


$$\forall o (\text{OgraniczenieWolności}(o) \to \text{KonieczneDla}(o, \text{Bezpieczeństwo}) \land \text{Współmierne}(o, \text{Zagrożenie}) \land \neg \text{NaruszaIstoty}(o, \text{PrawaFundamentalne}))$$

2.3. Inne cele narodowe i społeczne powinny być realizowane z poszanowaniem wolności, która jest jednak wyzwaniem do poświęcenia, oddania i służby w imię solidarności.

**Predykaty logiczne:**


$$\forall c (\text{CelSpołeczny}(c) \to \text{RealizacjaZPoszanowaniem}(\text{Wolność}))$$

**Sprawiedliwość**

2.4. Sprawiedliwość domaga się akceptacji zasady wzajemności: oczekuję takich praw, jakie jestem gotów przyznać innym. Zasada ta dotyczy jednak osób, a nie organizacji.

**Predykaty logiczne:**


$$\forall x,y \in \text{Osoby} (\text{OczekujePrawa}(x, p) \to \text{GotówPrzyznać}(x, y, p))$$

**Tolerancja**

2.5. Różnorodność jest wartością. Dlatego należy unikać wymuszania zmiany poglądów lub rozwiązywania konfliktów w sferze idei przemocą. Jedynym uzasadnieniem dla takich działań może być ochrona praw podstawowych.

**Predykaty logiczne:**


$$\forall f (\text{WymuszaniePoglądów}(f) \to \text{KonieczneDlaOchrony}(f, \text{PrawaPodstawowe}))$$

2.5.1. Tolerancja polega na akceptacji sytuacji, w której w przestrzeni publicznej ścierają się różne idee. Uznajemy jednak istnienie spraw prywatnych $intymnych$, które nie powinny być przedmiotem działań podejmowanych w przestrzeni publicznej.

**Predykaty logiczne:**


$$\forall s (\text{SprawaPrywatna}(s) \to \neg \text{PrzedmiotDziałańPublicznych}(s))$$

2.5.2. W tym duchu należy uznać prawomocność obecności w sferze publicznej organizacji i symboliki religijnej, zgodnych z polską tradycją.

**Predykaty logiczne:**


$$\forall s (\text{SymbolikaReligijna}(s) \land \text{ZgodnaZTradycją}(s) \to \text{PrawomocnaObecnośćPubliczna}(s))$$

2.5.3. Tolerancja dla odmiennych poglądów nie może prowadzić do wymuszania akceptacji w jakiejkolwiek formie poglądów wewnętrznie sprzecznych, sprzecznych ze stanem naszej wiedzy i przekonaniami, czy też naruszającymi przyjęty system wartości. W tym ostatnim przypadku głoszenie takich poglądów może być prawnie zabronione. Zakazy takie muszą jednak mieć rangę konstytucyjną, a więc ich przyjęcie musi podlegać takiej samej procedurze jak ustawy o randze konstytucyjnej o których mowa w rozdziale III.

**Predykaty logiczne:**


$$\forall p (\text{Pogląd}(p) \land \text{NaruszaSystemWartości}(p) \to \exists z (\text{ZakazGłoszenia}(z, p) \land \text{RangaKonstytucyjna}(z)))$$

# Rozdział III

## **Państwo prawa**

3.0. Językiem urzędowym w Rzeczypospolitej Polskiej jest język polski, stanowiący również bazę do translacji przepisów na formalny język Systemu Ochrony Konstytucji o którym mowa w paragrafie 5.3.

**Predykaty logiczne:**


$$\text{JęzykUrzędowy}(\text{RP}) = \text{Polski} \land \text{BazaTranslacji}(\text{Polski}, \text{DSK})$$

3.1. Rzeczpospolita Polska jest państwem prawa. Oznacza to, że:
3.1.1. Każdy obywatel podlega takim samym prawom.

**Predykaty logiczne:**


$$\forall x,y \in \text{Obywatele} (\text{PodlegaPrawom}(x, P) \leftrightarrow \text{PodlegaPrawom}(y, P))$$

3.1.2. Prawo jest stabilne i jego zmiany mogą zachodzić jedynie z ważkich powodów społecznych, a nie dla umożliwienia rozstrzygnięcia jednej konkretnej sprawy.

**Predykaty logiczne:**


$$\forall z (\text{ZmianaPrawa}(z) \to \text{CelSpołeczny}(z) \land \neg \text{CelJednostkowy}(z))$$

3.1.3. Wszystkie struktury państwa działają według zasad określonych prawem.

**Predykaty logiczne:**


$$\forall s (\text{StrukturaPaństwa}(s) \to \text{DziałaZgodnieZ}(\text{Prawo}))$$

3.2. System prawa tworzą zapisy Konstytucji, ustawy przyjmowane przez Parlament składający się z demokratycznie wybranych przedstawicieli ogółu społeczeństwa oraz inne regulacje dopuszczane przez ustawy.

**Predykaty logiczne:**
*Definicja relacji zawierania:*


$$\forall p (\text{Prawo}(p) \to p \in \{\text{Konstytucja}, \text{Ustawy}, \text{InneRegulacje}\})$$

3.3. Zapisy niniejszej Konstytucji należy traktować jako nieprzekraczalne wymogi wobec wszelkich praw obowiązujących w państwie.

**Predykaty logiczne:**


$$\forall p (\text{Prawo}(p) \to \text{ZgodneZ}(p, \text{Konstytucja}))$$

3.4. Wyróżnia się ustawy o randze konstytucyjnej. Ustawy o randze konstytucyjnej to przełożenie zapisów Konstytucji na język konkretów. Regulują działanie władz i stanowią podstawę do logicznego uzasadnienia innych praw.

**Predykaty logiczne:**


$$\forall u (\text{UstawaRangiKonstytucyjnej}(u) \to \text{BazaLogicznaDla}(u, \text{UstawyZwykłe}))$$

3.5. Do ustaw o randze konstytucyjnej zalicza się regulacje ustanawiające:
3.5.1. Ustrój polityczny (...) 3.5.2. System Prawa (...) 3.5.3. Ustrój gospodarczy (...) 3.5.4. Siły zbrojne (...) 3.5.5. Ustawa o obywatelstwie.

**Predykaty logiczne:**
*Definicja dziedzinowa.*

3.6. Każda z ustaw o randze konstytucyjnej może być zmieniana niezależnie – bez konieczności zmiany Konstytucji. Uzasadnieniem dla wprowadzanych zmian może być dostosowanie do zmieniających się warunków, uzasadniona konieczność uściślenia przepisów lub uwzględnienie doświadczenia zdobytego w trakcie ich stosowania.

**Predykaty logiczne:**


$$\forall z (\text{Zmiana}(\text{UstawaKonstytucyjna}) \to \neg \text{WymagaZmiany}(\text{Konstytucja}))$$

3.7. Immunitet jako zwolnienie z odpowiedzialności prawnej osoby sprawującej władzę jest możliwy jedynie w odniesieniu do działań, których złych skutków nie można było racjonalnie przewidzieć na podstawie dostępnej wiedzy i modeli analitycznych zatwierdzonych ustawowo. W każdym innym przypadku osoby sprawujące władzę mogą być pociągnięte do odpowiedzialności za złamanie prawa.

**Predykaty logiczne:**


$$\forall d (\text{DziałanieWładzy}(d) \land \text{ZłeSkutki}(d) \land \text{Immunitet}(d) \to \neg \text{PrzewidywalneWModelu}(d, \text{ModeleAnalityczne}))$$

# Rozdział IV

## **Ustrój polityczny.**

**Parlament**

4.1. Rzeczpospolita Polska jest państwem demokratycznym w tym sensie, że władzę ustawodawczą sprawuje parlament do którego parlamentarzyści $posłowie i ewentualnie senatorowie$ są wybierani wyborach bezpośrednich i tajnych.

**Predykaty logiczne:**


$$\text{WładzaUstawodawcza} = \text{Parlament}$$

4.2. Parlamentarzystów nie obowiązują instrukcje wyborców – poza akceptacją wyników referendum organizowanego jako wiążące. Jednak mają oni obowiązek w swej działalności:

* kierować się zasadami etyki i strzec wyrażonych w Konstytucji wartości;
* działać w sposób odpowiedzialny, rozważając najgorsze możliwe skutki stanowionego prawa;
* postępować w sposób racjonalny, bez doktrynerstwa i z poszanowaniem systemu konstytucyjnych wartości;
* mieć na względzie wolę obywateli – co wyraża się w dążeniu do realizacji deklaracji złożonych przed wyborami, zachowywaniu stałej łączności z wyborcami i uwzględnianiu wyników referendów;
* Parlamentarzyści mają obowiązek przedłożenia do każdej propozycji ustawowej sformalizowanego, logicznego dowodu jej zgodności z prawami podstawowymi Konstytucji. Zatajenie przewidywalnych skutków stanowi naruszenie mandatu.



**Predykaty logiczne:**


$$\forall u (\text{PropozycjaUstawy}(u) \to \exists d (\text{DowódLogiczny}(d, u) \land \text{ZgodnyZKonstytucją}(d)))$$

$$\forall p (\text{ZatajenieSkutków}(p) \to \text{NaruszenieMandatu}(p))$$

4.3. Parlamentarzyści którzy nie postępują zgodnie z obowiązującymi ich zasadami mogą być odwoływani przed końcem kadencji drogą referendum. Mogą też sami złożyć rezygnację. Wówczas na ich miejsce wybierani są następcy.

**Predykaty logiczne:**


$$\forall p (\text{NaruszenieMandatu}(p) \to \text{MożliweOdwołanie}(p, \text{Referendum}))$$

4.4. Działalność parlamentarzystów jest finansowana przez państwo, ale sumaryczna wartość finansowania jest liczona jako stała kwota pomnożona przez ilość wyborców. Każdy z wyborców ma prawo wskazać parlamentarzystę który otrzyma przypisaną temu wyborcy kwotę. Reszta jest dzielona po równo między wszystkich parlamentarzystów.

**Predykaty logiczne:**


$$\forall w \in \text{Wyborcy} (\text{MożeWskazać}(w, \text{Parlamentarzysta}, \text{KwotaStała}))$$

**Prezydent**

4.5. - 4.5.5 Najwyższym przedstawicielem (...)

**Predykaty logiczne:**
*Definicje ról i kompetencji organów władzy państwowej (nie wymagają twardych blokad logicznych, stanowią strukturę decyzyjną).*

**Rząd**

4.6. - 4.8.1 Politykę wewnętrzną państwa (...)

**Predykaty logiczne:**
*Definicje kompetencji ustrojowych.*

4.8.2. Inicjatywa ustawodawcza przysługuje również grupie obywateli posiadających prawa wyborcze, w liczbie i na zasadach określonych w ustawie o randze konstytucyjnej.

**Predykaty logiczne:**


$$\text{MożeInicjowaćUstawę}(\text{GrupaObywateli}, \text{ZgodnieZUstawą})$$

**Samorząd**

4.9. - 4.9.2 Sposobem organizacji wspólnoty lokalnej jest samorząd terytorialny...

**REFERENDUM**

4.10. Referendum lokalne może być zorganizowane w dowolnej sprawie. W warunkach przewidzianych przez prawo referendum staje się wiążące dla reprezentujących region posłów i władz samorządowych. Warunki wiążącego referendum lokalnego nie mogą być mniej rygorystyczne niż warunki referendum ogólnopolskiego.

**Predykaty logiczne:**


$$\forall r (\text{ReferendumLokalne}(r) \land \text{Wiążące}(r) \to \text{Rygor}(r) \ge \text{Rygor}(\text{ReferendumOgólnopolskie}))$$

4.11. Parlament może zorganizować referendum ogólnopolskie, decydując czy i w jakich warunkach będzie ono wiążące dla parlamentarzystów. Wśród wymogów wobec wiążącego referendum musi się znaleźć frekwencja powyżej 50%.

**Predykaty logiczne:**


$$\forall r (\text{ReferendumOgólnopolskie}(r) \land \text{Wiążące}(r) \to \text{Frekwencja}(r) > 0.5)$$

**Podstawowe zasady sprawowania władzy**

4.12. Władza polityczna jest służbą społeczeństwu. Ta służba musi być zawsze ukierunkowana na dobro wspólne, poprzez które realizuje się dobro każdego obywatela. Troska o dobro poszczególnych grup społecznych nie oznacza ich ochrony w sposób niesprawiedliwy przed naturalnymi zmianami.

**Predykaty logiczne:**
*Norma metakierunkowa.*

4.12.1. Rząd, administracja rządowa i inne władze powinny działać w sposób transparentny, zrozumiały dla obywatela. Zasady powinny być formułowane za pomocą jednoznacznych reguł logicznych (predykatów), które dają się udowodnić i prześledzić w systemie informatycznym państwa, zapewniając każdemu obywatelowi algorytmiczne uzasadnienie decyzji. Zasada przejrzystości powinna być realizowana także przez równy i powszechny dostęp do informacji.

**Predykaty logiczne:**


$$\forall z (\text{ZasadaWładzy}(z) \to \exists f (\text{FormułaLogiczna}(f) \land \text{Równoważna}(z, f) \land \text{Weryfikowalna}(f, \text{DSK})))$$

4.12.2. - 4.12.4. W polityce międzynarodowej... Uznajemy integracje europejską jako wartość...

**Stany nadzwyczajne**

4.13. W sytuacjach szczególnych zagrożeń państwo może wprowadzić stan nadzwyczajny. Regulacje te określa ustawa o randze konstytucyjnej, z zastrzeżeniem, że prawa podstawowe ujęte w Rozdziale I niniejszej Konstytucji nie mogą ulec zawieszeniu.

**Predykaty logiczne:**


$$\forall s (\text{StanNadzwyczajny}(s) \to \neg \text{Zawiesza}(s, \text{PrawaPodstawowe}))$$

# Rozdział V

## **System Prawa**

5.1. Państwo powinno dbać o sprawiedliwy porządek prawny, budowany z poszanowaniem zasad etyki. Prawo nie może ograniczać wolności obywateli w sposób nie dający się uzasadnić na gruncie przyjętych zasad etyki i personalistycznej koncepcji społeczeństwa.

**Predykaty logiczne:**


$$\forall p (\text{Prawo}(p) \land \text{OgraniczaWolność}(p) \to \text{UzasadnioneEtycznie}(p))$$

5.2. Istnieje hierarchia praw, co oznacza iż akty prawne niższego rzędu muszą być zgodne z aktami wyższego rzędu, a w razie wątpliwości decydujące są zapisy aktów wyższego rzędu.

**Predykaty logiczne:**


$$\forall p1, p2 (\text{Prawo}(p1) \land \text{Prawo}(p2) \land \text{WyższyRząd}(p1, p2) \to \text{ZgodneZ}(p2, p1))$$

5.2.1. - 5.2.4 Procedury stanowienia praw niższych.

5.3. Nad spójnością logiczną prawa o której mowa powyżej czuwa informatyczny "System Ochrony Konstytucji" utrzymywany przez Instytut Utrzymania Systemu. Nowe lub zmieniane przepisy muszą zostać przełożone na zbiór logicznych i zweryfikowane przez System Ochrony Konstytucji pod względem spójności z pozostałymi przepisami. W razie niemożności stwierdzenia spójności z powodu niezrozumiałych zapisów, organ stanowiący prawo ma obowiązek niezwłocznego jego poprawienia – o ile to możliwe jeszcze zanim to prawo zacznie obowiązywać.

**Predykaty logiczne:**


$$\forall p (\text{NowePrawo}(p) \to \text{PrzetłumaczoneNaLogikę}(p) \land \text{Zweryfikowane}(\text{DSK}, p))$$

5.4. Zmiana Konstytucji...

5.5. Wszystkie inne prawa muszą być konkretne: regulować określone działania, wprowadzać konkretne prawa i obowiązki. Zabronione jest wprowadzanie praw, które nie odpowiadają na pytanie: co lub jak należy robić w określonej sytuacji? Każdy wprowadzany przepis musi jednoznacznie wskazywać: podmiot normy, warunek zastosowania oraz precyzyjny skutek prawny.

**Predykaty logiczne:**


$$\forall p (\text{Przepis}(p) \to \exists s \exists w \exists r (\text{Podmiot}(p, s) \land \text{Warunek}(p, w) \land \text{SkutekPrawny}(p, r)))$$

5.6. - 5.6.2 Wymiar sprawiedliwości...

5.6.3. Spory kompetencyjne między najwyższymi organami państwa rozstrzyga Sąd Najwyższy, posiłkując się logiczną weryfikacją przeprowadzoną przez System Ochrony Konstytucji w trybie określonym ustawowo.

**Predykaty logiczne:**


$$\forall s (\text{SpórKompetencyjny}(s) \to \text{Rozstrzyga}(\text{SądNajwyższy}, s) \land \text{KorzystaZ}(\text{DSK}, s))$$

5.7. Sędziowie są niezawiśli...

5.7.1. Wyroki sądu dotyczące stosunków między ludźmi lub ocenie ich czynów powinny zawierać uzasadnienie sformułowane w oparciu o prawo oraz wiedzę sędziego. Zakłada się domniemanie braku świadomej intencji naruszenia dobra wspólnego, dopóki udowodnione fakty materialne nie wykażą celowego działania na szkodę osoby lub wspólnoty.

**Predykaty logiczne:**


$$\forall c (\text{Czyn}(c) \land \neg \text{FaktyDziałaniaCelowego}(c) \to \neg \text{IntencjaNaruszenia}(c))$$

5.7.2. Inne wyroki powinny zawierać opis sprawy uściślony na tyle, by dało się stosując reguły logiczne wywieść wyrok z obowiązującego prawa. Notoryczne podważanie przez wyższą instancję poprawności wnioskowania w wyroku stanowi przesłankę do odsunięcia sędziego formułującego błędne wyroki od orzekania w tego typu sprawach.

**Predykaty logiczne:**


$$\forall w (\text{WyrokFormalny}(w) \to \text{DowodliwyLogicznie}(w, \text{PrawoObowiązujące}))$$

5.7.3. Państwo powinno dążyć do maksymalnej automatyzacji wnioskowania o którym mowa w punkcie 5.7.2.

# Rozdział VI

## **Ustrój gospodarczy państwa**

6.1. Podstawą funkcjonowania gospodarki jest aktywność obywateli. Nie wolno jej ograniczać z wyjątkiem sytuacji, w których systemowo dowiedziono, że aktywność ta bezpośrednio narusza prawa podstawowe innych osób lub stanowi bezpośrednie zagrożenie dla życia i zdrowia.

**Predykaty logiczne:**


$$\forall a (\text{AktywnośćGospodarcza}(a) \land \text{Ograniczenie}(a) \to \text{NaruszaPrawa}(a) \lor \text{ZagrożenieŻycia}(a))$$

6.2. Polska gospodarka jest zgodna z zasadami społecznej gospodarki rynkowej. Oznacza to, że zaspokojenie potrzeb społeczeństwa jest głównym celem gospodarki rozwijającej się w warunkach maksymalnej wolności. Odrzuca się zatem taką interpretację społecznej gospodarki rynkowej, że państwo opodatkowuje gospodarkę, aby mieć środki na niwelowanie niepożądanych jej efektów.

6.2.1. Państwo jest odpowiedzialne za takie kształtowanie ładu gospodarczego, który dąży do zapewnienia wszystkim obywatelom powszechnego udziału w wypracowanym dobru wspólnym poprzez algorytmicznie waloryzowany dochód gwarantowany, pokrywający ściśle zdefiniowany ustawowo koszyk minimum egzystencji:
a) daje wszystkim uczestnikom rynku równe szanse $brak dyskryminacji, stabilny i prosty system prawny$;
b) daje możliwość bogacenia się poprzez udział w efektach rozwoju, a nie wyzysku słabszych przez silniejszych; przez wyzysk rozumie się przy tym wynagrodzenia i opłaty niespełniające obiektywnych parametrów określonych w ustawach (np. wielokrotność stopy referencyjnej Narodowego Banku Polskiego);
c) przeciwdziała tworzeniu monopoli i opłat o charakterze monopolistycznym, nakładanych poza systemem wolnej konkurencji i wymagających odrębnej regulacji ustawowej.

**Predykaty logiczne:**


$$\forall x (\text{Obywatel}(x) \to \text{Posiada}(\text{DochódGwarantowany}(x) \ge \text{MinimumEgzystencji}))$$

$$\forall w (\text{Wynagrodzenie}(w) \to w \ge \text{ParametrUstawowy})$$

6.2.2. Państwo promuje i wspiera takie działania gospodarcze, które:
a) sprzyjają rozwojowi społeczeństwa i zaspokajaniu potrzeb obywateli;
b) przeciwdziałają dyskryminacji społecznie użytecznych zajęć niepodlegających bezpośredniej wycenie rynkowej (np. opieka i wychowanie dzieci w rodzinie).

6.2.3. Państwo kieruje się zasadą pomocniczości poprzez:
a) pomoc w powrocie do aktywności i przejęciu samodzielnej odpowiedzialności za siebie i rodzinę osobom, które znalazły się w szczególnie trudnej sytuacji ;
b) niwelowanie nierówności dochodowych i majątkowych poprzez system podatkowy;
c) zapewnienie godnego życia takiego, które nie urąga ze względów ekonomicznych godności człowieka wszystkim obywatelom oraz dążenie do wprowadzenia minimalnego dochodu gwarantowanego, którego parametry (np. koszyk minimum egzystencji) określa ustawa o randze konstytucyjnej o ustroju gospodarczym.

6.3. Opodatkowanie działalności gospodarczej jest sposobem zapłaty za korzyści jakie daje jej prowadzenie w danej lokalizacji.

6.3.1. Środki z tych podatków powinny w pierwszym rzędzie być zatem przeznaczone na rozwój społeczno-gospodarczy w tej lokalizacji. Wynagradzane powinny być z nich te prace, które choć ważne dla społeczeństwa i jego rozwoju, nie są kupowane wprost przez prowadzące działalność gospodarczą przedsiębiorstwa.

6.3.2. System podatkowy należy zmieniać w sposób nie zagrażający stabilności gospodarki. Celem państwa jest całkowita likwidacja podatku dochodowego i maksymalne uproszczenie systemu podatkowego.

**Predykaty logiczne:**
*Cel ustrojowy systemu gospodarczego:*


$$\text{Cel}(\text{Państwo}, \text{Likwidacja}(\text{PodatekDochodowy}))$$

6.4. Dopuszcza się tworzenie wielu systemów wymiany towarów i usług oraz wielu systemów walutowych.
6.4.1. Powołuje się Narodowy Bank Polski...

6.5. Celem państwa jest stworzenie systemu gospodarczego zapewniającego każdemu obywatelowi godne życie.
6.5.1. Państwo przeciwdziała podporządkowaniu dobra osób strukturom ekonomicznym $ekonomizm$.
6.5.2. W okresie przejściowym dopuszcza się funkcjonowanie państwowych systemów zasiłków i dotacji. Docelowo należy zamienić je na udział w systemie wymiany dóbr oraz udziały w przychodach podatkowych o których mowa w art. 6.3 niniejszej Konstytucji.

# Rozdział VII

## **Siły zbrojne**

7.1. Polskie siły zbrojne mają charakter obronny. Zakazany jest ich udział w wojnach, które nie mają charakteru obronnego.

**Predykaty logiczne:**


$$\forall w (\text{Wojna}(w) \land \text{Udział}(w, \text{SiłyZbrojneRP}) \to \text{CharakterObronny}(w))$$

7.2. Wszyscy obywatele mają obowiązek obrony swojego państwa poprzez gotowość do uczestnictwa w systemie obronnym.

**Predykaty logiczne:**


$$\forall x (\text{Obywatel}(x) \to \text{ObowiązekObrony}(x))$$

# Rozdział VIII

## **Obywatelstwo**

8.1. Obywatelami Rzeczpospolitej Polskiej stają się osoby będące potomkami obywateli Rzeczpospolitej Polskiej lub jej prawnych poprzedników. Jeśli tylko jeden z rodziców danej osoby jest obywatelem Polski – prawo do nabycia obywatelstwa musi być potwierdzone wyrażeniem woli jego przyjęcia przez osobę której to dotyczy lub jej rodziców w przypadku osoby nieletniej.

**Predykaty logiczne:**


$$\forall x (\exists y (\text{Rodzic}(y, x) \land \text{ObywatelRP}(y)) \land \text{WyrażaWolę}(x) \to \text{ObywatelRP}(x))$$

8.2. Obywatelstwo polskie może zostać nabyte przez inne osoby trwale przebywające na terytorium Polski, pod warunkiem złożenia sformalizowanej przysięgi oraz wykazania się obiektywną znajomością Konstytucji, z zastrzeżeniem, że późniejsze celowe złamanie praw podstawowych może skutkować utratą tego obywatelstwa.

**Predykaty logiczne:**


$$\forall x (\text{NabycieObywatelstwa}(x) \to \text{ZłożeniePrzysięgi}(x) \land \text{ZnajomośćKonstytucji}(x))$$

$$\forall x (\text{CeloweZłamaniePrawPodstawowych}(x) \to \text{MożliwaUtrataObywatelstwa}(x))$$

8.3. Zobowiązania państwa wobec obywateli:
8.3.1. Wspólne dobro jest najważniejszym celem państwa. Dążenie do tego celu powinno odbywać się z troską o prawdę, z poszanowaniem wolności i sprawiedliwości.
8.3.2. Państwo otacza szczególną troską rodzinę, życie ludzkie, wychowanie młodego pokolenia.
8.3.3. Państwo zapewnia wszystkim obywatelom darmowy dostęp do podstawowej opieki medycznej, szkolnictwa na poziomie podstawowym i średnim.

**Predykaty logiczne:**


$$\forall x (\text{Obywatel}(x) \to \text{Zapewnione}(\text{OpiekaMedyczna}, x) \land \text{Zapewnione}(\text{EdukacjaPodstawowaIŚrednia}, x))$$

8.4. Obowiązki obywateli:
8.4.1. Wszyscy obywatele są zobowiązani do przestrzegania obowiązującego prawa.
8.4.2. Wszyscy są zobowiązani do troski o dobro wspólne. Troska ta przejawia się w szczególności w solidarnej współpracy – czyli pracy wykonywanej dla dobra wspólnego a nie tylko z chęci zysku.

**Predykaty logiczne:**


$$\forall x (\text{Obywatel}(x) \to \text{PrzestrzegaPrawa}(x) \land \text{TroskaODobroWspólne}(x))$$

# Rozdział IX

## **Przepisy przejściowe**

9.1. Do czasu uchwalenia nowych ustaw o randze konstytucyjnej przewidzianych w niniejszej Konstytucji, dotychczasowe regulacje ustawowe zachowują moc obowiązującą, o ile System Ochrony Konstytucji nie wykaże ich jawnej sprzeczności z prawami podstawowymi. Terminy dostosowawcze określą odrębne ustawy.

**Predykaty logiczne:**


$$\forall p (\text{StarePrawo}(p) \land \neg \text{SprzeczneZ}(\text{PrawaPodstawowe}, p, \text{DSK}) \to \text{Obowiązuje}(p))$$

9.2: „Organy władzy powołane na podstawie dotychczasowych przepisów zachowują uprawnienia do czasu ukonstytuowania organów przewidzianych niniejszą Konstytucją, nie dłużej jednak niż cztery lata od jej wejścia w życie."

**Predykaty logiczne:**


$$\forall o (\text{StaryOrgan}(o) \to \text{Uprawnienia}(o) \le \text{WejścieWŻycie}(\text{Konstytucja}) + 4\text{Lata})$$