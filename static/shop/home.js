$(document).ready(function() {

    function nextSlide() {
        var currentImg = $('.active1');
        var nextImg = currentImg.next();
    
        if(nextImg.length){
          currentImg.removeClass('active1').css('z-index', -10);
          nextImg.addClass('active1').css('z-index', -1);
        }
        else {
            var firstImg = $('.slide img:first-child');
            currentImg.removeClass('active1').css('z-index', -10);
            firstImg.addClass('active1').css('z-index', -1);
        }
    }
  
    function prevSlide() {
        var currentImg = $('.active1');
        var prevImg = currentImg.prev();
    
        if(prevImg.length){
          currentImg.removeClass('active1').css('z-index', -10);
          prevImg.addClass('active1').css('z-index', -1);
        }
        else {
            var lastImg = $('.slide img:last-child');
            currentImg.removeClass('active1').css('z-index', -10);
            lastImg.addClass('active1').css('z-index', -1);
        }
    }

    function autoNextSlide() {
        setInterval(nextSlide, 3000);
    }

    // autoNextSlide();
  
    $('.next').click(nextSlide);
    $('.prev').click(prevSlide);

    $('#orderNowBtn').click(function () {
        $('#orderForm').toggle();
    });
  
  });
  