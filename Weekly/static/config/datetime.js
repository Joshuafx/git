define(function(require){
//引入datetimepicker所需的模块并定义日历插件
	require('jquery');
	require('../modules/datetimepicker/js/bootstrap.min.js');
	require('../modules/datetimepicker/js/moment.min.js');
	require('../modules/datetimepicker/js/bootstrap-datetimepicker.min.js');

	$(document).ready(function(){
	
		$('input[id^=startime]').datetimepicker({
		    format: 'YYYY-MM-DD HH:mm'
		})

		$('input[id^=endtime]').datetimepicker({
		    format: 'YYYY-MM-DD HH:mm'
		})
		
	})

})