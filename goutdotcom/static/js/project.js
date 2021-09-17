/* Project specific Javascript goes here. */

/* Profiles app JS */
// function that searches for each MedicalProfile related 1to1 CKD model and hides, empties subfields if the value is empty //
function medical_profile_ckd() {
  if ($('#id_CKD-value').val() == '') {
      $('#div_id_CKD-stage').hide();
      $('#id_CKD-stage').val('');
      $('#div_id_CKD-dialysis').hide();
      $('#id_CKD-dialysis').val('');
  }
  else if ($('#id_CKD-value').val() == 'False') {
      $('#div_id_CKD-stage').hide();
      $('#id_CKD-stage').val('');
      $('#div_id_CKD-dialysis').hide();
      $('#id_CKD-dialysis').val('');
  }
  else {
      $('#div_id_CKD-stage').show();
      $('#div_id_CKD-dialysis').show();
  }
}

// function that searches for each MedicalProfile related 1to1 Hypertension model and hides, empties subfields if the value is empty //
function medical_profile_hypertension() {
  if ($('#id_hypertension-value').val() == '') {
      $('#div_id_hypertension-medication').hide();
      $('#id_hypertension-medication').val('');
  }
  else if ($('#id_hypertension-value').val() == 'False') {
      $('#div_id_hypertension-medication').hide();
      $('#id_hypertension-medication').val('');
  }
  else {
      $('#div_id_hypertension-medication').show();
  }
}

// function that searches for each MedicalProfile related 1to1 CHF model and hides, empties subfields if the value is empty //
function medical_profile_CHF() {
  if ($('#id_CHF-value').val() == '') {
      $('#div_id_CHF-systolic').hide();
      $('#id_CHF-systolic').val('');
  }
  else if ($('#id_CHF-value').val() == 'False') {
      $('#div_id_CHF-systolic').hide();
      $('#id_CHF-systolic').val('');
  }
  else {
      $('#div_id_CHF-systolic').show();
  }
}

// function that searches for each MedicalProfile related 1to1 diabetes model and hides, empties subfields if the value is empty //
function medical_profile_diabetes() {
  if ($('#id_diabetes-value').val() == '') {
      $('#div_id_diabetes-insulin').hide();
      $('#id_diabetes-insulin').val('');
      $('#div_id_diabetes-type').hide();
      $('#id_diabetes-type').val('');
  }
  else if ($('#id_diabetes-value').val() == 'False') {
      $('#div_id_diabetes-type').hide();
      $('#id_diabetes-type').val('');
      $('#div_id_diabetes-insulin').hide();
      $('#id_diabetes-insulin').val('');
  }
  else {
      $('#div_id_diabetes-insulin').show();
      $('#div_id_diabetes-type').show();
  }
}

// function that searches for each MedicalProfile related 1to1 organ_transplant model and hides, empties subfields if the value is empty //
function medical_profile_organ_transplant() {
  if ($('#id_organ_transplant-value').val() == '') {
      $('#div_id_organ_transplant-organ').hide();
      $('#id_organ_transplant-organ_1').prop("checked", false);
      $('#id_organ_transplant-organ_2').val('');
      $('#id_organ_transplant-organ_3').val('');
      $('#id_organ_transplant-organ_4').val('');
      $('#id_organ_transplant-organ_5').val('');
      $('#id_organ_transplant-organ_6').val('');
  }
  else if ($('#id_organ_transplant-value').val() == 'False') {
      $('#div_id_organ_transplant-organ').hide();
      $('#id_organ_transplant-organ_1').prop("checked", false);
      $('#id_organ_transplant-organ_2').val('');
      $('#id_organ_transplant-organ_3').val('');
      $('#id_organ_transplant-organ_4').val('');
      $('#id_organ_transplant-organ_5').val('');
      $('#id_organ_transplant-organ_6').val('');
  }
  else {
      $('#div_id_organ_transplant-organ').show();
  }
}

/* ULT app JS */

// function that hides/shows subsequent fields based upon first_flare value
function one_flare() {
  if ($('#id_num_flares').val() == 'one') {
      $('#id_freq_flares').val('one');
  }
  else if ($('#id_num_flares').val() == 'zero') {
      $('#id_freq_flares').val('');
  }
}

