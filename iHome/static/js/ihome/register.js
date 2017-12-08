function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
var imageCodeId = "";
var preimageCodeId = "";
// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    imageCodeId = generateUUID();
    url = '/api/v1.0/imagecode?cur=' + imageCodeId + '&pre=' + preimageCodeId;
    $('.image-code>img').attr('src', url);
    preimageCodeId = imageCodeId

}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var json_data = {'mobile': mobile, 'image_code': imageCode, 'image_code_id': imageCodeId };
    // 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    $.ajax({
    url:"/api/v1.0/smscode",    //请求的url地址
    dataType:"json",   //返回格式为json
    contentType: "application/json",
    headers: {"X-CSRFToken": getCookie('csrf_token')},
    async:true,//请求是否异步，默认为异步，这也是ajax重要特性
    data:JSON.stringify(json_data),    //参数值
    type:"POST",   //请求方式 get 或者post
    success:function(resp){
        //请求成功时处理
        generateImageCode();
        // alert('短信验证码已发送');
        if (resp.errno == 0){
            var num = 60;
            var t = setInterval(function () {
                num -= 1;
                if (num == 0){
                    clearInterval(t);
                    $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    $(".phonecode-a").html("获取验证码")

                }else {

                    $(".phonecode-a").html(num+'秒')
                }
            }, 1000, 60)
        }else if (resp.errno == 4103) {
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
            $("#mobile-err span").html(resp.errmsg);
            $("#mobile-err").show();
            alert(resp.errmsg)
        }else if (resp.errno == 4004){
            $("#image-code-err span").html(resp.errmsg);
            $("#image-code-err").show();
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
        }else if (resp.errno == 4003){
            $(".phonecode-a").attr("onclick", "sendSMSCode();");
            $("#mobile-err span").html(resp.errmsg);
            $("#mobile-err").show();
        }

    },
    error:function () {
        generateImageCode();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        alert('服务器错误, 请重试')
    }
});
}

$(document).ready(function() {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    // 注册的提交(判断参数是否为空)
    $('.form-register').submit(function (e) {
        e.preventDefault();
        mobile = $("#mobile").val();
        phonecode = $("#phonecode").val();
        password = $("#password").val();
        password2 = $("#password2").val();

        if (!mobile){
            $("#mobile-err span").html('请填写正确的手机号!');
            $("#mobile-err").show();
            return;
        }
        if (!phonecode){
            $("#phone-code-err span").html('请填写短信验证码!');
            $("#phone-code-err").show();
            return;
        }
        if (!password){
            $("#password-err span").html('请填写密码!');
            $("#password-err").show();
            return;
        }
        if (password != password2){
            $("#password2-err span").html('两次密码不一致!');
            $("#password2-err").show();
            return;
        }
        // todo: 发送ajax注册账号
        json_data = {'mobile': mobile, 'phonecode': phonecode,
                    'password': password, 'password2': password2};
         $.ajax({
             url: "/api/v1.0/user",    //请求的url地址
             dataType: "json",   //返回格式为json
             contentType: "application/json",
             headers: {"X-CSRFToken": getCookie('csrf_token')},
             async: true,//请求是否异步，默认为异步，这也是ajax重要特性
             data: JSON.stringify(json_data),    //参数值
             type: "POST",   //请求方式 get 或者post
             success:function (resp) {
                if (resp.errno == '0'){
                    location.href('/')
                }
                else{
                    $("#password2-err span").html(resp.errmsg);
                    $("#password2-err").show();
                }
             }
         });
    });
});
