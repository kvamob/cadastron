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
    //      document.getElementById('output_console').style.display = 'block';
    $('#output_console').append(line);
    //      document.getElementById('output_console').children[1].value += line;
    //      document.getElementById('output_console').children[1].rows = (parseInt(document.getElementById('output_console').children[1].rows) + 1) + '';
    //      window.scrollTo(0, document.body.scrollHeight);
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

  // if ($('#url_yandex').attr('disabled')) {
  //   console.log('Кнопка Yandex Maps disabled');
  // }
  //
  // if ($('#btn_create').attr('disabled')) {
  //   console.log('Кнопка Создать disabled');
  // } else {
  //   console.log('Кнопка Создать enabled');
  // }

  // Yandex Maps
  ymaps.ready(init);

  var myMap,
    myPlacemark;

  var lat = 56.842004;
  var lon = 60.553123;

  function init() {
    // var lat = 56.83;
    // var lon = 60.60;

    myMap = new ymaps.Map('map', {
      center: [lat, lon],
      zoom: 11
    });

    myPlacemark = new ymaps.Placemark([lat, lon], {
      hintContent: 'Екатеринбург',
      balloonContent: 'Столица Урала'
    });

    myMap.geoObjects.add(myPlacemark);
  }

    // Leaflet.js 
    var mapExtent = [57.52479930, 55.89930842, 62.99872460, 59.39520320];
    var mapMinZoom = 10;
    var mapMaxZoom = 12;
    
    var bounds = new L.LatLngBounds(
      new L.LatLng(mapExtent[1], mapExtent[0]),
      new L.LatLng(mapExtent[3], mapExtent[2]));
    var geomap = L.map('geomap').fitBounds(bounds);
    geomap.setView(new L.LatLng(lat, lon), 12);
    console.log('lat =', lat );
    console.log('lon =', lon );

//    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(geomap);
    var layer;
    var options = {
      minZoom: mapMinZoom,
      maxZoom: mapMaxZoom,
      //opacity: 0.4,
      opacity: 1.0,
      //attribution: 'Rendered with <a href="http://www.maptiler.com/">MapTiler</a>',
      tms: false
    };
    geomap.setView(new L.LatLng(lat, lon), 12);
    layer = L.tileLayer('geomap/{z}/{x}/{y}.png', options).addTo(geomap);

    var marker = L.marker([lat, lon]).addTo(geomap);

  //----------------------------------------------------------------------
  // Задать позицию цетра интерактивной Yandex карты
  //----------------------------------------------------------------------
  eel.expose(setYmapPosition_js);
  function setYmapPosition_js(lat, lon, scale, content) {
    myMap.setCenter([lat, lon], scale);
    newPlacemark = new ymaps.Placemark([lat, lon], {
      hintContent: 'Участок',
      iconContent: content
    }, {
      preset: 'islands#blueStretchyIcon'
    });
    myMap.geoObjects.add(newPlacemark);
  }

  //
  // Обработчики событий
  //

  // Кнопка Старт
  $('#btn_get').click(function() {
    let info = eel.load_info($('#inp_cadaster').val())();
    print_to_textarea_js(info);
    //    set_ymap_src_js('https://static-maps.yandex.ru/1.x/?pt=60.00,56.30,comma&z=13&size=600,450&l=map');
    //    setYmapPosition_js('55.0', '60.5', 12);
  });

  // Кнопка Создать
  $('#btn_create').click(function() {
    eel.create_report($('#dst_folder').val())();
    //    print_to_textarea_js(info);
  });

  // При открытии вкладки Геология карте нужно послать сигнал, чтобы обновить информацию о размере элемента
  $('#link_geomap').on('shown.bs.tab', function() {
    geomap.invalidateSize();
});

});
