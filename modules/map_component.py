def create_single_map(city, lat, lng):
    """
    Creates a Leaflet.js HTML map for a single location.
    Looks and feels like Google Maps — completely free.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <!-- Leaflet CSS -->
        <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        />

        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: Arial, sans-serif; }}
            #map {{
                height: 450px;
                width: 100%;
                border-radius: 12px;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>

        <!-- Leaflet JS -->
        <script
            src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
        </script>

        <script>
            // Create map centered on location
            var map = L.map('map').setView([{lat}, {lng}], 11);

            // Google Maps-like tile layer (free, no API key)
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }}).addTo(map);

            // Custom red marker
            var redIcon = L.icon({{
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            }});

            // Add marker with popup
            var marker = L.marker([{lat}, {lng}], {{icon: redIcon}}).addTo(map);
            marker.bindPopup(
                '<b>📍 {city}</b><br>Lat: {lat:.4f}<br>Lng: {lng:.4f}'
            ).openPopup();

            // Add circle around location
            L.circle([{lat}, {lng}], {{
                color: '#FF4B4B',
                fillColor: '#FF4B4B',
                fillOpacity: 0.1,
                radius: 5000
            }}).addTo(map);
        </script>
    </body>
    </html>
    """
    return html


def create_multi_map(destinations):
    """
    Creates a Leaflet.js HTML map with multiple destination markers.
    destinations = list of dicts with city, lat, lng keys.
    """

    # Build JavaScript markers string
    markers_js = ""
    bounds = []

    for i, dest in enumerate(destinations):
        city = dest["city"]
        lat = dest["lat"]
        lng = dest["lng"]
        cost = dest.get("cost", "N/A")
        rating = dest.get("rating", "N/A")

        # Alternate marker colors
        colors = ["red", "blue", "green", "orange", "purple"]
        color = colors[i % len(colors)]

        markers_js += f"""
        var icon{i} = L.icon({{
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-{color}.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        }});

        var marker{i} = L.marker([{lat}, {lng}], {{icon: icon{i}}}).addTo(map);
        marker{i}.bindPopup(
            '<b>📍 {city}</b><br>' +
            'Cost: KSh {cost}<br>' +
            'Rating: ⭐ {rating}'
        );

        bounds.push([{lat}, {lng}]);
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link
            rel="stylesheet"
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        />

        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: Arial, sans-serif; }}
            #map {{
                height: 500px;
                width: 100%;
                border-radius: 12px;
            }}
            .legend {{
                background: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                line-height: 1.8;
                box-shadow: 0 1px 5px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

        <script>
            // Start map centered on Africa
            var map = L.map('map').setView([0, 25], 3);

            // Tile layer
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }}).addTo(map);

            var bounds = [];

            // Add all markers
            {markers_js}

            // Auto zoom to fit all markers
            if (bounds.length > 0) {{
                map.fitBounds(bounds, {{padding: [40, 40]}});
            }}
        </script>
    </body>
    </html>
    """
    return html