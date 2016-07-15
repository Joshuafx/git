define(function(require){
	require('jquery')

	$(document).ready(function(){
		//保存按钮
		$('#save').click(function(){
			$('#basic').attr('action','/basic_save')
			$('#basic').submit();
		})
		

		//删除按钮
		$('#delete').click(function(){
			number = 8;
			for (i=0;i<number;i++) {
				id ='#delete'+ i;
				if ($(id).is(':checked') == true){
					$(id).parent('td').parent('tr').remove();
				}
			}
			$('#basic').attr('action','/basic_delete');	
			$('#basic').submit();					
		})


		//全选按钮
		$("#both").click(function(){
			var checkboxes = $("input[type=checkbox]"); 
			var number = checkboxes.length;
			var clear = 0;
			for(var i=0;i<number;i++) {
				var Id = 'delete' + i;
				var checks = document.getElementById(Id);
				if (checks.checked==false) {
					checks.checked=true;
					clear += 1;
				}
			}
			if (clear==0) {
				for (var i=0;i<number;i++) {
					document.getElementById('delete'+i).checked=false;
				}
			}
		})		

	})


})