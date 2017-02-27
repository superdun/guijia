/**
 * Created by dun on 17-2-24.
 */

    $(document).ready(function(){
        $('.carousel').carousel();
        $('select').material_select();
        $('.datepicker').pickadate({
            selectMonths: true, // Creates a dropdown to control month
            selectYears: 15 // Creates a dropdown of 15 years to control year
        });
        $('#comment').trigger('autoresize');

    });
