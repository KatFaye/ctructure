$(function(){
    $('#searchBtn').click(function(){
        $.ajax({
            url: '/search',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response){
                $("#result").html(response)
            },
            error: function(error){
                console.log(error);
            }
        });
        //alert($("input.form-input[type='radio']:checked").attr("value"))
    });
});