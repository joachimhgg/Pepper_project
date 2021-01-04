$(document).ready(function () {
    session = new QiSession();

    $('#page_1').show();

    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

    $('#Button1').on('click', function() {
        var prenom = document.getElementById("name").value;
        console.log(prenom);        
        raise('Web/Button1', prenom)
    });

});
