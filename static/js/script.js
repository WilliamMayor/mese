function addToQueryString(url, key, value) {
    var query = url.indexOf("?");
    var anchor = url.indexOf("#");
    if (query == url.length - 1) {
        // Strip any ? on the end of the URL
        url = url.substring(0, query);
        query = -1;
    }
    return (anchor > 0 ? url.substring(0, anchor) : url)
         + (query > 0 ? "&" + key + "=" + value : "?" + key + "=" + value)
         + (anchor > 0 ? url.substring(anchor) : "");
}

function removeFromPlaylist(index) {
	$("#playlist table tr").each(function(i, row) {
		if (i > index) {
			$(row).find("td.index span").text(i);
		}
	}).get(index).remove();

}

$(document).ready(function() {

	// HISTORY
	$("body").on("click", "a:not(.action)", function(e) {
		var href = $(this).attr("href");
		$("#container").load(addToQueryString(href, "slim", "true"));
		history.pushState(null, null, href);
		e.preventDefault();
	});
	$(window).bind("popstate", function(e) {
		$("#container").load(addToQueryString(location.pathname, "slim", "true"));
	});
	$(window).bind("unload", function() {
  		// Save playlist, position etc.
	});

	// MEDIA
	$("#video").hide();
	$("#audio").hide().bind('ended', function(e) {
		var index = $("#playlist table td.playing").parent("tr").index();
    	removeFromPlaylist(index);
    	$("#playlist table tr:eq(" + index + ") a").click();
	});

	// PLAYLIST
	$("#playlist a.remove").hide();
	$("#playlist table").on("click", "a", function(e) {
		if ($(this).hasClass('audio')) {
			$("#video").hide().get(0).pause();
			$("#audio").show();
			var audio = $("#audio").get(0);
			audio.src = $(this).attr("href");
			audio.play();
			$("#playlist td.playing").removeClass("playing");
			$(this).parent("td").prev("td").addClass("playing");
		}
		else if ($(this).hasClass('video')) {
			$("#video").show();
			$("#audio").hide().get(0).pause();
			var video = $("#video").get(0);
			video.src = $(this).attr("href");
			video.play();
			$("#playlist td.playing").removeClass("playing");
			$(this).parent("td").prev("td").addClass("playing");
		}
		e.preventDefault();
	});
});