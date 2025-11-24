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
    print(f"Pobrano: {pobrane}")
    print(f"#Słowa:  {licznik_slow}")
    print(f"Unikalne: {len(cnt)}\n")

    print("Najczęstsze 15 słów:")
    for slowo, ile in cnt.most_common(15):
        print(f"{slowo:15}  {ile}")


if __name__ == "__main__":
    main()
