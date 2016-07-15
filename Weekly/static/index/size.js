define(function(require,exports,module){
	require('jquery');

	$(document).ready(function(){
		
		function theSize() {	    
  	    	//导航区高度
  	    	$('#panel').height($(window).height() - $('#logo').outerHeight(true));
          //内容区高度
  	    	$('#content').width($(window).width() - $('#panel').outerWidth(true)); 
          $('#content').height($(window).height() - $('#logo').outerHeight(true));  		
  	    }
  	    theSize();
        
        //动态改边
        $(window).resize(function(){
  	    	theSize();
  	    })
	})

})