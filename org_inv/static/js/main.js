$(function () {

//GET URL VALUE FOR DATE RANGE
    function getUrlVars() {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

        for (var i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return vars;
    }

    getUrlVars();

//CHANGE TEXT VALUE FOR DATE RANGE ON PAGE LOAD
    $(document).ready(function () {
        var urlRange = getUrlVars()['range'];
        var urlUpc = getUrlVars() ['upc'];
        var checkId = getUrlVars() ['id'];

        $('.scan-input').focus();

        if(!urlRange) {
          $('.date-dropdown').val(dateInterval);
        } else {
          $('.date-dropdown').val(urlRange);
        }

        if (!urlUpc) {
            $('#id_brand :selected').text('Pick a Brand');
        }
    });

//HAMBURGER DROPDOWN MENU
    $('.nav-dropdown-btn').click(function () {
        $('.main-nav-ul').toggle('slow');
    });

    $('.dropdown-icon').click(function () {
        $('.slide-in-menu').slideDown('slow');
        $('.click-catch').toggle();
    });

    $('.slide-in-menu-exit').click(function () {
        $('.slide-in-menu').slideUp('slow');
        $('.click-catch').hide();
    });

//FORM FLOATING LABELS
    $('input').focusin(function () {
        $(this).siblings('span').addClass('focus-in');
    });

    $('input').focusout(function () {
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
    $(window).resize(function () {
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
    $('.Product label').remove();

//SET FLOATING LABELS THAT ALREADY CONTAIN CONTENT
    $('input, textarea').each(function () {
        var val = $(this).val();
        if (val.length) {
            $(this).siblings('span').addClass('focus-in');
        }
    });

//PREVENT SCAN FROM FROM AUTO SUBMITTING
    $('.scan-form').keypress(function (e) {
      if (e.which === 13) {
        e.preventDefault();
        e.stopPropagation();

        var checkNum = $('.scan-input').val();
        
        if (isNaN(checkNum)) {
          checkName();
        } else {
          checkUpc();
        }
      }
    });

    $('.cancel-submit').keypress(function (e) {
        if (e.which === 13) {
            e.preventDefault();
            e.stopPropagation();
        }
    });

//CHECK UPC INPUT AND COMPARE TO EXISTING PRODUCTS
    function checkUpc() {
        var upcInput = parseInt($('.scan-input').val());
        var arr = [];

        $('.table-upc tr').each(function () {
            var upcData = parseInt($(this).attr('data-upc'));
            arr.push(upcData);


            for (var i = 0; i < arr.length; i++) {
                if (arr.indexOf(upcInput) > -1) {
                    $('.scan-details').css('display', 'inline');
                    $('.scan-update').css('display', 'inline');
                    $('.scan-new').css('display', 'none');

                    var trIndex = arr.indexOf(upcInput);
                    $('tr:eq(' + trIndex + ')').css('background-color', '#add8e6');
                } else {
                    $('.scan-new').css('display', 'inline');
                    $('.scan-details').css('display', 'none');
                    $('.scan-update').css('display', 'none');
                }
            }
        });
    }

    function checkName() {
      var nameInput = $('.scan-input').val().toLowerCase();
      var name = [];

      console.log(nameInput);

      $('.table-upc tr').each(function () {
        var nameData = $(this).attr('name');
        name.push(nameData);

        for (var i = 0; i < name.length; i++) {
          if (name.indexOf(nameInput) > -1 ) {
          var trIndexName = name.indexOf(nameInput);
            $('tr:eq(' + trIndexName + ')').css('background-color', '#add8e6');
          }
        }
      });
    }

//EXIT SUCCESS MESSAGES
    $('.success-exit').click(function () {
        $(this).parent().slideUp();
    });

//DELETE ITEM FROM ORDER FORM
    $('.delete-item').click(function () {
        $(this).parent().slideUp();
        $(this).siblings('input').val(0);
    });

    $('.display-chart-btn').click(function () {
        $('.ref-chart').slideToggle();
    });

//DASHBOARD

    $('.appointment-drop').click(function () {
      $('.appointments-list-container').slideToggle('slow');
      // $('.appointment-button').fadeToggle('slow');
      $(this).toggleClass('dropdown-switch');
    });

    $('.product-drop').click(function () {
      $('.products-list-container').slideToggle('slow');
      // $('.product-button').fadeToggle('slow');
      $(this).toggleClass('dropdown-switch');
    });

    $('.show-chart-icon').click(function () {
      $('.chart-container').toggleClass('chart-container-show');
      $(this).toggle('fast');
      $('.show-chart-icon-click').toggle('fast');
    });

    $('.show-chart-icon-click').click(function() {
      $(this).toggle('fast');
      $('.show-chart-icon').toggle('fast');
      $('.chart-container').toggleClass('chart-container-show');
    });

    $('.header-dropdown-icon').click(function() {
      $('.main-nav-container').slideToggle();
      $('.click-catch').toggle();
    });

    $('.click-catch').click(function() {
      $('.main-nav-container-click').slideToggle();
      $('.slide-in-menu').slideToggle();
      $(this).hide();
    });



});
