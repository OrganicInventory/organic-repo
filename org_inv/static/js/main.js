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

  // $('.scan-input').focus();

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

//STICKY HEADER ON RESIZE
  $(window).resize(function() {
    var width = $(window).width();
    if (width > 700) {
      stickyHeader();
      $('.main-nav-ul').show();
      $('.dropdown-icon-bottom').css('display', 'none');
    } else {
      $('.slide-in-menu').css('display', 'none');
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

//PREVENT SCAN FROM FROM AUTO SUBMITTING
  $('.scan-form').keypress(function(e) {
    if(e.which === 13) {
    e.preventDefault();
    e.stopPropagation();

    // checkUpc();
    }
  });

  // function checkUpc() {
  //   var upcInput  = parseInt($('.scan-input').val());
  //   var productCount = $('.get-upc').length;
  //   var arr = [];
  //   // var upcVal = $(this).val();
  //   console.log(upcInput);
  //
  //   $('.get-upc').each(function() {
  //     // console.log($(this).val());
  //     arr.push($(this).val());
  //     // console.log(arr.length);
  //   });
  //
  //   for (var i = 0; i < arr.length; i++) {
  //     console.log(parseInt(arr[i]));
  //     if (upcInput = 123456789) {
  //       $('.scan-details').css('display', 'inline');
  //       $('.scan-update').css('display', 'inline');
  //       $('.scan-new').css('display', 'none');
  //     } else {
  //       $('.scan-new').css('display', 'inline');
  //       $('.scan-details').css('display', 'none');
  //       $('.scan-update').css('display', 'none');
  //     }
  //   }
  // }

  // console.log(tr.data('upc'));

  // function checkUpc() {
  //   $('table-upc tr').each(function (i, tr) {
  //     var test = tr.data('upc');
  //   });
  // }
  // checkUpc();


  // $('table-upc tr').each(function (i, tr) {
  //   tr.data('upc');
  // });

});
