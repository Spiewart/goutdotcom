/* Project specific Javascript goes here. */

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


function check_treatment_1() {
  if ($('#id_treatment_1').is(":checked")) {
    $('#colchicine_for_flare').show();
} else {
    $('#colchicine_for_flare').hide();
    $('#colchicine_for_flare').find('#id_dose').val('');
    $('#colchicine_for_flare').find('#id_freq').val('');
    $('#colchicine_for_flare').find('#date_started').val('');
    $('#colchicine_for_flare').find('#id_date_ended').val('');
    $('#colchicine_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_2() {
  if ($('#id_treatment_2').is(":checked")) {
    $('#ibuprofen_for_flare').show();
} else {
    $('#ibuprofen_for_flare').hide();
    $('#ibuprofen_for_flare').find('#id_dose').val('');
    $('#ibuprofen_for_flare').find('#id_freq').val('');
    $('#ibuprofen_for_flare').find('#date_started').val('');
    $('#ibuprofen_for_flare').find('#id_date_ended').val('');
    $('#ibuprofen_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_3() {
  if ($('#id_treatment_3').is(":checked")) {
    $('#naproxen_for_flare').show();
} else {
    $('#naproxen_for_flare').hide();
    $('#naproxen_for_flare').find('#id_dose').val('');
    $('#naproxen_for_flare').find('#id_freq').val('');
    $('#naproxen_for_flare').find('#date_started').val('');
    $('#naproxen_for_flare').find('#id_date_ended').val('');
    $('#naproxen_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_4() {
  if ($('#id_treatment_4').is(":checked")) {
    $('#celecoxib_for_flare').show();
} else {
    $('#celecoxib_for_flare').hide();
    $('#celecoxib_for_flare').find('#id_dose').val('');
    $('#celecoxib_for_flare').find('#id_freq').val('');
    $('#celecoxib_for_flare').find('#date_started').val('');
    $('#celecoxib_for_flare').find('#id_date_ended').val('');
    $('#celecoxib_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_5() {
  if ($('#id_treatment_5').is(":checked")) {
    $('#meloxicam_for_flare').show();
} else {
    $('#meloxicam_for_flare').hide();
    $('#meloxicam_for_flare').find('#id_dose').val('');
    $('#meloxicam_for_flare').find('#id_freq').val('');
    $('#meloxicam_for_flare').find('#date_started').val('');
    $('#meloxicam_for_flare').find('#id_date_ended').val('');
    $('#meloxicam_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_6() {
  if ($('#id_treatment_6').is(":checked")) {
    $('#prednisone_for_flare').show();
} else {
    $('#prednisone_for_flare').hide();
    $('#prednisone_for_flare').find('#id_dose').val('');
    $('#prednisone_for_flare').find('#id_freq').val('');
    $('#prednisone_for_flare').find('#date_started').val('');
    $('#prednisone_for_flare').find('#id_date_ended').val('');
    $('#prednisone_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_7() {
  if ($('#id_treatment_7').is(":checked")) {
    $('#methylprednisolone_for_flare').show();
} else {
    $('#methylprednisolone_for_flare').hide();
    $('#methylprednisolone_for_flare').find('#id_dose').val('');
    $('#methylprednisolone_for_flare').find('#id_freq').val('');
    $('#methylprednisolone_for_flare').find('#date_started').val('');
    $('#methylprednisolone_for_flare').find('#id_date_ended').val('');
    $('#methylprednisolone_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_8() {
  if ($('#id_treatment_8').is(":checked")) {
    $('#tinctureoftime_for_flare').show();
} else {
    $('#tinctureoftime_for_flare').hide();
    $('#tinctureoftime_for_flare').find('#id_duration').val('');
    $('#tinctureoftime_for_flare').find('#id_dose').val('');
    $('#tinctureoftime_for_flare').find('#id_freq').val('');
    $('#tinctureoftime_for_flare').find('#date_started').val('');
    $('#tinctureoftime_for_flare').find('#id_date_ended').val('');
    $('#tinctureoftime_for_flare').find('#id_side_effects').val('');
  }
}

function check_treatment_9() {
  if ($('#id_treatment_9').is(":checked")) {
    $('#othertreat_for_flare').show();
} else {
    $('#othertreat_for_flare').hide();
    $('#othertreat_for_flare').find('#id_name').val('');
    $('#othertreat_for_flare').find('#id_description').val('');
    $('#othertreat_for_flare').find('#id_dose').val('');
    $('#othertreat_for_flare').find('#id_freq').val('');
    $('#othertreat_for_flare').find('#date_started').val('');
    $('#othertreat_for_flare').find('#id_date_ended').val('');
    $('#othertreat_for_flare').find('#id_side_effects').val('');
  }
}

function flare_base() {
  $('#urate-logged-div').hide();
  $('#urate-desire-div').hide();
  $('#treatment-logged-div').hide();
  $('#treatment-desire-div').hide();
  $('#flare-no-urate-button').hide();
  $('#flare-with-urate-button').hide();
}

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

function treatment_decider() {
  if ($('#treatment-logged').val() == "Yes") {
    $('#treatment-desire').show();
  }
  else if ($('#treatment-logged').val() == "No") {
    $('#treatment-desire').hide();
  }
}
