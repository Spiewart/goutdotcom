/* Project specific Javascript goes here. */

// function that hides/shows subsequent fields based upon first_flare value
function check_first_flare() {
  if ($('#id_first_flare').val() == 'True') {
      $('#div_id_num_flares').hide();
      $('#div_id_freq_flares').hide();
      $('#div_id_erosions').hide();
      $('#div_id_tophi').hide();
      $('#div_id_stones').hide();
      $('#div_id_ckd').hide();
      $('#div_id_uric_acid').hide();
  } else {
      $('#div_id_num_flares').show();
      $('#div_id_freq_flares').show();
      $('#div_id_erosions').show();
      $('#div_id_tophi').show();
      $('#div_id_stones').show();
      $('#div_id_ckd').show();
      $('#div_id_uric_acid').show();
  }   
}


