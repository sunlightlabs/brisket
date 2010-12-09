(function($) {
    $.fn.multiellipsis = function(lineCount) {
        return this.each(function() {
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
    $.fn.expando = function(itemCount) {
        return this.each(function() {
            var $this = $(this);
            var $ul = $this.find('ul').eq(0);
            var $lis = $ul.find('li');
            if ($lis.length > itemCount) {
                var $outer = $('<div><div></div></div>').css({'display': 'none', 'position': 'relative'}).prependTo($this);
                var $inner = $outer.find('div').css({'position': 'absolute', 'top': 0, 'left': 0, 'opacity': 0, 'overflow': 'hidden'});
                $inner.append($ul.clone())
                var removed = $lis.slice(itemCount).remove();
                var moreTotal = removed.length + 1;
                
                $lis.eq(itemCount - 1).addClass('morelink').html('<a href="javascript:void(0)">' + moreTotal + ' more</a>').click(function() {
                    $outer.show();
                    $inner.offset($this.offset());
                    var padding = -1 * parseInt($inner.css('top'));
                    var bg = $this.parent().css('background-color');
                    bg = bg && bg != 'transparent' && bg != 'rgba(0, 0, 0, 0)' ? bg : '#ffffff';
                    $inner.css({'padding': padding - 1, 'border': '1px solid #dadbd6', 'width': $this.width(), 'background-color': bg});
                    var height = $inner.height();
                    
                    $inner.css({'height': $this.height()});
                    
                    $inner.animate({'opacity': 1}, 'fast', function() {
                        $inner.animate({'height': height < 400 ? height : 400}, 'fast', function() {
                            $inner.css('overflow', 'auto');
                        })
                    });
                    
                    $('table .expanded .lesslink').click();
                    $inner.addClass('expanded');
                })
                
                $inner.find('ul').append('<li class="lesslink"><a href="javascript:void(0)">less</a></li>').find('li').eq(-1).click(function() {
                    $inner.css('overflow', 'hidden').removeClass('expanded');
                    $inner.animate({'height': $this.height()}, 'fast', function() {
                        $inner.animate({'opacity': 0}, 'fast', function() {
                            $inner.css({'top': 0, 'left': 0, 'opacity': 0, 'overflow': 'hidden', 'border': '', 'padding': '', 'height': 'auto'})
                            $outer.css('display', 'none');
                        })
                    });
                })
            }
        })
    }
})(jQuery);
