from django.core.management.base import BaseCommand
from django.db import transaction
from stats.models import WaterWell
from pyproj import Transformer
from .public_data import public_data

class Command(BaseCommand):
    help = 'Import water well data from public_data'

    def handle(self, *args, **options):
        transformer = Transformer.from_crs('EPSG:4674', 'EPSG:4326')  # SIRGAS 2000 -> WGS84

        # Acessa os dados dos poços corretamente
        wells_data = public_data['queryResult'][0][0]['values']

        for entry in wells_data:
            # Extrai os dados de cada poço
            shplink = entry[0]['shplink']
            well_id = entry[1]
            uf = entry[2]
            locality = entry[3]
            nature = entry[4]
            ne = entry[5]
            nd = entry[6]
            flow_rate = entry[7]

            # Extrai as coordenadas do shplink
            try:
                # O shplink contém uma string no formato "latitude+longitude"
                coords = shplink[2].split('+')
                latitude_raw = float(coords[1])  # Latitude
                longitude_raw = float(coords[0])  # Longitude
            except (IndexError, ValueError):
                self.stdout.write(self.style.WARNING(f'Coordenadas inválidas para o poço {well_id}'))
                continue

            # Converte as coordenadas de SIRGAS 2000 para WGS84
            try:
                latitude, longitude = transformer.transform(latitude_raw, longitude_raw)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Erro ao transformar coordenadas para o poço {well_id}: {e}'))
                continue

            # Cria ou atualiza o poço no banco de dados
            WaterWell.objects.update_or_create(
                public_id=well_id,
                defaults={
                    'name': f"Poço {well_id}",  # Nome padrão, pode ser ajustado
                    'uf': uf,
                    'locality': locality,
                    'nature': nature,
                    'ne': float(ne) if ne else None,
                    'nd': float(nd) if nd else None,
                    'flow_rate': float(flow_rate) if flow_rate else None,
                    'latitude': latitude,
                    'longitude': longitude,
                    'capacity': 0.0,  # Capacidade padrão, pode ser ajustada
                }
            )

        self.stdout.write(self.style.SUCCESS('Dados dos poços importados com sucesso!'))