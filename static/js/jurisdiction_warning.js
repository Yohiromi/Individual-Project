function bindCaptchaButtonClick() {
    //用于绑定对应的按钮。通过id去绑定
    $("#input_wenjuan").on("click",function (event) {
       var jurisdiction= $("input[name='user_jurisdiction']").val();//获取输入框的值
        if (jurisdiction!="管理员"){
            alert("您没有权限访问！");
            return;
        }
    });
}
//前面有个$可以使里面的函数在网页全部加载完成后再执行
$(function () {
    bindCaptchaButtonClick();
})