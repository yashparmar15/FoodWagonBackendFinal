$("#sliderShuffle").cycle({
    next: '#next',
    prev: '#prev'
});

$('.owl-carousel').owlCarousel({
    items:4,
    loop:true,
    margin:15,
    autoplay:true,
    autoplayTimeout:3000, //3 Second
    nav:true,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:3,
            nav:true
        },
        1000:{
            items:4,
            nav:true
        }
    }

});

$(function(){
    $(".productCategories ul li").click(function(){
        $(".productCategories ul li").not(this).find(".megamenu").hide();
        $(this).find(".megamenu").toggle();
    });
    $(".otherInfoBody").hide();
    $(".otherInfoHandle").click(function(){
        $(".otherInfoBody").slideToggle();
    });
    $(".signBtn").click(function(){
        $("body").css("overflow", "hidden");
        $(".loginBox").slideDown();
    });
    $(".closeBtn").click(function(){
        $("body").css("overflow", "visible");
        $(".loginBox").slideUp();
    });
    $(".productViewBtn").click(function(e){
        e.preventDefault();
        $("body").css("overflow", "hidden");
        $(".productViewBox").slideDown();
    });
    $(".productViewBox-closeBtn").click(function(){
        $("body").css("overflow", "visible");
        $(".productViewBox").slideUp();
    });
});