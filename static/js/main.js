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
            $(IdCode.targetButton).removeAttr('disabled');
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
        re = /^1\d{10}$/;
        if (re.test($('#contact_phone').val())) {
            var idCodeObj1 = IdCode;
            idCodeObj1.targetLable = '#idCodeLable1';
            idCodeObj1.targetButton = '#getIdCode1';
            idCodeObj1.getIdCode($('#contact_phone').val());
        }
        else {
            $('#contact_phone').addClass('invalid')
        }

    });
    $('#getIdCode2').click(function () {
        re = /^1\d{10}$/;
        if (re.test($('#join_phone').val())) {
            var idCodeObj2 = IdCode;
            idCodeObj2.targetLable = '#idCodeLable2';
            idCodeObj2.targetButton = '#getIdCode2';

            idCodeObj2.getIdCode($('#join_phone').val());
        }
        else {
            $('#join_phone').addClass('invalid')
        }

    });

    $('#newProfile').click(function () {
        if (!$('#idCode1').val()) {
            $('#idCode1').addClass('invalid')
        }
        else {
            var formData = new FormData();
            formData.append('lost_name', $('#lost_name').removeClass('invalid').val());
            formData.append('gender', $('#gender').removeClass('invalid').val());
            formData.append('birthday', $('#birthday').removeClass('invalid').val());
            formData.append('lost_date', $('#lost_date').removeClass('invalid').val());
            formData.append('lost_loc_province', $('#lost_loc_province').removeClass('invalid').val());
            formData.append('lost_loc_city', $('#lost_loc_city').removeClass('invalid').val());
            formData.append('lost_loc_town', $('#lost_loc_town').removeClass('invalid').val());
            formData.append('height', $('#height').removeClass('invalid').val());
            formData.append('description', $('#description').removeClass('invalid').val());
            formData.append('contact_name', $('#contact_name').removeClass('invalid').val());
            formData.append('contact_phone', $('#contact_phone').removeClass('invalid').val());
            formData.append('idCode', $('#idCode1').removeClass('invalid').val());
            formData.append('img', document.getElementById("image").files[0]);

            $.ajax({
                url: 'api/profile',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function (result) {
                    if (result['status'] == 'lacked') {
                        result['msg'].forEach(function (v, k) {
                            $('#' + v).removeClass('valid').addClass('invalid')
                        })
                    }
                    if (result['status'] == 'nopic') {
                        $('#image').removeClass('valid').addClass('invalid')
                    }
                    if (result['status'] == 'wrongcode') {
                        $('#idCode1').removeClass('valid').addClass('invalid')
                    }
                }

            })

        }
    });
        $('#newMember').click(function () {
        if (!$('#idCode2').val()) {
            $('#idCode2').addClass('invalid')
        }
        else {
            var formDataJoin = new FormData();
            formDataJoin.append('join_name', $('#join_name').removeClass('invalid').val());
            formDataJoin.append('join_description', $('#join_description').removeClass('invalid').val());
            formDataJoin.append('join_phone', $('#join_phone').removeClass('invalid').val());
            formDataJoin.append('idCode', $('#idCode2').removeClass('invalid').val());

            $.ajax({
                url: '/api/member',
                type: 'POST',
                data: formDataJoin,
                contentType: false,
                processData: false,
                success: function (result) {
                    if (result['status'] == 'lacked') {
                        result['msg'].forEach(function (v, k) {
                            $('#' + v).removeClass('valid').addClass('invalid')
                        })
                    }
                    if (result['status'] == 'wrongcode') {
                        $('#idCode2').removeClass('valid').addClass('invalid')
                    }
                }

            })

        }
    });
    $('#description').trigger('autoresize');

});
