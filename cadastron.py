import requests
import math
from datetime import datetime
import settings
import shutil
import os
import sys
import webbrowser
import locale
import codecs
from collections import namedtuple
from jinja2 import Template

# Преобразование координат из метрической системы (которую выдает сервис Росеестра) в WGS-84
# Позаимствовано отсюда: https://github.com/rendrom/rosreestr2coord/blob/master/scripts/utils.py


def y2lat(y):
    return (2 * math.atan(math.exp(y / 6378137)) - math.pi / 2) / (math.pi / 180)


def x2lon(x):
    return x / (math.pi / 180.0) / 6378137.0


def xy2lonlat(x, y):
    return [x2lon(x), y2lat(y)]


def degrees2dms(coord):
    """
        Конвертация координаты, заданной в формате Градусы.ДробнаяЧасть, в формат градусы, минуты, секунды
        coord - координата в формате float
        Возвращает ответ в строковом формате
        Тест: degrees2dms(61.234567) Ответ 61°14ʹ4ʺ

    """
    degrees = int(coord)
    minutes = (coord - float(degrees)) * 60.0
    seconds = (minutes - int(minutes)) * 60.0
    return '{deg:02d}°{min:02d}ʹ{sec:02d}ʺ'.format(deg=degrees, min=int(minutes), sec=int(seconds))


def get_nomenclature(lat, lon):
    """
        Определение номенклатуры листа карты M1:200000 по координатам
        Параметры: lat, lon - широта и долгота в десятичном виде
        Возвращаемое значение: Строка вида O-41-25
    """
    letter_n = int(int(lat) / 4) + 1  # Номер ряда
    lat_north = letter_n * 4
    letter = chr(64 + letter_n)  # Преобразуем номер ряда в букву

    colonna = int(int(lon) / 6) + 31
    lon_west = (colonna - 31) * 6

    # В масштабе 1:200000 лист делится на 6x6 = 36 частей: через 40 сек по широте и через 1 градус по долготе
    col = int((lon - float(lon_west))) + 1

    row = int(((float(lat_north) - lat) * 3) / 2) + 1
    if row > 6:
        row = 6

    cell = 6 * (row - 1) + col
    return '{0}-{1}-{2}'.format(letter, colonna, cell)


def parse_cadaster(input_str):
    """
    Обрабатывает входной параметр - кадастровый номер, который может быть в традиционной форме (aa:bb:ccccccc:ee..)
    кроме того, он может быть с разделителями - пробелами либо вообще без разделителей
    Возвращает кадастровый номер в традиционной форме
    :type input_str: str
    """
    if input_str.find(':') > -1:      # Кадастровый номер задан в традиционном формате
        return input_str
    cn = ''.join(input_str.split())     # Удаляем пробелы, если они есть
    cadaster = '{}:{}:{}:{}'.format(cn[0:2], cn[2:4], cn[4:11], cn[11:])
    return cadaster


def parse_coords(input_str):
    """
    Обрабатывает входной параметр - координаты центра участка, которые могут быть заданы через пробел (lat lon)
    В качестве десятичного разделителя может быть точка или запятая
    Возвращает кортеж (lat, lon) в виде строк с десятичной точкой
    :type input_str: str
    """
    (lat, lon) = input_str.replace(',', '.').split()

    return lat, lon


def get_obj_id(cadaster):
    """
        Получить id участка по его кадастровому номеру
        obj_id - это кадастровый номер с убранными ведущими нулями
        Типичный кадастровый номер 66:06:0301012:102
        Для этого кадастрового номера id = 66:6:301012:102
        При успешном завершении возвращает id, при ошибке - пустую строку (False)
    """
    try:
        codes = cadaster.split(':')
        if len(codes) != 4:
            return False

        lst = [str(int(code)) for code in codes]  # При преобразовании строки в целое исчезают лидирующие нули
        obj_id = ':'.join(lst)

        return obj_id

    except ValueError as e:
        print(e)

    return False


