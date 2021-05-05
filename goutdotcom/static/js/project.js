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

function check_treatment() {
  if ($('#id_treatment').val() == "Colcrys") {
    $('#div_id_colchicine').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Advil") {
    $('#div_id_ibuprofen').show();
    $('#div_id_colchicine').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Aleve") {
    $('#div_id_naproxen').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_colchicine').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Celebrex") {
    $('#div_id_celecoxib').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_colchicine').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Mobic") {
    $('#div_id_meloxicam').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_colchicine').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Pred") {
    $('#div_id_prednisone').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_colchicine').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_methylprednisolone').hide();
} else if ($('#id_treatment').val() == "Methylpred") {
    $('#div_id_methylprednisolone').show();
    $('#div_id_ibuprofen').hide();
    $('#div_id_colchicine').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
} 
  else {
    $('#div_id_colchicine').hide();
    $('#div_id_ibuprofen').hide();
    $('#div_id_naproxen').hide();
    $('#div_id_celecoxib').hide();
    $('#div_id_meloxicam').hide();
    $('#div_id_prednisone').hide();
    $('#div_id_methylprednisolone').hide();
  }   
}

function check_urate_draw() {
  if ($('#id_urate_draw').val() == 'True') {
      $('#div_id_urate_log').show();
} 
  else {
    $('#div_id_urate_log').hide();
    $('#div_id_urate').hide();
    $('#div_id_uric_acid').hide();
  }   
}

function check_urate_desire() {
  if ($('#id_urate_log').val() == "Already logged it") {
    $('#div_id_urate').show();
    $('#div_id_uric_acid').hide();
  }   
  else if ($('#id_urate_log').val() == "Will log it now") {
    $('#div_id_urate').hide();
    $('#div_id_uric_acid').show();
  } 
  else {
    $('#div_id_urate').hide();
    $('#div_id_uric_acid').hide();
  } 
}

function flare_base() {
  $('#urate-logged').hide();
  $('#urate-desire').hide();
  $('#treatment-logged').hide();
  $('#treatment-desire').hide();
  $('#flare-no-urate-button').hide();
  $('#flare-with-urate-button').hide();
}

function urate_decider() {
  if ($('#urate-decision').val() == "No") {
    $('#urate-decision').hide();
    $('#urate-logged').hide();
    $('#urate-desire').hide();
    $('#flare-no-urate-button').show();
  } 
  else if ($('#urate-decision').val() == "Yes") {
    if ($('#urate-logged').val() == "Yes") {
      $('#urate-logged').hide();
      $('#flare-no-urate-button').show();
      $('#flare-with-urate-button').hide();
      $('#urate-desire').hide();
    }
    else if ($('#urate-logged').val() == "No") {
      if ($('#urate-desire').val() == "No") {
        $('#urate-desire').hide();
        $('#flare-no-urate-button').show();
        $('#flare-with-urate-button').hide();
      }
      else if ($('#urate-desire').val() == "Yes") {
        $('#urate-desire').hide();
        $('#flare-no-urate-button').hide();
        $('#flare-with-urate-button').show();
      }
      else {
        $('#urate-logged').hide();
        $('#urate-desire').show();
        $('#flare-no-urate-button').hide();
        $('#flare-with-urate-button').hide();
      }
    }
    else {
      $('#urate-decision').hide();
      $('#urate-logged').show();
      $('#flare-no-urate-button').hide();
      $('#flare-with-urate-button').hide();
    }
  }
  else {
    $('#urate-logged').hide();
    $('#urate-desire').hide();
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