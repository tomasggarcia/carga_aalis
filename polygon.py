from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


aali_polygon = []

aali_point= (-57.650538,-25.268934)
if aali_point in aali_polygon:
    print('ok')
point = Point(aali_point)
polygon = Polygon(aali_polygon)
print(polygon.contains(point))