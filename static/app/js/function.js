// 自动回调用户购物车金额
function money() {
    $.get('/app/money/', function (data) {
        if (data.code == '200'){
            $('#summoney').html(data.money)
        }

    })
}

money()


// 自动回调用户是否全选
function check_all() {
    $.get('/app/check_all/', function (data) {

        if (data.ch == '1'){
            $('#checkbox_all').prop("checked",true);
        }else {
            $('#checkbox_all').prop("checked",false);
        }

    })
}
check_all()


//自动回调目前选中商品数量
function cartnum() {
    $.get('/app/cartnum/',function (data) {
        if (data.code == '200'){
            $('#cartallnum').html(data.selectncartnum)
        }
    })
}
cartnum()


// 添加数量
function add(good_id) {
    var value = $('#cartnum').attr('value')
    value = parseInt(value)+1
    $("#cartnum").attr("value",value);
    $.post('/app/good_add_money/',{'good_id':good_id,'num': value}, function (data) {
        $('#total_value').html(data.money)

    })


}

//减少数量
function minus(good_id) {
    var value = $('#cartnum').attr('value')
    value = parseInt(value)-1
    if (value <= 0){ value = 0}
    $("#cartnum").attr("value",value);
    $.post('/app/good_minus_money/',{'good_id':good_id,'num': value}, function (data) {
        $('#total_value').html(data.money)

    })
}

//加入购物车
function addcart(good_id) {

    var num =  $('#cartnum').attr('value')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/app/addcart/',
        type: 'POST',
        dataType:'json',
         headers:{'X-CSRFToken':csrf},
        data:{'good_id': good_id, 'num':num},
        success:function(data){
            console.log(data)
            if (data.code == '200'){
                alert('添加成功')
                 $("#cartnum").attr("value",1);
            }
        },
        error:function(data){
            alert('添加失败')
        }
    })
}


//直接购买
function shop(good_id) {

    var num =  $('#cartnum').attr('value')
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/app/shop/',
        type: 'POST',
        dataType:'json',
         headers:{'X-CSRFToken':csrf},
        data:{'good_id': good_id, 'num':num},
        success:function(data){
            console.log(data)
            if (data.code == '200'){
                alert('添加成功')
                 $("#cartnum").attr("value",1);
            }
        },
        error:function(data){
            alert('添加失败')
        }
    })
}





// 添加购物车当中的数量
function add_cart_goods(cartgood_id) {

    var value = $('#cartgoodnum_'+cartgood_id).attr('value')
    value = parseInt(value)+1
    $('#cartgoodnum_'+cartgood_id).attr("value",value);
    $.post('/app/alter_cart_goods/',{'cartgood_id':cartgood_id,'num': value}, function (data) {
        if (data.code == '200'){
            var cartmoney = parseFloat(data.pirce) * value

            $('#cartmoney_'+cartgood_id).html(String(cartmoney.toFixed(2))+'元')
            money()

        }
    })
}



//减少购物车中的数量
function minus_cart_goods(cartgood_id) {
    var value = $('#cartgoodnum_'+cartgood_id).attr('value')
    value = parseInt(value)-1
    $('#cartgoodnum_'+cartgood_id).attr("value",value);

    $.post('/app/alter_cart_goods/',{'cartgood_id':cartgood_id,'num': value}, function (data) {
        if (data.code == '200'){
            if (value == 0){
                  $('#good_'+cartgood_id).remove()
            }
             var cartmoney = parseFloat(data.pirce) * value
             $('#cartmoney_'+cartgood_id).html(String(cartmoney.toFixed(2))+'元')
            money()
        }
    })
}






//单选
function radio(cartgood_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/app/alter_cart_select/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'cartgood_id': cartgood_id},
        success: function (data) {
            if (data.select == '0'){
                check_all()
                 money()
                cartnum()
            }
           else {
                check_all()
                money()
                cartnum()
            }
        },
        error: function (data) {
        }
    })
}

//全选
function allcheck() {
    $.get('/app/goodsall/',function (data) {
        money()
        cartnum()
        if (data.status == '1'){
            for (var i = 0 ; i <= data.cartlist.length; i++){
                $('#checked_'+data.cartlist[i]).prop("checked",true);
            }
        }else {

            for(var i = 0 ; i <= data.cartlist.length; i++){
                 $('#checked_'+data.cartlist[i]).prop("checked",false);
            }
        }
    })
  
   
}






















