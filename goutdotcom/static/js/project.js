/* Project specific Javascript goes here. */

/* Profiles app JS */
/* MedicalProfile model JS */
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

/* SocialHistory model JS */
// function that checks whether or not the user has selected that they drink alcohol or not (id_alcohol_value) and adjusts the subfields accordingly
function alcohol () {
  if ($('#id_alcohol_value').val() == '') {
      $('#div_id_stroke-value').hide();
      $('#stroke_bar').hide()
      $('#id_stroke-value').val('');
      $('#div_id_heartattack-value').hide();
      $('#heartattack_bar').hide()
      $('#id_heartattack-value').val('');
      $('#div_id_bleed-value').hide();
      $('#bleed_bar').hide()
      $('#id_bleed-value').val('');
  }
  else if ($('#id_alcohol_value').val() == 'False') {
      $('#div_id_stroke-value').hide();
      $('#stroke_bar').hide()
      $('#id_stroke-value').val('');
      $('#div_id_heartattack-value').hide();
      $('#heartattack_bar').hide()
      $('#id_heartattack-value').val('');
      $('#div_id_bleed-value').hide();
      $('#bleed_bar').hide()
      $('#id_bleed-value').val('');
  }
  else {
      $('#div_id_stroke-value').show();
      $('#stroke_bar').show()
      $('#div_id_heartattack-value').show();
      $('#heartattack_bar').show()
      $('#div_id_bleed-value').show();
      $('#bleed_bar').show()
  }
}

/* Contraindication model JS */
// function that checks the value of contraindication (all) and displays sub-contraindication feels as appropriate
function contraindications() {
  if ($('#id_contraindication').val() == '') {
      $('#div_id_stroke-value').hide();
      $('#stroke_bar').hide()
      $('#id_stroke-value').val('');
      $('#div_id_heartattack-value').hide();
      $('#heartattack_bar').hide()
      $('#id_heartattack-value').val('');
      $('#div_id_bleed-value').hide();
      $('#bleed_bar').hide()
      $('#id_bleed-value').val('');
  }
  else if ($('#id_contraindication').val() == 'False') {
      $('#div_id_stroke-value').hide();
      $('#stroke_bar').hide()
      $('#id_stroke-value').val('');
      $('#div_id_heartattack-value').hide();
      $('#heartattack_bar').hide()
      $('#id_heartattack-value').val('');
      $('#div_id_bleed-value').hide();
      $('#bleed_bar').hide()
      $('#id_bleed-value').val('');
  }
  else {
      $('#div_id_stroke-value').show();
      $('#stroke_bar').show()
      $('#div_id_heartattack-value').show();
      $('#heartattack_bar').show()
      $('#div_id_bleed-value').show();
      $('#bleed_bar').show()
  }
}

// function that searches for each MedicalProfile related 1to1 Stroke model and hides, empties subfields if the value is empty //
function contraindications_profile_stroke() {
  if ($('#id_stroke-value').val() == '') {
      $('#div_id_stroke-number').hide();
      $('#id_stroke-number').val('');
      $('#div_id_stroke-date').hide();
      $('#id_stroke-date').val('');
  }
  else if ($('#id_stroke-value').val() == 'False') {
      $('#div_id_stroke-number').hide();
      $('#id_stroke-number').val('');
      $('#div_id_stroke-date').hide();
      $('#id_stroke-date').val('');
  }
  else {
      $('#div_id_stroke-number').show();
      $('#div_id_stroke-date').show();
  }
}

