document.addEventListener('DOMContentLoaded', function() {
    // Show loading placeholder
    var loadingPlaceholder = document.getElementById('loading-placeholder');
    loadingPlaceholder.style.display = 'block';

    // Load jQuery and Galleria scripts from CDN
    var jqueryScript = document.createElement('script');
    jqueryScript.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js";
    document.head.appendChild(jqueryScript);

    jqueryScript.onload = function() {
        var galleriaScript = document.createElement('script');
        galleriaScript.src = "https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/galleria.min.js";
        document.head.appendChild(galleriaScript);

        galleriaScript.onload = function() {
            var exifScript = document.createElement('script');
            exifScript.src = "https://cdnjs.cloudflare.com/ajax/libs/exif-js/2.3.0/exif.min.js";
            document.head.appendChild(exifScript);

            exifScript.onload = function() {
                // Fix getScriptPath: with dynamic script loading, $('script:last').attr('src') can be undefined
                var origGetScriptPath = Galleria.utils.getScriptPath;
                Galleria.utils.getScriptPath = function(src) {
                    src = src || (typeof $ !== 'undefined' && $('script[src]').last().attr('src')) || '';
                    return origGetScriptPath.call(this, src);
                };
                // Flickr plugin expects window.JQuery (capital J); jQuery only sets window.jQuery
                if (window.jQuery && !window.JQuery) window.JQuery = window.jQuery;
                var flickrScript = document.createElement('script');
                flickrScript.src = "https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/plugins/flickr/galleria.flickr.min.js";
                document.head.appendChild(flickrScript);
                flickrScript.onload = function() {
                    loadingPlaceholder.style.display = 'none';

                    var themeUrl = "https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/folio/galleria.folio.min.js";
                    Galleria.loadTheme(themeUrl);

                    // Your Flickr API key (baophotography); photoset ID 72177720308771651
                    var FLICKR_API_KEY = '95a7b666148701836aede2470fcb286b';
                    var PHOTOSET_ID = '72177720308771651';
                    var flickr = new Galleria.Flickr(FLICKR_API_KEY);
                    flickr.setOptions({
                        sort: 'interestingness-desc',
                        thumbSize: 'big',
                        imageSize: 'original',
                        description: true,
                        max: 50
                    }).set(PHOTOSET_ID, function(data) {
                        Galleria.run('.galleria', { dataSource: data });
                    });
                };
            };
        };
    };
});
