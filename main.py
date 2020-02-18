from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
geolocator = Nominatim(user_agent="main.py")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def read_file(file, year):
    """
    (str, str) -> dict
    This function returns the dictionary where the key is a location,
    and by the key user can get the list of movies
    that were shot at that location that year.

    Function example:
    {'Riverdale Collegiate Institute, Toronto, Ontario, Canada':
    ['1-800-Missing'], 'Toronto, Ontario, Canada':
    ['1-800-Missing', '72 Hours: True Crime', '>Play',
    "America's Next Top Model", ...
    """
    locations = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip().split("\t")
            if year in line[0]:
                line1 = line[0].split('"')
                if len(line1) > 1:
                    film_name = line1[1]
                    if line[-1].startswith("("):
                        if line[-2] not in locations:
                            locations[line[-2]] = []
                        if film_name not in locations[line[-2]]:
                            locations[line[-2]].append(film_name)
                    else:
                        if line[-1] not in locations:
                            locations[line[-1]] = []
                        if film_name not in locations[line[-1]]:
                            locations[line[-1]].append(film_name)
    return locations


def location_of_input(latitude, longitude):
    """
    (str, str) -> list
    This function returns the list of the words
    of the location entered by user.

    >>> location_of_input('43.6502652', '-79.9036058')[:2]
    ['199', ' Guelph Street']
    """
    coord = latitude + ", " + longitude
    location = geolocator.reverse(coord, language='en')
    country = location.address.split(",")
    return country


def find_coordinates(locations, latitude, longitude):
    """
    (dict, str, str) -> dict
    This function returns the dictionary
    where the keys are latitude and longitude of the location,
    and by keys user can get the list of the movies
    that were shot at that location that year.

    >>> locations = {'Hampton, South Carolina, USA': ['Anderson Cooper 360°']}
    >>> find_coordinates(locations, '32.4048602', '-81.0414726')
    {(32.7861789, -81.1237271): ['Anderson Cooper 360°']}

    >>> locations = {'Berlin, Germany': ['Small World']}
    >>> find_coordinates(locations, '51.0493286', '13.7381437')
    {(52.5170365, 13.3888599): ['Small World']}
    """
    new_locations = {}
    counter = 0
    my_country = location_of_input(latitude, longitude)[-1].strip()
    for i in locations:

        if counter < 240:
            this_country = i.split(",")[-1].strip()
            if my_country == 'United States of America':
                my_country = 'USA'
            if this_country == 'United Kingdom':
                this_country = 'UK'

            if this_country == my_country:
                counter += 1
                try:
                    location = geolocator.geocode(i, timeout=3)
                    new_locations[(location.latitude, location.longitude)] \
                        = locations[i]
                except Exception:
                    continue

        else:
            break
    return new_locations


def find_distance(new_locations, latitude, longitude):
    """
    (dict, str, str) -> dict
    This function returns the dictionary
    where the keys are latitude and longitude of the location,
    that has the smallest distance from this location
    to the location specified by the user.
    By keys user can get the list of the movies
    that were shot at that location that year.

    >>> new_locations = {(32.7861789, -81.1237271): ['Anderson Cooper 360°']}
    >>> find_distance(new_locations, '51.0493286', '13.7381437')
    {(32.7861789, -81.1237271): ['Anderson Cooper 360°']}

    >>> new_locations = {(52.5170365, 13.3888599): ['Small World']}
    >>> find_distance(new_locations, '51.0493286', '13.7381437')
    {(52.5170365, 13.3888599): ['Small World']}
    """
    my_location = (float(latitude), float(longitude))
    distances = {}
    for loc in new_locations:
        l1, l2 = loc
        this_location = (l1, l2)
        distance = great_circle(my_location, this_location)
        distance = str(distance)
        distances[float(distance[:-3])] = [loc, new_locations[loc]]

    min_distances = {}
    new_distances = []
    for i in distances:
        new_distances.append(i)

    while (len(min_distances) != 10) and new_distances != []:
        min_dist = new_distances[0]
        for i in new_distances:
            if i > min_dist:
                max_dist = i
        min_distances[distances[min_dist][0]] = distances[min_dist][1]
        new_distances.remove(min_dist)

    return min_distances


