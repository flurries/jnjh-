function seekbutton() {
    var seek = $('#seeks').val()
    location.href = '/app/seek/?page=1&seek='+ seek
}

$(function() {
    $('#seeks').bind('keypress', function (event) {
        if(event.keyCode == "13")
        {
           seekbutton()
            }
    })
})


