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
                $popdown.slideUp('fast', function() { $this.trigger('reflow'); });
                $this.removeClass('active');
            } else {
                if (!$popdown.hasClass('loaded')) {
                    var id = $row.attr('data-expand-id');
                    
                    var url = expand_url.replace('{id}', id);
                    
                    $loading.slideDown('fast', function() { $this.trigger('reflow'); });
                    $.getJSON(url, function(data) {
                        var rData = _.extend({'formatDate': function(d) {
                            var date = d.split('-');
                            return months[parseInt(date[1], 10) - 1] + ' ' + parseInt(date[2], 10) + ', ' + date[0];
                        }}, $.isArray(data) ? {'documents': data} : data);
                        var table = template(rData);
                        
                        $popdown.append(table);
                        
                        $loading.slideUp('fast');
                        $popdown.slideDown('fast', function() { $this.trigger('reflow'); });
                        
                        $popdown.addClass('loaded');
                    })
                } else {
                    $popdown.slideDown('fast', function() { $this.trigger('reflow'); });
                }
                
                $this.addClass('active');
            }
        });
    });
});

// base64 function for external links
var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(a){var b="";var c,chr2,chr3,enc1,enc2,enc3,enc4;var i=0;a=Base64._utf8_encode(a);while(i<a.length){c=a.charCodeAt(i++);chr2=a.charCodeAt(i++);chr3=a.charCodeAt(i++);enc1=c>>2;enc2=((c&3)<<4)|(chr2>>4);enc3=((chr2&15)<<2)|(chr3>>6);enc4=chr3&63;if(isNaN(chr2)){enc3=enc4=64}else if(isNaN(chr3)){enc4=64}b=b+this._keyStr.charAt(enc1)+this._keyStr.charAt(enc2)+this._keyStr.charAt(enc3)+this._keyStr.charAt(enc4)}return b},decode:function(a){var b="";var c,chr2,chr3;var d,enc2,enc3,enc4;var i=0;a=a.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(i<a.length){d=this._keyStr.indexOf(a.charAt(i++));enc2=this._keyStr.indexOf(a.charAt(i++));enc3=this._keyStr.indexOf(a.charAt(i++));enc4=this._keyStr.indexOf(a.charAt(i++));c=(d<<2)|(enc2>>4);chr2=((enc2&15)<<4)|(enc3>>2);chr3=((enc3&3)<<6)|enc4;b=b+String.fromCharCode(c);if(enc3!=64){b=b+String.fromCharCode(chr2)}if(enc4!=64){b=b+String.fromCharCode(chr3)}}b=Base64._utf8_decode(b);return b},_utf8_encode:function(a){a=a.replace(/\r\n/g,"\n");var b="";for(var n=0;n<a.length;n++){var c=a.charCodeAt(n);if(c<128){b+=String.fromCharCode(c)}else if((c>127)&&(c<2048)){b+=String.fromCharCode((c>>6)|192);b+=String.fromCharCode((c&63)|128)}else{b+=String.fromCharCode((c>>12)|224);b+=String.fromCharCode(((c>>6)&63)|128);b+=String.fromCharCode((c&63)|128)}}return b},_utf8_decode:function(a){var b="";var i=0;var c=c1=c2=0;while(i<a.length){c=a.charCodeAt(i);if(c<128){b+=String.fromCharCode(c);i++}else if((c>191)&&(c<224)){c2=a.charCodeAt(i+1);b+=String.fromCharCode(((c&31)<<6)|(c2&63));i+=2}else{c2=a.charCodeAt(i+1);c3=a.charCodeAt(i+2);b+=String.fromCharCode(((c&15)<<12)|((c2&63)<<6)|(c3&63));i+=3}}return b}}
