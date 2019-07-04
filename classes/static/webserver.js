jQuery(function () {
    webserver.init();
});

var webserver = {
	init : function() {
        $.ajaxSetup({
            cache: false
        });
		jQuery('main').load('./static/main.html');
        webserver.loadNavi();
    }
	, loadNavi : function() {
        jQuery('nav').load("./static/nav.html", function () {
            jQuery('#speechControl').click(function () {
				jQuery('main').load('./static/speechControl.html');
				jQuery('a.active').removeClass('active');
                jQuery(this).addClass('active');
            });
            jQuery('#buttonControl').click(function () {
				jQuery('main').load('./static/buttonControl.html');
				jQuery('a.active').removeClass('active');
                jQuery(this).addClass('active');
            });
        });
    }
	, handleAnimalButton : function(animal) {
		console.log(animal);
        $.ajax({
		  type: "POST",
		  url: "/search_animal",
		  data: {animal: animal},
		});
    }
    , handleButton : function() {
		console.log("ButtonPressed");
        $.ajax({
		  type: "POST",
		  url: "/testDistance",
          success: function(result){
            jQuery('#distance').text(result);
            jQuery('#slider').val(result);
            console.log(result);
            setTimeout(function(){
                webserver.handleButton();
            }, 1000);
          }
		});
    }
}