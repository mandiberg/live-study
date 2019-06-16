$(function() {
  $(".navbar-collapse li a").click(function() {
    $(".navbar-collapse").collapse("hide");
  });

  var onResize = function() {
    var scrollWidth = $(window).width();
    scrollWidth =
      scrollWidth -
      (scrollWidth % (g.c.ITEM_WIDTH + g.c.ITEM_MARGIN)) -
      g.c.ITEM_MARGIN;
    $(".pw-width").width(scrollWidth);
  };

  resizeScheduled = false;
  $(window).on("resize", function() {
    if (!resizeScheduled) {
      //debounce
      setTimeout(function() {
        onResize();
        resizeScheduled = false;
      }, 500);
      resizeScheduled = true;
    }
  });
  onResize();
});

var modal = null;

function getVideoSize() {
  var videoRatio = g.c.VIDEO_WIDTH / g.c.VIDEO_HEIGHT;
  var videoWidth = window.innerWidth - 2 * g.c.MODAL_MARGIN;
  videoWidth = Math.min(videoWidth, g.c.MAX_VIDEO_WIDTH)
  var videoHeight = videoWidth / videoRatio;
  if (videoHeight > window.innerHeight - 2 * g.c.MODAL_MARGIN) {
    videoHeight = window.innerHeight - 2 * g.c.MODAL_MARGIN;
    videoWidth = videoHeight * videoRatio;
  }
  return {
    videoHeight: videoHeight,
    videoWidth: videoWidth
  };
}

function openModal(entry) {
  if (!modal) {
    modal = $('<div>').appendTo(document.body);
  }
  var data = jQuery.extend(getVideoSize(), entry);
  console.log(data);
  var modalContents = g.tmpl("modal")(data);
  modal.html(modalContents);
}

window.addEventListener('resize', function() {
  if (modal) {
    var s = getVideoSize();
    $(modal).find('iframe').attr({
      height: s.videoHeight,
      width: s.videoWidth
    });
  }
});

function closeModal() {
  if (modal) {
    $(modal).remove();
    modal = null;
  }
}