function check_first_flare() {
  if ($('#id_num_flares').val().length == 0) {
      $('#div_id_freq_flares').hide();
      $('#div_id_erosions').hide();
      $('#div_id_tophi').hide();
      $('#div_id_stones').hide();
      $('#div_id_ckd').hide();
      $('#div_id_uric_acid').hide();
  }
  else if ($('#id_num_flares').val() == 'zero') {
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('one');
      $('#div_id_erosions').hide();
      $('#div_id_tophi').hide();
      $('#div_id_stones').hide();
      $('#div_id_ckd').hide();
      $('#div_id_uric_acid').hide();
  }
  else if ($('#id_num_flares').val() == 'one') {
      $('#div_id_freq_flares').val('one');
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('one');
      $('#div_id_erosions').show();
      $('#div_id_tophi').show();
      $('#div_id_stones').show();
      $('#div_id_ckd').show();
      $('#div_id_uric_acid').show();
  }
  else {
      $('#div_id_freq_flares').show();
      $('#div_id_erosions').show();
      $('#div_id_tophi').show();
      $('#div_id_stones').show();
      $('#div_id_ckd').show();
      $('#div_id_uric_acid').show();
  }
}

/* FLARE app JS flare_form.html */

// function that checks if the HTML button #location_check is checked and displays upper and lower extremity options
function check_location() {
  if ($('#location_check').is(":checked")) {
    $('#upper_extremity_check').show();
    $('label[for="upper_extremity_check"]').show();
    $('#lower_extremity_check').show();
    $('label[for="lower_extremity_check"]').show();
} else {
    $('#upper_extremity_check').hide();
    $('label[for="upper_extremity_check"]').hide();
    $('#lower_extremity_check').hide();
    $('label[for="lower_extremity_check"]').hide();
  }
}

