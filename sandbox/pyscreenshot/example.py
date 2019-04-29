# Снятие скриншота
# https://github.com/ponty/pyscreenshot
# pip install pyscreenshot
# pip install Pillow

import pyscreenshot as ImageGrab
# смещение можно получить в JS из объекта window:
# window.screenX, window.screenY

screenX = 852
screenY = 31

if __name__ == '__main__':
    # part of the screen
    im = ImageGrab.grab(bbox=(screenX + 75, screenY + 257, screenX + 725, screenY + 840))  # X1,Y1,X2,Y2
    im.save('screenshot.png')
    im.show()
