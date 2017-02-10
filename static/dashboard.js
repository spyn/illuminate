

$( document ).ready(function() {
    var dev = [];
    var fx = [];

    $.getJSON('/devices', function(json) {
      dev = json;
      $.each(json, function(k, v){
        $('#device_list').append('<li type="'+v.type+'" name="'+ v.name +'" alias="' + v.alias + '" class="devfx"><a href="#">' + v.name + '</a></li>');
      });

    });
    $.getJSON('/effects', function(json) {
      fx = json;
    });

    $('#device_list').on('click', '.devfx', function(){
      var name = $(this).attr('name');
      var alias = $(this).attr('alias');
      var type = $(this).attr('type');
      $('#main-header').text(name + ': ' + type);
      $('#effects').empty();

      if(type == 'hyperion') {
        $.each(fx.hyperion, function(k, v) {
          $('#effects').append('<li name="'+v.name+'" device="'+alias+'" class="runfx"><a href="#">' + v.name + '</a></li>');
        });
      }
      else if(type == 'yeelight') {
        $.each(fx.yeelight, function(k, v) {
          $('#effects').append('<li name="'+v.name+'" device="'+alias+'" class="runfx"><a href="#">' + v.name + '</a></li>');
        });
      }
    });

    $('#effects').on('click', '.runfx', function(e) {
      var device = $(this).attr('device');
      var effect = $(this).attr('name');
      var url = '/' + device + '/' + effect;

      e.preventDefault();
      $.ajax({
        url: url,
        type: 'GET',
        timeout: 5000
      });
    });

});




