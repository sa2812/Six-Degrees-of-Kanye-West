$(document).foundation()

function Expand(obj){
	if ( $(window).width() > 1023) {
		if (!obj.savesize) obj.savesize=obj.size;
		obj.size=Math.max(obj.savesize,obj.value.length);
	}
}

$(function () {
	$('.artist').focus(function () {
		$(this).data('placeholder', $(this).attr('placeholder'))
		.attr('placeholder', '');
		$(this).css('border', '0px solid #9B9B9B');
		$(this).css('border-bottom-width', '3px');
		$(this).css('text-color', '#9B9B9B');
	}).blur(function () {
		$(this).attr('placeholder', $(this).data('placeholder'));
		if (!$(this).val()) {
			$(this).css('border', '0px solid #9B9B9B');
			$(this).css('border-bottom-width', '3px');
			$(this).css('text-color', '#9B9B9B');
		}
	});
});

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-81336038-1', 'auto');
ga('send', 'pageview');
