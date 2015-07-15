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
  var urlUpc = getUrlVars() ['upc'];

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

    if (!urlUpc) {
      $('#id_brand :selected').text('Pick a Brand');
    }

  });

//HAMBURGER DROPDOWN MENU
  $('.nav-dropdown-btn').click(function() {
    $('.main-nav-ul').toggle('slow');
  });

  $('.dropdown-icon').click(function() {
    $('.slide-in-menu').slideDown('slow');
  });

  $('.slide-in-menu-exit').click(function() {
    $('.slide-in-menu').slideUp('slow');
  });

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
        $('.top-nav-container').css('display', 'none');
        $('.top-nav-container-hide').css('display', 'block');
        $('.dropdown-icon-bottom').css('display', 'block');
      } else {
        stick.removeClass('sticky');
        $('.top-nav-container').css('display', 'block');
        $('.top-nav-container-hide').css('display', 'none');
        $('.dropdown-icon-bottom').css('display', 'none');
      }
    });
  }

//STICKY HEADER ON RESIZE
  $(window).resize(function() {
    var width = $(window).width();
    if (width > 700) {
      stickyHeader();
      $('.main-nav-ul').show();
    } else {
      $('.slide-in-menu').css('display', 'none');
    }
  }).resize();

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

//PREVENT SCAN FROM FROM AUTO SUBMITTING
  $('.scan-form').keypress(function(e) {
    if(e.which === 13) {
    e.preventDefault();
    e.stopPropagation();

    checkUpc();
    }
  });

//CHECK UPC INPUT AND COMPARE TO EXISTING PRODUCTS
  function checkUpc() {
    var upcInput = parseInt($('.scan-input').val());
    var arr = [];

    $('.table-upc tr').each(function() {
    var upcData = parseInt($(this).attr('data-upc'));
      arr.push(upcData);

      for (var i = 0; i < arr.length; i++) {
        if (arr.indexOf(upcInput) > -1) {
          $('.scan-details').css('display', 'inline');
          $('.scan-update').css('display', 'inline');
          $('.scan-new').css('display', 'none');

          var trIndex = arr.indexOf(upcInput);
          $( 'tr:eq(' + trIndex + ')').css('background-color', 'red').css('color', 'white');
        } else {
          $('.scan-new').css('display', 'inline');
          $('.scan-details').css('display', 'none');
          $('.scan-update').css('display', 'none');
        }
      }
    });
  }

});
