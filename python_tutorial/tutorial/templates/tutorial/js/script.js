$(document).ready(function() {
    $("#<your_button_id>").click( function() {

        $.post("your_python_script_url", {}, function () {
            // What to do when request successfully completed
        });
    })
})