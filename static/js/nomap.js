/**
 * Created by lidad on 2017/3/15.
 */
var nomapHandle = function () {
    if ($('#innerDituhuiMapFlash').text()) {
        $('#innerDituhuiMapFlash').remove()
    }
};
$(document).ready(
    function () {
        setTimeout(nomapHandle,1000);
    }
);