def get_info(cadaster):
    """
        Выполним GET запрос к API Росеестра и получим данные об участке
        Функция возвращает именованный кортеж с полями:

        errmsg В случае ошибки сюда записывается сообщение об ошибке
        address
        coords
        lat
        lon
        nomenclature
        info
        ozi_info
        cadaster
        yandex_url
        yandex_url_static

    """
    Result = namedtuple('Result', 'errmsg address coords lat lon nomenclature info brief ozi_info cadaster yandex_url '
                                  'yandex_url_static')
    Result.info = ''
    Result.errmsg = ''
    Result.cadaster = cadaster

    obj_id = get_obj_id(cadaster)
    if not obj_id:
        Result.errmsg = 'Ошибка(опечатка) в кадастровом номере!'
        return Result
    url = 'http://pkk5.rosreestr.ru/api/features/1/' + obj_id

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()  # Проверим на ошибки HTTP
        data = r.json()
    except requests.exceptions.Timeout as e:
        Result.errmsg = 'Ошибка по тайм-ауту: `{}`'.format(e)
        return Result
    except requests.exceptions.HTTPError as e:
        Result.errmsg = 'Ошибка HTTP: `{}`'.format(e)
        return Result
    except requests.exceptions.RequestException as e:
        Result.errmsg = 'Ошибка запроса: `{}`'.format(e)
        return Result

    if data:
        try:
            feature = data.get('feature')
            if feature:
                if feature.get('attrs'):
                    attrs = feature['attrs']
                    Result.address = attrs['address']
                    if Result.address is None:
                        Result.address = 'Адрес не задан'
                else:
                    Result.address = ''

                center_x = feature['center']['x']
                center_y = feature['center']['y']
                lat = y2lat(center_y)
                lon = x2lon(center_x)
                lat_s = str(round(lat, 6))
                lon_s = str(round(lon, 6))
                Result.lat = lat_s
                Result.lon = lon_s

                Result.yandex_url = (
                    'https://yandex.ru/maps/?mode=search&text={latitude}%2C{longitude}'
                ).format(latitude=lat_s, longitude=lon_s)
                Result.yandex_url_static = (
                    'https://static-maps.yandex.ru/1.x/?pt={longitude},{latitude},comma&z=13&size=600,450&l=map'
                ).format(latitude=lat_s, longitude=lon_s)

                Result.nomenclature = get_nomenclature(lat, lon)
                Result.coords = '{0}\t{1}'.format(lat_s.replace('.', ','), lon_s.replace('.', ','))

                Result.info = (
                    'Кадастровый номер: {cad}\n'
                    'Адрес: {addr}\n'
                    'Координаты:\n{lat:9}\t{lon:9}\n{latdms} с.ш. {londms} в.д.\n'
                    'Лист М 1:200000 : {nomenclature}\n\n'
                    '{url}\n\n'
                    'file://d:/OziExplorer/data/CADASTER.txt\n'
                    'Datum,WGS 84\n'
                    'WP,D,{cad},{latp:9},{lonp:9},{day},{time},,D,N,-9999\n'
                ).format(addr=Result.address, lat=lat_s.replace('.', ','), latdms=degrees2dms(lat),
                         lon=lon_s.replace('.', ','), londms=degrees2dms(lon), nomenclature=get_nomenclature(lat, lon),
                         url=Result.yandex_url, day=datetime.now().strftime('%m/%d/%y'),
                         cad=cadaster, latp=lat_s, lonp=lon_s,
                         time=datetime.now().strftime('%H/%M/%S'))

                Result.brief = (
                    'Кадастровый номер: {cad}\n'
                    'Адрес: {addr}\n'
                    'Координаты: {lat:9} {lon:9}\n\n'
                    'Лист М 1:200000 : {nomenclature}\n'
                ).format(cad=cadaster, addr=Result.address, lat=lat_s.replace('.', ','),
                         lon=lon_s.replace('.', ','), nomenclature=get_nomenclature(lat, lon)
                         )

                Result.ozi_info = (
                    'Datum,WGS 84\n'
                    'WP,D,{cad},{latp:9},{lonp:9},{day},{time},,D,N,-9999\n'
                ).format(day=datetime.now().strftime('%m/%d/%y'),
                         cad=cadaster, latp=lat_s, lonp=lon_s,
                         time=datetime.now().strftime('%H/%M/%S'))

            else:
                Result.errmsg = 'Данных об участке нет'

        except Exception as err:
            Result.errmsg = 'Ошибка get_info(): {0}'.format(repr(err))

    return Result


