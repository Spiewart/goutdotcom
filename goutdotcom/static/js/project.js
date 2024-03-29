/* Project specific Javascript goes here. */
/* User Dashboard JS */
// Function that checks the value of an accordion field and changes the color of the accordion button if value == True or == False

/* ProfilesApp JS */
/* MedicalProfile model JS */
// function that checks whether or not leukocytosis is checked and hides/shows WBC, leukopenia fields as appropriate
function leukocytosis_checker() {
// function that checks whether leukocytosis is checked or not, shows wbc, leukopenia fields or hides/empties them
  if ($('#id_leukocytosis-value').is(":checked")) {
      $('#div_id_wbc_leukocytosis-value').show();
      $('#div_id_leukopenia-value').hide();
      $('#id_leukopenia-value').prop("checked", false);
      $('#div_id_wbc_leukopenia-value').hide();
      $('#id_wbc_leukopenia-value').val('');
      $('#leukopenia_col').hide();
  }
  else {
    $('#div_id_wbc_leukocytosis-value').hide();
    $('#id_wbc_leukocytosis-value').val('');
    $('#div_id_leukopenia-value').show();
    $('#leukopenia_col').show();
  }
}

// function that checks whether or not leukopenia is checked and hides/shows WBC, leukocytosis fields as appropriate
function leukopenia_checker() {
// function that checks whether leukopenia is checked or not, shows wbc, leukocytosis fields or hides/empties them
  if ($('#id_leukopenia-value').is(":checked")) {
      $('#div_id_wbc_leukopenia-value').show();
      $('#div_id_leukocytosis-value').hide();
      $('#id_leukocytosis-value').prop("checked", false);
      $('#div_id_wbc_leukocytosis-value').hide();
      $('#id_wbc_leukocytosis-value').val('');
      $('#leukocytosis_col').hide();
  }
  else {
    $('#div_id_wbc_leukopenia-value').hide();
    $('#id_wbc_leukopenia-value').val('');
    $('#div_id_leukocytosis-value').show();
    $('#leukocytosis_col').show();
  }
}

// function that checks whether or not thrombocytosis is checked and hides/shows platelet, thrombocytopenia fields as appropriate
function thrombocytosis_checker() {
// function that checks whether thrombocytosis is checked or not, shows platelet, thrombocytosis fields or hides/empties them
  if ($('#id_thrombocytosis-value').is(":checked")) {
      $('#div_id_platelet_thrombocytosis-value').show();
      $('#div_id_thrombocytopenia-value').hide();
      $('#id_thrombocytopenia-value').prop("checked", false);
      $('#div_id_platelet_thrombocytopenia-value').hide();
      $('#id_platelet_thrombocytopenia-value').val('');
      $('#thrombocytopenia_col').hide();
  }
  else {
    $('#div_id_platelet_thrombocytosis-value').hide();
    $('#id_platelet_thrombocytosis-value').val('');
    $('#div_id_thrombocytopenia-value').show();
    $('#thrombocytopenia_col').show();
  }
}

// function that checks whether or not thrombocytopenia is checked and hides/shows platelet, thrombocytosis fields as appropriate
function thrombocytopenia_checker() {
// function that checks whether thrombocytopenia is checked or not, shows platelet, thrombocytosis fields or hides/empties them
  if ($('#id_thrombocytopenia-value').is(":checked")) {
      $('#div_id_platelet_thrombocytopenia-value').show();
      $('#div_id_thrombocytosis-value').hide();
      $('#id_thrombocytosis-value').prop("checked", false);
      $('#div_id_platelet_thrombocytosis-value').hide();
      $('#id_platelet_thrombocytosis-value').val('');
      $('#thrombocytosis_col').hide();
  }
  else {
    $('#div_id_platelet_thrombocytopenia-value').hide();
    $('#id_platelet_thrombocytopenia-value').val('');
    $('#div_id_thrombocytosis-value').show();
    $('#thrombocytosis_col').show();
  }
}

// function that checks whether or not anemia is checked and hides/shows hemoglobin, polycythemia fields as appropriate
function anemia_checker() {
// function that checks whether anemia is checked or not, shows hemoglobin, polycythemia fields or hides/empties them
  if ($('#id_anemia-value').is(":checked")) {
      $('#div_id_hemoglobin_anemia-value').show();
      $('#div_id_polycythemia-value').hide();
      $('#id_polycythemia-value').prop("checked", false);
      $('#div_id_hemoglobin_polycythemia-value').hide();
      $('#id_hemoglobin_polycythemia-value').val('');
      $('#polycythemia_col').hide();
  }
  else {
    $('#div_id_hemoglobin_anemia-value').hide();
    $('#id_hemoglobin_anemia-value').val('');
    $('#div_id_polycythemia-value').show();
    $('#polycythemia_col').show();
  }
}

