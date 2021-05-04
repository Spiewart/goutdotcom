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