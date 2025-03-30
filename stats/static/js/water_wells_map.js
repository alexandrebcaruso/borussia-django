document.addEventListener('DOMContentLoaded', function() {
    const center = [-47.9297, -15.7801];  // [lon, lat] de exemplo
    const map = new ol.Map({
        target: 'map',
        layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
        view: new ol.View({
            center: ol.proj.fromLonLat(center),
            zoom: 10
        })
    });

    // Função para converter coordenadas com vírgula para float
    const parseCoord = (coordStr) => {
        if (!coordStr) return NaN;
        // Substitui vírgula por ponto e converte para número
        return parseFloat(coordStr.replace(',', '.'));
    };

    const wells = document.querySelectorAll('#table-wells tbody tr');
    const features = [];

    wells.forEach(well => {
        const lonStr = well.dataset.lng;  // Exemplo: "-50,361388"
        const latStr = well.dataset.lat;  // Exemplo: "-20,275848"
        const lon = parseCoord(lonStr);
        const lat = parseCoord(latStr);
        const wellId = well.dataset.wellId;

        if (!isNaN(lon) && !isNaN(lat)) {
            const marker = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
                name: `Poço ${wellId}`
            });

            marker.setStyle(new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 6,
                    fill: new ol.style.Fill({ color: 'red' }),
                    stroke: new ol.style.Stroke({ color: 'white', width: 2 })
                })
            }));
            features.push(marker);
        } else {
            console.error(`Coordenadas inválidas para o poço ${wellId}: lon=${lonStr}, lat=${latStr}`);
        }
    });

    const vectorLayer = new ol.layer.Vector({
        source: new ol.source.Vector({ features: features })
    });
    map.addLayer(vectorLayer);

    // Interação com clique (opcional)
    map.on('click', function(evt) {
        const feature = map.forEachFeatureAtPixel(evt.pixel, (f) => f);
        if (feature) {
            alert(`Poço selecionado: ${feature.get('name')}`);
        }
    });
});''