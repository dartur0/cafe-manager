# Left no Crumbs – Dokumentacja Techniczna i Podręcznik Użytkownika

Left No Crumbs to rozbudowana, dwuwymiarowa (2D) gra zręcznościowo-strategiczna czasu rzeczywistego, stworzona w języku Python przy użyciu biblioteki Pygame. Gracz wciela się w rolę managera restauracji serwującej unikalne wyroby cukiernicze oraz napoje kofeinowe dla wymagającej, paranormalnej klienteli.

Aplikacja charakteryzuje się zaawansowaną mechaniką zarządzania czasem, dynamicznym systemem ekonomiczno-sklepowym, adaptacyjną krzywą trudności oraz pełnym pokryciem kluczowej logiki biznesowej zautomatyzowanymi testami jednostkowymi. Projekt został w pełni skonteneryzowany za pomocą narzędzia Docker i przystosowany do pracy w środowiskach bezfizycznego ekranu (headless).

## 1. Struktura Projektu

Architektura katalogów opiera się na ścisłym separowaniu warstwy danych i logiki biznesowej (Backend) od komponentów renderowania grafiki i obsługi zdarzeń interfejsu użytkownika (Frontend/UI).

```text
cafe_manager/
├── assets/                      # Zasoby multimedialne wykorzystywane przez grę
│   ├── fonts/                   # Czcionki TrueType (np. Pacifico.ttf dla stylizowanego GUI)
│   ├── images/                  # Tekstury stacji roboczych, ikon składników, ciast i kaw
│   ├── music/                   # Ścieżka dźwiękowa i tła muzyczne poziomu
│   └── sounds/                  # Efekty dźwiękowe (kliknięcia, parzenie kawy, dźwięk ukończenia)
├── saves/                       # Katalog przeznaczony na trwałe pliki zapisu stanu gry
├── src/                         # Kod źródłowy aplikacji podzielony modułowo
│   ├── core/                    # Rdzeń silnika gry i czysta logika biznesowa
│   │   ├── decorators/          # Implementacja modyfikatorów obiektów (Wzorzec Dekorator)
│   │   ├── entities/            # Encje domenowe (Customer, Kitchen, Coffee, Cake, Order)
│   │   ├── states/              # Klasy zarządzające cyklem życia ekranów (Wzorzec Stan)
│   │   ├── systems/             # Systemy peryferyjne (SaveManager, LevelManager, SoundManager)
│   │   └── game.py              # Główna pętla gry (Game Loop) i koordynacja podsystemów
│   └── ui/                      # Warstwa prezentacji, komponenty i ekrany interfejsu GUI
│       ├── components/          # Panele interaktywne (CakePanel, CoffeePanel, Button)
│       └── screens/             # Ekrany menu głównego, sklepu oraz podsumowania dnia
├── tests/                       # Pakiet automatycznych testów jednostkowych (Pytest)
│   ├── test_customer.py         # Weryfikacja mechaniki cierpliwości, algorytmu napiwków i typów gości
│   ├── test_decorators.py       # Testy poprawności obliczeń cenowych i nazw wzorca Dekorator
│   ├── test_kitchen.py          # Weryfikacja gospodarki zasobami, limitów tacek i witryn
│   ├── test_level.py            # Testy warunków wygranej, progresji trudności i przyznawania gwiazdek
│   └── test_order.py            # Weryfikacja mechanizmu sprawdzania zgodności zamówień (Combo/Single)
├── Dockerfile                   # Przepis budowania odchudzonego obrazu Linux-slim
├── docker-compose.yml           # Deklaracja usług, wolumenów i zmiennych środowiskowych audio/wideo
├── requirements.txt             # Ścisła lista zależności pakietów Pythona
└── save.json                    # Serializowany stan gry tworzony automatycznie (Auto-save)

```

## 2. Zależności i Wymagania Środowiskowe

Aplikacja została zoptymalizowana pod kątem działania w środowiskach Python 3.12 oraz Python 3.14.

### Zależności Pythona (plik requirements.txt):

* pygame==2.6.1 – Odpowiada za niskopoziomową komunikację z bibliotekami SDL (obsługa okna graficznego, renderowanie powierzchni 2D, przetwarzanie miksera audio, obsługa zdarzeń systemowych myszy).
* pytest==9.1.0 – Wykorzystywany do izolowanego wykonywania asercji testowych w środowisku lokalnym oraz CI/CD.

### Wymagania systemowe dla instalacji natywnej:

