import os, sys
import datetime
import pickle

def usun_spacje_na_poczatku_i_na_koncu(slowo):
    while slowo and slowo[0]==" ":
        slowo=slowo[1:]
        
    while slowo and slowo[-1]==" ":
        slowo=slowo[:-1]
        
    return slowo

def main():
    typ=input("czlonek czy os?\n")
    if not (typ=="czlonek" or typ=="os"):
        print("Oczewkiwano czlonek/os")
        return
    
    ile=input("Ile osób?\n")
    try:
        ile=int(ile)
    except:
        print("Oczekiwano liczby całkowitej")
        return
        
    with open("nr_czlonka_os.pkl", "rb") as f:
        nr_czlonka, nr_os = pickle.load(f)
    
    #  nr_decyzji=input("Nr pierwszej osoby?\n")
    #  try:
        #  nr_decyzji=int(nr_decyzji)
    #  except:
        #  print("Oczekiwano liczby całkowitej")
        #  return
        
    print("Wklej dane z formularza")
    
    osoby = []
    for i in range(ile):
        dane = input().split("\t")
        if (typ=="czlonek" and len(dane)<9) or (typ=="os" and len(dane)<8):
            print("Za mało danych")
            return
        osoby.append(dane)
    
    lista_maili = []
    
    for dane in osoby:
        
        for i in range(len(dane)):
            dane[i]=usun_spacje_na_poczatku_i_na_koncu(dane[i])
        
        if typ=="czlonek":
            data, zgoda1, zgoda2, zgoda3, imie, nazwisko, telefon, email, nr_indeksu = dane[:9]
        else:
            data, zgoda1, zgoda2, zgoda3, imie, nazwisko, telefon, email = dane[:8]
                
        lista_maili.append(email)
            
        rok = str(datetime.date.today().year)
        
        imie_biernik, nazwisko_biernik = input("Biernik od "+imie+" "+nazwisko+"\n").split()
        
        nazwa_pliku = ""
        if typ=="czlonek":
            nazwa_pliku+="DC "
            nr_decyzji = nr_czlonka
        elif typ=="os":
            nazwa_pliku+="DOS "
            nr_decyzji = nr_os
            
        nazwa_pliku+=str(nr_decyzji)+" - "+rok+" "+imie+" "+nazwisko+".tex"
        
        with open(nazwa_pliku, "w", encoding="utf-8") as my_file:
            my_file.write("""\\documentclass{article}
\\usepackage{polski}
\\usepackage[utf8]{inputenc}
\\usepackage[margin=3cm, a4paper, bottom=2cm]{geometry}
\\usepackage{graphicx}

\\setlength{\\parindent}{0pt}
\\author{Andrzej Gwiazda}
\\pagenumbering{gobble}

\\begin{document}

\\includegraphics[width=100px]{../kzuw_logo.png}

\\begin{center}
\\textbf{
Decyzja nr """+str(nr_decyzji)+"/"+rok+"""\\\\
O przyznaniu """+("członkostwa" if typ=="czlonek" else "statusu osoby stowarzyszonej")+"""\\\\
Klubu Żeglarskiego Uniwersytetu Warszawskiego\\\\
z dnia \\today\\\\
}
\\end{center}


Na podstawie § 15 Regulaminu Klubu Żeglarskiego Uniwersytetu Warszawskiego przyjmuje się w poczet
"""+("członków" if typ=="czlonek" else "osób stowarzyszonych")+" "+imie_biernik+" "+nazwisko_biernik+(", numer albumu: "+nr_indeksu if typ=="czlonek" else "")+""".
\\\\\\\\\\\\\\\\\\\\
\\noindent\\rule{\\textwidth}{0.3pt}
\\\\\\\\\\\\\\\\
Andrzej Gwiazda\\\\
Prezes Klubu Żeglarskiego Uniwersytetu Warszawskiego

\\end{document}
""")
        os.system("pdflatex '"+nazwa_pliku+"'")
        os.system("rm '"+nazwa_pliku[:-3]+"aux'")
        os.system("rm '"+nazwa_pliku[:-3]+"log'")
        nr_decyzji += 1
        
        if typ == "czlonek":
            os.system(
    f"rclone copy '{nazwa_pliku[:-3]+'pdf'}' "
    "gdrive:Klub\\ Żeglarski\\ UW/Członkostwo/Decyzje/DC/ --progress"
)
            nr_czlonka+=1
        else:
            os.system(
    f"rclone copy '{nazwa_pliku[:-3]+'pdf'}' "
    "gdrive:Klub\\ Żeglarski\\ UW/Członkostwo/Decyzje/DOS/ --progress"
)
            nr_os+=1
    print("\nMaile:\n")
    for email in lista_maili:
        print(email)
        
    with open("nr_czlonka_os.pkl", "wb") as f:
        pickle.dump((nr_czlonka, nr_os), f)

if __name__ == "__main__":
    main()
