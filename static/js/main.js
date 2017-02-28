/**
 * Created by dun on 17-2-24.
 */
var IdCode = {

    getIdCode: function (phone) {
        $.ajax({
            type: 'POST',
            url: "api/idcode",
            dataType: 'json',
            data: {phone: phone},
            success: function (result) {
                $(IdCode.targetButton).attr('disabled', 'true');
                IdCode.time = 10;
                IdCode.timer = setInterval(IdCode.refreshTime, 1000)
            }
        })

    },
    refreshTime: function () {
        IdCode.time -= 1;
        console.log(IdCode.time);
        $(IdCode.targetLable).text(IdCode.time + "秒后可重新获取");
        if (IdCode.time == 0) {
            clearInterval(IdCode.timer);
            $(IdCode.targetButton).removeAttr('disabled')
            $(IdCode.targetLable).text("输入验证码");
        }
    }
};


$(document).ready(function () {
    $('.carousel').carousel();
    $('select').material_select();
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15 // Creates a dropdown of 15 years to control year
    });
    $('#getIdCode1').click(function () {
        var idCodeObj1 = IdCode;
        idCodeObj1.targetLable = '#idCodeLable1';
        idCodeObj1.targetButton = '#getIdCode1';
        idCodeObj1.getIdCode($('#contact_phone').val());
    });
    $('#getIdCode2').click(function () {
        var idCodeObj2 = IdCode;
        idCodeObj2.targetLable = '#idCodeLable2';
        idCodeObj1.targetButton = '#getIdCode2';

        idCodeObj2.getIdCode($('#market_phone').val());
    });
    $('#getIdCode3').click(function () {
        var idCodeObj3 = IdCode;
        idCodeObj3.targetLable = '#idCodeLable3';
        idCodeObj1.targetButton = '#getIdCode3';

        idCodeObj3.getIdCode($('#design_phone').val());
    });
    $('#submit_inform').click(function () {
        var formData = new FormData();
        formData.append('name', $('#lost_name').val());
        formData.append('gender', $('#gender').val());
        formData.append('birthday', $('#birthday').val());
        formData.append('lost_date', $('#lost_date').val());
        formData.append('home_loc_province', $('#home_loc_province').val());
        formData.append('home_loc_city', $('#home_loc_city').val());
        formData.append('home_loc_town', $('#home_loc_town').val());
        formData.append('lost_loc_province', $('#lost_loc_province').val());
        formData.append('lost_loc_city', $('#lost_loc_city').val());
        formData.append('lost_loc_town', $('#lost_loc_town').val());
        formData.append('height', $('#height').val());
        formData.append('description', $('#comment').value());
        formData.append('c_name', $('#contact_name').val());
        formData.append('c_tel', $('#c_tel').val());
        formData.append('idCode', $('#idCode1').val());
        formData.append('img', document.getElementById("image").files[0]);

        $.ajax({
            url: 'api / newinform',
            type: 'POST',
            data: formData,
            success:function (result) {
                
            }

        })
    });
    $('#comment').trigger('autoresize');

});
