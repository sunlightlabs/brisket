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
    
    /* descriptor toggles */
    $("a.descriptor").toggle(
        function() {
            var hsh = this.hash;
            if (hsh[0] != '#') hsh = '#' + hsh;
            $(this).addClass("active");
            $(hsh).slideDown("fast");
        },
        function() {
            var hsh = this.hash;
            if (hsh[0] != '#') hsh = '#' + hsh;
            $(this).removeClass("active");
            $(hsh).slideUp("fast");
        }
    );

    /* make entity landing pages sortable */
    $(".sortable").tablesorter({ widgets: ['zebra']});

    /* deal with top menu */
    $("nav > ul > li")
        .hover(function() {
            $(this).find("ul").fadeIn("fast");
        }, function() {
            $(this).find("ul").fadeOut("fast");
        }).find(">a").click(function(evt) {
            if ($(this).attr('href') == "#") {
                evt.preventDefault();
            }
        })
    
    /* deal with the floating TOC */
    var $navbar = $('#floatingNav');
    if ($navbar.length) {
        var top = $navbar.offset().top + $navbar.height() + 5;
        
        var $sections, sectionNames, sectionOffsets;
        var calculateSectionOffsets = function() {
            $sections = $('.sectionLink');
            sectionNames = $sections.map(function(item) { return $(this).attr('name'); })
            sectionOffsets = $sections.map(function(item) { return $(this).offset().top; });
            sectionOffsets.push($('#mainContent_bottom').offset().top);
        }
        calculateSectionOffsets();

        var mode = 'static';
        var section = null;

        var scrollHandler = function() {
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
        };

        var $window = $(window);
        $window.scroll(scrollHandler);

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

        /* deal with reflows from animation */
        $(document).bind('reflow', function() {
            calculateSectionOffsets();
            scrollHandler();  
        })
    }
});
