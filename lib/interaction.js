$(document).ready(
    function(){
	/* menu */
	$('li.menu_sections')
	    .mouseenter(function(){$(this).children('*').css('display', 'block'); })
	    .mouseleave( function(){ $(this).children('*').css('display', 'none'); })	
    }

)
