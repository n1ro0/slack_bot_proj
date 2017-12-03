$(document).ready(function() {
  $('li.active').removeClass('active');
  $('a[href="' + location.pathname + '"]').closest('li').addClass('active');
  if ($(document).height() <= $(window).height())
    $("footer").addClass("navbar-fixed-bottom");
});
