import folium
import geopy
import time

# This is for easier work:
geostuff = geopy.geocoders.Nominatim()


# Functions:
def create_layer(layer_display_name, layers_list):
    """
    (str, list) -> None
    This function adds layer called layer_display_name to list of layers called layers_list.
    """
    layers_list.append(folium.FeatureGroup(name=layer_display_name))
    return None


def add_layers(layers_list, my_map):
    """
    (list, folium.folium.map) -> None
    This function adds all layers in list called layers_list to map called my_map.
    """
    for layer_1 in layers_list:
        my_map.add_child(layer_1)
    my_map.add_child(folium.LayerControl())
    return None


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
    if line_of_film[0] == "'":
        result_str = find_text_between_symbols(line_of_film, "'", "'")
    elif line_of_film[0] == '"':
        result_str = find_text_between_symbols(line_of_film, '"', '"')
    else:
        # Alternative version:
        result_str = ""
        index_1 = 0
        # Checking characters in line_of_film one by one:
        while line_of_film[index_1 + 1] != "(":
            result_str += line_of_film[index_1]
            index_1 += 1

    return result_str


def get_year():
    """
    (None) -> int
    This function gets year from user (must be typed using keyboard).
    """
    print("\nThis program creates map showing places where films where shot.")
    year_str = input("Enter year of film release, please: ")
    try:
        year_1 = eval(year_str)
        # Now I will check if entered value can be year:
        if type(year_1) == int and 1500 < year_1 < 2100:
            return year_1
        else:
            return get_year()
    except:
        return get_year()


def add_mark(popup_str, lat, lon, layers_list):
    """
    (str, float, float, list) -> None
    This function adds pointer with latitude lat and longitude lon,
    and popup popup_str to the map.
    """
    layers_list[0].add_child(folium.Marker(location=[lat, lon], popup=popup_str, icon=folium.Icon()))


def main_func():
    """
    (None) -> None
    This is main function of this module which creates a map.
    """
    year_1 = get_year()

    print("Reading file...")
    list_of_films = read_file("locations.list")

    print("Looking for films released in year " + str(year_1) + "...")
    list_of_films = leave_one_year(list_of_films, year_1)

    # Checking if there are films which were released in entered year:
    if len(list_of_films) == 0:
        print("No films were released in year " + str(year_1) + ". The map wasn't generated.")
        return None
    else:
        # Creating map:
        my_map = folium.Map(location=[49.817545, 24.023932], zoom_start=10, tiles="Mapbox Bright")

        # Creating layers:
        layers_list = []
        create_layer("Main layer", layers_list)
        create_layer("First empty layer", layers_list)
        create_layer("Second empty layer", layers_list)

        # Now I will remove dublicates from list_of_films:
        print("Removing dublicates...")
        len_1 = len(list_of_films)
        list_of_films = list(set(list_of_films))
        print("Removed " + str(len_1 - len(list_of_films)) + " dublicates;")
        print("Initial length of list of films was " + str(len_1))

        # Now adding places to the map:
        print("Adding places to the map...")
        for line_of_film in list_of_films:
            film_name = find_film_name(line_of_film)
            # Latitude and longitude:
            tuple_1 = get_location(line_of_film.split("\t")[-1])
            if tuple_1 is None:
                print("Wasn't able to find location of film '" + film_name + "'.")
                print("------------------------------------------------------------------------")
            else:
                lat = tuple_1[0]
                lon = tuple_1[1]
                add_mark('"' + film_name + '"', lat, lon, layers_list)
                print("Added a lcation of film '" + film_name + "'.")
                print("------------------------------------------------------------------------")

        # Adding layers to the map and saving it:
        add_layers(layers_list, my_map)
        my_map.save("Mykola_Stefaniv_film_locations_" + str(year_1) + ".html")

        print('Map "Mykola_Stefaniv_film_locations_"' + str(year_1) + '.html" was')
        print("successfully created!")

        return None


main_func()
