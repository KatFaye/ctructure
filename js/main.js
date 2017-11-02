$( document ).ready(function() {

    $(".navbar-collapse li").click(function(){
        $(this).siblings().each(function(){
            $(this).removeClass('active')
        });
        $(this).addClass('active')
        $(".main.container").trigger('change_tab')
    });

    $(".main.container").on('change_tab', function(){
        var tab_id = $(".navbar-collapse li.active").attr('id');
        var file_name= tab_id+".html"
        $(this).load(file_name)
    })

    $(".main.container").trigger('change_tab')

});