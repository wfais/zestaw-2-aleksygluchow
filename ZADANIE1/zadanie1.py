def dodaj_element(wejscie):
    # 1. Najpierw znajdziemy maksymalną głębokość listy.
    max_depth = -1



    def znajdz_max_glebokosc(obj, depth):
        """
        obj   - aktualny obiekt (lista / krotka / słownik / cokolwiek)
        depth - aktualna głębokość
        """
        nonlocal max_depth 

        if isinstance(obj, list): #sprawdzamy czy jest lista
            if depth > max_depth:
                max_depth = depth

            # schodzimy głębiej do jej elementów
            for x in obj:
                znajdz_max_glebokosc(x, depth + 1)

        elif isinstance(obj, tuple): #sprawdzamy czy jest krotka
            
            for x in obj:
                znajdz_max_glebokosc(x, depth + 1)

        elif isinstance(obj, dict): #sprawdzamy czy jest slownikiem
            
            for v in obj.values():
                znajdz_max_glebokosc(v, depth + 1)
        else:           #JESLI NIE LISTA, NIE KROTKA, NIE SLOWNIK

            pass




    
    znajdz_max_glebokosc(wejscie, 0) #uruchamiamy pierwsze przejście

    # 2. Drugie przejście – faktycznie dodajemy element do "najgłębszych" list.
    def dodaj_do_najglebszych(obj, depth):
        if isinstance(obj, list):
            if depth == max_depth:
                # to jest jedna z najgłębiej zagnieżdżonych list
                # wybieramy z niej liczby całkowite
                liczby = [x for x in obj if isinstance(x, int)]
                if liczby:
                    nowy = max(liczby) + 1
                else:
                    # pusta lista albo bez liczb -> zaczynamy od 1
                    nowy = 1
                obj.append(nowy)
            else:
                # schodzimy głębiej
                for x in obj:
                    dodaj_do_najglebszych(x, depth + 1)

        elif isinstance(obj, tuple):
            for x in obj:
                dodaj_do_najglebszych(x, depth + 1)

        elif isinstance(obj, dict):
            for v in obj.values():
                dodaj_do_najglebszych(v, depth + 1)
        else:   #JESLI NIE LISTA, NIE KROTKA, NIE SLOWNIK
            
            pass

    dodaj_do_najglebszych(wejscie, 0)
    return wejscie


if __name__ == '__main__':
    input_list = [
        1, 2, [3, 4, [5, {"klucz": [5, 6], "tekst": [1, 2]}], 5],
        "hello", 3, [4, 5], (5, (6, (1, [7, 8])))
    ]
    output_list = dodaj_element(input_list)
    print(input_list) 