* Linux (Ubuntu/Debian): Wymaga instalacji pakietów deweloperskich biblioteki SDL2 z poziomu menedżera pakietów Advanced Package Tool (apt): libsdl2-dev, libsdl2-image-dev, libsdl2-mixer-dev, libsdl2-ttf-dev, libfreetype6-dev.
* macOS: Wymaga środowiska Python 3.12+ oraz ewentualnych bibliotek wsparcia zainstalowanych poprzez system Homebrew.
* Windows: Instalacja Pygame poprzez pip automatycznie dostarcza prekompilowane biblioteki dynamiczne (DLL) SDL.

## 3. Architektura i Zastosowane Wzorce Projektowe

### A. Wzorzec Stan (State Pattern)

Wzorzec ten służy do zarządzania maszyną stanów aplikacji (Finite State Machine). Klasa główna Game przechowuje instancję aktualnego stanu reprezentowanego przez obiekt polimorficzny dziedziczący po klasie bazowej GameState z pliku base_state.py. Przełączanie ekranów odbywa się bez zakłócania ciągłości głównej pętli gry.

* Implementacja: Każdy stan nadpisuje cztery kluczowe metody: on_enter() (inicjalizacja i alokacja zasobów), handle_event() (przechwytywanie wejścia użytkownika), update() (aktualizacja delty czasowej fizyki i logiki) oraz draw() (wywołanie renderowania na obiekt screen).
* Klasy stanów:
* MenuState: Obsługa interfejsu powitalnego oraz wyboru profilu gry.
* DayState: Główna faza gry, zarządzanie zamówieniami oraz pracą kuchni.
* GameoverState: Obsługa warunku przegranej, zatrzymanie czasu i wyświetlenie statystyk końcowych.
* PauseState: Natychmiastowe wstrzymanie pętli gry bez utraty danych sesji.
* SettingsState: Menu konfiguracji audio, wideo oraz sterowania.
* ShopState: Zarządzanie fazą ekonomiczną i zakupem ulepszeń pomiędzy poziomami.
* TutorialState: Wydzielony samouczek prezentujący podstawy mechaniki nowym użytkownikom.



### B. Wzorzec Dekorator (Decorator Pattern)

Zastosowany w celu uniknięcia eksplozji kombinatorycznej klas (dziedziczenia) przy tworzeniu złożonych produktów spożywczych o zmiennych właściwościach i cenach.

* Implementacja: Klasa podstawowa BaseCake reprezentuje czysty korzec ciasta o z góry zdefiniowanej cenie bazowej. W momencie wyboru składników przez gracza, obiekt ten jest dynamicznie opakowywany przez konkretne dekoratory smaku ciasta oraz dekoratory kremów.
* Konsekwencje architektoniczne: Wywołanie metody get_price(), get_name() lub get_prep_time() na obiekcie finalnym powoduje rekurencyjne przejście po strukturze dekoratorów, dynamicznie sumując ceny poszczególnych komponentów, modyfikując ciąg znaków nazwy oraz obliczając finalny czas pieczenia w zależności od stopnia skomplikowania przepisu.


## 4. Instrukcja Uruchomienia i Konfiguracji

### Opcja A: Uruchomienie lokalne (Środowisko Natywne)

1. Upewnij się, że w systemie zainstalowany jest interpreter języka Python w wersji minimum 3.12.
2. Otwórz konsolę/terminal w głównym katalogu projektu cafe_manager i zainstaluj wymagane pakiety:

```bash
pip install -r requirements.txt

```

3. Uruchom punkt wejścia aplikacji:

```bash
python src/core/game.py

```

### Opcja B: Uruchomienie w kontenerze Docker (Środowisko Izolowane)

Obraz kontenera został oparty na minimalistycznej dystrybucji python:3.12-slim. W celu umożliwienia poppingu działania gry w środowisku bez dostępu do fizycznej karty graficznej i dźwiękowej (np. na serwerze integracyjnym CI), w architekturze kontenera zastosowano:

* Xvfb (X Virtual Framebuffer): Wirtualny serwer X11, który symuluje obecność monitora o rozdzielczości 1280x720 z 24-bitową głębią kolorów w pamięci RAM.
* Zmienną środowiskową SDL_AUDIODRIVER=dummy: Przekierowuje zapytania miksera dźwiękowego Pygame do wirtualnej platformy bezdźwiękowej, zapobiegając krytycznemu błędowi pygame.error: mixer not initialized.

1. Uruchom oficjalne środowisko wykonawcze Docker Desktop na swoim komputerze.
2. Przeprowadź proces budowania obrazu na podstawie instrukcji z pliku Dockerfile:

```bash
docker compose build

```

3. Uruchom usługę w trybie odizolowanym (detachment mode), co zainicjalizuje proces gry na wirtualnym ekranie w tle:

```bash
docker compose up -d

```

4. Aby wyłączyć kontener i zwolnić zasoby systemowe komputera, wykonaj:

```bash
docker compose down --remove-orphans

```


## 5. Zautomatyzowane Testy Jednostkowe

Aplikacja posiada rygorystyczne pokrycie kodu testami jednostkowymi, podzielonymi na 5 logicznych modułów testowych w katalogu tests/.

### Wykonanie testów w środowisku lokalnym:

```bash
PYTHONPATH=src pytest tests/

```

### Wykonanie testów wewnątrz kontenera Docker:

```bash
docker compose run game bash -c "PYTHONPATH=src python3 -m pytest tests/"

```

*Prawidłowy wynik operacji to komunikat: ============================= 45 passed in ...s =============================, zaświadczający o braku regresji w logice biznesowej gry.*


## 6. Instrukcja dla Użytkownika

### Cel Rozgrywki

Gracz staje przed wyzwaniem przetrwania kolejnych dni roboczych w kawiarni. Każdy dzień definiuje cel główny (np. Serve 5 customers – Obsłuż 5 klientów). Nad głowami pojawiających się gości wyświetlają się dymki z precyzyjnymi zamówieniami (kawa o określonym typie mleka, ciasto o konkretnej bazie i kremie lub zestawy Combo).

Gracz musi zarządzać surowcami, kolejką kuchenną oraz czasem reakcji. Jeśli pasek cierpliwości klienta spadnie do zera, opuszcza on lokal, generując stratę finansową i uniemożliwiając zdobycie kompletu gwiazdek.

### Pierwsze Kroki po Uruchomieniu

1. Ekran Menu Głównego: Użytkownik ma do wyboru interaktywne opcje sterowane za pomocą kliknięć myszy:
* PLAY: Wczytuje ostatni stan rozgrywki z pliku zapisu (jeśli istnieje) i przenosi do aktualnego dnia.
* NEW GAME: Nadpisuje dotychczasowe postępy, przyznaje stan początkowy (0.00 monet) i uruchamia Dzień 1.
* TUTORIAL: Uruchamia stan samouczka wyjaśniający rozkład elementów graficznych.
* SETTINGS: Otwiera panel konfiguracji głośności efektów oraz muzyki.
* SHOP: Skrót dający bezpośredni dostęp do panelu ulepszeń kawiarni.
* END: Bezpieczne zamknięcie aplikacji, czyszczenie pamięci podręcznej i wyjście do systemu operacyjnego.


2. Po kliknięciu PLAY lub NEW GAME gra inicjuje stan DayState.

### Obsługa Interfejsu i Wykonywanie Operacji

#### A. Klienci (Stanowiska przy ladzie)

* W kawiarni może przebywać jednocześnie do 4 klientów. Każdy z nich posiada indywidualny, widoczny pasek cierpliwości.
* Zadaniem gracza jest przygotowanie i wydanie zamówienia zanim czas wskaźnika cierpliwości upłynie.

#### B. Stacja Kawowa / Parzenie Kawy (Lewy Panel Interfejsu)

1. Wybór Rodzaju Napoju: Kliknij przycisk "ESP" (czyste, esencjonalne Espresso) lub "MILK" (Kawa mleczna). W pierwszej kolejności należy zaparzyć bazę espresso.
2. Dodanie Mleka (Wymagane tylko dla opcji MILK): Kliknij na jedną z trzech ikon kartonów mleka znajdujących się poniżej: REG (zwykłe mleko), LACT_FR (mleko bezlaktozowe), OAT (mleko owsiane). Jeśli wybierzesz Espresso, wybór mleka zostanie zablokowany automatycznie.
3. Uruchomienie Ekspresu Ciśnieniowego: Kliknij przycisk z napisem "BREW".
* Napój pojawi się na jednej z trzech tacek ekspresu, prezentując cyfrowy czas parzenia oraz miniaturowy pasek postępu.
* Ukończenie parzenia sygnalizowane jest zielonym wskaźnikiem "OK" oraz dedykowanym efektem dźwiękowym.


4. Ekspozycja na Witrynie: Kliknij na filiżankę ze statusem "OK". Kawa powędruje na witrynę wystawową.

#### C. Stacja Cukiernicza / Przygotowanie Ciasta (Prawy Panel Interfejsu)