// function that checks whether or not polycythemia is checked and hides/shows hemoglobin, anemia fields as appropriate
function polycythemia_checker() {
// function that checks whether polycythemia is checked or not, shows hemoglobin, anemia fields or hides/empties them
  if ($('#id_polycythemia-value').is(":checked")) {
      $('#div_id_hemoglobin_polycythemia-value').show();
      $('#div_id_anemia-value').hide();
      $('#id_anemia-value').prop("checked", false);
      $('#div_id_hemoglobin_anemia-value').hide();
      $('#id_hemoglobin_anemia-value').val('');
      $('#anemia_col').hide();
  }
  else {
    $('#div_id_hemoglobin_polycythemia-value').hide();
    $('#id_hemoglobin_polycythemia-value').val('');
    $('#div_id_anemia-value').show();
    $('#anemia_col').show();
  }
}

// function that checks whether or not transaminitis is checked and hides/shows AST/ALT fields as appropriate
function transaminitis_checker() {
  if ($('#id_transaminitis-value').is(":checked")) {
      $('#div_id_alt_transaminitis-value').show();
      $('#div_id_ast_transaminitis-value').show();
  }
  else {
    $('#div_id_alt_transaminitis-value').hide();
    $('#id_alt_transaminitis-value').val('');
    $('#div_id_ast_transaminitis-value').hide();
    $('#id_ast_transaminitis-value').val('');
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

/* Lab app JS */
// Function that checks whether all the labs were drawn on the same date and hides the model-specific date_drawn form inputs, otherwise displays them individually for each
function date_drawn_checker() {
$('#div_id_alt_form-date_drawn').hide();
$('#div_id_ast_form-date_drawn').hide();
$('#div_id_creatinine_form-date_drawn').hide();
$('#div_id_hemoglobin_form-date_drawn').hide();
$('#div_id_platelet_form-date_drawn').hide();
$('#div_id_wbc_form-date_drawn').hide();
$('#div_id_urate_form-date_drawn').hide();
}

/* ULTAid app JS */
function ULT_exists_checker() {
  var ult = JSON.parse(document.getElementById('user_ult').textContent);
  if (ult == "Indicated") {
    $('#id_need').val('True');
  }
  else if (ult == "Conditional") {
    $('#id_need').val('True');
  }
  else if (ult == "Not Indicated") {
    $('#id_need').val('False');
  }
  else if (ult == "Dialysis") {
    $('#id_need').val('False');
  }
}

function need_want_checker() {
// function that checks whether need/want are checked and shows subfields <div> if both True
  if ($('#id_need').val() == 'True' && $('#id_want').val() == 'True') {
    $('#subfields').show();
  }
  // length == 0 works for checking whether id_need is in the form or not
  else if ($('#id_need').length == 0 && $('#id_want').val() == 'True') {
    $('#subfields').show();
  }

  else {
    $('#subfields').hide();
  }
}

// function that checks whether or not CKD is checked and hides/shows dialysis/stage fields as appropriate
function CKD_checker() {
// function that checks whether CKD is checked or not, shows dialysis and stage fields or hides/empties them
  if ($('#id_CKD-value').is(":checked")) {
      $('#div_id_CKD-dialysis').show();
      $('#div_id_CKD-stage').show();
      $('#div_id_creatinine_CKD-value').show();
  }
  else {
    $('#div_id_CKD-dialysis').hide();
    $('#id_CKD-dialysis').prop("checked", false);
    $('#div_id_CKD-stage').hide();
    $('#id_CKD-stage_1').prop("checked", false);
    $('#id_CKD-stage_2').prop("checked", false);
    $('#id_CKD-stage_3').prop("checked", false);
    $('#id_CKD-stage_4').prop("checked", false);
    $('#id_CKD-stage_5').prop("checked", false);
    $('#div_id_creatinine_CKD-value').hide();
    $('#id_creatinine_CKD-value').val('');
  }
}

function transplant_checker() {
// function that checks whether CKD is checked or not, shows dialysis and stage fields or hides/empties them
  if ($('#id_organ_transplant-value').is(":checked")) {
      $('#div_id_organ_transplant-organ').show();
  }
  else {
    $('#div_id_organ_transplant-organ').hide();
    $('#id_organ_transplant-organ_1').prop("checked", false);
    $('#id_organ_transplant-organ_2').prop("checked", false);
    $('#id_organ_transplant-organ_3').prop("checked", false);
    $('#id_organ_transplant-organ_4').prop("checked", false);
    $('#id_organ_transplant-organ_5').prop("checked", false);
    $('#id_organ_transplant-organ_6').prop("checked", false);
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
      $('#num_flares-line').show();
      $('#div_id_freq_flares').hide();
      $('#freq_flares-line').hide();
      $('#div_id_freq_flares').val('');
      $('#subfields').hide();
      $('#subfields-line').hide();
  }
  else if ($('#id_num_flares').val() == 'zero') {
      $('#num_flares-line').show();
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('');
      $('#freq_flares-line').hide();
      $('#subfields').hide();
      $('#subfields-line').hide();
  }
  else if ($('#id_num_flares').val() == 'one') {
      $('#num_flares-line').show();
      $('#div_id_freq_flares').hide();
      $('#div_id_freq_flares').val('one');
      $('#freq_flares-line').hide();
      $('#subfields').show();
      $('#subfields-line').show();
  }
  else {
      $('#num_flares-line').show();
      $('#div_id_freq_flares').show();
      $('#freq_flares-line').show();
      $('#subfields').show();
      $('#subfields-line').show();
  }
}

function check_subfields() {
// function that checks whether the user already has some MedicalProfile fields that are shown on the ULT form
  $('#subfields input[type=checkbox]').each(function() {
    if ($(this).is(":checked")) {
      $('#subfields').show();
      $('#subfields-line').show();
    }
  })
}

function check_ckd() {
// function that checks whether CKD is checked or not, shows dialysis field or hides/empties it
  if ($('#id_CKD-value').is(":checked")) {
      $('#div_id_CKD-dialysis').show();
      $('#div_id_CKD-stage').show();
  }
  else {
    $('#div_id_CKD-dialysis').hide();
    $('#div_id_CKD-stage').hide();
    $('#id_CKD-dialysis').prop("checked", false);
    $('#id_CKD-stage').prop("checked", false);
  }
}

/* FlareApp JS flare_form.html */
/* Manages Location of Flare form fields */
function mono_vs_poly() {
  if ($('#id_monoarticular_1').is(":checked")) {
    $('#div_id_firstmtp').show();
    if ($('#id_firstmtp_1').is(":checked")) {
      $('#div_id_location').hide();
      $('#symptoms').show();
      $('#id_location_1').prop("checked", false);
      $('#id_location_2').prop("checked", false);
      $('#id_location_3').prop("checked", false);
      $('#id_location_4').prop("checked", false);
      $('#id_location_5').prop("checked", false);
      $('#id_location_6').prop("checked", false);
      $('#id_location_7').prop("checked", false);
      $('#id_location_8').prop("checked", false);
      $('#id_location_9').prop("checked", false);
      $('#id_location_10').prop("checked", false);
      $('#id_location_11').prop("checked", false);
      $('#id_location_12').prop("checked", false);
      $('#id_location_13').prop("checked", false);
      $('#id_location_14').prop("checked", false);
      $('#id_location_15').prop("checked", false);
      $('#id_location_16').prop("checked", false);
    } else if ($('#id_firstmtp_2').is(":checked")) {
      $('#div_id_location').show();
      $('#symptoms').show();
    } else {
        $('#div_id_location').hide();
        $('#symptoms').hide();
        $('#id_location_1').prop("checked", false);
        $('#id_location_2').prop("checked", false);
        $('#id_location_3').prop("checked", false);
        $('#id_location_4').prop("checked", false);
        $('#id_location_5').prop("checked", false);
        $('#id_location_6').prop("checked", false);
        $('#id_location_7').prop("checked", false);
        $('#id_location_8').prop("checked", false);
        $('#id_location_9').prop("checked", false);
        $('#id_location_10').prop("checked", false);
        $('#id_location_11').prop("checked", false);
        $('#id_location_12').prop("checked", false);
        $('#id_location_13').prop("checked", false);
        $('#id_location_14').prop("checked", false);
        $('#id_location_15').prop("checked", false);
        $('#id_location_16').prop("checked", false);
    }
  } else if ($('#id_monoarticular_2').is(":checked")) {
    $('#div_id_firstmtp').show();
    $('#div_id_location').show();
    if ($('#id_firstmtp_1').is(":checked")) {
      $('#symptoms').show();
    } else if ($('#id_firstmtp_2').is(":checked")) {
      $('#symptoms').show();
    } else {
      $('#symptoms').hide();
    }
  } else {
    $('#div_id_firstmtp').hide();
    $('#div_id_location').hide();
    $('#symptoms').hide();
  }
}

/* Manages Symptoms of Flare form fields */
function symptoms() {
  if ($('#id_onset_1').is(":checked")) {
    $('#div_id_duration').show();
    if($('#id_duration').val()) {
      $('#div_id_redness').show();
      if ($('#id_redness_1').is(":checked")) {
        $('#history').show();
      } else if ($('#id_redness_2').is(":checked")) {
        $('#history').show();
      } else {
        $('#history').hide();
      }
    } else {
      $('#div_id_redness').hide();
      $('#history').hide();
    }
  } else if ($('#id_onset_2').is(":checked")) {
    $('#div_id_duration').show();
      if($('#id_duration').val()) {
        $('#div_id_redness').show();
        if ($('#id_redness_1').is(":checked")) {
          $('#history').show();
        } else if ($('#id_redness_2').is(":checked")) {
          $('#history').show();
        } else {
          $('#history').hide();
        }
      } else {
        $('#div_id_redness').hide();
        $('#history').hide();
      }
  } else {
    $('#div_id_duration').hide();
    $('#div_id_redness').hide();
    $('#history').hide();
  }
}

/* Manages History of Flare form fields */
function history() {
  if ($('#id_male_1').is(":checked")) {
    $('#div_id_prior_gout').show();
    if($('#id_prior_gout_1').is(":checked")) {
      $('#urate_fields').show();
      $('#cardiacdiseases').show();
      $('#treatment').show();
      $('#submit-flare').show();
    } else if($('#id_prior_gout_2').is(":checked")) {
        $('#urate_fields').show();
        $('#cardiacdiseases').show();
        $('#treatment').show();
        $('#submit-flare').show();
    } else {
      $('#urate_fields').hide();
      $('#cardiacdiseases').hide();
      $('#treatment').hide();
      $('#submit-flare').hide();
    }
  } else if ($('#id_male_2').is(":checked")) {
    $('#div_id_prior_gout').show();
      if($('#id_prior_gout_1').is(":checked")) {
        $('#urate_fields').show();
        $('#cardiacdiseases').show();
        $('#treatment').show();
        $('#submit-flare').show();
      } else if($('#id_prior_gout_2').is(":checked")) {
        $('#urate_fields').show();
        $('#cardiacdiseases').show();
        $('#treatment').show();
        $('#submit-flare').show();
      } else {
        $('#urate_fields').hide();
        $('#cardiacdiseases').hide();
        $('#treatment').hide();
        $('#submit-flare').hide();
      }
  } else {
    $('#div_id_prior_gout').hide();
    $('#urate_fields').hide();
    $('#cardiacdiseases').hide();
    $('#treatment').hide();
    $('#submit-flare').hide();
  }
}

/* FlareAidApp JS */
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
  else if ($('#id_Osteoporosis-value').is(":checked")) {
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

/* PPxAidApp JS */
// Function that loads on PPxAid Create page, hides all fields other than the first (perfect_health)
function ppx_aid_initial() {
  if ($('#id_anticoagulation-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_bleed-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_CKD-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_ColchicineInteractions-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_diabetes-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_heartattack-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_IBD-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_Osteoporosis-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else if ($('#id_stroke-value').is(":checked")) {
    $('#id_perfect_health').val('False');
    $('#subfields').show();
  }
  else {
    $('#subfields').hide();
  }
}

function ppx_aid_fields () {
  if ($('#id_perfect_health').val() == "True") {
    $('#subfields').hide();
  }
  else if ($('#id_perfect_health').val() == "False") {
    $('#subfields').show();
  }
  else {
    $('#subfields').hide();
  }
}

function ppx_aid_dialysis () {
  if ($('#id_CKD-value').is(":checked")) {
    $('#div_id_CKD-dialysis').show();
    $('#div_id_CKD-stage').show();
  }
  else {
    $('#div_id_CKD-stage').hide();
    $('#id_CKD-stage').prop("checked", false);
    $('#div_id_CKD-dialysis').hide();
    $('#id_CKD-dialysis').prop("checked", false);
  }
}
