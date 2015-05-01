$(function () {
    
    $.get('/get_cadet_list_json/', function(data) {
        console.log(data);
    });
})