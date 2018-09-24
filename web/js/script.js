$(function() {

  // Эти функции вызываются из Python
  eel.expose(say_hello_js); // Expose this function to Python
  function say_hello_js(x) {
    console.log('Hello from ' + x);
  }

  eel.expose(print_to_textarea_js); // Expose this function to Python
  function print_to_textarea_js(x) {
    $('#output').val(x);
  }

  // Execution output
  eel.expose(addOutput);
  function addOutput(line) {
    $('#output_console').append(line);
  }

  eel.expose(print_to_input_report_js); // Expose this function to Python
  function print_to_input_report_js(x) {
    $('#dst_folder').val(x);
  }

  eel.expose(print_to_url_js); // Expose this function to Python
  function print_to_url_js(x) {
    $('#url_yandex').prop('href', x);
  }

  eel.expose(print_nomenclature_js); // Expose this function to Python
  function print_nomenclature_js(x) {
    console.log(x);
    $('#nomenclature').text(x);
  }

  eel.expose(set_ymap_src_js); // Expose this function to Python
  function set_ymap_src_js(x) {
    $('#img_map').attr('src', x);
  }

  // У кнопки "Yandex Maps" убрать класс disabled
  eel.expose(enable_btn_yandex_js); // Expose this function to Python
  function enable_btn_yandex_js() {
    $('#url_yandex').removeClass('disabled');
  }

  // У кнопки "Создать отчет" убрать атрибут disabled
  eel.expose(enable_btn_create_js); // Expose this function to Python
  function enable_btn_create_js() {
    $('#btn_create').removeAttr('disabled');
  }

  //
  //
  //
  say_hello_js('Javascript World!');
  eel.handleinput('connected!'); // Call a Python function

  // ДЛЯ ОТЛАДКИ ЗАДАДИМ НАЧАЛЬНОЕ ЗНАЧЕНИЕ
  $('#inp_cadaster').val('74090607001634');
  addOutput('');
  $('#nomenclature').val('Лист O-41-25');


  // ---------------- Yandex Maps ----------------------------------------------------
  ymaps.ready(init);

  var myMap,
    myPlacemark;

  var lat = 56.842004;
  var lon = 60.553123;
  var geomap;
  var address;

  function init() {

    myMap = new ymaps.Map('map', {
      center: [lat, lon],
      zoom: 12
    });
    // Удалим лишние контролы с карты
    myMap.controls.remove('zoomControl');
//    myMap.controls.remove('rulerControl');
    myMap.controls.remove('typeSelector');
    myMap.controls.remove('fullscreenControl');
    myMap.controls.remove('geolocationControl');
    myMap.controls.remove('routeButtonControl');
    myMap.controls.remove('trafficControl');
    myMap.controls.remove('searchControl');
    // myMap.controls.remove('');

    myPlacemark = new ymaps.Placemark([lat, lon], {
      hintContent: 'Екатеринбург',
      balloonContent: 'Столица Урала'
    });

    myMap.geoObjects.add(myPlacemark);

  }

  // ------- Leaflet.js --------------------------------------------------------------
  var mapExtent = [57.52479930, 55.89930842, 62.99872460, 59.39520320];
  var mapMinZoom = 10;
  var mapMaxZoom = 13;

  var bounds = new L.LatLngBounds(
    new L.LatLng(mapExtent[1], mapExtent[0]),
    new L.LatLng(mapExtent[3], mapExtent[2]));

  var map_options = {
      attributionControl: false,
      zoomControl: false
    };


  geomap = L.map('geomap', map_options).fitBounds(bounds);
  //      var geomap = L.map('geomap').fitBounds(bounds);
  //    var geomap = L.map('geomap', {center: [lat, lon], zoom: 12});

  geomap.setView(new L.LatLng(lat, lon), 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(geomap);

  var layer;
  var options = {
    minZoom: mapMinZoom,
    maxZoom: mapMaxZoom,
    opacity: 1.0,
    attributionControl: false,
    zoomControl: false,
    //opacity: 1.0,
    //attribution: 'Rendered with <a href="http://www.maptiler.com/">MapTiler</a>',
    tms: false
  };

// Слой с тайлами гелогической карты - локальный веб-сервер
// Почему-то тайлы плохо грузятся, если использовать доступ к локальной папке без веб-сервера
//  layer = L.tileLayer('geomap/{z}/{x}/{y}.png', options).addTo(geomap);
//   layer = L.tileLayer('http://localhost/{z}/{x}/{y}.png', options).addTo(geomap);
   layer = L.tileLayer('http://ex1c.delrus.ru/geomap/{z}/{x}/{y}.png', options).addTo(geomap);
//  layer = L.tileLayer('http://geo.mfvsegei.ru/200k/o-41/o-41-31/1/{z}/{x}/{y}.png', options).addTo(geomap);
  var marker = L.marker([lat, lon]).addTo(geomap);

  //----------------------------------------------------------------------
  // Задать позицию цетра интерактивной Yandex карты
  // И установить маркер на центр
  //----------------------------------------------------------------------
  eel.expose(setYmapPosition_js);
  function setYmapPosition_js(lat, lon, zoom, content) {
    myMap.setCenter([lat, lon], zoom);
    newPlacemark = new ymaps.Placemark([lat, lon], {
      hintContent: 'Участок',
      iconContent: content
    }, {
      preset: 'islands#blueStretchyIcon'
    });
    myMap.geoObjects.add(newPlacemark);
  }

  //----------------------------------------------------------------------
  // Задать позицию цетра интерактивной геологической карты (на Leaflet.js)
  // И установить маркер на центр
  //----------------------------------------------------------------------
  eel.expose(setGeoMapPosition_js);
  function setGeoMapPosition_js(lat, lon) {

    console.log('lat=', lat);
    console.log('lon=', lon);

    geomap.setView(new L.LatLng(lat, lon));
    L.marker([lat, lon]).addTo(geomap);
  }

//-----------------------------------------------------------------------
// Выполнить запрос к API Yandex карт и получить адрес по координатам
// ВОзвращает полученный адрес
//-----------------------------------------------------------------------
//  eel.expose(getAddress);
  function getAddress(coords) {
      ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            var addressLine;
            addressLine = firstGeoObject.getAddressLine()   // Адрес, полученный по координатам

            $('#inp_address').val(addressLine); // Заполним поле ввода адреса

            });
  }


  // Кнопка Старт (по кадастровому номеру)
  $('#btn_get').click(function() {
    // let info = eel.load_info($('#inp_cadaster').val())();
    console.log('eel.load_info');
    eel.load_info($('#inp_cadaster').val())();
  });


  // Кнопка Адрес (по координатам)
  $('#btn_get_address').click(function() {
    console.log('eel.getAddress');
    getAddress($('#inp_coords').val()); // Получим адрес по координатам из Yandex API
  });

  // Кнопка Старт (по координатам)
  $('#btn_get_by_coords').click(function() {
    console.log('eel.load_info_by_coords');
//    getAddress($('#inp_coords').val()); // Получим адрес по координатам из Yandex API
    eel.load_info_by_coords($('#inp_coords').val(), $('#inp_address').val())();
  });

  // Кнопка Создать
  $('#btn_create').click(function() {
    eel.create_report($('#dst_folder').val())();
  });

  // При открытии вкладки Геология карте нужно послать сигнал, чтобы обновить информацию о размере элемента
  $('#link_geomap').on('shown.bs.tab', function() {
    geomap.invalidateSize();
  });

  $('#cb_show_geomap').on('click', function() {
    let checked = $('#cb_show_geomap').is(':checked');
    console.log('CHECKBOX -->', checked);

    if (checked) {
      layer.setOpacity(1.0);
      console.log('Show layer');
    }
    else {
      layer.setOpacity(0.2);
      console.log('Hide layer');
    }

  });

});
