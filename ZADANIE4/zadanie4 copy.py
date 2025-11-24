import os
import time
import threading
import sys

# Stałe konfiguracyjne
LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    # Funkcja oblicza częściową sumę przybliżenia liczby pi metodą prostokątów.
    # Argumenty:
    #     pocz, kon - zakres iteracji (indeksy kroków całkowania),
    #     krok      - szerokość pojedynczego prostokąta (1.0 / LICZBA_KROKOW),
    #     wyniki    - lista, do której należy wpisać wynik dla danego wątku na pozycji indeks,
    #     indeks    - numer pozycji w liście 'wyniki' do zapisania rezultatu.

    # Każdy wątek powinien:
    #   - obliczyć lokalną sumę dla przydzielonego przedziału,
    #   - wpisać wynik do wyniki[indeks].

    pass  # zaimplementuj obliczanie fragmentu całki dla danego wątku


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    # Wstępne uruchomienie w celu stabilizacji środowiska wykonawczego
    krok = 1.0 / LICZBA_KROKOW
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    # ---------------------------------------------------------------
    # Tu zaimplementować:
    #   - utworzenie wielu wątków (zgodnie z LICZBY_WATKOW),
    #   - podział pracy na zakresy [pocz, kon) dla każdego wątku,
    #   - uruchomienie i dołączenie wątków (start/join),
    #   - obliczenie przybliżenia π jako sumy wyników z poszczególnych wątków,
    #   - pomiar czasu i wypisanie przyspieszenia.
    # ---------------------------------------------------------------


if __name__ == "__main__":
    main()