// function that searches for each Contraindications related 1to1 HeartAttack model and hides, empties subfields if the value is empty //
function contraindications_profile_heartattack() {
  if ($('#id_heartattack-value').val() == '') {
      $('#div_id_heartattack-number').hide();
      $('#id_heartattack-number').val('');
      $('#div_id_heartattack-date').hide();
      $('#heartattack_date.pk').val('');
      $('#div_id_heartattack-stent').hide();
      $('#id_heartattack-stent').val('');
      $('#div_id_heartattack-stent_date').hide();
      $('#stent_date.pk').val('');
      $('#div_id_heartattack-cabg').hide();
      $('#id_heartattack-cabg').val('');
      $('#div_id_heartattack-cabg_date').hide();
      $('#cabg_date.pk').val('');
  }
  else if ($('#id_heartattack-value').val() == 'False') {
      $('#div_id_heartattack-number').hide();
      $('#id_heartattack-number').val('');
      $('#div_id_heartattack-date').hide();
      $('#heartattack_date.pk').val('').attr('type', 'text').attr('type', 'date');
      $('#div_id_heartattack-stent').hide();
      $('#id_heartattack-stent').val('');
      $('#div_id_heartattack-stent_date').hide();
      $('#stent_date.pk').val('');
      $('#div_id_heartattack-cabg').hide();
      $('#id_heartattack-cabg').val('');
      $('#div_id_heartattack-cabg_date').hide();
      $('#cabg_date.pk').val('');
  }
  else {
      $('#div_id_heartattack-number').show();
      $('#div_id_heartattack-date').show();
      $('#div_id_heartattack-stent').show();
      $('#div_id_heartattack-cabg').show();
  }
}

function contraindications_profile_stent() {
  if ($('#id_heartattack-stent').val() == 'True') {
        $('#div_id_heartattack-stent_date').show();
      }
  else if ($('#id_heartattack-stent').val() == 'False') {
        $('#div_id_heartattack-stent_date').hide();
        $('#id_heartattack-stent_date.pk').val('');
      }
  else if ($('#id_heartattack-stent').val() == '') {
        $('#div_id_heartattack-stent_date').hide();
        $('#id_heartattack-stent_date.pk').val('');
      }
  }

function contraindications_profile_cabg() {
  if ($('#id_heartattack-cabg').val() == 'True') {
        $('#div_id_heartattack-cabg_date').show();
      }
  else if ($('#id_heartattack-cabg').val() == 'False') {
    $('#div_id_heartattack-cabg_date').hide();
    $('#cabg_date.pk').val('');
      }
  else if ($('#id_heartattack-cabg').val() == '') {
    $('#div_id_heartattack-cabg_date').hide();
    $('#-cabg_date.pk').val('');
      }
  }

// function that searches for each Contraindications related 1to1 Bleed model and hides, empties subfields if the value is empty //
function contraindications_profile_bleed() {
  if ($('#id_bleed-value').val() == '') {
      $('#div_id_bleed-number').hide();
      $('#id_bleed-number').val('');
      $('#div_id_bleed-date').hide();
      $('#id_bleed-date').val('');
      $('#div_id_bleed-GIB').hide();
      $('#id_bleed-GIB').val('');
      $('#div_id_bleed-GIB_date').hide();
      $('#id_bleed-GIB_date').val('');
      $('#div_id_bleed-CNS').hide();
      $('#id_bleed-CNS').val('');
      $('#div_id_bleed-CNS_date').hide();
      $('#id_bleed-CNS_date').val('');
      $('#div_id_bleed-transfusion').hide();
      $('#id_bleed-transfusion').val('');
  }
  else if ($('#id_bleed-value').val() == 'False') {
      $('#div_id_bleed-number').hide();
      $('#id_bleed-number').val('');
      $('#div_id_bleed-date').hide();
      $('#id_bleed-date').val('');
      $('#div_id_bleed-GIB').hide();
      $('#id_bleed-GIB').val('');
      $('#div_id_bleed-GIB_date').hide();
      $('#id_bleed-GIB_date').val('');
      $('#div_id_bleed-CNS').hide();
      $('#id_bleed-CNS').val('');
      $('#div_id_bleed-CNS_date').hide();
      $('#id_bleed-CNS_date').val('');
      $('#div_id_bleed-transfusion').hide();
      $('#id_bleed-transfusion').val('');
  }
  else {
      $('#div_id_bleed-number').show();
      $('#div_id_bleed-date').show();
      $('#div_id_bleed-GIB').show();
      $('#div_id_bleed-GIB_date').show();
      $('#div_id_bleed-CNS').show();
      $('#div_id_bleed-CNS_date').show();
      $('#div_id_bleed-transfusion').show();
  }
}
/* ULT app JS */
// function that adjusts value of freq_flares based off num_flares and uses check_first_flare() to hides/shows subsequent fields based upon first_flare value
function one_flare() {
  if ($('#id_num_flares').val() == 'one') {
      $('#id_freq_flares').val('one');
  }
  else if ($('#id_num_flares').val() == 'zero') {
      $('#id_freq_flares').val('');
  }
}

