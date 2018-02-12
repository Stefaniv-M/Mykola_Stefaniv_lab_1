import folium

my_map = folium.Map(location=[49.817545, 24.023932], zoom_start=17, tiles="Mapbox Bright")

# This is list of layers of the map:
layers_list = []


def create_layer(layer_display_name, layers_list):
    """
    (str, list) -> None
    This function adds layer called layer_display_name to list of layers called layers_list
    """
    layers_list.append(folium.FeatureGroup(name=layer_display_name))
    return None


def add_layers(layers_list, my_map):
    """
    (list, folium.folium.map) -> None
    This function adds all layers in layers_list list and folium.LayerControl() to map called my_map.
    """
    for layer_1 in layers_list:
        my_map.add_child(layer_1)
    my_map.add_child(folium.LayerControl())
    return None


# Creating four layers:
for text_str in ["First (Main) Layer", "Second Layer", "Third Layer", "Fourth Layer"]:
    create_layer(text_str, layers_list)

layers_list[0].add_child(folium.Marker(location=[49, 24], popup="​1900 рік ", icon=folium.Icon()))
layers_list[1].add_child(folium.Marker(location=[50, 25], popup="​1902 рік ", icon=folium.Icon()))

add_layers(layers_list, my_map)

my_map.save("Map_1.html")