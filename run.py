import eel
import settings
import os
import webbrowser
import cadastron


web_location = 'web'
web_path = os.path.dirname(os.path.realpath(__file__)) + '\\' + web_location
eel.init(web_path)                  # Give folder containing web files

# eel.init('web')                     # Give folder containing web files

area = tuple()


@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)


@eel.expose                         # Expose this function to Javascript
def load_info(x):
    print('Входная строка %s' % x)
    cadno = cadastron.parse_cadaster(x)
    global area
    eel.print_to_textarea_js('Идет поиск...')
    area = cadastron.get_info(cadno)
    if not area.errmsg:
        # eel.print_to_textarea_js(area.brief)
        eel.print_to_textarea_js(area.info)
        eel.print_to_url_js(area.yandex_url)
        eel.enable_btn_yandex_js()
        eel.enable_btn_create_js()
        eel.print_to_input_report_js(cadastron.gen_report_folder(area.address))
        cadastron.make_ozi_file(settings.OZI_WAYPOINTS_FILE, area.ozi_info)
        eel.addOutput('>>> Создаем файл Ozi Waypoints\n')
        eel.setYmapPosition_js(area.lat, area.lon, 13, area.cadaster)
        eel.set_ymap_src_js(area.yandex_url_static)
        eel.print_nomenclature_js('Лист ' + area.nomenclature)
    else:
        eel.print_to_textarea_js(area.errmsg)


@eel.expose                         # Expose this function to Javascript
def create_report(folder):
    global area
    print('Адрес:', area.address)
    print('Папка с отчетом:', folder)

    # Копируем папку с шаблоном отчета в папку с изысканиями
    dst_path = os.path.join(settings.REPORTS_PATH, folder)
    print('Путь к папке с отчетом:', dst_path)
    eel.addOutput('>>> Копируем шаблон отчета в папку {0}\n'.format(dst_path))
    err = cadastron.copy_report_folder(settings.TEX_TEMPLATE_PATH, dst_path)
    if not err:
        eel.addOutput('>>> Шаблон скопирован\n')

        # Заменим в файле шаблона water.tex адрес, кад. номер и номенклатуру на реальные
        fname = os.path.join(dst_path, settings.TEX_TEMPLATE_FILE)
        cadastron.modify_tex_file(fname, area.address, area.cadaster, area.nomenclature, area.coords)

        # Откроем проводник в папке назначения
        webbrowser.open(dst_path)
    else:
        eel.addOutput('*** Ошибка копирования: {0}\n'.format(err))


eel.say_hello_js('connected!')   # Call a Javascript function
eel.print_to_textarea_js('')     # Call a Javascript function

eel.start('main.html', size=(800, 900))    # Start
