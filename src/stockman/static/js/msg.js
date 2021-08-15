    $(document).ready(function() {
        setTimeout(function() {
            $('.message').fadeOut('slow');
        }, 5000);

        $('.del-msg').live('click', function(){
            $('del-msg').parent().attr('style', 'display:none;');
        })
    });