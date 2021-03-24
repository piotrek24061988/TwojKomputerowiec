jQuery(function($)
{
    //Scroll to top when button selected
    $('.scrollup').click(function()
    {
        $.scrollTo(0, 1500);
    });

    //Show / hide button depend os position
    $(window).scroll(function()
    {
        if($(this).scrollTop()>500) $('.scrollup').fadeIn();
        else $('.scrollup').fadeOut();
    });
});