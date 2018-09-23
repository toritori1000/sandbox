$(document).ready(function () {

    // nav-bar active link switch 
    $.each($('.navbar').find('li'), function () {
        $(this).toggleClass('active',
            // redirect to destination of original click 
            window.location.pathname.indexOf($(this).find('a').attr('href')) > -1);
    });

    $('#recipeCarousel').carousel({
        //interval: 10000
        pause: true,
        interval: false
    })

    $('.carousel .carousel-item').each(function () {
        var next = $(this).next();
        if (!next.length) {
            next = $(this).siblings(':first');
        }
        next.children(':first-child').clone().appendTo($(this));

        for (var i = 0; i < 2; i++) {
            next = next.next();
            if (!next.length) {
                next = $(this).siblings(':first');
            }

            next.children(':first-child').clone().appendTo($(this));
        }
    });




});

