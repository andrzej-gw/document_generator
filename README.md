
Klub Żeglarski UW – Automatyzacja decyzji członkowskich ⛵

Ten projekt automatyzuje obsługę zgłoszeń członkowskich i osób stowarzyszonych
w Klubie Żeglarskim Uniwersytetu Warszawskiego.

Funkcjonalności:
- pobieranie nowych zgłoszeń z Google Forms / Google Sheets
- ręczna weryfikacja zgłoszeń w terminalu
- generowanie PDF decyzji (LaTeX → PDF)
- wysyłanie PDF na Google Drive (rclone)
- aktualizacja statusów i kolorów w Google Sheets

Projekt działa jako lokalne narzędzie CLI.


STRUKTURA PROJEKTU
------------------

.
├── decyzja.py           # starsza, ręczna wersja generatora decyzji
├── decyzja2.py          # generowanie + upload PDF dla pojedynczego zgłoszenia
├── biernik.py           # odmiana imię+nazwisko (Gemini API + potwierdzenie)
├── google_sheets.py     # integracja z Google Sheets (read / write / colors)
├── update.py            # główny workflow (walidacja → PDF → Sheets)
├── nr_czlonka_os.pkl    # licznik numerów decyzji (członek / OS)
├── .gitignore
└── README.md


WYMAGANIA
---------

System:
- Linux / macOS
- pdflatex
- rclone

Python:
- Python 3.10+
- biblioteki:
  google-api-python-client
  google-auth
  google-auth-oauthlib
  google-auth-httplib2
  google-generativeai


KONFIGURACJA
------------

Google Sheets API:
- skonfigurowane OAuth (Desktop App)
- pliki:
  - client_secret*.json
  - token.json (tworzony automatycznie)

Pliki te są ignorowane przez git.

Gemini API (biernik):
Ustaw zmienną środowiskową:

export GEMINI_API_KEY="TWÓJ_KLUCZ_API"


URUCHAMIANIE
------------

Główny punkt wejścia:

python update.py

Skrypt:
1. sprawdza nowe zgłoszenia w arkuszach
2. wyświetla dane w terminalu
3. pyta o akceptację
4. generuje PDF decyzji
5. wysyła PDF na Google Drive
6. aktualizuje arkusz Google


LOGIKA ARKUSZA GOOGLE
--------------------

Nowe zgłoszenie:
- kolumna A niepusta
- kolumna S pusta

Po akceptacji:
- kolumny P–T wypełnione:
  - "tak"
  - numer decyzji
  - imię osoby decyzyjnej
  - "tak"
  - "wyslij"
- tekst kolumn A–O kolor zielony (#35a853)

Po odrzuceniu:
- kolumna S = "tak"
- tekst kolumn A–O kolor czerwony (#ea4335)


OPIS MODUŁÓW
------------

google_sheets.py
- wykrywanie nowych wierszy
- zapisywanie danych do arkusza
- kolorowanie zakresów (kolor tekstu)

biernik.py
- automatyczna odmiana imienia i nazwiska (Gemini)
- ręczne potwierdzenie lub korekta

decyzja2.py
- generowanie LaTeX
- kompilacja PDF
- upload przez rclone


DANE WRAŻLIWE
------------

Ignorowane przez .gitignore:
- token.json
- client_secret*.json
- pliki PDF i TEX
- __pycache__/


POMYSŁY NA ROZBUDOWĘ
-------------------

- tryb w pełni automatyczny (bez input)
- batch processing bez przerywania po pierwszym błędzie
- timestamp i autor decyzji w arkuszu
- walidacja e-maili i danych wejściowych


AUTOR
-----

Andrzej Gwiazda
Prezes Klubu Żeglarskiego Uniwersytetu Warszawskiego
