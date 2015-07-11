$(function() {
  // $('select label').each(function() {
  //    var $this = $(this);
  //    var labelText = $this.text();
  //    $this.empty();
  //    $this.append('<span class="focus-out">' + labelText + '</span>');
  //  });

  $('.nav-dropdown-btn').click(function() {
    $('.main-nav-ul').slideToggle('slow');
  });

  $(window).resize(function() {
    var width = $(window).width();
    if (width > 700) {
      stickyHeader();
    } else if (width <= 700) {

    }
  }).resize();

 // Form


  $('input').focusin(function() {
    $(this).siblings('span').addClass('focus-in');
  });

  $('input').focusout(function() {
    var characters = $(this).val();
    if (characters === '') {
      $(this).siblings('span').removeClass('focus-in');
    }
  });

  // $('.scan-form').submit(function(e) {
  //   e.preventDefault();
  //   e.stopPropagation();
  //
  //   alert($('.scan-form input').val());
  // });

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

  $(document).ready(function() {
  var urlRange = getUrlVars()['range'];

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

  function stickyHeader() {
    var stick = $('.page-header-footer');

    $(window).scroll(function () {
      if ($(this).scrollTop() >= 136) {
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


  $('#id_service').siblings().remove();
  $('#id_product').siblings().remove();

  $('input, select, textarea').each(function(){
    var val = $(this).val();
    if (val.length) {
      $(this).siblings('span').addClass('focus-in');
    }
  });

  // function iconColorChange() {
  //   var icon = $('.nav-dropdown-btn');
  //   var addIcon = $('.add-btn-mobile');
  //
  //   $(window).scroll(function () {
  //     if ($(this).scrollTop() >= 40) {
  //       $(icon).css('color', '#444c5a');
  //       $(addIcon).css('color', '#444c5a');
  //     } else {
  //       $(icon).css('color', '#eee');
  //       $(addIcon).css('color', '#eee');
  //     }
  //   });
  // }
  // iconColorChange();


});
