function tglinkclick(){
  var href =  $("#tg-link").attr("href");
  if(href == "/login")
  {
    alert("请先登录!");
  }
};

// 表单验证
function validate_required(field,alerttxt)
{
with (field)
  {
  if (value==null||value=="")
    {alert(alerttxt);return false}
  else {return true}
  }
}
// 提示登录
function alert_login(){
  alert("请先登录!");
}
// 禁用回车提交表单
function ban_enter_key()
{
  if(event.keyCode==13){
    return false;
  }
}
