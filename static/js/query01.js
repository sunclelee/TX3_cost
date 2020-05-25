$(function() {
	$('#softvalue').hide();  //隐藏滑块输入框
	$('#pinggu').click(function() { //当提交表单时，会发生 submit 事件。
		//此处可做表单验证
		var fm = document.getElementsByTagName('form')[0];	
		var yxb = Trim(fm.yxb.value);
		if (fm.module.value == 'yxb') {
			if (!/^http:\/\/bang.tx3.163.com\/bang\/role\/\d{1,3}_\d{3,9}$/.test(yxb)) {
				alert('英雄榜链接格式不正确');
				//fm.username.value = ''; //清空
				fm.yxb.focus(); //将焦点以至表单字段
				return false;
			}	
		}
		else if (fm.module.value == 'name'){
			if (!/^[\u4e00-\u9fa5]{3,4}-/.test(yxb)) {
				alert('角色名称格式不正确');
				//fm.username.value = ''; //清空
				fm.yxb.focus(); //将焦点以至表单字段
				return false;
			}
		}

		//var postData = $("#form1").serialize(); //序列化表单，后台可正常通过post方法获取数据
		var role=$('#yxb').val();
		var queryType = $('#module').val();
		var clothesNum = $('#clothNum').val();
		var riderNum = $('#riderNum').val();
		var clothes = [];
		var riders = [];
		$("input[name='clothList']:checked").each(function(i){//把所有被选中的复选框的值存入数组
			clothes[i] =$(this).val();
		});
		$("input[name='riderList']:checked").each(function(i){//把所有被选中的复选框的值存入数组
			riders[i] =$(this).val();
		});
		//验证时装数量和珍兽数量输入是否合法,需同时满足三个条件才算合法：是数字，数量大于等于选择量，没有小数点
		if (isNaN(clothesNum) || (clothesNum < clothes.length) || (clothesNum.indexOf('.')>=0)){
			alert('时装数量输入有误');
			$('#clothNum').focus();
			return false;
		} 
		if (isNaN(riderNum) || (riderNum < riders.length) || (riderNum.indexOf('.')>=0)){
			alert('珍兽数量输入有误');
			$('#riderNum').focus();
			return false;
		} 
		//验证通过，开始传值
		var yuanhunzhuNum = $("input[name='yuanhunzhu']:checked").val();
		var vip = $("input[name='vip']:checked").val();
		var isExtra;
		if (document.getElementById('extra').style.display == "block") {
			isExtra = true;
		}	else {
			isExtra = false;
		}
		
		var data= {
			data: JSON.stringify({
				'role': role,
				'module':queryType,
				'clothesList':clothes,
				'clothesNum':clothesNum,
				'riders':riders,
				'riderNum':riderNum,
				'yuanhunzhu':yuanhunzhuNum,
				'vip':vip,
				'softvalue':$('#softvalue').val(),
				'isExtra':isExtra
			}),
		}
		
		$.ajax({
			type: "POST",
			url: "/sendAjax",
			data: data,
			dataType: 'json',
			beforeSend: function() {
				$("#pinggu").attr({ disabled: "disabled" });//提交表单前的处理，防止用户多次点击【登陆】，重复提交表单
				$('#footer').html('正在评估中');
				//显示加载器.for jQuery Mobile 1.2.0
				$.mobile.loading('show', {
					text: '正在评估中...', //加载器中显示的文字
					textVisible: true, //是否显示文字
					theme: 'a',        //加载器主题样式a-e
					textonly: false,   //是否只显示文字
					html: ""           //要显示的html内容，如图片等
				});
				_hmt.push(['_trackPageview', '/sendAjax']);  //百度统计PV	 			
			},
			success:function(res){
				$('#result').empty();
				var html = '';
				for (var val in res) {
					//alert(val + " " + res[val]);
					html = html + '<b>' + val + '</b>：' + res[val] + '<br>';					
				}
				$.mobile.loading('hide');  
				$('#result').css("text-align","center");
				$('#result').html(html);
				$("#pinggu").prop("disabled",false);
                $("#pinggu").val("点击评估");
				$('#footer').html('评估结果仅供参考');		 			
			},
			error:function(res){
				$.mobile.loading('hide'); 
				console.log(res);
				$('#result').empty();
				$('#footer').html('评估出错了！');
			},
		});
	});
});
	
function Trim(str){ 
    return str.replace(/(^\s*)|(\s*$)/g, ""); 
}

function submitTest(){
	var fm = document.getElementsByTagName('form')[0];	
	var yxb = Trim(fm.yxb.value);
	if (fm.module.value == 'yxb') {
		if (!/^http:\/\/bang.tx3.163.com\/bang\/role\/\d{1,3}_\d{3,9}$/.test(yxb)) {
			alert('英雄榜链接格式不正确');
			//fm.username.value = ''; //清空
			fm.yxb.focus(); //将焦点以至表单字段
			return false;
		}	
	}
	else if (fm.module.value == 'name'){
		if (!/^[\u4e00-\u9fa5]{3,4}-/.test(yxb)) {
			alert('角色名称格式不正确');
			//fm.username.value = ''; //清空
			fm.yxb.focus(); //将焦点以至表单字段
			return false;
		}
	}
	return true;
}

function setPrompt(){
	var aaa = document.getElementById('module');
	var bbb = document.getElementById('yxb');
	if (aaa.value == 'yxb') {
		bbb.placeholder = '请输入英雄榜，要带http://';
	}
	else if (aaa.value == 'name') {
		bbb.placeholder = '请输入“服务器-角色全名”';
	}
}

//切换右上图标及展开补充内容
function display(){
	var a = document.getElementById('extra').style.display;
	if (a == "none") {
		document.getElementById('extra').style.display = "block";
		var b = document.getElementById('addinfo').getAttribute("class").replace("ui-icon-plus","ui-icon-minus");
		document.getElementById('addinfo').setAttribute("class",b);
	}  else if (a == "block") {
		document.getElementById('extra').style.display = "none";
		var c = document.getElementById('addinfo').getAttribute("class").replace("ui-icon-minus","ui-icon-plus");
		document.getElementById('addinfo').setAttribute("class",c);
	}
}