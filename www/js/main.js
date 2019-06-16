$(function(){
	$('.navbar-collapse li a').click(function(){
		$('.navbar-collapse').collapse('hide');
	});


	var onResize = function(){
		var scrollWidth = $(window).width();
		scrollWidth = scrollWidth - (scrollWidth % (g.c.ITEM_WIDTH + g.c.ITEM_MARGIN)) - g.c.ITEM_MARGIN;
		$('.pw-width').width(scrollWidth);
	};

	resizeScheduled = false;
	$(window).on('resize', function(){
		if(!resizeScheduled) { //debounce
			setTimeout(function(){
				onResize();
				resizeScheduled = false;
			}, 500);
			resizeScheduled = true;
		}
	});
	onResize();
});

var modal = null;
function openModal(entry) {
	if (!modal) {
		modal = $('<div class="modal">').appendTo(document.body);
		$('<h2>' + entry.title + '</h2>').appendTo(modal);
	}

}

function closeModal() {
	if (modal) {
		$(doucument).remove(modal);
		modal = null;
	} else {
		throw Error('there is no modal to close!');
	}
}
