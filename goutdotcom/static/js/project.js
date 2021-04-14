/* Project specific Javascript goes here. */

// function that hides/shows field_four based upon first_flare value
function check_first_flare(new_val) {
    if(new_val == false) {
        // #id_field_four should be actually the id of the HTML element
        // that surrounds everything you want to hide.  Since you did
        // not post your HTML I can't finish this part for you.
        $('#div_id_num_flares').addClass('hidden');
    } else {
        $('#div_id_num_flares').removeClass('hidden');
    }   
  }
    // this is executed once when the page loads
  $(document).ready(function() {
    // set things up so my function will be called when first_flare
    $('#id_first_flare').change( function() {
      check_first_flare(this.value);
      alert("Hi");
    });
  });


