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
    $(".button-collapse").sideNav();
    $('select').material_select();
    $('.modal').modal();
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
    $('#getIdCode3').click(function () {
        re = /^1\d{10}$/;
        if (re.test($('#phone').val())) {
            var idCodeObj3 = IdCode;
            idCodeObj3.targetLable = '#idCodeLable3';
            idCodeObj3.targetButton = '#getIdCode3';
            idCodeObj3.getIdCode($('#phone').val());
        }
        else {
            $('#phone').addClass('invalid')
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
                    if (result['status'] == 'ok') {
                        alert('信息录入成功，我们将尽快审核，如成功将用短信通知您')
                    }
                }

            })

        }
    });
    $('#newClu').click(function () {
        if (!$('#idCode1').val()) {
            $('#idCode1').addClass('invalid')
        }
        else {
            var formData = new FormData();
            formData.append('find_date', $('#find_date').removeClass('invalid').val());
            formData.append('find_loc_province', $('#find_loc_province').removeClass('invalid').val());
            formData.append('find_loc_city', $('#find_loc_city').removeClass('invalid').val());
            formData.append('find_loc_town', $('#find_loc_town').removeClass('invalid').val());
            formData.append('description', $('#description').removeClass('invalid').val());
            formData.append('contact_name', $('#contact_name').removeClass('invalid').val());
            formData.append('contact_phone', $('#contact_phone').removeClass('invalid').val());
            formData.append('idCode', $('#idCode1').removeClass('invalid').val());
            formData.append('img', document.getElementById("image").files[0]);

            $.ajax({
                url: 'api/clu',
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
                    if (result['status'] == 'ok') {
                        alert('信息录入成功，我们将尽快审核，如成功将用短信通知您')
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
                    if (result['status'] == 'ok') {
                        alert('信息录入成功，我们将尽快审核，如成功将用短信通知您')
                    }
                }

            })

        }
    });
    $('#login').click(function () {
        if (!$('#idCode3').val()) {
            $('#idCode3').addClass('invalid')
        }
        else {
            var formDataJoin = new FormData();
            formDataJoin.append('phone', $('#phone').removeClass('invalid').val());
            formDataJoin.append('idCode', $('#idCode1').removeClass('invalid').val());
            formDataJoin.append('password', $('#password').removeClass('invalid').val());
            $.ajax({
                url: '/api/login',
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
                        $('#idCode1').removeClass('valid').addClass('invalid')
                    }
                    if(result['status']=='ok'){
                        window.location.href = "/admin";
                    }

                }

            })

        }
    });

    $('#description').trigger('autoresize');
    var input = document.getElementById("image");
    var result, div;


    if (typeof FileReader === 'undefined') {
        result.innerHTML = "抱歉，你的浏览器不支持 FileReader";
        input.setAttribute('disabled', 'disabled');
    } else {
        if (input) {
            input.addEventListener('change', readFile, false);

        }
        else {
            return 0
        }
    }　　　　//handler
    function readFile() {

        if (!input['value'].match(/.jpg|.gif|.png|.bmp/i)) {　　//判断上传文件格式
            return alert("上传的图片格式不正确，请重新选择")
        }
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
        reader.onload = function (e) {
            result = '<div class="card"><div class="card-image" id="result" align="center"><img src="' + this.result + '" alt="" style="width:100%"/></div></div>';
            dataResult = this.result;
            document.getElementById('uploadContainer').innerHTML = result;
        }

    }
});
