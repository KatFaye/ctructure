$(function(){
    $('#submitBtn').click(function(){
        $.ajax({
            url: '/changeInfo',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
        //alert($("input.form-input[type='radio']:checked").attr("value"))
    });
});