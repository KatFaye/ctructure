$( document ).ready(function() {
    $("button.submit-button").click(function(){
        var password = $("input[name='password']").val();
        var repeated_password = $("input[name='repeated_password']").val();
        if (password == repeated_password){
            var user_info={
            "username": $("input[name='username']").val(),
            "first_name": $("input[name='first_name']").val(),
            "last_name": $("input[name='last_name']").val(),
            "email": $("input[name='email']").val(),
            "password": password,
            "repeated_password": repeated_password
            }
        }
        else{
            alert("The repeated password doesn't match the password.");
        }

         $.ajax({
            url: '/login',
            data: $('form[name = "newuser"]').serialize(),
            type: 'GET',
            success: function(response) {
                alter(response)
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

    });
});