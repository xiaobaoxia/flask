function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get('/api/v1.0/areas', function (resp) {
       if (resp.errno == '0'){
           for (var i=0; i<resp.data.length; i++){
               $("#area-id").append('<option value="'+resp.data[i].aid+'">'+resp.data[i].aname+'</option>')
           }
       } else {
           alert(resp.errmsg)
       }
    });

    // TODO: 处理房屋基本信息提交的表单数据
    $("#form-house-info").submit(function (e) {
        e.preventDefault();

        var params = {};
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value
        });
        var facility = [];
        $(":checkbox:checked").each(function (i, j) {
            facility[i] = j.value
        });
        params['facility'] = facility;
        $.ajax({
            url: '/api/v1.0/house',
            data: JSON.stringify(params),
            contentType: 'application/json',
            type: 'post',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    $("#form-house-info").hide();
                    $("#form-house-image").show();
                }else if (resp.errno == '4101'){
                    location.href = '/login.html'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    });
    // TODO: 处理图片表单的数据
    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/api/v1.0/house/image',
            type: 'post',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (resp) {
                if (resp.errno == '0'){
                    alert('添加成功')
                }else if (resp.errno == '4101'){
                    location.href = '/login.html'
                }else {
                    alert(resp.errmsg)
                }
            }
        })
    })
});