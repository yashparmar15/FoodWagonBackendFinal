$('.counter-count').each(function counterr() {
    $(this).prop('Counter',0).animate({
        Counter: $(this).text()
    }, {
        duration: 5000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now));
        }
    });
});










var button = document.getElementById('slide');
button.onclick = function () {
    var container = document.getElementById('container-box');
    sideScroll(container,'right',25,100,10);
};

var back = document.getElementById('slideback');
back.onclick = function () {
    var container = document.getElementById('container-box');
    sideScroll(container,'left',25,100,10);
};

function sideScroll(element,direction,speed,distance,step){
    scrollAmount = 0;
    var slideTimer = setInterval(function(){
        if(direction == 'left'){
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        if(scrollAmount >= distance){
            window.clearInterval(slideTimer);
        }
    }, speed);
}




$(document).ready(function(){
    $('.parallax').parallax();
  });