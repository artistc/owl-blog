// home page infinite scroll: load the next page automatically when the user
// scrolls to the end. Each page is rendered using the home_article.html template.
$(function() { 
	var config = {
		distanceThreshold: 200,
		timeThreshold: 1000 // 1 second
	};

	// used to determine if the user is scrolling up or down.
	var lastDistance = 0;

	// used to prevent many back-to-back requests.
	var lastLoadTime = new Date;

	// check for a special "last page" flag and disable the infinite scroll when we see it.
	function checkForLastPage() {
		if ( $("#the-last-page-of-the-internet").length ) {
			$(window).unbind("scroll", loadNextPageIfNeeded);
		}
	}

	// add a new content page and load the next article into it.
	function loadNextPage() {
		var index = $('.content-page').length;
		$("#main-wrapper").append('<div class="content-page"></div>');
		$('.content-page:last').load('/infinite/?index=' + index, undefined, checkForLastPage);
		lastLoadTime = new Date;
		return false;
	}

	// scroll event handler.  Loads the next page if the user is scrolling downward and is near
	// the bottom of the page.
	function loadNextPageIfNeeded() {
		// detect scroll direction
		var distance = $(document.body).height() - $(window).height() - $(window).scrollTop();
		var delta = distance - lastDistance;
		lastDistance = distance;

		// don't do anything if a load just occured.
		var timeDelta = new Date - lastLoadTime;
		if ( timeDelta < config.distanceThreshold ) return;

		// if they're scrolling downward...
		if ( delta < 0 ) {
			// and they're nearly to the end...
			if ( distance < config.distanceThreshold && $('.content-page:last').html() !== "" ) {
				loadNextPage();
			}
		}
	}

	// it's possible for a page to load already scrolled, for example if the back button was used.
	// So we check once, right off the bat.
	loadNextPageIfNeeded();

	// check to see if we need to load another page each time the user scrolls.
	$(window).scroll(loadNextPageIfNeeded);
});

