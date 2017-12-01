var hide_page = false;
django.jQuery(document).ready(function(){
    if (django.jQuery('#id_address').is(':checked')) {
        django.jQuery(".field-gps_location").show();
        hide_page=true;
    }
    else {
        django.jQuery(".field-gps_location").hide();
        hide_page=false;
    }

    django.jQuery("#id_address").click(function(){
        hide_page = !hide_page;
        if(hide_page) {
            django.jQuery(".field-gps_location").show();
        }
        else {
            django.jQuery(".field-gps_location").hide();
        }
    })
});
