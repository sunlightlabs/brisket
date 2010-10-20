$(function() {
    // API key
    var API = 'c07c748bd711478d8f1427eac6ab029a'
    // replace candidate box with a selection box
    var $td = $('#id_td_id');
    var candidate = $td.val();
    $td.replaceWith('<select id="id_td_id" name="td_id"><option selected="selected" value="">---------</option></select>');
    
    // reformat the image boxes
    $('input[type=radio]').addClass('radio').each(function(num, item) {
        $item = $(item);
        $item.parent().attr('id', $item.attr('id') + '_label').html($item).append('<div class="postcardImage"></div>');
    })
    
    var load_candidates = function(callback) {
        var state = $('#id_state').val();
        var office = "federal:" + $('#id_office').val();
        if (state && office) {
            $.getJSON("http://transparencydata.com/api/1.0/entities/race/" + state + ".json?apikey=" + API + "&cycle=2010&callback=?", function(data) {
                var $td = $('#id_td_id');
                $td.html('<option selected="selected" value="">---------</option>')
                
                data = $.map(data, function(val) {
                    if ((val.party == "R" || val.party == "D") && val.seat == office) {
                        return val;
                    } else {
                        return null;
                    }
                })
                data.sort(function(a, b) {
                    var contest = a['seat'] == 'federal:senate' ? 'state' : 'district';
                    var comp = cmp(a[contest], b[contest]);
                    if (comp != 0) {
                        return comp;
                    } else {
                        return cmp(a.name, b.name)
                    }
                })
                
                $.each(data, function(num, val) {
                    if (office == 'federal:senate') {
                        var contest = 'state';
                    } else {
                        var contest = 'district';
                    }
                    $td.append("<option value='" + val.entity_id + "' data-contest='" + val[contest] + "'>" + val.name.replace(")", "-" + val[contest] + ")") + "</option>")
                })
                
                callback();
            })
        }
    }
    var load_photos = function() {
        var selected = $('#id_td_id option:selected');
        // single-candidate
        $('#id_num_candidates_0_label div').html('<img src="/postcard/thumbnail/candidate/' + (selected.attr('value') || 'none') + '" alt="Single-candidate"/>')
        //double candidate
        $('#id_num_candidates_1_label div').html('<img src="/postcard/thumbnail/race/' + (selected.attr('data-contest') || 'none') + '" alt="Double-candidate"/>')
        
        // Disable photo and button if there's only one candidate
        var $td = $('#id_td_id');
        if ($td.val() && $td.find('option[data-contest=' + selected.attr('data-contest') + ']').length < 2) {
            //force-select the first radio
            $('input.radio').eq(0).attr('checked', 'checked').end().eq(1).attr('disabled', 'disabled').removeAttr('checked');
            $('#id_num_candidates_1_label div img').css('opacity', 0.4);
        } else {
            $('input.radio').removeAttr('disabled');
            $('#id_num_candidates_1_label div img').css('opacity', '');
        }
        
        // Make sure the location record is current
        $('#id_location').val(selected.attr('data-contest'));
    };
    
    var cmp = function(a, b) {
        if (a < b) {
            return -1;
        } else if (a > b) {
            return 1;
        } else {
            return 0;
        }
    }
    
    if (candidate || ($('#id_state').val() && $('#id_office').val())) {
        load_candidates(function() {
            if (candidate) {
                $('#id_td_id').val(candidate);
                load_photos();
            }
        });
    }
    
    $('#id_office, #id_state').change(function() {
        load_candidates(load_photos);
    });
    $('#id_td_id').change(load_photos);
    load_photos();
});