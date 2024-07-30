function bindCaptchaButtonClick() {
    //用于绑定对应的按钮。通过id去绑定
    $("#captcha-btn").on("click",function (event) {
       var email= $("input[name='email']").val();//获取输入框的值
        if (!email){
            alert("请先输入邮箱");
            return;
        }
        //通过js发送网络请求：ajax
        $.ajax(
            {
                url:"/user/captcha",
                method:'POST',
                data:{
                    "email":email
                },
                success:function (res) {
                    var code=res['code'];
                    if (code == 200){
                        //取消点击事件
                        $("#captcha-btn").off("click");
                        //验证码倒计时60秒
                        var countDown=60;
                        //setInterval为倒计时函数
                        var timer=setInterval(function () {
                            countDown--;
                            if (countDown>0) {
                                $("#captcha-btn").text(countDown + "秒后可重新发送");
                            }
                            else {
                                $("#captcha-btn").text("获取验证码");
                                //重新执行函数,重新绑定点击时间
                                bindCaptchaButtonClick();
                                //清除倒计时
                                clearInterval(timer);
                            }

                        },1000);
                        alert("验证码发送成功！");
                    }
                    else {alert(res['message']);}
                }
            }
        )
    });
}
//前面有个$可以使里面的函数在网页全部加载完成后再执行
$(function () {
    bindCaptchaButtonClick();
})