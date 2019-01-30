<h1 align="center">Cadastron</h1>
<p align="center">Получение информации по участку по его кадастровому номеру либо координатам, создание отчета по изысканиям из шаблона, создание паспорта скважины из шаблона. GUI основан на Python пакете <a href="https://github.com/ChrisKnott/Eel">Eel</a></p>
<p align="center">Идею GUI подсмотрел в проекте <a href="https://github.com/brentvollebregt/auto-py-to-exe/"><strong> Auto PY to EXE </strong></a></p>
<p align="center">Также пользовался описанием Eel из статьи <a href="http://nitratine.net/python-gui-using-chrome/"><strong> Python GUI Using Chrome </strong></a></p>

<!-- <div align="center">
    <img src="https://i.imgur.com/EuUlayC.png" alt="Empty interface">
</div> -->

# Getting Started

## Требования к системе

    - Python : Python 3.3+
    - Chrome : библиотека Eel использует Chrome в режиме приложения

## Установка

- Клонировать/скачать этот репозиторий
- Если в системе не установлен Chrome, установить его
- Открыть ```cmd/terminal``` и перейти в папку с проектом
- В папку ```web/geomap``` скопровать тайлы геологической карты (лежат тут: ```D:\Home System\РАЗНОЕ\Государственная геологическая карта РФ Урал\Сводная карта Урала - тайлы\geomap```) (Если используется внешний веб-сервер, то тайлы копировать не надо)!
- Установить локальный веб-сервер (IIS), с домашним каталогом ```web/geomap``` 
( В настоящее время локальный веб-сервер не используется, тайлы геокарты лежат здесь: http://ex1c.delrus.ru/geomap/{z}/{x}/{y}.png). Этот URL присваивается переменной `urlTemplate` в файле `web/js/script.js`
- Если не установлен пакет `pyvenv`, поставим его: `$ sudo apt install -y python3-venv` (под Windows можно так: `pip3 install virtualenv`)
- `$ pyvenv venv` создаем виртуальное окружение python3 (под Windows: `> virtualenv venv` )
- `$ source venv/bin/activate` Активируем виртуальное окружение (под Windows: `> venv\Scripts\activate`)
- `(venv) $ pip3 install -r requirements.txt` Устанавливаем необходимые пакеты и библиотеки в виртуальное окружение
- При необходимости изменить настройки в файле ```settings.py```
- Скопировать файл ```hooks/pre-commit``` в папку ```.git/hooks```. Это скрипт, автоматически меняющий номер версии и дату сборки проекта в файле ```app/__init__.py``` перед каждым коммитом

## Запуск

- Активировать виртуальное окружение ```venv\Scripts\Activate```

- Запустить приложение: ```python run.py```

- Можно создать файл cadastron.cmd и запускать его:

#### Файл cadastron.cmd
    cd d:
    cd \GIT-REPOS\cadastron
    call venv\Scripts\Activate
    python run.py

- **Chrome** запустится в режиме приложения с этим проектом внутри.

## TODO

- ~Добавить входной параметр - координаты участка~

## Something is Wrong?

    There could be a chance that you were using an old version and I have changed something and your cache is now a mess. Press Shift+F5 in the chrome app to force reload everything.

If this doesn't work please report it and I will look into it!

## Screenshots

![Start screen](screenshots/screenshot1.png "Start screen")

![Map1 tab](screenshots/screenshot2.png "Yandex Map tab")

![Map2 tab](screenshots/screenshot3.png "Yandex image tab")

![Map2 tab](screenshots/screenshot4.png "Geology tab")


