function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息
    $.get('/api/v1.0/user/auth', function (resp) {
        if (resp.errno == '0'){
            if (resp.data.real_name && resp.data.id_card){
                $("#real-name").val(resp.data.real_name);
                $("#id-card").val(resp.data.id_card);
                $("#real-name").prop('disabled', true);
                $("#id-card").prop('disabled', true);
                $(".btn-success").hide();
            }
        }else if (resp.errno == '4101'){
            location.href = '/login.html'
        }else {
            alert(resp.errmsg)
        }
    });

    // TODO: 管理实名信息表单的提交行为
    $("#form-auth").submit(function (e) {
        e.preventDefault();
        var real_name = $("#real-name").val();
        var id_card = $("#id-card").val();

        if (!real_name || !id_card){
            $(".error-msg").show();
            return
        }
        var pattern = /^[\u4E00-\u9FA5]{1,6}$/;
        if (!pattern.test(real_name)){
            $("#real-name").focus();
            alert('姓名有误');
            return
        }
        var reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
        if (!reg.test(id_card)){
            alert('身份证有误');
            $("#id-card").focus();
            return
        }

        $(".error-msg").hide();
        data = {
            'real_name': real_name,
            'id_card': id_card
        };
        $.ajax({
            url: '/api/v1.0/user/auth',
            type: 'post',
            data: JSON.stringify(data),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    showSuccessMsg();
                    $("#real-name").prop('disabled', true);
                    $("#id-card").prop('disabled', true);
                    $(".btn-success").hide();
                }else if (resp.errno == '4101'){
                    location.href = '/login.html'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })
});