// function that checks how many gout flares are reported, hides unnecessary subfields if number of flares is blank, zero, or one, shows subfields otherwise, shows frequency of flares option if number of flares > 1
function check_first_flare() {
  if ($('#id_num_flares').val().length == 0) {
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('');
      $('#subfields').hide();
  }
  else if ($('#id_num_flares').val() == 'zero') {
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('');
      $('#subfields').hide();
  }
  else if ($('#id_num_flares').val() == 'one') {
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('one');
      $('#subfields').show();
  }
  else {
      $('#div_id_freq_flares').show();
      $('#subfields').show();
  }
}

function check_subfields() {
// function that checks whether the user already has some MedicalProfile fields that are shown on the ULT form
  $('#subfields input[type=checkbox]').each(function() {
    if ($(this).is(":checked")) {
      $('#subfields').show();
    }
  })
}

/* FLARE app JS flare_form.html */
// function that checks what the initial location values are for flare UpdateView and de/populates form fields as needed
function check_initial_location() {
  if ($("input[type=radio][name=id_location_0]:checked").val()) {
    alert("got this far");
    $('#location_check').prop("checked", true);
    $('#lower_extremity_check').prop("checked", true);
  }
}
 /* $('input', $('#locations-col-1')).each(function() {
  var $this = $(this);
  if ($this.is(":checked")) {
    $('#location_check').prop("checked", true);
    $('#lower_extremity_check').show();
    $('label[for="lower_extremity_check"]').show();
    $('#lower_extremity_check').prop("checked", true);
  }
  })
 $('input', $('#locations-col-2')).each(function() {
  var $this = $(this);
  if ($this.is(":checked")) {
    $('#location_check').prop("checked", true);
    $('#upper_extremity_check').show();
    $('label[for="upper_extremity_check"]').show();
    $('#upper_extremity_check').prop("checked", true);
  }
  })
} */
/*
// function that checks if the HTML button #location_check is checked and displays upper and lower extremity options
function check_location() {
  if ($('#location_check').is(":checked")) {
    $('#upper_extremity_check').show();
    $('label[for="upper_extremity_check"]').show();
    $('#lower_extremity_check').show();
    $('label[for="lower_extremity_check"]').show();
} else {
    $('#upper_extremity_check').hide();
    $('#upper_extremity_check').prop("checked", false);
    $('label[for="upper_extremity_check"]').hide();
    $('#lower_extremity_check').hide();
    $('#lower_extremity_check').prop("checked", false);
    $('label[for="lower_extremity_check"]').hide();
    $('#location_check_hr').hide();
    $('input', $('#div_id_location')).each(function() {
    var $this = $(this);
    $this.prop("checked", false);
    })
  }
}

// function that checks if the HTML buttons #lower_extremity_check and #upper_extremity_check are checked and displays appropriate options, now BLANKs VALUES WHEN UNCHECKED
function check_extremity() {
  if ($('#lower_extremity_check').is(":checked")) {
    if ($('#upper_extremity_check').is(":checked")) {
      $('#div_id_location').show();
      $('#id_location_0').show();
      $('#id_location_0').parent().show();
      $('label[for="id_location_0"]').show();
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
      $('#location_check_hr').show();
    }
    else {
      $('#div_id_location').show();
      $('#id_location_0').show();
      $('#id_location_0').parent().show();
      $('label[for="id_location_0"]').show();
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
      $('#id_location_16').hide();
      $('#id_location_16').prop('checked', false);
      $('#id_location_16').parent().hide();
      $('label[for="id_location_16"]').hide();
      $('#id_location_17').hide();
      $('#id_location_17').prop('checked', false);
      $('#id_location_17').parent().hide();
      $('label[for="id_location_17"]').hide();
      $('#id_location_18').hide();
      $('#id_location_18').prop('checked', false);
      $('#id_location_18').parent().hide();
      $('label[for="id_location_18"]').hide();
      $('#id_location_19').hide();
      $('#id_location_19').prop('checked', false);
      $('#id_location_19').parent().hide();
      $('label[for="id_location_19"]').hide();
      $('#id_location_20').hide();
      $('#id_location_20').prop('checked', false);
      $('#id_location_20').parent().hide();
      $('label[for="id_location_20"]').hide();
      $('#id_location_21').hide();
      $('#id_location_21').prop('checked', false);
      $('#id_location_21').parent().hide();
      $('label[for="id_location_21"]').hide();
      $('#id_location_22').hide();
      $('#id_location_22').prop('checked', false);
      $('#id_location_22').parent().hide();
      $('label[for="id_location_22"]').hide();
      $('#id_location_23').hide();
      $('#id_location_23').prop('checked', false);
      $('#id_location_23').parent().hide();
      $('label[for="id_location_23"]').hide();
      $('#id_location_24').hide();
      $('#id_location_24').prop('checked', false);
      $('#id_location_24').parent().hide();
      $('label[for="id_location_24"]').hide();
      $('#id_location_25').hide();
      $('#id_location_25').prop('checked', false);
      $('#id_location_25').parent().hide();
      $('label[for="id_location_25"]').hide();
      $('#id_location_26').hide();
      $('#id_location_26').prop('checked', false);
      $('#id_location_26').parent().hide();
      $('label[for="id_location_26"]').hide();
      $('#id_location_27').hide();
      $('#id_location_27').prop('checked', false);
      $('#id_location_27').parent().hide();
      $('label[for="id_location_27"]').hide();
      $('#id_location_28').hide();
      $('#id_location_28').prop('checked', false);
      $('#id_location_28').parent().hide();
      $('label[for="id_location_28"]').hide();
      $('#id_location_29').hide();
      $('#id_location_29').prop('checked', false);
      $('#id_location_29').parent().hide();
      $('label[for="id_location_29"]').hide();
      $('#id_location_30').hide();
      $('#id_location_30').prop('checked', false);
      $('#id_location_30').parent().hide();
      $('label[for="id_location_30"]').hide();
      $('#id_location_31').hide();
      $('#id_location_31').prop('checked', false);
      $('#id_location_31').parent().hide();
      $('label[for="id_location_31"]').hide();
      $('#location_check_hr').show();
    }
}
  else if ($('#upper_extremity_check').is(":checked")) {
    if ($('#lower_extremity_check').is(":checked")) {
      $('#div_id_location').show();
      $('#id_location_0').show();
      $('#id_location_0').parent().show();
      $('label[for="id_location_0"]').show();
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
      $('#location_check_hr').show();
    }
    else {
      $('#div_id_location').show();
      $('#id_location_0').hide();
      $('#id_location_0').prop('checked', false);
      $('#id_location_0').parent().hide();
      $('label[for="id_location_0"]').hide();
      $('#id_location_1').hide();
      $('#id_location_1').prop('checked', false);
      $('#id_location_1').parent().hide();
      $('label[for="id_location_1"]').hide();
      $('#id_location_2').hide();
      $('#id_location_2').prop('checked', false);
      $('#id_location_2').parent().hide();
      $('label[for="id_location_2"]').hide();
      $('#id_location_3').hide();
      $('#id_location_3').prop('checked', false);
      $('#id_location_3').parent().hide();
      $('label[for="id_location_3"]').hide();
      $('#id_location_4').hide();
      $('#id_location_4').prop('checked', false);
      $('#id_location_4').parent().hide();
      $('label[for="id_location_4"]').hide();
      $('#id_location_5').hide();
      $('#id_location_5').prop('checked', false);
      $('#id_location_5').parent().hide();
      $('label[for="id_location_5"]').hide();
      $('#id_location_6').hide();
      $('#id_location_6').prop('checked', false);
      $('#id_location_6').parent().hide();
      $('label[for="id_location_6"]').hide();
      $('#id_location_7').hide();
      $('#id_location_7').prop('checked', false);
      $('#id_location_7').parent().hide();
      $('label[for="id_location_7"]').hide();
      $('#id_location_8').hide();
      $('#id_location_8').prop('checked', false);
      $('#id_location_8').parent().hide();
      $('label[for="id_location_8"]').hide();
      $('#id_location_9').hide();
      $('#id_location_9').prop('checked', false);
      $('#id_location_9').parent().hide();
      $('label[for="id_location_9"]').hide();
      $('#id_location_10').hide();
      $('#id_location_10').prop('checked', false);
      $('#id_location_10').parent().hide();
      $('label[for="id_location_10"]').hide();
      $('#id_location_11').hide();
      $('#id_location_11').prop('checked', false);
      $('#id_location_11').parent().hide();
      $('label[for="id_location_11"]').hide();
      $('#id_location_12').hide();
      $('#id_location_12').prop('checked', false);
      $('#id_location_12').parent().hide();
      $('label[for="id_location_12"]').hide();
      $('#id_location_13').hide();
      $('#id_location_13').prop('checked', false);
      $('#id_location_13').parent().hide();
      $('label[for="id_location_13"]').hide();
      $('#id_location_14').hide();
      $('#id_location_14').prop('checked', false);
      $('#id_location_14').parent().hide();
      $('label[for="id_location_14"]').hide();
      $('#id_location_15').hide();
      $('#id_location_15').prop('checked', false);
      $('#id_location_15').parent().hide();
      $('label[for="id_location_15"]').hide();
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
      $('#location_check_hr').show();
    }
}
  else {
    $('#id_location_0').hide();
    $('#id_location_0').prop('checked', false);
    $('#id_location_0').parent().hide();
    $('label[for="id_location_0"]').hide();
    $('#id_location_1').hide();
    $('#id_location_1').prop('checked', false);
    $('#id_location_1').parent().hide();
    $('label[for="id_location_1"]').hide();
    $('#id_location_2').hide();
    $('#id_location_2').prop('checked', false);
    $('#id_location_2').parent().hide();
    $('label[for="id_location_2"]').hide();
    $('#id_location_3').hide();
    $('#id_location_3').prop('checked', false);
    $('#id_location_3').parent().hide();
    $('label[for="id_location_3"]').hide();
    $('#id_location_4').hide();
    $('#id_location_4').prop('checked', false);
    $('#id_location_4').parent().hide();
    $('label[for="id_location_4"]').hide();
    $('#id_location_5').hide();
    $('#id_location_5').prop('checked', false);
    $('#id_location_5').parent().hide();
    $('label[for="id_location_5"]').hide();
    $('#id_location_6').hide();
    $('#id_location_6').prop('checked', false);
    $('#id_location_6').parent().hide();
    $('label[for="id_location_6"]').hide();
    $('#id_location_7').hide();
    $('#id_location_7').prop('checked', false);
    $('#id_location_7').parent().hide();
    $('label[for="id_location_7"]').hide();
    $('#id_location_8').hide();
    $('#id_location_8').prop('checked', false);
    $('#id_location_8').parent().hide();
    $('label[for="id_location_8"]').hide();
    $('#id_location_9').hide();
    $('#id_location_9').prop('checked', false);
    $('#id_location_9').parent().hide();
    $('label[for="id_location_9"]').hide();
    $('#id_location_10').hide();
    $('#id_location_10').prop('checked', false);
    $('#id_location_10').parent().hide();
    $('label[for="id_location_10"]').hide();
    $('#id_location_11').hide();
    $('#id_location_11').prop('checked', false);
    $('#id_location_11').parent().hide();
    $('label[for="id_location_11"]').hide();
    $('#id_location_12').hide();
    $('#id_location_12').prop('checked', false);
    $('#id_location_12').parent().hide();
    $('label[for="id_location_12"]').hide();
    $('#id_location_13').hide();
    $('#id_location_13').prop('checked', false);
    $('#id_location_13').parent().hide();
    $('label[for="id_location_13"]').hide();
    $('#id_location_14').hide();
    $('#id_location_14').prop('checked', false);
    $('#id_location_14').parent().hide();
    $('label[for="id_location_14"]').hide();
    $('#id_location_15').hide();
    $('#id_location_15').prop('checked', false);
    $('#id_location_15').parent().hide();
    $('label[for="id_location_15"]').hide();
    $('#id_location_16').hide();
    $('#id_location_16').prop('checked', false);
    $('#id_location_16').parent().hide();
    $('label[for="id_location_16"]').hide();
    $('#id_location_17').hide();
    $('#id_location_17').prop('checked', false);
    $('#id_location_17').parent().hide();
    $('label[for="id_location_17"]').hide();
    $('#id_location_18').hide();
    $('#id_location_18').prop('checked', false);
    $('#id_location_18').parent().hide();
    $('label[for="id_location_18"]').hide();
    $('#id_location_19').hide();
    $('#id_location_19').prop('checked', false);
    $('#id_location_19').parent().hide();
    $('label[for="id_location_19"]').hide();
    $('#id_location_20').hide();
    $('#id_location_20').prop('checked', false);
    $('#id_location_20').parent().hide();
    $('label[for="id_location_20"]').hide();
    $('#id_location_21').hide();
    $('#id_location_21').prop('checked', false);
    $('#id_location_21').parent().hide();
    $('label[for="id_location_21"]').hide();
    $('#id_location_22').hide();
    $('#id_location_22').prop('checked', false);
    $('#id_location_22').parent().hide();
    $('label[for="id_location_22"]').hide();
    $('#id_location_23').hide();
    $('#id_location_23').prop('checked', false);
    $('#id_location_23').parent().hide();
    $('label[for="id_location_23"]').hide();
    $('#id_location_24').hide();
    $('#id_location_24').prop('checked', false);
    $('#id_location_24').parent().hide();
    $('label[for="id_location_24"]').hide();
    $('#id_location_25').hide();
    $('#id_location_25').prop('checked', false);
    $('#id_location_25').parent().hide();
    $('label[for="id_location_25"]').hide();
    $('#id_location_26').hide();
    $('#id_location_26').prop('checked', false);
    $('#id_location_26').parent().hide();
    $('label[for="id_location_26"]').hide();
    $('#id_location_27').hide();
    $('#id_location_27').prop('checked', false);
    $('#id_location_27').parent().hide();
    $('label[for="id_location_27"]').hide();
    $('#id_location_28').hide();
    $('#id_location_28').prop('checked', false);
    $('#id_location_28').parent().hide();
    $('label[for="id_location_28"]').hide();
    $('#id_location_29').hide();
    $('#id_location_29').prop('checked', false);
    $('#id_location_29').parent().hide();
    $('label[for="id_location_29"]').hide();
    $('#id_location_30').hide();
    $('#id_location_30').prop('checked', false);
    $('#id_location_30').parent().hide();
    $('label[for="id_location_30"]').hide();
    $('#id_location_31').hide();
    $('#id_location_31').prop('checked', false);
    $('#id_location_31').parent().hide();
    $('label[for="id_location_31"]').hide();
    $('#location_check_hr').hide();
  }
}
*/
// function that checks if the HTML button #lab_check is checked and shows the optional labs Flare model field check boxes, used on #lab_check click
function check_labs() {
  if ($('#lab_check').is(":checked")) {
    $('#div_id_labs').show();
} else {
    $('#div_id_labs').hide();
    $('input', $('#div_id_labs')).each(function() {
    var $this = $(this);
    $this.prop("checked", false);
    })
    $('#urate_fields').hide();
    $('input', $('#urate_fields')).each(function() {
    var $this = $(this);
    $this.val('');
    })
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
    $('input', $('#urate_fields')).each(function() {
    var $this = $(this);
    $this.val('');
    })
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
    $('input', $('#div_id_treatment')).each(function() {
    var $this = $(this);
    $this.prop("checked", false);
    })
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_1() {
  if ($('#id_treatment_1').is(":checked")) {
    $('#colchicine_for_flare').show();
} else {
    $('#colchicine_for_flare').hide();
    $('input', $('#colchicine_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_2() {
  if ($('#id_treatment_2').is(":checked")) {
    $('#ibuprofen_for_flare').show();
} else {
    $('#ibuprofen_for_flare').hide();
    $('input', $('#ibuprofen_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_3() {
  if ($('#id_treatment_3').is(":checked")) {
    $('#naproxen_for_flare').show();
} else {
    $('#naproxen_for_flare').hide();
    $('input', $('#naproxen_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_4() {
  if ($('#id_treatment_4').is(":checked")) {
    $('#celecoxib_for_flare').show();
} else {
    $('#celecoxib_for_flare').hide();
    $('input', $('#celecoxib_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment (#id_treatment_XXX) button is checked and, if so, displays appropriate treatment form
function check_treatment_5() {
  if ($('#id_treatment_5').is(":checked")) {
    $('#meloxicam_for_flare').show();
} else {
    $('#meloxicam_for_flare').hide();
    $('input', $('#meloxicam_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment prednisone (#id_treatment_6) button is checked and, if so, displays appropriate treatment form
function check_treatment_6() {
  if ($('#id_treatment_6').is(":checked")) {
    $('#prednisone_for_flare').show();
} else {
    $('#prednisone_for_flare').hide();
    $('input', $('#prednisone_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment methylprednisolone (#id_treatment_7) button is checked and, if so, displays appropriate treatment form
function check_treatment_7() {
  if ($('#id_treatment_7').is(":checked")) {
    $('#methylprednisolone_for_flare').show();
} else {
    $('#methylprednisolone_for_flare').hide();
    $('input', $('#methylprednisolone_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
  }
}

// function that checks whether Flare model field treatment tinctureoftime (#id_treatment_8) button is checked and, if so, displays appropriate treatment form
function check_treatment_8() {
  if ($('#id_treatment_8').is(":checked")) {
    $('#tinctureoftime_for_flare').show();
} else {
    $('#tinctureoftime_for_flare').hide();
    $('input', $('#tinctureoftime_for_flare')).each(function() {
    var $this = $(this);
    $this.val('');
  })
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

/* FlareAid app JS */
// Function that loads on FlareAid Create page, hides all fields other than the first (perfect_health)
function flare_aid_initial() {
  if ($('#id_anticoagulation-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_bleed-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_CKD-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_Colchicine_Interactions-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_diabetes-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_heartattack-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_IBD-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_osteoporosis-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else if ($('#id_stroke-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else {
    $('#div_id_monoarticular').hide();
    $('#monoarticular-line').hide();
    $('#subfields').hide();
  }
}

function flare_aid_fields () {
  if ($('#id_perfect_health').val() == "True") {
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').hide();
  }
  else if ($('#id_perfect_health').val() == "False") {
    $('#div_id_monoarticular').show();
    $('#monoarticular-line').show();
    $('#subfields').show();
  }
  else {
    $('#div_id_monoarticular').hide();
    $('#monoarticular-line').hide();
    $('#subfields').hide();
  }
}

function flare_aid_dialysis () {
  if ($('#id_CKD-value').is(":checked")) {
    $('#div_id_CKD-dialysis').show();
  }
  else {
    $('#div_id_CKD-dialysis').hide();
    $('#id_CKD-dialysis').prop("checked", false);
  }
}
/* Flare app JS */
// Long if / else if function displaying appropriate HTML form elements for Flare model Create and Update views
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
