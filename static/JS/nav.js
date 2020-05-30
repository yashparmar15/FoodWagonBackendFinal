$(function () {
    $(document).scroll(function () {
      var $nav = $(".navbar-fixed-top");
      var $link = $(".nav-link");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
      $link.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
    });
  });