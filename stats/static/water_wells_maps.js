document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Inicializa o mapa com OpenStreetMap
    const map = L.map('map').setView([-29.887, -50.270], 12); // Coordenadas de Osório/RS

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Busca dados do GeoJSON
    fetch("http://localhost:8001/agua/estatisticas/painel/api/wells-geojson/")
        .then(response => response.json())
        .then(geojson => {
            // Adiciona os marcadores ao mapa
            const markers = L.geoJSON(geojson, {
                pointToLayer: (feature, latlng) => {
                    // Cria um marcador para cada poço
                    const marker = L.marker(latlng, {
                        title: feature.properties.name
                    });

                    // Adiciona um popup ao marcador
                    marker.bindPopup(`
                        <b>${feature.properties.name}</b><br>
                        Vazão: ${feature.properties.flow_rate} m³/h<br>
                        <a href="/poco/${feature.id}/">Ver Detalhes</a>
                    `);

                    // Adiciona interatividade entre o marcador e a tabela
                    marker.on('click', function() {
                        // Destaca a linha correspondente na tabela
                        const tableRow = document.querySelector(`tr[data-well-id="${feature.id}"]`);
                        if (tableRow) {
                            tableRow.classList.add('highlight');
                            setTimeout(() => tableRow.classList.remove('highlight'), 1000);
                        }
                    });

                    return marker;
                }
            }).addTo(map);

            // Adiciona interatividade entre a tabela e os marcadores
            const tableRows = document.querySelectorAll('#table-wells tbody tr');
            tableRows.forEach(row => {
                row.addEventListener('click', function() {
                    const lat = parseFloat(row.getAttribute('data-lat'));
                    const lng = parseFloat(row.getAttribute('data-lng'));
                    map.setView([lat, lng], 15); // Centraliza o mapa no poço selecionado

                    // Abre o popup do marcador correspondente
                    markers.eachLayer(layer => {
                        if (layer.getLatLng().lat === lat && layer.getLatLng().lng === lng) {
                            layer.openPopup();
                        }
                    });
                });
            });
        })
        .catch(error => console.error('Erro ao carregar poços:', error));
});