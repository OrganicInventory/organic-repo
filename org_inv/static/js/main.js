$(function() {

//GET URL VALUE FOR DATE RANGE
  function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

    for(var i = 0; i < hashes.length; i++) {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }

    return vars;
}
getUrlVars();

//CHANGE TEXT VALUE FOR DATE RANGE ON PAGE LOAD
  $(document).ready(function() {
  var urlRange = getUrlVars()['range'];

  $('.scan-input').focus();

  $('.date-dropdown').val(urlRange);
    if (urlRange === '1') {
      $('.date-range-display').text('1 Day');
    } else if (urlRange === '7') {
      $('.date-range-display').text('1 Week');
    } else if (urlRange === '14') {
      $('.date-range-display').text('2 Weeks');
    } else if (urlRange === '30') {
      $('.date-range-display').text('1 Month');
    } else if (urlRange === '60') {
      $('.date-range-display').text('2 Months');
    } else {
      $('.date-dropdown').val('14');
    }

  });

//HAMBURGER DROPDOWN MENU
  $('.nav-dropdown-btn').click(function() {
    $('.main-nav-ul').slideToggle('slow');
  });

//STICKY HEADER ON RESIZE
  $(window).resize(function() {
    var width = $(window).width();
    if (width > 700) {
      stickyHeader();
    } else if (width <= 700) {

    }
  }).resize();

//FORM FLOATING LABELS
  $('input').focusin(function() {
    $(this).siblings('span').addClass('focus-in');
  });

  $('input').focusout(function() {
    var characters = $(this).val();
    if (characters === '') {
      $(this).siblings('span').removeClass('focus-in');
    }
  });

//STICKY HEADER
  function stickyHeader() {
    var stick = $('.page-header-footer');

    $(window).scroll(function () {
      if ($(this).scrollTop() > 136) {
        stick.addClass('sticky');
        $('.top-nav-container-hide').fadeIn('slow');
        $('.top-nav-container').fadeOut('slow');
      } else {
        stick.removeClass('sticky');
        $('.top-nav-container-hide').fadeOut('slow');
        $('.top-nav-container').fadeIn(2000);
      }
    });
  }

//MODAL
  // $('.add-content-button').click(function() {
  //   $('.modal-container').fadeToggle();
  //   $('.add-content-button').toggleClass('modal-exit-btn');
  //   $('.add-button').toggleClass('modal-exit-icon');
  // });

//REMOVING SPECIFIC LABELS
  $('#id_service').siblings().remove();
  $('#id_product').siblings().remove();

//SET FLOATING LABELS THAT ALREADY CONTAIN CONTENT
  $('input, textarea').each(function(){
    var val = $(this).val();
    if (val.length) {
      $(this).siblings('span').addClass('focus-in');
    }
  });

  $('.scan-form').submit(function(e) {
    e.preventDefault();
    e.stopPropagation();
  });

});
