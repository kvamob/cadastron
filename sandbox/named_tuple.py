from collections import namedtuple


def get_info():
    Result = namedtuple('Result', 'info ozi')
#    rv = Retvals('Info1', 'OZi')
    Result.info = '>>>>>>> Info---------'
    Result.ozi = '>>>>>>> Ozi'

    return Result


vv = get_info()
print(vv.info)
print(vv.ozi)

