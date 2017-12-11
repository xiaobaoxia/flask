function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // TODO: 获取该房屋的详细信息
    $.get('/api/v1.0/houses/' + houseId, function (resp) {
        if (resp.errno == '0'){
            if (resp.data.user_id != resp.data.house_info.user_id){
                $(".book-house").attr('href', '/booking.html?hid='+houseId)
                $(".book-house").show();
            };
            $(".swiper-container").html(template('house-image-tmpl', {'img_urls': resp.data.house_info.img_urls, 'price': resp.data.house_info.price}))
            // TODO: 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            $(".detail-con").html(template('house-detail-tmpl', {'house': resp.data.house_info}))
        }else {
            alert(resp.errmsg)
        }
    });


})