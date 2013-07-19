/*!
 * Socialite v2.0 - Plain Twitter Extension
 * Copyright (c) 2013 Dan Drinkard
 * Dual-licensed under the BSD or MIT licenses: http://socialitejs.com/license.txt
 */
(function(window, document, Socialite, undefined)
{
    // https://dev.twitter.com/docs/intents/events/

    var twitterActivate = function(instance)
    {
        if (window.twttr && typeof window.twttr.widgets === 'object' && typeof window.twttr.widgets.load === 'function') {
            window.twttr.widgets.load();
        }
    };

    Socialite.widget('twitter', 'simple',   { init: function(instance){
        var el = document.createElement('a'),
            href = "//twitter.com/intent/tweet?";
        el.className = instance.widget.name;
        Socialite.copyDataAttributes(instance.el, el);
        href += Socialite.getDataAttributes(el, true);
        el.setAttribute('href', href);
        el.setAttribute('data-lang', instance.el.getAttribute('data-lang') || Socialite.settings.twitter.lang);
        if (instance.el.getAttribute('data-image')) {
            imgTag = document.createElement('img');
            imgTag.src = instance.el.getAttribute('data-image');
            el.appendChild(imgTag);
        }
        instance.el.appendChild(el);
    }, activate: twitterActivate });

})(window, window.document, window.Socialite);

