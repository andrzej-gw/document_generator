import google_sheets
import pickle
import decyzja2

def validate(row, typ):
    cz = '''Sygnatura czasowa	Deklaruję chęć dołączenia do Klubu Żeglarskiego Uniwersytetu Warszawskiego, zwanego dalej Klubem. Zobowiązuję się do zachowania szacunku wobec innych osób, działania na rzecz realizacji celów Klubu oraz przestrzegania obowiązków członkowskich zawartych w Regulaminie. 	Wyrażam zgodę na przetwarzanie swoich danych osobowych na potrzeby prowadzenia Klubu oraz publikację wizerunku, uzyskanego w ramach działań w Klubie, do realizacji celów organizacji, w szczególności relacji z działań Klubu. Zasady przetwarzania danych osobowych w Klubie Żeglarskim UW: https://goo.gl/wWSjHL	Oświadczam, że jestem aktualnie studentem bądź doktorantem Uniwersytetu Warszawskiego i zobowiązuję się poinformować Zarząd Klubu o utracie statusie statusu studenta UW. 	Imię	Nazwisko	Numer telefonu	Adres e-mail	Numer indeksu (tylko studenci UW)	Numer legitymacji AZS (tylko członkowie AZS)	Jakie masz doświadczenie z żaglami? Dopiero zaczynasz, pływałaś/eś po morzu, regularnie uczestniczysz w regatach? Powiedz nam coś o sobie :)	Czy i jakie masz uprawnienia żeglarskie (patent, SRC, LRC, uprawnienia instruktorskie, inne)?	Uczestnicząc w organizacji pracy Klubu, czym chciał(a)byś się zająć?	"Które kryterium członkostwa spełniasz?
np. uczestniczyłem w Majówce 2023"'''.split('\t')
    os = '''Sygnatura czasowa	Deklaruję chęć dołączenia na zasadach osoby stowarzyszonej do Klubu Żeglarskiego Uniwersytetu Warszawskiego, zwanego dalej Klubem. Zobowiązuję się do zachowania szacunku wobec innych osób, działania na rzecz realizacji celów Klubu oraz przestrzegania obowiązków członkowskich zawartych w Regulaminie.	Wyrażam zgodę na przetwarzanie swoich danych osobowych na potrzeby prowadzenia Klubu oraz publikację wizerunku, uzyskanego w ramach działań w Klubie, do realizacji celów organizacji, w szczególności relacji z działań Klubu. Zasady przetwarzania danych osobowych w Klubie Żeglarskim UW: https://goo.gl/wWSjHL	Oświadczam, że:	Imię	Nazwisko	Numer telefonu	Adres e-mail	Jestem:	Numer legitymacji AZS (tylko dla członków AZS)	Jakie masz doświadczenie z żaglami? Dopiero zaczynasz, pływałaś/eś po morzu, regularnie uczestniczysz w regatach? Powiedz nam coś o sobie :)	Czy i jakie masz uprawnienia żeglarskie (patent, SRC, LRC, uprawnienia instruktorskie, inne)?	Uczestnicząc w organizacji pracy Klubu, czym chciał(a)byś się zająć?	Adres e-mail	"Które kryterium członkostwa spełniasz?
np. uczestniczyłem w Majówce 2023"'''.split('\t')

    if typ=="czlonek":
        pola = cz
    else:
        pola = os
    
    for i in range(len(pola)):
        print("\033[34m"+pola[i]+"\033[0m")
        print(row[i])
        print()
    while True:
        odp = input("Czy akceptujesz? (y/n):\n")
        if odp == "y":
            return True
        if odp == "n":
            return False


def main():
    SPREADSHEET_ID_CZLONKOWIE = "1W9Bvpve6t40w-9JMtZ-ydMqIA_ip5jEhy8-dXWDG11o"
    SPREADSHEET_ID_OS = "1SK0wIP1_JhbvXaoXaZ4A9CVlg0Bxsq5t9OWQdxSxYVY"
        
    forms = [{'SPREADSHEET_ID':SPREADSHEET_ID_CZLONKOWIE, 'typ':"czlonek"},
            {'SPREADSHEET_ID':SPREADSHEET_ID_OS, 'typ':"os"}]

    for f in forms:
        SPREADSHEET_ID = f['SPREADSHEET_ID']
        typ = f['typ']
        
        rows = google_sheets.check_new_rows(SPREADSHEET_ID)

        if not rows:
            print(f"Nie ma nowych {typ}!")
        else:
            print(f"Zgłoszono {len(rows)} nowych {typ}:")
            for row_number, row in rows:
                accepted = validate(row, typ)
                if not accepted:
                    google_sheets.set_status_in_cols_p_t(SPREADSHEET_ID, row_number, ["","","","tak",""])
                    #red
                    google_sheets.color_cols_a_o_green(SPREADSHEET_ID, row_number, color = "#ea4335")
                    return
                with open("nr_czlonka_os.pkl", "rb") as f:
                    nr_czlonka, nr_os = pickle.load(f)
                if typ=="czlonek":
                    nr = nr_czlonka
                else:
                    nr = nr_os
                google_sheets.set_status_in_cols_p_t(SPREADSHEET_ID, row_number, ["tak",nr,"Andrzej Gwiazda","tak","wyslij"])
                #green
                google_sheets.color_cols_a_o_green(SPREADSHEET_ID, row_number, color = "#35a853")
                decyzja2.create_and_upload_pdfs(typ, row, nr)
                if typ=="czlonek":
                    nr_czlonka+=1
                else:
                    nr_os+=1
                with open("nr_czlonka_os.pkl", "wb") as f:
                    pickle.dump((nr_czlonka, nr_os), f)
                
if __name__ == "__main__":
    main()