1. Wybór Bazy Ciasta: W górnej sekcji panelu kliknij lewym przyciskiem myszy na ikonę odpowiadającą pożądanemu smakowi korca (VANILLA, CHOC - czekoladowy, RED - czerwony aksamit, CARROT - marchewkowy). Wybrany komponent zostanie podświetlony zieloną ramką.
2. Wybór Kremu: W rzędzie poniżej wybierz rodzaj pokrycia kremowego (VANILLA, CHOC, STRAWB - truskawkowy, BANANA, BLUEB - jagodowy, PISTACH - pistacjowy).
3. Inicjalizacja Procesu Pieczenia: Po wybraniu bazy i dodaniu kremu kliknij na jeden z wolnych prostoktnych Slotów Kuchennych (zlokalizowanych w dolnej-środkowej części ekranu).
* Slot zostanie zablokowany, a na ekranie pojawi się numeryczne odliczanie czasu pozostałego do upieczenia.
* Po zakończeniu procesu na slocie pojawi się zielona obwódka i napis "READY".


4. Ekspozycja na Witrynie: Kliknij na gotowy slot z napisem "READY". Ciasto zostanie automatycznie przetransportowane na szklaną witrynę wystawową.

#### D. Witryna i Wydawanie Zamówień (Środek Ekranu)

* Gotowe produkty oczekują na wydanie w sekcji witryny wystawowej.
* Jeżeli na Twojej witrynie znajduje się produkt dokładnie odpowiadający preferencjom klienta wyświetlanym w dymku nad jego głową, kliknij bezpośrednio na postać tego klienta.
* Logika gry automatycznie pobierze właściwy produkt z witryny, usunie klienta z lady, zwolni slot dla kolejnego gościa, a na konto gracza wpłynie cena produktu powiększona o dynamicznie wyliczony napiwek.

#### E. Kontrola Magazynu i Logistyka (Przycisk REFILL)

* Każde użycie ziaren kawy, bazy ciasta czy porcji kremu trwale pomniejsza zasoby kawiarni. Aktualny stan ilościowy wyświetla się w formie liczbowej (np. x3, Cream: 10/10) bezpośrednio na panelach.
* W przypadku braku surowca, system zablokuje produkcję, wyświetlając komunikat ostrzegawczy na konsoli debugowania.
* Aby uzupełnić zasoby, kliknij przycisk "REFILL" umieszczony w dolnej części ekranu. Spowoduje to natychmiastowe, darmowe odnowienie wszystkich zapasów magazynowych do ich maksymalnych limitów pojemnościowych.

#### F. Warunki Progresu i Gwiazdki (Shop Phase)

* Do ukończenia dnia wymagane jest zrealizowanie celu dobowego (obsłużenie wskazanej liczby gości).
* Poziom zadowolenia obsłużonych klientów (zależny od czasu oczekiwania) bezpośrednio przekłada się na liczbę przyznanych gwiazdek na koniec dnia (skala od 0 do 3).
* Po udanym zakończeniu dnia roboczego następuje automatyczne przejście do ekranu ShopState, gdzie za zarobione pieniądze gracz może dokonać ulepszeń technicznych: kupić dodatkowe sloty kuchenne, zwiększyć pojemność zbiornika na krem lub odblokować unikalne przepisy. Zakupione ulepszenia trwale modyfikują logikę i interfejs gry od następnego dnia.


## 7. System Trwałości Danych (Zapis i Wczytywanie)

Gra posiada w pełni zautomatyzowany, przezroczysty dla użytkownika system automatycznego zapisu stanu (Auto-save).

* Format Danych: Stan gry jest serializowany do zunifikowanego formatu maszynowego JSON i zapisywany w pliku tekstowym save.json w głównym katalogu aplikacji.
* Moment Zapisu: Procedura zapisu wywoływana jest automatycznie w dwóch kluczowych momentach: w ułamku sekundy po pomyślnym zatwierdzeniu zakończenia dnia roboczego oraz natychmiast po wyjściu z panelu sklepu ulepszeń.
* Zakres Zapisu: Plik przechowuje informacje o numerze bieżącego poziomu (day), całkowitym stanie konta bankowego gracza (money), tablicę unikalnych identyfikatorów zakupionych ulepszeń (purchased) oraz historię zdobytych gwiazdek.
* Moduł SaveManager dba o to, by przy nagłym zamknięciu aplikacji użytkownik mógł bezstresowo powrócić do zarządzania kawiarnią bez utraty wypracowanych postępów.
