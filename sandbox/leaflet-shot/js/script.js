$(function () {
  // import 'leaflet';

  var lat = 56.162464;
  var lon = 60.915409;
  var geomap;


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
  var urlTemplate = 'https://ex1c.delrus.ru/geomap/{z}/{x}/{y}.png';
  // var urlTemplate = 'http://localhost/{z}/{x}/{y}.png';
  // var urlTemplate = 'http://geo.mfvsegei.ru/200k/o-41/o-41-31/1/{z}/{x}/{y}.png';
  layer = L.tileLayer(urlTemplate, options).addTo(geomap);
  var marker = L.marker([lat, lon]).addTo(geomap);

var simpleMapScreenshoter = L.simpleMapScreenshoter({
  hidden: true
}).addTo(geomap);
  
  geomap.invalidateSize();
  


    // return as image
    document.getElementById('screenMapAndPast').addEventListener('click', function () {
      simpleMapScreenshoter.takeScreen('image', {
          caption: function () {
              return 'Hello world'
          }
      }).then(image => {
          var img = document.createElement('img')
          img.src = image
          document.getElementById('screens').appendChild(img)
      }).catch(e => {
          alert(e.toString())
      })
  })

  //----------------------------------------------------------------------
  // Задать позицию цетра интерактивной Yandex карты
  // И установить маркер на центр
  //----------------------------------------------------------------------
  // eel.expose(setYmapPosition_js);


  //----------------------------------------------------------------------
  // Задать позицию цетра интерактивной геологической карты (на Leaflet.js)
  // И установить маркер на центр
  //----------------------------------------------------------------------

  function setGeoMapPosition_js(lat, lon) {

    console.log('lat=', lat);
    console.log('lon=', lon);

  }


  // При открытии вкладки Геология карте нужно послать сигнал, чтобы обновить информацию о размере элемента
  // Bootstrap
  // $('#link_geomap').on('shown.bs.tab', function () {
  //   geomap.invalidateSize();
  // });


});