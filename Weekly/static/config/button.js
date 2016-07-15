define(function(require){
	require('jquery');

	
	$(document).ready(function(){	
		//显示剔除参数按钮功能
		$("#show_filter").click(function(){
			var select = $("#filter").children("div")
			if (select.eq(0).css("display")=="block"&&select.eq(1).css("display")=="block"&&select.eq(2).css("display")=="block")
				select.slideUp("slow")
			else
				select.slideDown("slow")
		})

		var time_count = $("#time_list").children('li').length;
		var event_count = $("#event_list").children('li').length;
		var ip_count=$("#ip_list").children('li').length;

		//添加剔除参数时间、事件、ip选项功能
		var addObject = function(button,id,type,count) {
			$(button).click(function(){
			count += 1;
				if (type=="time") {
					$(id).append("<li>从&nbsp<input type='text' style='width:8em;'/>&nbsp到&nbsp<input type='text' style='width:8em;'/><img id='minus' alt='点我删除' title='删除' src='../static/config/img/minus.png'></li>");
					$(id).children("li").last().children("input").first().attr({"id":"star"+type+count,"name":"star"+type+count});
					$(id).children("li").last().children("input").last().attr({"id":"end"+type+count,"name":"end"+type+count});
					$(id).children("li").last().children("input").datetimepicker({
		   				format: 'YYYY-MM-DD HH:mm'
					})
				 }
				else {
					if (type=="event"){
						$(id).append("<li><input type='text' style='width:20em;'/><img id='minus' alt='点我删除' title='删除' src='../static/config/img/minus.png'></li>");
				    }
				    if (type=="ip"){
						$(id).append("<li><input type='text' style='width:8em;'/><img id='minus' alt='点我删除' title='删除' src='../static/config/img/minus.png'></li>");
				    }
				    $(id).children("li").last().children("input").attr({"id":type+count,"name":type+count});
				}
			})
		}

		addObject("#add_time","#time_list","time",time_count);
		addObject("#add_event","#event_list","event",event_count);
		addObject("#add_ip","#ip_list","ip",ip_count);

		//删除剔除参数选项功能
		$("ol").delegate("#minus","click",function(){
			$(this).parent('li').remove();
		})


	})








})