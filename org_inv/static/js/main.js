$(function() {

  // $('#datepicker').datepicker();

  // $('#id_date').addClass('datepicker');
  // $('#id_date').attr('id', 'datepicker');

  // $('label').each(function() {
  //    var $this = $(this);
  //    var labelText = $this.text();
  //    $this.empty();
  //    $this.append('<span class="focus-out">' + labelText + '</span>');
  //  });

 // Form
  $('input, select, textarea').each(function(){
    var val = $(this).val();
    if (val.length){
      $(this).siblings('span').addClass('focus-in');
    }
  });

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

  //$('.scan-form').submit(function(e) {
  //  e.preventDefault();
  //  e.stopPropagation();
  //
  //  alert($('.scan-form input').val());
  //});

  // var value = $("a").attr("href");
  // console.log(value);
  //
  // if (value) {
  //   alert('it is');
  // }


});
