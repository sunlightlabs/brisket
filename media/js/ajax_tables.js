$(function() {
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    var templates = [];
    
    $('.expandTable').each(function() {
        var $table = $(this);
        var expand_url = $table.attr('data-expand-url');
            
        var template_name = $table.attr('data-expand-template');
        if (typeof(templates[template_name]) == 'undefined') {
            templates[template_name] = _.template($(template_name).html())
        }
        var template = templates[template_name];
        
        $table.find('.expandTableRow a.toggle').click(function() {
            var $this = $(this);
            var $row = $this.parents('.expandTableRow');
            var $popdown = $row.find('.expandDocList');
            var $loading = $row.find('.loading');
            
            if ($popdown.is(':visible')) {
                $popdown.slideUp('fast');
                $this.removeClass('active');
            } else {
                if (!$popdown.hasClass('loaded')) {
                    var id = $row.attr('data-expand-id');
                    
                    var url = expand_url.replace('{id}', id);
                    
                    $loading.slideDown('fast');
                    $.getJSON(url, function(data) {
                        var table = template({'documents': $.map(data, function(row) {
                            var out = $.extend({}, row);
                            if (typeof(row.date_posted) != 'undefined') {
                                var date = row.date_posted.split('-');
                                $.extend(out, {'nice_date': months[parseInt(date[1], 10) - 1] + ' ' + parseInt(date[2], 10) + ', ' + date[0]});
                            }
                            return out;
                        })});
                        
                        $popdown.append(table);
                        
                        $loading.slideUp('fast');
                        $popdown.slideDown('fast');
                        
                        $popdown.addClass('loaded');
                    })
                } else {
                    $popdown.slideDown('fast');
                }
                
                $this.addClass('active');
            }
        });
    });
});