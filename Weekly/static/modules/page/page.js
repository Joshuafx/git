define(function(require,exports){
	require('jquery');
 	
 	var page = function(table) {
		$(document).ready(function(){
			var rowAll = document.getElementById(table).rows;
			var rowNumber = rowAll.length;
			
			//设置每页最大行数
			var rowMax = 20;
	        var theCount = rowMax + 1
			
			//当前页数和全部页数和总行数
			var nowPage = 1;
			$("#now_page").val(nowPage);
			var allPage = Math.ceil((rowNumber-1)/rowMax);
			$("#all_page").val(allPage);
			$("#all_row").val(rowNumber-1)
			
			//隐藏第一页后的内容
			if (rowNumber > rowMax)
			{
			    for (i=rowMax+1;i<rowNumber;i++)
				{
					rowAll[i].setAttribute("style","display:none;");
				}
				
			}
			
			//下一页按钮功能
			$("#next_page").click(function(){
				var checkboxes = $("input[type=checkbox]"); 
				var number = checkboxes.length;
				if(theCount<rowNumber)
				{
					if (rowNumber<theCount+rowMax)
				    { 
					    var x = rowNumber ;
				    }
				    else
				    {
					    var x = theCount + rowMax;
				    }
				    for (i=theCount;i<x;i++)
				    {
					
					    rowAll[i].setAttribute("style","display:table-row;");
				    }
				
				    for (i=theCount-1;i>theCount-1-rowMax;i--)
				    {
					    rowAll[i].setAttribute("style","display:none;");
				    }
				    theCount += rowMax;
					nowPage += 1;
			        $("#now_page").val(nowPage);
				}

				for (var i=0;i<number;i++) {
					if (checkboxes.eq(i).parent().parent().css('display')=='none'){
						document.getElementById('delete'+i).checked=false;
					}
				}
				
			})
			
			//上一页按钮功能
			$("#prev_page").click(function(){
				var x = 2*rowMax;
				var checkboxes = $("input[type=checkbox]"); 
				var number = checkboxes.length;
				if (theCount-x>0)   
				{	
			        if (theCount > rowNumber)
					{
						 for (i=theCount-rowMax;i<rowNumber;i++)
					    {
						    rowAll[i].setAttribute("style","display:none;");
					    }
					}
					else
					{
					    for (i=theCount-rowMax;i<theCount;i++)
					    {
						    rowAll[i].setAttribute("style","display:none;");
					    }
					}
					
					for (i=theCount-x;i<theCount-rowMax;i++)
					{
						rowAll[i].setAttribute("style","display:table-row;");
					}
					theCount -=rowMax;
					nowPage -= 1;
			        $("#now_page").val(nowPage);
				}

				for (var i=0;i<number;i++) {
					if (checkboxes.eq(i).parent().parent().css('display')=='none'){
						document.getElementById('delete'+i).checked=false;
					}
				}
				
			})
    
   		 })

	}

	exports.page = page;

})