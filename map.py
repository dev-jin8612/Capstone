from capstone import openrouteservice as ops
import math


# ?먭뎄愿(8): 37.58335553489893, 127.00914144515993
# 怨듯븰愿(13): 37.581744341658116, 127.00977444648743
# ?곸긽愿(4): 37.582418156266044, 127.0102545619011

def calculate_angle_and_direction(coord1, coord2, coord3):
    """
    ??醫뚰몴瑜?諛쏆븘??媛곷룄? 諛⑺뼢??怨꾩궛?⑸땲??
    coord1: 泥?踰덉㎏ 醫뚰몴 [longitude, latitude]
    coord2: ??踰덉㎏ 醫뚰몴 [longitude, latitude]
    coord3: ??踰덉㎏ 醫뚰몴 [longitude, latitude]
    """

    def get_bearing(pointA, pointB):
        """
        ??醫뚰몴 媛꾩쓽 諛⑹쐞瑜?怨꾩궛?⑸땲??
        """
        lat1 = math.radians(pointA[1])
        lat2 = math.radians(pointB[1])
        diffLong = math.radians(pointB[0] - pointA[0])
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing

    bearing1 = get_bearing(coord1, coord2)
    bearing2 = get_bearing(coord2, coord3)
    angle = abs(bearing1 - bearing2)
    direction = "right" if (bearing2 - bearing1) % 360 < 180 else "left"
    if angle > 180:
        angle = 360 - angle
    return angle, direction


def calculate_distance(coord1, coord2):
    """
    ??醫뚰몴 ?ъ씠??嫄곕━瑜?怨꾩궛?⑸땲??
    coord1: 泥?踰덉㎏ 醫뚰몴 [longitude, latitude]
    coord2: ??踰덉㎏ 醫뚰몴 [longitude, latitude]
    """
    R = 6371000  # 吏援ъ쓽 諛섍꼍(誘명꽣)
    lat1, lon1 = math.radians(coord1[1]), math.radians(coord1[0])
    lat2, lon2 = math.radians(coord2[1]), math.radians(coord2[0])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


def mainAction(a):
    # OpenRouteService ?대씪?댁뼵??珥덇린??
    client = ops.Client(key='5b3ce3597851110001cf624831ab13f710ff41a28a34b16e336e9d0b')
    # print(a)
    # print(type(a))

    coordinates = None
    if a == "13":  # 상상관
        coordinates = [[127.01092243194581, 37.58233525826788], [127.0102545619011, 37.582418156266044]]
    elif a == "8":  # 탐구관
        coordinates = [[127.01092243194581, 37.58233525826788], [127.00961619615558, 37.58192501809774]]
    elif a == "4":  #
        #   print("back")
        coordinates = [[127.01092243194581, 37.58233525826788], [127.00914144515993, 37.58335553489893]]

    if coordinates is None:
        print(f"Invalid input: {a}")
        return []

    # 寃쎈줈 ?붿껌
    route = client.directions(
        coordinates=coordinates,
        profile='cycling-electric',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    # 寃쎈줈??紐⑤뱺 醫뚰몴 異붿텧
    route_coordinates = route['features'][0]['geometry']['coordinates']

    # 爰얠씠??遺遺꾩쓽 醫뚰몴 異붿텧 諛?異쒕젰
    significant_points = []
    for i in range(1, len(route_coordinates) - 1):
        angle, direction = calculate_angle_and_direction(route_coordinates[i - 1], route_coordinates[i],
                                                         route_coordinates[i + 1])
        distance = calculate_distance(route_coordinates[i], route_coordinates[i + 1])
        if angle > 15:
            significant_points.append((route_coordinates[i], angle, direction, distance))


    significant_points.append(coordinates[1])
    # route_coordinates[i], angle,direction,distance媛 諛섑솚?섍쾶 留뚮뱾湲?
    return significant_points