// function that checks if the HTML buttons #lower_extremity_check and #upper_extremity_check are checked and displays appropriate options
// NEED TO BLANK VALUES WHEN UNCHECKED
function check_extremity() {
  if ($('#lower_extremity_check').is(":checked")) {
    if ($('#upper_extremity_check').is(":checked")) {
      $('#div_id_location').show();
      $('#id_location_1').show();
      $('#id_location_1').parent().show();
      $('label[for="id_location_1"]').show();
      $('#id_location_2').show();
      $('#id_location_2').parent().show();
      $('label[for="id_location_2"]').show();
      $('#id_location_3').show();
      $('#id_location_3').parent().show();
      $('label[for="id_location_3"]').show();
      $('#id_location_4').show();
      $('#id_location_4').parent().show();
      $('label[for="id_location_4"]').show();
      $('#id_location_5').show();
      $('#id_location_5').parent().show();
      $('label[for="id_location_5"]').show();
      $('#id_location_6').show();
      $('#id_location_6').parent().show();
      $('label[for="id_location_6"]').show();
      $('#id_location_7').show();
      $('#id_location_7').parent().show();
      $('label[for="id_location_7"]').show();
      $('#id_location_8').show();
      $('#id_location_8').parent().show();
      $('label[for="id_location_8"]').show();
      $('#id_location_9').show();
      $('#id_location_9').parent().show();
      $('label[for="id_location_9"]').show();
      $('#id_location_10').show();
      $('#id_location_10').parent().show();
      $('label[for="id_location_10"]').show();
      $('#id_location_11').show();
      $('#id_location_11').parent().show();
      $('label[for="id_location_11"]').show();
      $('#id_location_12').show();
      $('#id_location_12').parent().show();
      $('label[for="id_location_12"]').show();
      $('#id_location_13').show();
      $('#id_location_13').parent().show();
      $('label[for="id_location_13"]').show();
      $('#id_location_14').show();
      $('#id_location_14').parent().show();
      $('label[for="id_location_14"]').show();
      $('#id_location_15').show();
      $('#id_location_15').parent().show();
      $('label[for="id_location_15"]').show();
      $('#id_location_16').show();
      $('#id_location_16').parent().show();
      $('label[for="id_location_16"]').show();
      $('#id_location_17').show();
      $('#id_location_17').parent().show();
      $('label[for="id_location_17"]').show();
      $('#id_location_18').show();
      $('#id_location_18').parent().show();
      $('label[for="id_location_18"]').show();
      $('#id_location_19').show();
      $('#id_location_19').parent().show();
      $('label[for="id_location_19"]').show();
      $('#id_location_20').show();
      $('#id_location_20').parent().show();
      $('label[for="id_location_20"]').show();
      $('#id_location_21').show();
      $('#id_location_21').parent().show();
      $('label[for="id_location_21"]').show();
      $('#id_location_22').show();
      $('#id_location_22').parent().show();
      $('label[for="id_location_22"]').show();
      $('#id_location_23').show();
      $('#id_location_23').parent().show();
      $('label[for="id_location_23"]').show();
      $('#id_location_24').show();
      $('#id_location_24').parent().show();
      $('label[for="id_location_24"]').show();
      $('#id_location_25').show();
      $('#id_location_25').parent().show();
      $('label[for="id_location_25"]').show();
      $('#id_location_26').show();
      $('#id_location_26').parent().show();
      $('label[for="id_location_26"]').show();
      $('#id_location_27').show();
      $('#id_location_27').parent().show();
      $('label[for="id_location_27"]').show();
      $('#id_location_28').show();
      $('#id_location_28').parent().show();
      $('label[for="id_location_28"]').show();
      $('#id_location_29').show();
      $('#id_location_29').parent().show();
      $('label[for="id_location_29"]').show();
      $('#id_location_30').show();
      $('#id_location_30').parent().show();
      $('label[for="id_location_30"]').show();
      $('#id_location_31').show();
      $('#id_location_31').parent().show();
      $('label[for="id_location_31"]').show();
      $('#id_location_32').show();
      $('#id_location_32').parent().show();
      $('label[for="id_location_32"]').show();
    }
    else {
      $('#div_id_location').show();
      $('#id_location_1').show();
      $('#id_location_1').parent().show();
      $('label[for="id_location_1"]').show();
      $('#id_location_2').show();
      $('#id_location_2').parent().show();
      $('label[for="id_location_2"]').show();
      $('#id_location_3').show();
      $('#id_location_3').parent().show();
      $('label[for="id_location_3"]').show();
      $('#id_location_4').show();
      $('#id_location_4').parent().show();
      $('label[for="id_location_4"]').show();
      $('#id_location_5').show();
      $('#id_location_5').parent().show();
      $('label[for="id_location_5"]').show();
      $('#id_location_6').show();
      $('#id_location_6').parent().show();
      $('label[for="id_location_6"]').show();
      $('#id_location_7').show();
      $('#id_location_7').parent().show();
      $('label[for="id_location_7"]').show();
      $('#id_location_8').show();
      $('#id_location_8').parent().show();
      $('label[for="id_location_8"]').show();
      $('#id_location_9').show();
      $('#id_location_9').parent().show();
      $('label[for="id_location_9"]').show();
      $('#id_location_10').show();
      $('#id_location_10').parent().show();
      $('label[for="id_location_10"]').show();
      $('#id_location_11').show();
      $('#id_location_11').parent().show();
      $('label[for="id_location_11"]').show();
      $('#id_location_12').show();
      $('#id_location_12').parent().show();
      $('label[for="id_location_12"]').show();
      $('#id_location_13').show();
      $('#id_location_13').parent().show();
      $('label[for="id_location_13"]').show();
      $('#id_location_14').show();
      $('#id_location_14').parent().show();
      $('label[for="id_location_14"]').show();
      $('#id_location_15').show();
      $('#id_location_15').parent().show();
      $('label[for="id_location_15"]').show();
      $('#id_location_16').show();
      $('#id_location_16').parent().show();
      $('label[for="id_location_16"]').show();
      $('#id_location_17').hide();
      $('#id_location_17').parent().hide();
      $('label[for="id_location_17"]').hide();
      $('#id_location_18').hide();
      $('#id_location_18').parent().hide();
      $('label[for="id_location_18"]').hide();
      $('#id_location_19').hide();
      $('#id_location_19').parent().hide();
      $('label[for="id_location_19"]').hide();
      $('#id_location_20').hide();
      $('#id_location_20').parent().hide();
      $('label[for="id_location_20"]').hide();
      $('#id_location_21').hide();
      $('#id_location_21').parent().hide();
      $('label[for="id_location_21"]').hide();
      $('#id_location_22').hide();
      $('#id_location_22').parent().hide();
      $('label[for="id_location_22"]').hide();
      $('#id_location_23').hide();
      $('#id_location_23').parent().hide();
      $('label[for="id_location_23"]').hide();
      $('#id_location_24').hide();
      $('#id_location_24').parent().hide();
      $('label[for="id_location_24"]').hide();
      $('#id_location_25').hide();
      $('#id_location_25').parent().hide();
      $('label[for="id_location_25"]').hide();
      $('#id_location_26').hide();
      $('#id_location_26').parent().hide();
      $('label[for="id_location_26"]').hide();
      $('#id_location_27').hide();
      $('#id_location_27').parent().hide();
      $('label[for="id_location_27"]').hide();
      $('#id_location_28').hide();
      $('#id_location_28').parent().hide();
      $('label[for="id_location_28"]').hide();
      $('#id_location_29').hide();
      $('#id_location_29').parent().hide();
      $('label[for="id_location_29"]').hide();
      $('#id_location_30').hide();
      $('#id_location_30').parent().hide();
      $('label[for="id_location_30"]').hide();
      $('#id_location_31').hide();
      $('#id_location_31').parent().hide();
      $('label[for="id_location_31"]').hide();
      $('#id_location_32').hide();
      $('#id_location_32').parent().hide();
      $('label[for="id_location_32"]').hide();
    }
}
  else if ($('#upper_extremity_check').is(":checked")) {
    if ($('#lower_extremity_check').is(":checked")) {
      $('#div_id_location').show();
      $('#id_location_1').show();
      $('#id_location_1').parent().show();
      $('label[for="id_location_1"]').show();
      $('#id_location_2').show();
      $('#id_location_2').parent().show();
      $('label[for="id_location_2"]').show();
      $('#id_location_3').show();
      $('#id_location_3').parent().show();
      $('label[for="id_location_3"]').show();
      $('#id_location_4').show();
      $('#id_location_4').parent().show();
      $('label[for="id_location_4"]').show();
      $('#id_location_5').show();
      $('#id_location_5').parent().show();
      $('label[for="id_location_5"]').show();
      $('#id_location_6').show();
      $('#id_location_6').parent().show();
      $('label[for="id_location_6"]').show();
      $('#id_location_7').show();
      $('#id_location_7').parent().show();
      $('label[for="id_location_7"]').show();
      $('#id_location_8').show();
      $('#id_location_8').parent().show();
      $('label[for="id_location_8"]').show();
      $('#id_location_9').show();
      $('#id_location_9').parent().show();
      $('label[for="id_location_9"]').show();
      $('#id_location_10').show();
      $('#id_location_10').parent().show();
      $('label[for="id_location_10"]').show();
      $('#id_location_11').show();
      $('#id_location_11').parent().show();
      $('label[for="id_location_11"]').show();
      $('#id_location_12').show();
      $('#id_location_12').parent().show();
      $('label[for="id_location_12"]').show();
      $('#id_location_13').show();
      $('#id_location_13').parent().show();
      $('label[for="id_location_13"]').show();
      $('#id_location_14').show();
      $('#id_location_14').parent().show();
      $('label[for="id_location_14"]').show();
      $('#id_location_15').show();
      $('#id_location_15').parent().show();
      $('label[for="id_location_15"]').show();
      $('#id_location_16').show();
      $('#id_location_16').parent().show();
      $('label[for="id_location_16"]').show();
      $('#id_location_17').show();
      $('#id_location_17').parent().show();
      $('label[for="id_location_17"]').show();
      $('#id_location_18').show();
      $('#id_location_18').parent().show();
      $('label[for="id_location_18"]').show();
      $('#id_location_19').show();
      $('#id_location_19').parent().show();
      $('label[for="id_location_19"]').show();
      $('#id_location_20').show();
      $('#id_location_20').parent().show();
      $('label[for="id_location_20"]').show();
      $('#id_location_21').show();
      $('#id_location_21').parent().show();
      $('label[for="id_location_21"]').show();
      $('#id_location_22').show();
      $('#id_location_22').parent().show();
      $('label[for="id_location_22"]').show();
      $('#id_location_23').show();
      $('#id_location_23').parent().show();
      $('label[for="id_location_23"]').show();
      $('#id_location_24').show();
      $('#id_location_24').parent().show();
      $('label[for="id_location_24"]').show();
      $('#id_location_25').show();
      $('#id_location_25').parent().show();
      $('label[for="id_location_25"]').show();
      $('#id_location_26').show();
      $('#id_location_26').parent().show();
      $('label[for="id_location_26"]').show();
      $('#id_location_27').show();
      $('#id_location_27').parent().show();
      $('label[for="id_location_27"]').show();
      $('#id_location_28').show();
      $('#id_location_28').parent().show();
      $('label[for="id_location_28"]').show();
      $('#id_location_29').show();
      $('#id_location_29').parent().show();
      $('label[for="id_location_29"]').show();
      $('#id_location_30').show();
      $('#id_location_30').parent().show();
      $('label[for="id_location_30"]').show();
      $('#id_location_31').show();
      $('#id_location_31').parent().show();
      $('label[for="id_location_31"]').show();
      $('#id_location_32').show();
      $('#id_location_32').parent().show();
      $('label[for="id_location_32"]').show();
    }
    else {
      $('#div_id_location').show();
      $('#id_location_1').hide();
      $('#id_location_1').parent().hide();
      $('label[for="id_location_1"]').hide();
      $('#id_location_2').hide();
      $('#id_location_2').parent().hide();
      $('label[for="id_location_2"]').hide();
      $('#id_location_3').hide();
      $('#id_location_3').parent().hide();
      $('label[for="id_location_3"]').hide();
      $('#id_location_4').hide();
      $('#id_location_4').parent().hide();
      $('label[for="id_location_4"]').hide();
      $('#id_location_5').hide();
      $('#id_location_5').parent().hide();
      $('label[for="id_location_5"]').hide();
      $('#id_location_6').hide();
      $('#id_location_6').parent().hide();
      $('label[for="id_location_6"]').hide();
      $('#id_location_7').hide();
      $('#id_location_7').parent().hide();
      $('label[for="id_location_7"]').hide();
      $('#id_location_8').hide();
      $('#id_location_8').parent().hide();
      $('label[for="id_location_8"]').hide();
      $('#id_location_9').hide();
      $('#id_location_9').parent().hide();
      $('label[for="id_location_9"]').hide();
      $('#id_location_10').hide();
      $('#id_location_10').parent().hide();
      $('label[for="id_location_10"]').hide();
      $('#id_location_11').hide();
      $('#id_location_11').parent().hide();
      $('label[for="id_location_11"]').hide();
      $('#id_location_12').hide();
      $('#id_location_12').parent().hide();
      $('label[for="id_location_12"]').hide();
      $('#id_location_13').hide();
      $('#id_location_13').parent().hide();
      $('label[for="id_location_13"]').hide();
      $('#id_location_14').hide();
      $('#id_location_14').parent().hide();
      $('label[for="id_location_14"]').hide();
      $('#id_location_15').hide();
      $('#id_location_15').parent().hide();
      $('label[for="id_location_15"]').hide();
      $('#id_location_16').hide();
      $('#id_location_16').parent().hide();
      $('label[for="id_location_16"]').hide();
      $('#id_location_17').show();
      $('#id_location_17').parent().show();
      $('label[for="id_location_17"]').show();
      $('#id_location_18').show();
      $('#id_location_18').parent().show();
      $('label[for="id_location_18"]').show();
      $('#id_location_19').show();
      $('#id_location_19').parent().show();
      $('label[for="id_location_19"]').show();
      $('#id_location_20').show();
      $('#id_location_20').parent().show();
      $('label[for="id_location_20"]').show();
      $('#id_location_21').show();
      $('#id_location_21').parent().show();
      $('label[for="id_location_21"]').show();
      $('#id_location_22').show();
      $('#id_location_22').parent().show();
      $('label[for="id_location_22"]').show();
      $('#id_location_23').show();
      $('#id_location_23').parent().show();
      $('label[for="id_location_23"]').show();
      $('#id_location_24').show();
      $('#id_location_24').parent().show();
      $('label[for="id_location_24"]').show();
      $('#id_location_25').show();
      $('#id_location_25').parent().show();
      $('label[for="id_location_25"]').show();
      $('#id_location_26').show();
      $('#id_location_26').parent().show();
      $('label[for="id_location_26"]').show();
      $('#id_location_27').show();
      $('#id_location_27').parent().show();
      $('label[for="id_location_27"]').show();
      $('#id_location_28').show();
      $('#id_location_28').parent().show();
      $('label[for="id_location_28"]').show();
      $('#id_location_29').show();
      $('#id_location_29').parent().show();
      $('label[for="id_location_29"]').show();
      $('#id_location_30').show();
      $('#id_location_30').parent().show();
      $('label[for="id_location_30"]').show();
      $('#id_location_31').show();
      $('#id_location_31').parent().show();
      $('label[for="id_location_31"]').show();
      $('#id_location_32').show();
      $('#id_location_32').parent().show();
      $('label[for="id_location_32"]').show();
    }
}
  else {
    $('#id_location_1').hide();
    $('#id_location_1').parent().hide();
    $('label[for="id_location_1"]').hide();
    $('#id_location_2').hide();
    $('#id_location_2').parent().hide();
    $('label[for="id_location_2"]').hide();
    $('#id_location_3').hide();
    $('#id_location_3').parent().hide();
    $('label[for="id_location_3"]').hide();
    $('#id_location_4').hide();
    $('#id_location_4').parent().hide();
    $('label[for="id_location_4"]').hide();
    $('#id_location_5').hide();
    $('#id_location_5').parent().hide();
    $('label[for="id_location_5"]').hide();
    $('#id_location_6').hide();
    $('#id_location_6').parent().hide();
    $('label[for="id_location_6"]').hide();
    $('#id_location_7').hide();
    $('#id_location_7').parent().hide();
    $('label[for="id_location_7"]').hide();
    $('#id_location_8').hide();
    $('#id_location_8').parent().hide();
    $('label[for="id_location_8"]').hide();
    $('#id_location_9').hide();
    $('#id_location_9').parent().hide();
    $('label[for="id_location_9"]').hide();
    $('#id_location_10').hide();
    $('#id_location_10').parent().hide();
    $('label[for="id_location_10"]').hide();
    $('#id_location_11').hide();
    $('#id_location_11').parent().hide();
    $('label[for="id_location_11"]').hide();
    $('#id_location_12').hide();
    $('#id_location_12').parent().hide();
    $('label[for="id_location_12"]').hide();
    $('#id_location_13').hide();
    $('#id_location_13').parent().hide();
    $('label[for="id_location_13"]').hide();
    $('#id_location_14').hide();
    $('#id_location_14').parent().hide();
    $('label[for="id_location_14"]').hide();
    $('#id_location_15').hide();
    $('#id_location_15').parent().hide();
    $('label[for="id_location_15"]').hide();
    $('#id_location_16').hide();
    $('#id_location_16').parent().hide();
    $('label[for="id_location_16"]').hide();
    $('#id_location_16').hide();
    $('#id_location_16').parent().hide();
    $('label[for="id_location_16"]').hide();
    $('#div_id_location').hide();
    $('#id_location_17').hide();
    $('#id_location_17').parent().hide();
    $('label[for="id_location_17"]').hide();
    $('#id_location_18').hide();
    $('#id_location_18').parent().hide();
    $('label[for="id_location_18"]').hide();
    $('#id_location_19').hide();
    $('#id_location_19').parent().hide();
    $('label[for="id_location_19"]').hide();
    $('#id_location_20').hide();
    $('#id_location_20').parent().hide();
    $('label[for="id_location_20"]').hide();
    $('#id_location_21').hide();
    $('#id_location_21').parent().hide();
    $('label[for="id_location_21"]').hide();
    $('#id_location_22').hide();
    $('#id_location_22').parent().hide();
    $('label[for="id_location_22"]').hide();
    $('#id_location_23').hide();
    $('#id_location_23').parent().hide();
    $('label[for="id_location_23"]').hide();
    $('#id_location_24').hide();
    $('#id_location_24').parent().hide();
    $('label[for="id_location_24"]').hide();
    $('#id_location_25').hide();
    $('#id_location_25').parent().hide();
    $('label[for="id_location_25"]').hide();
    $('#id_location_26').hide();
    $('#id_location_26').parent().hide();
    $('label[for="id_location_26"]').hide();
    $('#id_location_27').hide();
    $('#id_location_27').parent().hide();
    $('label[for="id_location_27"]').hide();
    $('#id_location_28').hide();
    $('#id_location_28').parent().hide();
    $('label[for="id_location_28"]').hide();
    $('#id_location_29').hide();
    $('#id_location_29').parent().hide();
    $('label[for="id_location_29"]').hide();
    $('#id_location_30').hide();
    $('#id_location_30').parent().hide();
    $('label[for="id_location_30"]').hide();
    $('#id_location_31').hide();
    $('#id_location_31').parent().hide();
    $('label[for="id_location_31"]').hide();
    $('#id_location_32').hide();
    $('#id_location_32').parent().hide();
    $('label[for="id_location_32"]').hide();
  }
}

