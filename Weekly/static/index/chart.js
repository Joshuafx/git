define(function(require){
	require('jquery')
	require('../modules/highcharts/highcharts.js')
	require('../modules/highcharts/exporting')
	$(document).ready(function(){
		$("#chart_everyday").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'everyday' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'line'
 						},
 						
 						title:{
 							text:'每日报警量趋势图'
 						},
 						
 						xAxis:{
 							title:{
 								text:'日期'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},
 						
 						plotOptions: {
    						line:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})





	
		$("#chart_time").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'time' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'line'
 						},
 						
 						title:{
 							text:'分时报警量趋势图'
 						},
 						
 						xAxis:{
 							title:{
 								text:'时间'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},

 						plotOptions: {
    						line:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})




		$("#top_event").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'top_event' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'line'
 						},
 						
 						title:{
 							text:'事件报警基本信息'
 						},
 						
 						xAxis:{
 							title:{
 								text:null
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							},
							title:{
 								text:null
 							},
 						
 						},
 						
 						series: [
 							{
 							name:'报警类型',
 							type:'column',
 							data:data['value1']},

 							{
 							name:'报警累计比',
 							type:'line',
 							data:data['value2']
 							}
							
 						],

 						legend:{
 							align:'center',
 							verticalAlign:'bottom'

 						},

 						credits:{
 							enabled:false
 						},

 						plotOptions: {
    						line:{
       							dataLabels: {
            						enabled: true
        						}
   							},
    						column:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})




		$("#top_first").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'top_first' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'column'
 						},
 						
 						title:{
 							text:'一线报警前十事件统计'
 						},
 						
 						xAxis:{
 							title:{
 								text:'事件名称'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},
 						
 						plotOptions: {
    						column:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})



		$("#top_second").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'top_second' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'column'
 						},
 						
 						title:{
 							text:'二线报警前十事件统计'
 						},
 						
 						xAxis:{
 							title:{
 								text:'事件名称'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},

 						plotOptions: {
    						column:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})



		$("#top_ip").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'top_ip' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'column'
 						},
 						
 						title:{
 							text:'报警前十IP'
 						},
 						
 						xAxis:{
 							title:{
 								text:'物理IP'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},

  						plotOptions: {
    						column:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})




		$("#top_business").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'top_business' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'column'
 						},
 						
 						title:{
 							text:'报警前十业务'
 						},
 						
 						xAxis:{
 							title:{
 								text:'主要业务'
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [{
 							name:'汇总',
 							data:data['value']
 							
 						}],

 						legend:{
 							align:'right',
 							verticalAlign:'middle'

 						},

 						credits:{
 							enabled:false
 						},

  						plotOptions: {
    						column:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
 					})

    			})
			})

		})



		$("#chart_core").click(function(){
			$('#content').children().remove();
			$('#content').append("<div id='charts' style='width:800px;height:400px;margin:auto;margin-top:10%;'></div>");
			$.post('/charts',{ 'type':'chart_core' },function(data){
			    $(function(){
 					$('#charts').highcharts({
 						chart:{
 							type:'line'
 						},
 						
 						title:{
 							text:'核心业务相关'
 						},
 						
 						xAxis:{
 							title:{
 								text:null
 							},
 							categories: data['name']

 						},
 						
 						yAxis:{
							title:{
 								text:null
 							}
 						},
 						
 						series: [
 						   {
 							name:'OPENET',
 							data:data['value1']
 							},
 							{
 							name:'OPENAV',
 							data:data['value2']
 							},
 							{
 							name:'配载',
 							data:data['value3']
 							}
 						],

 						legend:{
 							align:'center',
 							verticalAlign:'bottom'

 						},

 						credits:{
 							enabled:false
 						},

  						plotOptions: {
    						line:{
       							dataLabels: {
            						enabled: true
        						}
   							}
					    }
  					})

    			})
			})

		})





	})
})