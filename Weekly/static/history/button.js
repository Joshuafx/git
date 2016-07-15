define(function(require,exports){
	require('jquery')

	var button = function(type){
		$(document).ready(function(){
			var url1 = '/history_' + type + '_delete'
			var url2 = '/history_' + type + '_event'
			var url3 = '/history_' + type + '_ip'
			var url4 = '/history_' + type + '_business'

			//删除按钮
			$('#delete').click(function(){
				number_event = document.getElementById("event_history_table").rows.length - 1;
				number_ip = document.getElementById("ip_history_table").rows.length - 1;
				number_business = document.getElementById("business_history_table").rows.length - 1;
				for (i=0;i<number_event;i++) {
					id ='#delete_event'+ i;
					name = "event"+i
					if ($(id).is(':checked') == true){
						$(id).next().attr("name",name)
					}
				}

				for (i=0;i<number_ip;i++) {
					id ='#delete_ip'+ i;
					name = "ip"+i
					if ($(id).is(':checked') == true){
						$(id).next().attr("name",name)
					}
				}
			
				for (i=0;i<number_business;i++) {
					id ='#delete_business'+ i;
					name = "business"+i
					if ($(id).is(':checked') == true){
						$(id).next().attr("name",name)
					}
				}
			
				$('#rows_event').val(number_event);
				$('#rows_ip').val(number_ip);
				$('#rows_business').val(number_business);
			
				$('#all_history').attr('action',url1);			
				$('#all_history').submit();								
			})


			//调出历史数据
			$('input[id^=Event]').click(function(){
				var value = $(this).val();
				$('h1').after("<form id='open'  method='post'><input type='text' id='table_name' name='table_name' style='display:none' /></form>");
				$('#table_name').attr('value',value);
				$('#open').attr('action',url2);
				$('#open').submit();
 			})

		
			$('input[id^=Ip]').click(function(){
				var value = $(this).val();
				$('h1').after("<form id='open' method='post'><input type='text' id='table_name' name='table_name' style='display:none' /></form>");
				$('#table_name').attr('value',value);
				$('#open').attr('action',url3);
				$('#open').submit();
			})

		
			$('input[id^=Business]').click(function(){
				var value = $(this).val();
				$('h1').after("<form id='open' method='post'><input type='text' id='table_name' name='table_name' style='display:none' /></form>");
				$('#table_name').attr('value',value);
				$('#open').attr('action',url4);
				$('#open').submit();
			})
		})
	}

	exports.button = button;

})