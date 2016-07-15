define(function(require,exports){
	require('jquery')
	
	var button = function(type,config) {
		$(document).ready(function(){
			
			


			if (config==1){
				
				var tableId = type + "_data_table";
				var formId = '#' + type + '_data';
				var theUrl = '/' + type;
				var detailTable = '#' + type + '_detail_table';
				var detailForm = '#' + type + '_detail'

				//保存按钮
				$('#save').click(function(){
					number = document.getElementById(tableId).rows.length - 1;
					$('#rows').val(number);
					$(formId).attr('action',theUrl+'_save_data')
					$(formId).submit();
				})
		

				//计算按钮
				$('#result').click(function(){
					number = document.getElementById(tableId).rows.length - 1;
					$('#rows').val(number);
					$(formId).attr('action',theUrl+'_result')
					$(formId).submit();
				})


				//删除按钮
				$('#delete').click(function(){
					number = document.getElementById(tableId).rows.length - 1;
					for (i=0;i<number;i++) {
						id ='#delete'+ i;
						if ($(id).is(':checked') == true){
							$(id).parent('td').parent('tr').remove();
						}
					}
					$('#rows').val(number);
					$(formId).attr('action',theUrl+'_delete');	
					$(formId).submit();					
				})


				//详细信息按钮
				$("img[id^=detail]").click(function(){
					var info = $(this).prev() .val()
					$.post(theUrl+'_detail',{ type:info },function(data){
						$(detailTable).children('tbody').children().remove();
							for (n in data)
							{
								var text = "<tr>"+"<td>"+data[n][0]+"</td>"+"<td>"+data[n][1]+"</td>"+"<td>"+data[n][2]+"</td>"+"<td>"+data[n][3]+"</td>"+"<td>"+data[n][4]+"</td>"+"<td>"+data[n][5]+"</td>"+"<td>"+data[n][6]+"</td>"+"</tr>"
								$(detailTable).children('tbody').append(text)
							}
						$(formId).hide();
						$(detailForm).show();
					})
				})


				//返回按钮
				$('#return').click(function(){
					$(detailTable).children('tbody').children().remove();
					$(detailForm).hide();
					$(formId).show();
				})


				//全选按钮
				$("#both").click(function(){
					var checkboxes = $("input[type=checkbox]"); 
					var number = checkboxes.length;
					var clear = 0;
					for(var i=0;i<number;i++) {
						var Id = 'delete' + i;
						var checks = document.getElementById(Id);
						if (checks.checked==false&&checkboxes.eq(i).parent().parent().css('display')!='none') {
							checks.checked=true;
							clear += 1;
						}
					}
					if (clear==0) {
						for (var i=0;i<number;i++) {
							if (checkboxes.eq(i).parent().parent().css('display')!='none'){
								document.getElementById('delete'+i).checked=false;
							}
						}
					}

				})
			}

			







			if (config==2) {
				
				var tableId = type + "_result_table";
				var formId = '#' + type + '_result';
				var theUrl = '/' + type;

				//保存按钮
				$('#save').click(function(){
					number = document.getElementById(tableId).rows.length - 1;
					$('#rows').val(number);
					$(formId).attr('action',theUrl+'_save_result')
					$(formId).submit();
				})
		

				//删除按钮
				$('#delete').click(function(){
					number = document.getElementById(tableId).rows.length - 1;
					for (i=0;i<number;i++) {
						id ='#delete'+ i;
						if ($(id).is(':checked') == true){
							$(id).parent('td').parent('tr').remove();
						}
					}
					$('#rows').val(number);
					$(formId).attr('action',theUrl+'_result_delete');	
					$(formId).submit();					
				})


				$("#both").click(function(){
					var checkboxes = $("input[type=checkbox]"); 
					var number = checkboxes.length;
					var clear = 0;
					for(var i=0;i<number;i++) {
						var Id = 'delete' + i;
						var checks = document.getElementById(Id);
						if (checks.checked==false&&checkboxes.eq(i).parent().parent().css('display')!='none') {
							checks.checked=true;
							clear += 1;
						}
					}
					if (clear==0) {
						for (var i=0;i<number;i++) {
							if (checkboxes.eq(i).parent().parent().css('display')!='none'){
								document.getElementById('delete'+i).checked=false;
							}
						}
					}

				})
			
			}




		})




	}

	
	exports.button = button


})