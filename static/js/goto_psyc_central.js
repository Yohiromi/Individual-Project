function bindClick() {
    //用于绑定对应的按钮。通过id去绑定
    $("#psyc_central").on("click", function (event) {
        var psyc_id = $("input[name='psyc_id']").val();//获取输入框的值
        if (!psyc_id) {
            alert("获取失败");
            return;
        }
        //通过js发送网络请求：ajax
        $.ajax(
            {
                url: "/psychologist/get_psychologist",
                method: 'POST',
                data: {
                    "psyc_id": psyc_id
                },
                success: function (result) {
                    var code=result['code'];
                    if (code==200)
                    {
                        alert("success");
                    }

                },
                error: function () {
                    alert('错误');
                }
            }
        )
    });
}

//前面有个$可以使里面的函数在网页全部加载完成后再执行
$(function () {
    bindClick();
})