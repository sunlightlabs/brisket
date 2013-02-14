/*!
 * Socialite v2.0 - Plain FB Share Extension
 * Copyright (c) 2013 Dan Drinkard
 * Dual-licensed under the BSD or MIT licenses: http://socialitejs.com/license.txt
 */
(function(window, document, Socialite, undefined)
{

    /**
     * FB Share is no longer supported, but params are:
     * u | data-url    | URL to share
     * t | data-title  | Title to share
     *
     * Others may work, but that will come later. For now just set OG tags.
     *
     */

    function addEvent(obj, evt, fn, capture) {
        if (window.attachEvent) {
            obj.attachEvent("on" + evt, fn);
        }
        else {
            if (!capture) capture = false; // capture
            obj.addEventListener(evt, fn, capture);
        }
    }

    Socialite.widget('facebook', 'share', {
        init: function(instance) {
            var el = document.createElement('a'),
                href = "//www.facebook.com/share.php?",
                attrs = Socialite.getDataAttributes(instance.el, true, true);

            el.className = instance.widget.name;
            Socialite.copyDataAttributes(instance.el, el);
            if(attrs.url) href += 'u=' + encodeURIComponent(attrs.url);
            if(attrs['title']) href += '&t=' + encodeURIComponent(attrs['title']);
            href += '&' + Socialite.getDataAttributes(el, true);
            el.setAttribute('href', href);
            el.setAttribute('data-lang', instance.el.getAttribute('data-lang') || Socialite.settings.facebook.lang);
            if (instance.el.getAttribute('data-image')) {
                imgTag = document.createElement('img');
                imgTag.src = instance.el.getAttribute('data-image');
                el.appendChild(imgTag);
            }
            addEvent(el, 'click', function(e){
                var t = e? e.target : window.event.srcElement;
                e.preventDefault();
                window.open(el.getAttribute('href'), 'fb-share', 'left=' + (screen.availWidth/2 - 350) + ',top=' + (screen.availHeight/2 - 163) + ',height=325,width=700,menubar=0,resizable=0,status=0,titlebar=0');
            });
            instance.el.appendChild(el);
        },
        activate: function(){}
    });

})(window, window.document, window.Socialite);

