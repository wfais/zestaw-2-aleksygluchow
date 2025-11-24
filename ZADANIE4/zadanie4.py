import os
import time
import threading
import sys

# Stałe konfiguracyjne
LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    
    lokalna_suma = 0.0

    for i in range(pocz, kon):
        x = (i + 0.5) * krok
        lokalna_suma += 4.0 / (1.0 + x * x)

    # mnożymy przez krok – ten fragment to już kawałek całki
    wyniki[indeks] = lokalna_suma * krok


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    krok = 1.0 / LICZBA_KROKOW

    # Wstępne uruchomienie w celu "rozgrzania" środowiska
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    czas_jednowatkowy = None

    for n_watkow in LICZBA_WATKOW:
        
        wyniki = [0.0] * n_watkow
        watki: list[threading.Thread] = []

        start_czas = time.perf_counter()
        for idx in range(n_watkow):
            pocz = idx * LICZBA_KROKOW // n_watkow
            kon = (idx + 1) * LICZBA_KROKOW // n_watkow
            t = threading.Thread(
                target=policz_fragment_pi,
                args=(pocz, kon, krok, wyniki, idx),
            )
            watki.append(t)

        
        for t in watki:
            t.start()

        
        for t in watki:
            t.join()

        przyblizenie_pi = sum(wyniki)
        czas_trwania = time.perf_counter() - start_czas

        if czas_jednowatkowy is None:
            czas_jednowatkowy = czas_trwania
            przyspieszenie = 1.0
        else:
            przyspieszenie = czas_jednowatkowy / czas_trwania if czas_trwania > 0 else float("inf")

        # Prosty, czytelny raport
        print(
            f"Wątki: {n_watkow:2d}  "
            f"pi ≈ {przyblizenie_pi:.10f}  "
            f"czas: {czas_trwania:.3f} s  "
            f"przyspieszenie: {przyspieszenie:.2f}x"
        )


if __name__ == "__main__":
    main()
