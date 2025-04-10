from math import radians, sin, atan2, sqrt, cos


def distance_km(self):
    def parse_coordinates(coord_str):
        try:
            lat, lon = map(float, coord_str.split(','))
            return lat, lon
        except (ValueError, AttributeError):
            return None, None

    dep_lat, dep_lon = parse_coordinates(self.departure_airport.coordinates)
    arr_lat, arr_lon = parse_coordinates(self.arrival_airport.coordinates)

    if None in (dep_lat, dep_lon, arr_lat, arr_lon):
        return None

    lat1 = radians(dep_lat)
    lon1 = radians(dep_lon)
    lat2 = radians(arr_lat)
    lon2 = radians(arr_lon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = 6371 * c

    return round(distance, 2)
