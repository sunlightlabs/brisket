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
    $.fn.expando = function(itemCount, parent, child, moreClass) {
        if (!parent) parent = 'ul';
        if (!child) child = 'li';
        moreClass = moreClass ? moreClass + ' ' : '';
        return this.each(function() {
            var $this = $(this);
            var $ul = $this.find(parent).eq(0);
            var $lis = $ul.find(child);
            if ($lis.length > itemCount) {
                var contents = $this.html();
                var $outer = $('<div><div></div></div>').css({'display': 'none', 'position': 'relative'}).prependTo($this);
                var $inner = $outer.find('div').css({'position': 'absolute', 'top': 0, 'left': 0, 'opacity': 0, 'overflow': 'hidden'});
                $inner.append(contents)
                var removed = $lis.slice(itemCount).remove();
                var moreTotal = removed.length + 1;
                
                $lis.eq(itemCount - 1).addClass(moreClass + 'morelink').html('<a href="javascript:void(0)">and ' + moreTotal + ' more &raquo;</a>').click(function() {
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
                
                var childSplit = child.split('.');
                var childTag = childSplit[0];
                var childClass = childSplit.length > 1 ? childSplit[1] + " " : "";
                $inner.find(parent).append('<' + childTag + ' class="' + moreClass + childClass + 'lesslink"><a href="javascript:void(0)">&laquo; view less</a></' + childTag + '>').find(child).eq(-1).click(function() {
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
