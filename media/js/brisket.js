$(function() {
    $("input, textarea").placehold();
    
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
        function() {
            var hsh = this.hash;
            if (hsh[0] != '#') hsh = '#' + hsh;
            $(this).addClass("active");
            $(hsh).slideDown("slow");
        },
        function() {
            var hsh = this.hash;
            if (hsh[0] != '#') hsh = '#' + hsh;
            $(this).removeClass("active");
            $(hsh).slideUp("slow");
        }
    );

    /* make entity landing pages sortable */
    $(".sortable").tablesorter({ widgets: ['zebra']});
    
    /* deal with the floating TOC */
    var $navbar = $('#floatingNav');
    if ($navbar.length) {
        var top = $navbar.offset().top + $navbar.height() + 5;
        
        var $sections = $('.sectionLink');
        var sectionNames = $sections.map(function(item) { return $(this).attr('name'); })
        var sectionOffsets = $sections.map(function(item) { return $(this).offset().top; });
        sectionOffsets.push($('#mainContent_bottom').offset().top);

        var mode = 'static';
        var section = null;

        var $window = $(window);
        $window.scroll(function() {
            var pos = $window.scrollTop();
            if (mode == 'static' && pos >= top) {
                mode = 'floating';
                $navbar.addClass('floating');
            }
            if (mode == 'floating') {
                if (pos < top) {
                    mode = 'static';
                    $navbar.removeClass('floating');

                    section = null;
                    $navbar.find('#miniNav li.active').removeClass('active');
                } else {
                    var realPos = pos + 20;
                    /* look for the section */
                    if (section != null && (realPos < sectionOffsets[0] || realPos >= sectionOffsets[sectionOffsets.length - 1])) {
                        section = null;
                        $navbar.find('#miniNav li.active').removeClass('active');
                    } else {
                        for (var i = sectionOffsets.length - 2; i >= 0; i--) {
                            if (realPos >= sectionOffsets[i] && realPos < sectionOffsets[i + 1]) {
                                if (sectionNames[i] != section) {
                                    section = sectionNames[i];
                                    $navbar.find('#miniNav li.active').removeClass('active');
                                    $navbar.find('#miniNav a[href=#' + section + ']').parent().addClass('active');
                                }
                                break;
                            }
                        };
                    }
                }
            }
        })

        /* set up smooth scrolling, but only for browsers that play nice */
        $('#miniNav a').each(function(idx, item) {
            if ($.browser.mozilla) {
                $(item).click(function() {
                    $('html').animate({'scrollTop': sectionOffsets[idx]}, 'ease');
                    return false;
                });
            } else if ($.browser.webkit) {
                $(item).click(function() {
                    $('body').animate({'scrollTop': sectionOffsets[idx]}, 'ease');
                    return false;
                });
            }
        })
    }
});