def result_dictionary(max_distances):
    """
    (dict) -> dict
    This function returns the dictionary
    where the keys are 'lat', 'lon' and 'film'.
    By keys user can get list where items with the same ordinal number
    match one movie (in 'lat' - the latitude of the location
    where this film was shot, in 'lon' - the longitude,
    in 'film' - the name of movie.

    >>> max_distances = {(32.7861789, -81.1237271): ['Anderson Cooper 360°']}
    >>> result_dictionary(max_distances)['lat']
    [32.7861789]

    >>> max_distances = {(52.5170365, 13.3888599): ['Small World']}
    >>> result_dictionary(max_distances)
    {'lat': [52.5170365], 'lon': [13.3888599], 'film': ['Small World']}
    """
    latitude = []
    longitude = []
    films = []
    result_dict = {}

    for i in max_distances:
        lat, lon = i
        film_name = max_distances[i]
        film_name_1 = ''
        if type(film_name) == list:
            for i in film_name:
                film_name_1 += i + ", "
            film_name_1 = film_name_1[:-2]
        else:
            film_name_1 = film_name
        latitude.append(lat)
        longitude.append(lon)
        films.append(film_name_1)

    result_dict['lat'] = latitude
    result_dict['lon'] = longitude
    result_dict['film'] = films

    return result_dict


def color_creator(country):
    """
    (str) -> str
    This function takes the name of the country
    and returns the name of the color
    in which the country label will be painted.

    >>> color_creator('1 - United States of America')
    'green'
    >>> color_creator('4 - United Kingdom')
    'blue'
    >>> color_creator('5 - India')
    'pink'
    """
    if country == '1 - United States of America':
        return "green"
    elif country == '2- China':
        return "yellow"
    elif country == '3 - Japan':
        return "red"
    elif country == '4 - United Kingdom':
        return "blue"
    else:
        return "pink"


def web_map(result_dict, my_lat, my_lon):
    """
    (dict, str, str) ->
    This function generates a web map (html page)
    by using module folium.
    """
    lat = result_dict['lat']
    lon = result_dict['lon']
    film = result_dict['film']

    map = folium.Map(location=[my_lat, my_lon],
                     zoom_start=2)

    fg_1 = folium.FeatureGroup(name='Films on this year near your location')

    for lt, ln, fl in zip(lat, lon, film):
        fg_1.add_child(folium.Marker(location=[lt, ln], radius=10, popup=fl))

    lat_1 = []
    lon_1 = []
    geolocator = Nominatim(user_agent="main.py")
    countries = ['1 - United States of America', '2- China', '3 - Japan',
                 '4 - United Kingdom', '5 - India']
    for country in countries:
        location = geolocator.geocode(country.split("-")[1][1:])
        lat_1.append(location.latitude)
        lon_1.append(location.longitude)

    fg_2 = folium.FeatureGroup(name="Top 5 leading film markets worldwide "
                                    "in 2018")

    for lt, ln, coun in zip(lat_1, lon_1, countries):
        fg_2.add_child(folium.CircleMarker(location=[lt, ln], radius=10,
                                           popup=coun,
                                           fill_color=color_creator(coun),
                                           color='red',
                                           fill_opacity=0.5))

    map.add_child(fg_1)
    map.add_child(fg_2)
    map.add_child(folium.LayerControl())
    map.save('movies_map.html')


if __name__ == '__main__':
    print("Please enter a year you would like to have a map for: ")
    year = input()
    print("Please enter your location (format: lat, long): ")
    loc = input()

    print("Map is generating...")
    print("Please wait...")
    latitude = loc.split(",")[0]
    longitude = loc.split(",")[1]
    locations = find_coordinates(read_file("locations.list", year), latitude,
                                 longitude)
    max_distances = find_distance(locations, latitude, longitude)
    result_dict = result_dictionary(max_distances)
    web_map(result_dict, latitude, longitude)
    print("Finished. Please have look at the map movies_map.html")
