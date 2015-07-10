$(function() {
  // $('label').each(function() {
  //    var $this = $(this);
  //    var labelText = $this.text();
  //    $this.empty();
  //    $this.append('<span class="focus-out">' + labelText + '</span>');
  //  });

 // Form
  // $('input, select, textarea').each(function(){
  //   var val = $(this).val();
  //   if (val.length) {
  //     $(this).siblings('span').addClass('focus-in');
  //   }
  // });



  // $('select').each(function() {
  //   $('label').remove();
  // });

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
var urlRange = getUrlVars()['range'];

  $(document).ready(function() {
    console.log(urlRange);
    if (urlRange === '1') {
      $('.date-range-display').text('1 Day');
    } else if (urlRange === '7') {
      $('.date-range-display').text('One Week');
    } else if (urlRange === '14') {
      $('.date-range-display').text('Two Weeks');
    } else if (urlRange === '30') {
      $('.date-range-display').text('1 Month');
    } else if (urlRange === '60') {
      $('.date-range-display').text('2 Months');
    }

  });

});