// function that checks if the HTML button #lab_check is checked and shows the optional labs Flare model field check boxes, used on #lab_check click
function check_labs() {
  if ($('#lab_check').is(":checked")) {
    $('#div_id_labs').show();
} else {
    $('#div_id_labs').hide();
  }
}

// function that checks whether any Urate is present in the Flare model instance and reveals the appropriate fields for modification in Flare UpdateView
function check_initial_urate() {
  if ($('#id_urate-value').val()) {
    $('#lab_check').prop("checked", true);
    $('#id_labs_1').prop("checked", true);
} else {
    $('#div_id_labs').hide();
  }
}

// function that checks whether Urate #id_labs_1 field is checked and if so shows the options for creation/update of Flare-associated Urate field, evaluated on checking #id_labs_1=Urate
function check_urate() {
  if ($('#id_labs_1').is(":checked")) {
    $('#urate_fields').show();
} else {
    $('#urate_fields').hide();
    $('#urate_fields').find('#id_urate-value').val('');
    $('#urate_fields').find('#urate-date_drawn').val('');
  }
}

// function that checks whether any treatments were selected on the Flare model field and reveals the appropriate fields for modification in Flare UpdateView
function check_initial_treatments() {
  if ($('#id_treatment_1').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_2').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_3').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_4').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_5').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_6').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_7').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_8').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else if ($('#id_treatment_9').is(":checked")) {
    $('#treatment_check').prop("checked", true);
}
  else {
    $('#treatment_check').prop("checked", false);
  }
}

