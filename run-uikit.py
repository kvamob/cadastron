import eel
import settings
import os
import webbrowser
import logging

import cadastron
import app


web_location = 'web'
web_dir = os.path.dirname(os.path.realpath(__file__))
web_path = os.path.join(web_dir, web_location)
print('web_path : ', web_path)
eel.init(web_path)                  # Give folder containing web files

area = tuple()

logging.basicConfig(
    handlers=[logging.FileHandler('cadastron.log', 'a', 'utf-8')],
    # level=logging.INFO,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%d-%m-%Y %I:%M:%S'
)


@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)


@eel.expose                         # Expose this function to Javascript
def load_info(x):
    print(f'Введенный кад. номер: {x}')
    logging.debug(f'Введенный кад. номер: {x}')
    cadno = cadastron.parse_cadaster(x)
    global area
    eel.print_to_textarea_js('Идет поиск...')
    eel.turn_spinner_js('1') # Запустим спиннер на кнопке Старт

    area = cadastron.get_info(cadno)

    if not area.errmsg:
        # eel.print_to_textarea_js(area.brief)
        eel.print_to_textarea_js(area.info)
        logging.info(area.info)
        eel.print_to_url_js(area.yandex_url)
        eel.enable_btn_yandex_js()
        eel.enable_btn_create_js()
        eel.print_to_input_report_js(cadastron.gen_report_folder(area.address))
        eel.print_to_input_bhpassport_js(cadastron.gen_bhpassport_folder(area.address))
        cadastron.make_ozi_file(settings.OZI_WAYPOINTS_FILE, area.ozi_info)
        eel.addOutput('>>> Создаем файл Ozi Waypoints\n')
        eel.setYmapPosition_js(area.lat, area.lon, 12, area.cadaster)
        eel.set_ymap_src_js(area.yandex_url_static)
        eel.setGeoMapPosition_js(area.lat, area.lon)
        eel.setOSMMapPosition_js(area.lat, area.lon)
        eel.print_nomenclature_js('Лист ' + area.nomenclature)

        eel.addOutput('>>> Latitude  : {0}\n'.format(area.lat))
        eel.addOutput('>>> Longitude : {0}\n'.format(area.lon))

    else:
        eel.print_to_textarea_js(area.errmsg)
        logging.debug(area.errmsg)
 
    eel.turn_spinner_js('0')  # Остановим спиннер на кнопке Старт


@eel.expose                         # Expose this function to Javascript
def load_info_by_coords(coords, address):
    global area
    print(f'Входная строка 1(координаты) {coords}')
    logging.debug(f'Входная строка 1(координаты) {coords}')
    print(f'Входная строка 2 {address}')
    logging.debug(f'Входная строка 2 {address}')
    (lat, lon) = cadastron.parse_coords(coords)
    print(f'Lat {lat} Lon {lon}')
    logging.debug(f'Lat {lat} Lon {lon}')

    eel.print_to_textarea_js('Получение информации по координатам...')
    logging.debug('Получение информации по координатам...')

    area = cadastron.get_info_by_coords(lat, lon, address)

    if not area.errmsg:
        # eel.print_to_textarea_js(area.brief)
        eel.print_to_textarea_js(area.info)
        logging.debug(area.info)
        eel.print_to_url_js(area.yandex_url)
        eel.enable_btn_yandex_js()
        eel.enable_btn_create_js()
        eel.print_to_input_report_js(cadastron.gen_report_folder(area.address))
        eel.print_to_input_bhpassport_js(cadastron.gen_bhpassport_folder(area.address))
        cadastron.make_ozi_file(settings.OZI_WAYPOINTS_FILE, area.ozi_info)
        eel.addOutput('>>> Создаем файл Ozi Waypoints\n')
        eel.setYmapPosition_js(area.lat, area.lon, 12, '')
        eel.set_ymap_src_js(area.yandex_url_static)
        eel.setGeoMapPosition_js(area.lat, area.lon)
        eel.setOSMMapPosition_js(area.lat, area.lon)
        eel.print_nomenclature_js('Лист ' + area.nomenclature)

        eel.addOutput(f'>>> Latitude  : {area.lat}\n')
        eel.addOutput(f'>>> Longitude : {area.lon}\n')

    else:
        eel.print_to_textarea_js(area.errmsg)
        logging.debug(area.errmsg)


@eel.expose                         # Expose this function to Javascript
def create_report(folder, addr):
    global area

    if addr:
        area.address = addr

    print(f'Адрес:{area.address}')
    logging.debug(f'Адрес:{area.address}')
    print(f'Папка с отчетом:{folder}')
    logging.debug(f'Папка с отчетом:{folder}')

    # Копируем папку с шаблоном отчета в папку с изысканиями
    dst_path = os.path.join(settings.REPORTS_PATH, folder)
    print(f'Путь к папке с отчетом:{dst_path}')
    eel.addOutput(f'>>> Копируем шаблон отчета в папку {dst_path}\n')
    err = cadastron.copy_template_folder(settings.TEX_TEMPLATE_PATH, dst_path)
    if not err:
        eel.addOutput('>>> Шаблон скопирован\n')

        # Заменим в файле шаблона water.tex адрес, кад. номер и номенклатуру на реальные
        fname = os.path.join(dst_path, settings.TEX_TEMPLATE_FILE)
        cadastron.modify_tex_file(fname, area.address, area.cadaster, area.nomenclature, area.coords)

        # Откроем проводник в папке назначения
        webbrowser.open(dst_path)
    else:
        eel.addOutput(f'*** Ошибка копирования: {err}\n')
        logging.debug(f'*** Ошибка копирования: {err}\n')


@eel.expose                         # Expose this function to Javascript
def create_bhpassport(folder):
    global area
    print(f'Адрес:{area.address}')
    logging.debug(f'Адрес:{area.address}')
    print(f'Папка с паспортом:{folder}')
    logging.debug(f'Папка с паспортом:{folder}')

    # Копируем папку с шаблоном отчета в папку с изысканиями
    dst_path = os.path.join(settings.BHPASSPORTS_PATH, folder)
    print(f'Путь к папке с отчетом:{dst_path}')
    logging.debug(f'Путь к папке с отчетом:{dst_path}')
    eel.addOutput(f'>>> Копируем шаблон отчета в папку {dst_path}\n')
    err = cadastron.copy_template_folder(settings.TEX_BH_TEMPLATE_PATH, dst_path)
    if not err:
        eel.addOutput('>>> Шаблон скопирован\n')

        # Заменим в файле шаблона bhpassport.tex адрес, кад. номер и номенклатуру на реальные
        fname = os.path.join(dst_path, settings.TEX_BH_TEMPLATE_FILE)
        cadastron.modify_tex_file(fname, area.address, area.cadaster, area.nomenclature, area.coords)

        # Откроем проводник в папке назначения
        webbrowser.open(dst_path)
    else:
        eel.addOutput(f'*** Ошибка копирования: {err}\n')
        logging.debug(f'*** Ошибка копирования: {err}\n')


eel.print_build_js(f'v {app.version} Build: {app.build}')     # Call a Javascript function
logging.info(f'******************** Starting Cadastron v{app.version} Build: {app.build} ********************')
eel.say_hello_js('connected!')   # Call a Javascript function
eel.print_to_textarea_js('')     # Call a Javascript function

eel.start('main-uikit.html', size=(800, 1000))    # Start
