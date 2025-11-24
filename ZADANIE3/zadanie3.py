import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100  
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    """
    Zwraca listę słów:
        - tylko litery
        - małe litery
        - długość > 3
    """
    slowa = WORD_RE.findall(text)
    slowa = [s.lower() for s in slowa]
    slowa = [s for s in slowa if len(s) > 3]
    return slowa


def ramka(text: str, width: int = 80) -> str:
    """
    Zwraca napis w kwadratowej ramce:
        [   wyśrodkowany tekst   ]
    Jeśli tekst jest za długi → obcinamy i dodajemy „…”
    """
    maxlen = width - 2 

    if len(text) > maxlen:
        text = text[: maxlen - 1] + "…"

    centered = text.center(maxlen)
    return f"[{centered}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    
    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            data = requests.get(URL, headers=HEADERS, timeout=10).json()
        except Exception:
            # problem z siecią → spróbuj ponownie
            time.sleep(0.1)
            continue

        
        title = data.get("title") or ""
        line = "\r" + ramka(title, 80)
        print(line, end="", flush=True)

        
        extract = data.get("extract") or ""
        slowa = selekcja(extract)

        cnt.update(slowa)
        licznik_slow += len(slowa)
        pobrane += 1

        time.sleep(0.05)

    print("\n")
    print(f"Pobrano wpisów: {pobrane}")
    print(f"Słów (≥4) łącznie: {licznik_slow}")
    print(f"Unikalnych (≥4): {len(cnt)}\n")

    print("Top 15 słów (≥4):")
    for slowo, ile in cnt.most_common(15):
        print(f"{slowo:15}  {ile}")



if __name__ == "__main__":
    main()









#tego nie potrzebujemy ale testy narzekaja:


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