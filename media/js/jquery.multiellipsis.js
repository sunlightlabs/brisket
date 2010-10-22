(function($) {
    $.fn.multiellipsis = function(lineCount) {
	return this.each( function() {
	    var $this = $(this);
	    var lh = $this.css('line-height');
	    lh = lh ? parseInt(lh) : 20;
	    
	    if ($this.height() > lineCount * lh) {
		var words = $this.html().split(' ');
		var osDiv = $('<div>').css({position: 'absolute', width: $this.width() + 'px', 'left': '-9999px'}).appendTo($this).html(words.join(' '));
		for (var i = words.length; i >= 0; i--) {
		    if (osDiv.height() <= lineCount * lh) {
			$this.html(osDiv.html());
			break;
		    }
		    osDiv.html(words.slice(0, i).join(' ') + '...');
		}
	    }
	})
    }
})( jQuery );
	
