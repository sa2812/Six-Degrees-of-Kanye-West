$(document).foundation()

function Expand(obj){
	if ( $(window).width() > 1023) {
		if (!obj.savesize) obj.savesize=obj.size;
		obj.size=Math.max(obj.savesize,obj.value.length);
	}
}

$(function () {
	$('input,textarea').focus(function () {
		$(this).data('placeholder', $(this).attr('placeholder'))
		.attr('placeholder', '');
		$(this).css('border', '0px solid #9B9B9B');
		$(this).css('border-bottom-width', '3px');
		$(this).css('text-color', '#9B9B9B');
	}).blur(function () {
		$(this).attr('placeholder', $(this).data('placeholder'));
		if (!$(this).val()) {
			$(this).css('border', '0px solid #CB5959');
			$(this).css('border-bottom-width', '3px');
			$(this).css('text-color', '#CB5959');
		}
	});
});

$(function() {
	$("form input").keypress(function (e) {
		if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
			if ($('input').val()) {
				$('button[type=submit] .default').click();
				console.log($(this).val());
				$('.artist').val('');
				return false;	
			}
		} else {
			return true;
		}
		return false;
	});
});