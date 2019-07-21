jQuery(function () {
    webserver.init();
    setTimeout(function(){
      webserver.runDiagnostics()
      webserver.runImageRaw()
      webserver.runImageDNN()
    }, 1000);
});

// var boolDiagnostics = false;
// var boolLive = false;
// var boolDNN = false;
var boolDiagnostics = true;
var boolLive = true;
var boolDNN = true;
var timeStarted = null;
var boolIsRunning = false;
var selectedAnimal = '';

var webserver = {
	init : function() {
    $.ajaxSetup({
        cache: false
    });
    jQuery('main').load('./static/main.html', function() {
      componentHandler.upgradeDom();
    });
  }, 
  handleAnimalSelection : function(ev) {
    jQuery("button[id^='animal_']").removeClass("animal-selected");
    jQuery("#"+ev.currentTarget.id).addClass("animal-selected");
    jQuery("#btn-start").attr('disabled',false);
    selectedAnimal = ev.currentTarget.id;
  }, 
  handleButtonStart : function(ev) {
    jQuery("button[id^='animal_']").attr('disabled',true);
    jQuery("#btn-start").attr('disabled',true);
    $.ajax({
      type: "POST",
      data: {animal: selectedAnimal},
      url: "/searchAnimal",
          success: function(result){
            result = JSON.parse(result);
          },
          error: function(){
            console.log("Error in handleButtonStart")
          }
    });
    boolIsRunning = true;
    jQuery('#animalFound').text("...");
    initClock();
  }, 
  handleButtonStop : function(ev) {
    jQuery("button[id^='animal_']").attr('disabled',false);
    boolIsRunning = false;
    $.ajax({
      type: "GET",
      url: "/stop",
          success: function(result){
            
          },
          error: function(){
            console.log("Error in handleButtonStop")
          }
    });
  }, 
  handleButtonReset : function(ev) {
    boolIsRunning = false;
    $.ajax({
      type: "GET",
      url: "/reset",
          success: function(result){
            
          },
          error: function(){
            console.log("Error in handleButtonReset")
          }
    });
  }, 
  handleSwitchDiagnostics : function(ev) {
    if(ev.checked) {
      boolDiagnostics = true
      webserver.runDiagnostics()
    } else {
      boolDiagnostics = false
    }
  }, 
  handleSwitchLive : function(ev) {
    if(ev.checked) {
      boolLive = true
      webserver.runImageRaw()
    } else {
      boolLive = false
    }
  }, 
  handleSwitchDNN : function(ev) {
    if(ev.checked) {
      boolDNN = true
      webserver.runImageDNN()
    } else {
      boolDNN = false
    }
  }, 
  runDiagnostics : function() {
    if(boolDiagnostics === true){
      $.ajax({
        type: "GET",
        url: "/getDiagnostics",
            success: function(result){
              result = JSON.parse(result);

              console.log(result);

              jQuery('#distance').text(result.distance.toFixed(1));
              jQuery('#cpuTempValue').text(result.cpu_temp.toFixed(1)+'°C');
              jQuery('#cpuUsageValue').text(result.cpu_usage.toFixed(1)+'%');
              jQuery('#ramUsageValue').text(result.ram_usage[2].toFixed(1)+'%');
              jQuery('#cpuClockValue').text( (result.cpu_clock[0]/1000).toFixed(1)+" GHz");
              jQuery('#status').text(result.status);

              if(result.finished == true){
                boolIsRunning = false;
                jQuery("button[id^='animal_']").attr('disabled',false);
              }

              if(result.animal_found == true){
                jQuery('#animalFound').text("Ja");
              }else{
                jQuery('#animalFound').text("Nein");
              }

              setTimeout(function(){
                  webserver.runDiagnostics();
              }, 500);
            },
            error: function(){
              setTimeout(function()
              {
                  webserver.runDiagnostics();
              }, 500);
            }
      });
    }
  }, 
  runImageRaw : function() {
    if(boolLive === true){
      $.ajax({
        type: "GET",
        url: "/getImageRaw",
            success: function(result){
              jQuery("#imageRaw").attr("src", 'data:image/jpeg;base64,'+result);
              setTimeout(function(){
                  webserver.runImageRaw();
              }, 200);
            },
            error: function(){
              setTimeout(function()
              {
                  webserver.runImageRaw();
              }, 500);
            }
      });
    }
  }, 
  runImageDNN : function() 
  {
    if(boolDNN === true){
        $.ajax({
          type: "GET",
          url: "/getImageDnn",
            success: function(result)
            {
              if( jQuery('#imageDNN').attr('src') != 'data:image/jpeg;base64,'+result ){
                jQuery("#imageDNN").fadeToggle("fast");
                jQuery("#imageDNN").attr("src", 'data:image/jpeg;base64,'+result);
                jQuery("#imageDNN").fadeToggle("fast");
              }
    
              $.ajax({
                type: "GET",
                url: "/getDnnResults",
                    success: function(result){
                      result = JSON.parse(result);
    
                      let newHTML = "";
                      result.forEach(function(value, index) {
                        let animal = value[0];
                        let percentage = (value[1]*100).toFixed(1);
                        let color = 'red';
                        newHTML += `
                          <div class="dnn-results align-right mdl-grid">
                            <div class="dnn-row mdl-cell mdl-cell--2-col">
                                <span class="progress-animal">${animal}</span>
                            </div>
                            <div class="dnn-row align-right mdl-cell mdl-cell--3-col">
                                <span class="progress-percent">${percentage} %</span>
                            </div>
                            <div class="dnn-progress-background mdl-cell mdl-cell--7-col">
                                <div id="percentage${index}" class="progress-${color}"></div>
                            </div>
                          </div>
                        `
                      });                  
    
                      jQuery('#dnnResults').html(newHTML);
                      result.forEach(function(value, index) {
                        jQuery('#percentage'+index).css('width',(value[1]*100).toFixed(1)+'%');
                      });
                    },
                    error: function(){
                      setTimeout(function()
                      {
                          webserver.runImageDNN();
                      }, 500);
                    }
              });
              setTimeout(function()
              {
                  webserver.runImageDNN();
              }, 250);
            },
            error: function(){
              setTimeout(function()
              {
                  webserver.runImageDNN();
              }, 500);
            }
        });
    }
  }
}

function initClock() {
  timeStarted = new Date();
  updateClock();
  window.setInterval("updateClock()", 10);
}

function updateClock() {
  if( boolIsRunning == true){
    let timeNow = new Date();
    let t = timeNow.getTime() - timeStarted.getTime();
    if(t >= 0){
      var min = Math.floor((t % (1000*60*60)) / (1000*60));
      var sec = Math.floor((t % (1000*60)) / 1000);
      var mili = Math.floor((t % 1000));
      jQuery("#minute").text( min.pad(2) );
      jQuery("#second").text( sec.pad(2) );
      jQuery("#milisecond").text( mili.pad(3) );
    }
  }
}

Number.prototype.pad = function(n) {
  for (var r = this.toString(); r.length < n; r = 0 + r);
  return r;
};
