$(document).ready(function () {
    // session = new QiSession("127.0.0.1:80");

    //  use qimessaging-json directly 
    // the port 8002 is the port qimessaging-json is listening to
    // the string "1.0" avoids to have to rewrite url with reverse proxy
    session = new QiSession("127.0.0.1:8002", "1.0");

    $('#page_empty').show();
    $('#page_1').hide();
    $('#page_2').hide();
    $('#page_3').hide();
    $('#page_4').hide();


var animal;

    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("SimpleWeb/Page0").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_empty').show();
                $('#page_1').hide();
                $('#page_2').hide();
		$('#page_3').hide();
                $('#page_4').hide();
		console.log("val:"+val);
		$('#text_start').html("<h1>"+val+"</h1>");
            });
        });


        ALMemory.subscriber("SimpleWeb/Page1").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_1').show();
                $('#page_empty').hide();
                $('#page_2').hide();
		$('#page_3').hide();
		$('#page_4').hide();

            });
        });

        ALMemory.subscriber("SimpleWeb/Page2").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_1').hide();
                $('#page_empty').hide();
                $('#page_2').show();
		$('#page_3').hide();
                $('#page_4').hide();
		console.log("val:"+val);
		animal = val;
		$('#text_start').html("<h1>Where do you want me to drop off your "+val+"?</h1>");

            });
        });

 	 ALMemory.subscriber("SimpleWeb/Page3").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_1').hide();
                $('#page_empty').hide();
                $('#page_2').hide();
		$('#page_3').show();
                $('#page_4').hide();
		console.log("val:"+val);
		$('#text_start').html("<h1>All right, I'll immediately put the "+animal+" in the "+val+"</h1>");

            });
        });

 	 ALMemory.subscriber("SimpleWeb/Page4").done(function(subscriber) {

            subscriber.signal.connect(function(val) {
                $('#page_1').hide();
                $('#page_empty').hide();
                $('#page_2').hide();
		$('#page_3').hide();
                $('#page_4').show();
		console.log("val:"+val);
		$('#text_start').html("<h1>"+val+"</h1>");

            });
        });


    });

    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

	$('#footer_start').on('click', function() {
        console.log("click Start");
        raise('SimpleWeb/Start', 1)
    });

    $('#choice_1_1').on('click', function() {
        console.log("click 1");
        raise('SimpleWeb/Button1', 1)
	
    });

    $('#choice_1_2').on('click', function() {
        console.log("click 2");
        raise('SimpleWeb/Button2', 1)
    });

    $('#choice_1_3').on('click', function() {
        console.log("click 3");
        raise('SimpleWeb/Button3', 1)
    });



    $('#choice_2_1').on('click', function() {
        console.log("click 4");
        raise('SimpleWeb/Button4', 1)
    });

    $('#choice_2_2').on('click', function() {
        console.log("click 5");
        raise('SimpleWeb/Button5', 1)
    });

    $('#choice_2_3').on('click', function() {
        console.log("click 6");
        raise('SimpleWeb/Button6', 1)
    });


    $('#return').on('click', function() {
        console.log("return");
        raise('SimpleWeb/Button7', 1)
    });

    $('#final').on('click', function() {
        console.log("No");
        raise('SimpleWeb/Button8', 1)
    });




});
