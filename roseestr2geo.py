import math

# Преобразование координат из метрической системы (которую выдает сервис Росеестра) в WGS-84
# Позаимствовано отсюда: https://github.com/rendrom/rosreestr2coord/blob/master/scripts/utils.py


def y2lat(y):
    return (2 * math.atan(math.exp(y / 6378137)) - math.pi / 2) / (math.pi / 180)


def x2lon(x):
    return x / (math.pi / 180.0) / 6378137.0


def xy2lonlat(x, y):
    return [x2lon(x), y2lat(y)]


# y = 386862.64
# x = 1525064.15

x = 6729270.25
y = 7720481.91

print(xy2lonlat(x, y))
