define(function(require,exports,module){
	require('jquery');
	
	$(document).ready(function(){
		//报警量激增列表
		$('#new_table').click(function(){
			$('#new_table_menu').slideToggle('slow');
		})

		//展示图
		$('#chart').click(function(){
			$('#chart_menu').slideToggle('slow');
		})

		//历史数据
   		$('#history_data').click(function(){
			$('#history_data_menu').slideToggle('slow');
		})

   		//配置参数
		$('#congfig').click(function(){
			window.open('/config','_self');				
		})

		//以事件类型为主的报警量激增列表
		$('#event_table').click(function(){
			window.open('/event_table','_self');
		})

		//以IP为主的报警量激增列表
		$('#ip_table').click(function(){
			window.open('/ip_table','_self');
		})

		//以业务为主的报警量激增列表
		$('#business_table').click(function(){
			window.open('/business_table','_self');
		})

		//基本信息表
		$('#basic_table').click(function(){
			window.open('/basic_table','_self');
		})

		//历史数据-原始数据
		$('#history_data_data').click(function(){
			window.open('/history_data','_self');
		})

		//历史数据-计算结果
		$('#history_data_result').click(function(){
			window.open('/history_result','_self');
		})

    })
})