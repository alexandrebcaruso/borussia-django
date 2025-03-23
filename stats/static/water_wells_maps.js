// water_wells_maps.js
document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Inicializa o mapa com OpenStreetMap
    const map = L.map('map').setView([-29.887, -50.270], 12); // Coordenadas de Osório/RS

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Busca dados do GeoJSON
    fetch("{% url 'wells_geojson' %}")
        .then(response => response.json())
        .then(geojson => {
            L.geoJSON(geojson, {
                pointToLayer: (feature, latlng) => {
                    return L.marker(latlng).bindPopup(
                        `<b>${feature.properties.name}</b><br>Vazão: ${feature.properties.flow_rate} m³/h`
                    );
                }
            }).addTo(map);
        })
        .catch(error => console.error('Erro ao carregar poços:', error));
});