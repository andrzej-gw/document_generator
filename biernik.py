import google.generativeai as genai
import os

def odmien(imie_nazwisko):

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-2.5-flash')

    response = model.generate_content(f"Podaj biernik od {imie_nazwisko}, uwaga nie pisz nic więcej tylko biernik tego wyrażenia.")

    biernik = response.text
 
    print(f"Biernik({imie_nazwisko}) -> {biernik}")
    
    
    odp = input("Może być? (y/n):\n")

    if odp == "y":
        return biernik
    if odp == "n":
        return input(f"Podaj biernik {imie_nazwisko}:\n")


if __name__ == "__main__":
    print(odmien("Bartosz Jaźwiec"))
