def rzymskie_na_arabskie(rzymskie):
    if not isinstance(rzymskie, str) or not rzymskie:
        raise ValueError("Liczba rzymska musi być niepustym napisem.")

    rzymskie = rzymskie.upper()

    wartosci = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    
    for ch in rzymskie:     # sprawdzenie dozwolonych znaków
        if ch not in wartosci:
            raise ValueError("Niepoprawny znak w liczbie rzymskiej.")

    
    wynik = 0    # podstawowa konwersja (reguła odejmowania)
    i = 0
    while i < len(rzymskie):
        
        v = wartosci[rzymskie[i]]  # wartość bieżącego znaku

        # jeśli następny znak istnieje i jest większy - ODEJMUJEMY
        if i + 1 < len(rzymskie):
            v_next = wartosci[rzymskie[i + 1]]
            if v < v_next:
                wynik += v_next - v
                i += 2
                continue

        # inaczej DODAJEMY
        wynik += v
        i += 1

    # zakres 1–3999
    if not (1 <= wynik <= 3999):
        raise ValueError("Liczba poza zakresem 1-3999.")

    # bardzo ważne: sprawdzamy, czy zapis był kanoniczny
    # (np. "IIII" da 4, ale poprawny zapis to "IV")
    if arabskie_na_rzymskie(wynik) != rzymskie:
        raise ValueError("Niepoprawny format liczby rzymskiej.")

    return wynik


# ARABSKA int - RZYMSKA str
def arabskie_na_rzymskie(arabskie):
    if not isinstance(arabskie, int):
        raise ValueError("Liczba arabska musi być typu int.")

    if not (1 <= arabskie <= 3999):
        raise ValueError("Liczba musi być w zakresie 1-3999.")

    wartosci = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    wynik = []
    n = arabskie

    for wartosc, symbol in wartosci:
        ile_razy = n // wartosc
        if ile_razy > 0:
            wynik.append(symbol * ile_razy)
            n -= wartosc * ile_razy

    return "".join(wynik)


if __name__ == '__main__':
    try:
        # Przykłady konwersji rzymskiej na arabską
        rzymska = "XXI"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")
        
        # Przykłady konwersji arabskiej na rzymską
        arabska = 1984
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")
        
    except ValueError as e:
        print(e)
