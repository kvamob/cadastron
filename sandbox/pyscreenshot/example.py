# Снятие скриншота
# https://github.com/ponty/pyscreenshot
# pip install pyscreenshot
# pip install Pillow

import pyscreenshot as ImageGrab

if __name__ == '__main__':
    # part of the screen
    im = ImageGrab.grab(bbox=(75, 257, 725, 840))  # X1,Y1,X2,Y2
    im.save('screenshot.png')
    im.show()
