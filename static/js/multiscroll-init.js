(function ($) {
'use strict';
    

    





    function multi() {

        if ($(window).width() > 991) {

            $('#myContainer').multiscroll({
                sectionsColor: ['#fff', '#fff', '#fff'],
                menu: '#menu',
                navigation: true,
                scrollingSpeed: 500,
                loopBottom: true,
                keyboardScrolling: false,
                loopTop: true,
                navigationTooltips: ['Wybór','Wyniki','Metody'],
                anchors: ['wybor', 'wyniki', 'metody'],
                easing: 'easeInQuart',
                menu: '#myMenu'
                // normalScrollElements: '#jobInfo',
                // scrollOverflow: true,
            });
            $("#multiscroll-nav ul li a").append("<svg width='30' height='30'><circle cx='15' cy='15' r='11.5'></circle></svg>");

        } else {

          

        }
    }
    multi(); 


})(jQuery);
$.fn.multiscroll.setMouseWheelScrolling(false);
