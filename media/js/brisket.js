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
	
	/* descriptor toggles */
	$("a.descriptor").toggle(
		function(){
			var hsh = this.hash;
			if (hsh[0] != '#') hsh = '#' + hsh;
			$(this).addClass("active");
			$(hsh).slideDown("slow");
		},
		function(){
			var hsh = this.hash;
			if (hsh[0] != '#') hsh = '#' + hsh;
			$(this).removeClass("active");
			$(hsh).slideUp("slow");
		} 
	);

	/* make entity landing pages sortable */
	$(".sortable").tablesorter({ widgets: ['zebra']}); 
	
	$('#orgSearchForm').submit(function() {
		var form = $(this);
		$.getJSON('http://staging.influenceexplorer.com:8000/api/1.0/entities.json?apikey=sunlight9&search=' + $('#idOrgSearch').val() + '&callback=?', function(data) {
			var list = $('<ul>')
			$('#orgSearchResults').html(list);
			$.each(data, function(num, item) {
				var listItem = $('<li><a id="link-' + item.id + '" href="">' + item.name + '</a></li>');
				list.append(listItem)
				listItem.find('a').click(function() {
					var id = $(this).attr('id').split('-')[1];
					var pol_id = form.find('#polId').val();
					
					$.getJSON('http://staging.influenceexplorer.com:8000/api/1.0/aggregates/recipient/' + pol_id + '/contributor/' + id + '/amount.json?apikey=sunlight9&callback=?', function(aggregate_data) {
						$('#orgSearchAmount').html('$' + aggregate_data.amount)
					});
					return false;
				})
			})
			
		})
		
		return false;
	})
});
