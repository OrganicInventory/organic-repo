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
  $('input').focusin(function() {
    $(this).siblings('span').addClass('focus-in');
  });

  $('input').focusout(function() {
    var characters = $(this).val();
    if (characters === '') {
      $(this).siblings('span').removeClass('focus-in');
    }
  });

  $('#id_service').siblings().remove();
  // $('select option:label').text('test');
  // $('option').attr('label').remove();


});
