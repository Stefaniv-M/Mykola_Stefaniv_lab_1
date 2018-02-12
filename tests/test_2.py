import geopy


# This is for easier work:
geostuff = geopy.geocoders.Nominatim()


def get_location(location_name):
    """
    (str) -> (float, float) or None
    This function returns location of film. Arguement is a
    last element of <line_in_list_file>.split("\t")[-1]. If
    function can find latitude and longitude of place, it returns
    those values, otherwise it will try to find address of last
    word of location. If it fails even it, the function returns None.
    """
    try:
        location_1 = geostuff.geocode(location_name)
        return location_1.latitude, location_1.longitude
    except:
        try:
            # If geopy can't find place by it's full address, it will search the last word:
            location_1 = geostuff.geocode(location_name.split(" ")[-1])
            return location_1.latitude, location_1.longitude
        except:
            return None


def read_file(file_name):
    """
    (str) -> list
    This function reads file file_name and returns list of lines of the file.
    """
    file_1 = open(file_name)
    result_list = file_1.readlines()
    file_1.close()
    return result_list


def find_year(line_of_film):
    """
    (str) -> int or None
    This function returns year of film that is in line of list file, or it returns zero if
    there is no film in this line.
    """
    year_1 = find_text_between_symbols(line_of_film, "(", ")")

    if year_1 is None:
        return None
    else:
        try:
            year_1 = eval(year_1)
            return year_1
        except:
            return None


def find_text_between_symbols(text_line, symb_1, symb_2):
    """
    (str, char) -> str
    This function returns text in text_line between symb_1 and symb_2.

    >>> find_text_between_symbols("Helloars tsatne atsne (sarten1)tn tnsra", "(", ")")
    'sarten1'
    """
    # This will be switched if symbol_1 in for cycle will be character between symbols:
    switch_1 = False
    # This is in case of equal symbols:
    switch_2 = True

    # This will be string with symbols:
    result_str = ""

    for symbol_1 in text_line:
        if symbol_1 == symb_1 and switch_2:
            switch_1 = True
            switch_2 = False
        elif symbol_1 == symb_2:
            switch_1 = False
        else:
            if switch_1 is True:
                result_str += symbol_1

    if result_str != "":
        return result_str
    else:
        return None


def leave_one_year(list_of_films, year_1):
    """
    (list, int) -> list
    This function returns only lines with those films, year of which was year_1.
    """
    result_list = []
    for line_1 in list_of_films:
        if find_year(line_1) == year_1:
            result_list.append(line_1)
    return result_list


def find_film_name(line_of_film):
    """
    (str) -> str
    This function returns name of film from line with it. If there is no name of film,
    the function will return None.
    """
    result_str = find_text_between_symbols(line_of_film, "'", "'")
    if result_str is None:
        result_str = find_text_between_symbols(line_of_film, '"', '"')

    if result_str is None:
        # Alternative version:
        result_str = ""
        index_1 = 0
        # Checking characters in line_of_film one by one:
        while line_of_film[index_1 + 1] != "(":
            result_str += line_of_film[index_1]
            index_1 += 1

    return result_str


list_1 = read_file("locations.list")
list_year = leave_one_year(list_1, 1985)

print(list_year)
