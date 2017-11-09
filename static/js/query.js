$(function(){
    $('#searchBtn').click(function(){
        $.ajax({
            url: '/search',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                $("#results").html(response)
            },
            error: function(error){
                console.log(error);
            }
        });
        //alert($("input.form-input[type='radio']:checked").attr("value"))
    });
});