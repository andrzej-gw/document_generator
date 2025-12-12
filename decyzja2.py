import os, sys
import datetime

import biernik

def usun_spacje_na_poczatku_i_na_koncu(slowo):
    while slowo and slowo[0]==" ":
        slowo=slowo[1:]
        
    while slowo and slowo[-1]==" ":
        slowo=slowo[:-1]
        
    return slowo

def create_and_upload_pdfs(typ, dane, nr):
    if not (typ=="czlonek" or typ=="os"):
        print("typ: Oczewkiwano czlonek/os")
        return
            
    if (typ=="czlonek" and len(dane)<9) or (typ=="os" and len(dane)<8):
        print("Za mało danych")
        return
        
    for i in range(len(dane)):
        dane[i]=usun_spacje_na_poczatku_i_na_koncu(dane[i])
    
    if typ=="czlonek":
        data, zgoda1, zgoda2, zgoda3, imie, nazwisko, telefon, email, nr_indeksu = dane[:9]
    else:
        data, zgoda1, zgoda2, zgoda3, imie, nazwisko, telefon, email = dane[:8]
            
    rok = str(datetime.date.today().year)
    
    imie_nazwisko_biernik = biernik.odmien(imie+" "+nazwisko)
    
    nazwa_pliku = ""
    if typ=="czlonek":
        nazwa_pliku+="DC "
        nr_decyzji = nr
    elif typ=="os":
        nazwa_pliku+="DOS "
        nr_decyzji = nr
        
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
"""+("członków" if typ=="czlonek" else "osób stowarzyszonych")+" "+imie_nazwisko_biernik+(", numer albumu: "+nr_indeksu if typ=="czlonek" else "")+""".
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
    
    if typ == "czlonek":
        os.system(
    f"rclone copy '{nazwa_pliku[:-3]+'pdf'}' "
    "gdrive:Klub\\ Żeglarski\\ UW/Członkostwo/Decyzje/DC/ --progress"
)
    else:
        os.system(
    f"rclone copy '{nazwa_pliku[:-3]+'pdf'}' "
    "gdrive:Klub\\ Żeglarski\\ UW/Członkostwo/Decyzje/DOS/ --progress"
)        
