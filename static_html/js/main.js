function trToggle(index_to_toggle) {
                $(".hide-fast"+index_to_toggle).toggle();
                $(".hide"+index_to_toggle).toggle('slow');
            }

function hideAllPopovers() {
                $("a[rel=popover]").popover('hide');
            }

// $(document).ready(function (){
//     $("a[rel=popover]").popover();
// });
$(document).ready(function (){
    $("a[rel=popover]")
      .popover()
      .click(function(e) {
        e.preventDefault()
      })
});