def get_info_by_coords(lat, lon, address):
    """
        Получим данные об участке по координатам его центра
        Функция возвращает именованный кортеж с полями:

        errmsg В случае ошибки сюда записывается сообщение об ошибке
        address
        coords
        lat
        lon
        nomenclature
        info
        ozi_info
        cadaster
        yandex_url
        yandex_url_static

    """
    Result = namedtuple('Result', 'errmsg address coords lat lon nomenclature info brief ozi_info cadaster yandex_url '
                                  'yandex_url_static')
    Result.info = ''
    Result.errmsg = ''
    Result.cadaster = 'Не задан'
    Result.address = address
    Result.lat = lat
    Result.lon = lon
    lat_f = float(lat)
    lon_f = float(lon)

    Result.yandex_url = (
        'https://yandex.ru/maps/?mode=search&text={latitude}%2C{longitude}'
    ).format(latitude=lat, longitude=lon)
    Result.yandex_url_static = (
        'https://static-maps.yandex.ru/1.x/?pt={longitude},{latitude},comma&z=13&size=600,450&l=map'
    ).format(latitude=lat, longitude=lon)

    Result.nomenclature = get_nomenclature(lat_f, lon_f)
    Result.coords = '{0}\t{1}'.format(lat.replace('.', ','), lon.replace('.', ','))

    Result.info = (
        'Кадастровый номер: {cad}\n'
        'Адрес: {addr}\n'
        'Координаты:\n{lat:9}\t{lon:9}\n{latdms} с.ш. {londms} в.д.\n'
        'Лист М 1:200000 : {nomenclature}\n\n'
        '{url}\n\n'
        'file://d:/OziExplorer/data/CADASTER.txt\n'
        'Datum,WGS 84\n'
        'WP,D,{cad},{latp:9},{lonp:9},{day},{time},,D,N,-9999\n'
    ).format(addr=Result.address, lat=lat.replace('.', ','), latdms=degrees2dms(lat_f),
             lon=lon.replace('.', ','), londms=degrees2dms(lon_f), nomenclature=get_nomenclature(lat_f, lon_f),
             url=Result.yandex_url, day=datetime.now().strftime('%m/%d/%y'),
             cad=Result.cadaster, latp=lat, lonp=lon,
             time=datetime.now().strftime('%H/%M/%S'))

    Result.brief = (
        'Кадастровый номер: {cad}\n'
        'Адрес: {addr}\n'
        'Координаты: {lat:9} {lon:9}\n\n'
        'Лист М 1:200000 : {nomenclature}\n'
    ).format(cad=Result.cadaster, addr=Result.address, lat=lat.replace('.', ','),
                         lon=lon.replace('.', ','), nomenclature=Result.nomenclature)

    Result.ozi_info = (
        'Datum,WGS 84\n'
        'WP,D,{cad},{latp:9},{lonp:9},{day},{time},,D,N,-9999\n'
    ).format(day=datetime.now().strftime('%m/%d/%y'),
                cad=Result.cadaster, latp=lat, lonp=lon,
                time=datetime.now().strftime('%H/%M/%S'))

    return Result


