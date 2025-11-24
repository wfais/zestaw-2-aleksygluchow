import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify


def _parsuj_wejscie(wejscie: str):
    """
    Wejście ma postać:
        "x**3 + 3*x + 1, -10 10"
    Zwracamy:
        funkcja_str, x_min, x_max
    """
    func_str, rest = wejscie.split(",", 1)
    func_str = func_str.strip()
    rest = rest.strip()
    x_min_str, x_max_str = rest.split()
    x_min = float(x_min_str)
    x_max = float(x_max_str)
    return func_str, x_min, x_max


# Funkcja rysująca wykres na podstawie eval()
def rysuj_wielomian(wejscie):
    # Parsujemy wejście
    func_str, x_min, x_max = _parsuj_wejscie(wejscie)

    # Generujemy punkty x
    x_val = np.linspace(x_min, x_max, 200)

    # Przygotowujemy środowisko dla eval – dopuszczamy tylko to, co potrzebne
    allowed = {
        "x": x_val,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "log": np.log,
    }

    # Liczymy y(x) za pomocą eval
    y_val = eval(func_str, {"__builtins__": {}}, allowed)

    # Jeśli wyszedł skalar (np. "5"), zamień na tablicę stałą
    if np.isscalar(y_val):
        y_val = np.full_like(x_val, float(y_val))

    # Rysujemy wykres (bez show!)
    plt.plot(x_val, y_val, label="eval()")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"f(x) = {func_str}  (eval)")
    plt.grid(True)
    plt.legend()

    # Zwracamy wartości na brzegach przedziału
    return float(y_val[0]), float(y_val[-1])



# Funkcja rysująca wykres na podstawie sympy i lambdify()
def rysuj_wielomian_sympy(wejscie):
    # Parsujemy wejście
    func_str, x_min, x_max = _parsuj_wejscie(wejscie)

    # Symboliczna zmienna
    x = symbols("x")

    # Zamiana napisu na wyrażenie sympy
    expr = sympify(func_str)

    # Funkcja numeryczna, backend numpy
    f_num = lambdify(x, expr, "numpy")

    # Punkty x i wartości y
    x_val = np.linspace(x_min, x_max, 200)
    y_val_sympy = f_num(x_val)

    # Rysujemy wykres (bez show!)
    plt.plot(x_val, y_val_sympy, "--", label="sympy")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"f(x) = {func_str}  (sympy)")
    plt.grid(True)
    plt.legend()

    # Zwracamy wartości na brzegach przedziału
    return float(y_val_sympy[0]), float(y_val_sympy[-1])


if __name__ == '__main__':
    # Przykładowe wywołanie pierwszej funkcji (eval)
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)

    # Drugie wejście dla funkcji sympy - bardziej złożona funkcja
    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (sympy):", wynik_sympy)

    # Wyświetlanie obu wykresów
    plt.show()
