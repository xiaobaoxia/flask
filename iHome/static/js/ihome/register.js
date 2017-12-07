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
    // TODO: 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    $.ajax({
    url:"/api/v1.0/smscode",    //请求的url地址
    dataType:"json",   //返回格式为json
    contentType: "application/json",
    headers: {"X-CSRFToken": getCookie('csrf_token')},
    async:true,//请求是否异步，默认为异步，这也是ajax重要特性
    data:JSON.stringify(json_data),    //参数值
    type:"POST",   //请求方式 get 或者post
    beforeSend:function(){
        //请求前的处理
    },
    success:function(req){
        //请求成功时处理

    },
    complete:function(){
        //请求完成的处理
    },
    error:function(){
        //请求出错处理
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

    // TODO: 注册的提交(判断参数是否为空)
})