def modify_tex_file(filename, address, cadaster, nomenclature, coords):
    """
        Заменим поля адреса участка, кадастрового номера и номенклатуры в шаблонном tex-файле на
        реальные
        Используется шаблонизатор Jinja2
    """

    # Словарь, содержащий ключи - имена переменных в tex шаблоне, которые заменяются на значения,
    # переданные в функцию
    # Например, строка \newcommand{\txtAddress}{{ ADDRESS }} заменяется на
    # \newcommand{\txtAddress}{Свердловская обл., р-н Каменский, СТ Россия}
    data = {
        'ADDRESS': '{' + address + '}',
        'CADASTER': '{' + cadaster + '}',
        'NOMENCLATURE': '{' + nomenclature + '}',
        'COORDINATES': '{' + coords + '}',
    }

    #  Прочитаем файл целиком
    try:
        with codecs.open(filename, 'r', 'utf-8') as input_file:
            template = Template(input_file.read())
        tex = template.render(**data)
    except IOError as e:
        print('*** Ошибка чтения файла', e, file=sys.stderr)
        return

    # А теперь запишем все в тот же файл :
    try:
        with codecs.open(filename, 'w', 'utf-8') as out_file:
            out_file.write(tex)
    except IOError as e:
        print('*** Ошибка записи файла', e, file=sys.stderr)

    return


def make_ozi_file(filename, content):
    """
    Запишем координаты в файл Ozi Explorer Waypoints
    filename - полный путь к файлу
    """
    try:
        with open(filename, 'w') as out_file:
            out_file.write(content)
            print('>>> Создаем файл Ozi Waypoints ', filename)
    except IOError as e:
        print('*** Ошибка записи в файл {0}: {1} '.format(filename, e), file=sys.stderr)


def gen_report_folder(addr):
    """
    # Сгенерировать имя папки по шаблону: Адрес Месяц Год
    addr - адрес
    Возвращает сгенерированную строку
    """
    locale.setlocale(locale.LC_ALL, "")  # Чтобы дата и время выдавались в текущей локали
    return '{0} {1}'.format(addr.replace('\"', ''), datetime.now().strftime('%B %Y'))


def copy_report_folder(src, dst):
    """
    # Копируем папку с шаблоном отчета в папку с изысканиями
    src - полный путь к папке с шаблонами отчета
    dst - полный путь к папке c отчетами по изысканиям
    """
    retval = ''
    try:
        print('>>> Копируем шаблон отчета в папку: {0}'.format(dst))
        shutil.copytree(src, dst)
        print('>>> Шаблон скопирован.')
    except IOError as e:
        retval = '*** Ошибка копирования: {0}'.format(e)
    return retval

#######################################################################################################################
#
#                                                    M A I N
#
#######################################################################################################################
if __name__ == '__main__':
    # input_txt = '66:06:4501021:005728'
    # input_txt = '66 06 4501021 005728'
    # input_txt = '6666010102358'
    input_txt = input('Введите кадастровый номер : ')
    cadaster = parse_cadaster(input_txt)
    print('===========================================================================================================')
    print('Кадастровый номер ---> {}'.format(cadaster))

    area = get_info(cadaster)   # получим именованный кортеж area
    if area.errmsg:  # Была ошибка
        print('*** ОШИБКА *** ', area.errmsg, file=sys.stderr)
        exit(1)

    print(area.info)
#    print(area.brief)
    print('===========================================================================================================')

    # Запишем координаты в файл Ozi Explorer Waypoints
    make_ozi_file(settings.OZI_WAYPOINTS_FILE, area.ozi_info)

    locale.setlocale(locale.LC_ALL, "")  # Чтобы дата и время выдавались в текущей локали

    address = area.address
    nomenclature = area.nomenclature
    coords = area.coords

    dst_folder = gen_report_folder(area.address)

    # Копируем папку с шаблоном отчета в папку с изысканиями
    dst_path = os.path.join(settings.REPORTS_PATH, dst_folder)
    # print('>>> Копируем шаблон отчета в папку', dst_path)
    err = copy_report_folder(settings.TEX_TEMPLATE_PATH, dst_path)
    if err:
        print(err, file=sys.stderr)
        exit(-1)
    else:
        print('>>> Шаблон скопирован')

    # Заменим в файле шаблона water.tex адрес, кад. номер и номенклатуру на реальные
    filename = os.path.join(dst_path, settings.TEX_TEMPLATE_FILE)
    modify_tex_file(filename, address, cadaster, nomenclature, coords)

    # Откроем проводник в папке назначения
    webbrowser.open(dst_path)
