function trToggle(index_to_toggle) {
                $(".hide-fast"+index_to_toggle).toggle();
                $(".hide"+index_to_toggle).toggle('slow');
            }

function hideAllPopovers() {
                $("a[rel=popover]").popover('hide');
            }