// function that checks whether the HTML button #treatment_check is checked or not, shows appropriate treatment Flare model field options if so
function check_treatment() {
  if ($('#treatment_check').is(":checked")) {
    $('#div_id_treatment').show();
} else {
    $('#div_id_treatment').hide();
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_1() {
  if ($('#id_treatment_1').is(":checked")) {
    $('#colchicine_for_flare').show();
} else {
    $('#colchicine_for_flare').hide();
    $('#colchicine_for_flare').find('#id_colchicine-dose').val('');
    $('#colchicine_for_flare').find('#id_colchicine-freq').val('');
    $('#colchicine_for_flare').find('#id_colchicine-date_started').val('');
    $('#colchicine_for_flare').find('#id_colchicine-date_ended').val('');
    $('#colchicine_for_flare').find('#id_colchicine-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_2() {
  if ($('#id_treatment_2').is(":checked")) {
    $('#ibuprofen_for_flare').show();
} else {
    $('#ibuprofen_for_flare').hide();
    $('#ibuprofen_for_flare').find('#id_ibuprofen-dose').val('');
    $('#ibuprofen_for_flare').find('#id_ibuprofen-freq').val('');
    $('#ibuprofen_for_flare').find('#id_ibuprofen-date_started').val('');
    $('#ibuprofen_for_flare').find('#id_ibuprofen-date_ended').val('');
    $('#ibuprofen_for_flare').find('#id_ibuprofen-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_3() {
  if ($('#id_treatment_3').is(":checked")) {
    $('#naproxen_for_flare').show();
} else {
    $('#naproxen_for_flare').hide();
    $('#naproxen_for_flare').find('#id_naproxen-dose').val('');
    $('#naproxen_for_flare').find('#id_naproxen-freq').val('');
    $('#naproxen_for_flare').find('#id_naproxen-date_started').val('');
    $('#naproxen_for_flare').find('#id_naproxen-date_ended').val('');
    $('#naproxen_for_flare').find('#id_naproxen-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_4() {
  if ($('#id_treatment_4').is(":checked")) {
    $('#celecoxib_for_flare').show();
} else {
    $('#celecoxib_for_flare').hide();
    $('#celecoxib_for_flare').find('#id_celecoxib-dose').val('');
    $('#celecoxib_for_flare').find('#id_celecoxib-freq').val('');
    $('#celecoxib_for_flare').find('#id_celecoxib-date_started').val('');
    $('#celecoxib_for_flare').find('#id_celecoxib-date_ended').val('');
    $('#celecoxib_for_flare').find('#id_celecoxib-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_5() {
  if ($('#id_treatment_5').is(":checked")) {
    $('#meloxicam_for_flare').show();
} else {
    $('#meloxicam_for_flare').hide();
    $('#meloxicam_for_flare').find('#id_meloxicam-dose').val('');
    $('#meloxicam_for_flare').find('#id_meloxicam-freq').val('');
    $('#meloxicam_for_flare').find('#id_meloxicam-date_started').val('');
    $('#meloxicam_for_flare').find('#id_meloxicam-date_ended').val('');
    $('#meloxicam_for_flare').find('#id_meloxicam-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment prednisone (#id_treatment_6) button is checked and, if so, displays appropriate treatment form
function check_treatment_6() {
  if ($('#id_treatment_6').is(":checked")) {
    $('#prednisone_for_flare').show();
} else {
    $('#prednisone_for_flare').hide();
    $('#prednisone_for_flare').find('#id_prednisone-dose').val('');
    $('#prednisone_for_flare').find('#id_prednisone-freq').val('');
    $('#prednisone_for_flare').find('#id_prednisone-date_started').val('');
    $('#prednisone_for_flare').find('#id_prednisone-date_ended').val('');
    $('#prednisone_for_flare').find('#id_prednisone-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment methylprednisolone (#id_treatment_7) button is checked and, if so, displays appropriate treatment form
function check_treatment_7() {
  if ($('#id_treatment_7').is(":checked")) {
    $('#methylprednisolone_for_flare').show();
} else {
    $('#methylprednisolone_for_flare').hide();
    $('#methylprednisolone_for_flare').find('#id_methylprednisolone-dose').val('');
    $('#methylprednisolone_for_flare').find('#id_methylprednisolone-freq').val('');
    $('#methylprednisolone_for_flare').find('#id_methylprednisolone-date_started').val('');
    $('#methylprednisolone_for_flare').find('#id_methylprednisolone-date_ended').val('');
    $('#methylprednisolone_for_flare').find('#id_methylprednisolone-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment tinctureoftime (#id_treatment_8) button is checked and, if so, displays appropriate treatment form
function check_treatment_8() {
  if ($('#id_treatment_8').is(":checked")) {
    $('#tinctureoftime_for_flare').show();
} else {
    $('#tinctureoftime_for_flare').hide();
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-duration').val('');
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-dose').val('');
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-freq').val('');
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-date_started').val('');
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-date_ended').val('');
    $('#tinctureoftime_for_flare').find('#id_tinctureoftime-side_effects').val('');
  }
}

// function that checks whether Flare model field treatment othertreat (#id_treatment_9) button is checked and, if so, displays appropriate treatment form
function check_treatment_9() {
  if ($('#id_treatment_9').is(":checked")) {
    $('#othertreat_for_flare').show();
} else {
    $('#othertreat_for_flare').hide();
    $('#othertreat_for_flare').find('#id_othertreat-name').val('');
    $('#othertreat_for_flare').find('#id_othertreat-description').val('');
    $('#othertreat_for_flare').find('#id_othertreat-dose').val('');
    $('#othertreat_for_flare').find('#id_othertreat-freq').val('');
    $('#othertreat_for_flare').find('#id_othertreat-date_started').val('');
    $('#othertreat_for_flare').find('#id_othertreat-date_ended').val('');
    $('#othertreat_for_flare').find('#id_othertreat-side_effects').val('');
  }
}

/* ULT app JS */
// Long if / else if function displaying appropriate HTML form elements for ULT model Create and Update views
// THIS LIKELY CAN BE DONE MORE INTELLIGENTLY BROKEN UP INTO SMALLER FUNCTIONS
function urate_decider() {
  if ($('#urate-decision').val() == "No") {
    $('#urate-decision-div').hide();
    $('#urate-logged-div').hide();
    $('#urate-desire-div').hide();
    $('#flare-no-urate-button').show();
  }
  else if ($('#urate-decision').val() == "Yes") {
    if ($('#urate-logged').val() == "Yes") {
      $('#urate-logged-div').hide();
      $('#flare-no-urate-button').show();
      $('#flare-with-urate-button').hide();
      $('#urate-desire-div').hide();
    }
    else if ($('#urate-logged').val() == "No") {
      if ($('#urate-desire').val() == "No") {
        $('#urate-desire-div').hide();
        $('#flare-no-urate-button').show();
        $('#flare-with-urate-button').hide();
      }
      else if ($('#urate-desire').val() == "Yes") {
        $('#urate-desire-div').hide();
        $('#flare-no-urate-button').hide();
        $('#flare-with-urate-button').show();
      }
      else {
        $('#urate-logged-div').hide();
        $('#urate-desire-div').show();
        $('#flare-no-urate-button').hide();
        $('#flare-with-urate-button').hide();
      }
    }
    else {
      $('#urate-decision-div').hide();
      $('#urate-logged-div').show();
      $('#flare-no-urate-button').hide();
      $('#flare-with-urate-button').hide();
    }
  }
  else {
    $('#urate-logged-div').hide();
    $('#urate-desire-div').hide();
  }
}

// STILL NEEDED?
function treatment_log() {
  if ($('#treatment-decision').val() == "Yes") {
    $('#treatment-logged').show();
  }
  else if ($('#treatment-decision').val() == "No") {
    $('#treatment-logged').hide();
  }
  else {
    $('#treatment-logged').hide();
    $('#treatment-desire').hide();
  }
}

// STILL NEEDED?
function treatment_decider() {
  if ($('#treatment-logged').val() == "Yes") {
    $('#treatment-desire').show();
  }
  else if ($('#treatment-logged').val() == "No") {
    $('#treatment-desire').hide();
  }
}
