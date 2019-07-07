jQuery(function () {
    webserver.init();
});

var webserver = {
	init : function() {
    $.ajaxSetup({
        cache: false
    });
    jQuery('main').load('./static/main.html', function() {
      componentHandler.upgradeDom();
    });
  }
  , 
  handleAnimalButton : function(animal) {
      console.log(animal);
        $.ajax({
      type: "POST",
      url: "/search_animal",
      data: {animal: animal},
    });
  }
  , handleButtonDiagnostics : function() {
  // console.log("getDiagnostics");
      $.ajax({
    type: "GET",
    url: "/getDiagnostics",
        success: function(result){
          result = JSON.parse(result);
          jQuery('#diagnostics').text(result);
          jQuery('#cpuTempValue').text(result.cpu_temp.toFixed(1)+'°C');
          jQuery('#cpuUsageValue').text(result.cpu_usage.toFixed(1)+'%');
          jQuery('#ramUsageValue').text(result.ram_usage[2].toFixed(1)+'%');
          jQuery('#cpuClockValue').text( (result.cpu_clock[0]/1000).toFixed(1)+" GHz");
          // jQuery('#distance').text(result);
          // jQuery('#slider').val(result);
          console.log(result);
          setTimeout(function(){
              webserver.handleButtonDiagnostics();
          }, 1000);
        }
  });
  }
  , handleButtonImageRaw : function() {
  // console.log("getImageRaw");
      $.ajax({
    type: "GET",
    url: "/getImageRaw",
        success: function(result){
          jQuery("#imageRaw").attr("src", 'data:image/jpeg;base64,'+result);
          // console.log(result);
          setTimeout(function(){
              webserver.handleButtonImageRaw();
          }, 200);
        }
  });
  }
  , handleButtonImageDNN : function() 
  {
  // console.log("getImageDnn");
    $.ajax({
      type: "GET",
      url: "/getImageDnn",
        success: function(result)
        {
          jQuery("#imageDNN").attr("src", 'data:image/jpeg;base64,'+result);

          $.ajax({
            type: "GET",
            url: "/getDnnResults",
                success: function(result){
                  console.log(result);
                  result = JSON.parse(result);

                  let newHTML = "";
                  result.forEach(function(value, index) {
                    let animal = value[0];
                    let percentage = (value[1]*100).toFixed(1);
                    newHTML += `
                    <div class="align-right mdl-grid">
                        <div class="mdl-cell mdl-cell--1-col"></div>
                        <div class="mdl-cell mdl-cell--4-col">
                            <span>${animal}</span>
                        </div>
                        <div class="align-right mdl-cell mdl-cell--2-col">
                            <span>${percentage} %</span>
                        </div>
                        <div class="mdl-cell mdl-cell--5-col"></div>
                    </div>`
                  });                  

                  jQuery('#dnnResults').html(newHTML);
                }
          });
          setTimeout(function()
          {
              webserver.handleButtonImageDNN();
          }, 500);
        }
    });
  }
}