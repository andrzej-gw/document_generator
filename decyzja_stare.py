import os, sys
def main():
    L = sys.argv[1].split(".")
    if len(L)!=8:
        print("Oczekiwany format to: czlonek/os.imie.nazwisko.nr_indeksu.nr.rok.imie_biernik.nazwisko_biernik")
        return
    typ, imie, nazwisko, nr_indeksu, nr_decyzji, rok, imie_biernik, nazwisko_biernik=L
    nazwa_pliku = ""
    if typ=="czlonek":
        nazwa_pliku+="DC "
    elif typ=="os":
        nazwa_pliku+="DOS "
    else:
        print("nieznany typ: "+typ)
        print("Oczekiwany format to: czlonek/os.imie.nazwisko.nr_indeksu.nr.rok.imie_biernik.nazwisko")
        return
        
    nazwa_pliku+=nr_decyzji+" - "+rok+" "+imie+" "+nazwisko+".tex"
    
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
Decyzja nr """+nr_decyzji+"/"+rok+"""\\\\
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
Wiceprezes Klubu Żeglarskiego Uniwersytetu Warszawskiego

\\end{document}
""")
    os.system("pdflatex '"+nazwa_pliku+"'")
main()
