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
                var flickrScript = document.createElement('script');
                flickrScript.src = "https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/plugins/flickr/galleria.flickr.min.js";
                document.head.appendChild(flickrScript);

                flickrScript.onload = function() {
                    // Hide loading placeholder
                    loadingPlaceholder.style.display = 'none';

                    // Your existing Galleria code
                    (function load() {
                        var themeUrl = "https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/folio/galleria.folio.min.js";
                    
                        Galleria.loadTheme(themeUrl);
                    
                        var flickr = new Galleria.Flickr();
                        flickr.setOptions({
                            sort: 'interestingness-desc',
                            thumbSize: 'big',
                            imageSize: 'original',
                            description: 'true',
                            max: 50
                        }).set('72177720308771651', function(data) {
                            Galleria.run('.galleria', {
                                dataSource: shuffleList(data)
                            });
                        });
                    
                        function shuffleList(list) {
                            for (let i = list.length - 1; i > 0; i--) {
                                const j = Math.floor(Math.random() * (i + 1));
                                [list[i], list[j]] = [list[j], list[i]];
                            }
                            return list;
                        }
                    }());
                };
            };
        };
    };
});
