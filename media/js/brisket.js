$().ready(function() {
    
    /* hide cycle submit button if JavaScript is enabled */
	$('#cycle_submit').hide();
	
	/* change cycle on select rather than using submit button */
	$('#id_cycle').bind('change', function() {
		$('#cycle_form').submit();
		return false;
	});
	
	/* bind to query input box
	 * on focus: clear the search box if the value equals data-initial
	 * on blur: set value to data-initial if value is empty string
	 */
	$('#id_query').bind('focus', function() {
		var q = $(this);
		if (q.val().toUpperCase() == q.attr('data-initial').toUpperCase()) {
			q.val('');
		}
	}).bind('blur', function() {
		var q = $(this);
		if (!q.val()) {
			q.val(q.attr('data-initial'));
		}
	});
	
	/* do not submit search form if its value matches data-initial */
	$('#searchForm').bind('submit', function() {
		var q = $('#id_query');
		return q.val() != q.attr('data-initial');
	});

	/* section toggles */
	$('.overviewBar a.toggle').toggle(
		function() {
			var bar = $(this).parent();
			bar.next('.chartModule').slideToggle('slow');
			bar.addClass("active");
		}, 
		function() {
			var bar = $(this).parent();
			bar.next('.chartModule').slideToggle('slow');
			bar.removeClass("active");
		}
	);
	
});