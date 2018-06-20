import settings

print(settings.OZI_WAYPOINTS_FILE)
try:
    with open(settings.OZI_WAYPOINTS_FILE, 'w') as output:
        output.write('Test1')
except IOError as e:
    print('Ошибка записи в файл {0}: {1} '.format(settings.OZI_WAYPOINTS_FILE, e.strerror))

