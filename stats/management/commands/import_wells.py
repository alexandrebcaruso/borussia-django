from django.core.management.base import BaseCommand
from django.db import transaction
from stats.models import WaterWell
from pyproj import Transformer
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import water well data with proper coordinate transformation'

    def handle(self, *args, **options):
        from .public_data import public_data  # Importação local para evitar circularidade
        
        # Configuração de sistemas de coordenadas
        self.transformer = Transformer.from_crs("EPSG:4674", "EPSG:4326", always_xy=True)
        
        # Contadores para estatísticas
        stats = {
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'no_transform': 0,
            'errors': 0
        }

        wells_data = self.get_wells_data(public_data)
        
        with transaction.atomic():
            for entry in wells_data:
                self.process_well_entry(entry, stats)

        # Relatório final
        self.stdout.write(self.style.SUCCESS(
            f"\nResumo da importação:\n"
            f" - Poços criados: {stats['created']}\n"
            f" - Poços atualizados: {stats['updated']}\n"
            f" - Poços ignorados: {stats['skipped']}\n"
            f" - Transformações não aplicadas: {stats['no_transform']}\n"
            f" - Erros: {stats['errors']}"
        ))

    def get_wells_data(self, public_data):
        """Extrai os dados de poços da estrutura do SIAGAS"""
        try:
            return public_data['queryResult'][0][0]['values']
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Erro ao acessar dados: {e}")
            return []

    def process_well_entry(self, entry, stats):
        """Processa um registro individual de poço"""
        try:
            shplink = entry[0]['shplink']
            well_id = entry[1]
            
            # Extrai coordenadas originais
            lon_raw, lat_raw = self.extract_coordinates(shplink)
            if None in (lon_raw, lat_raw):
                stats['skipped'] += 1
                logger.warning(f"Poço {well_id}: Coordenadas inválidas")
                return

            # Aplica transformação de coordenadas
            lon_wgs84, lat_wgs84 = self.apply_coordinate_transform(lon_raw, lat_raw, well_id)
            
            # Verifica se a transformação fez diferença
            if self.coordinates_are_equal(lon_raw, lat_raw, lon_wgs84, lat_wgs84):
                stats['no_transform'] += 1
                logger.warning(
                    f"Poço {well_id}: Transformação não alterou coordenadas\n"
                    f"Original: {lon_raw}, {lat_raw}\n"
                    f"Transformado: {lon_wgs84}, {lat_wgs84}"
                )

            # Prepara dados para salvamento
            well_data = {
                'name': f"Poço {well_id}",
                'uf': entry[2],
                'locality': entry[3],
                'nature': entry[4],
                'ne': self.parse_float(entry[5]),
                'nd': self.parse_float(entry[6]),
                'flow_rate': self.parse_float(entry[7]),
                'latitude': lat_wgs84,
                'longitude': lon_wgs84,
                'original_latitude': lat_raw,
                'original_longitude': lon_raw,
                'original_crs': 'EPSG:4674',
                'capacity': 0.0
            }

            # Cria ou atualiza o registro
            _, created = WaterWell.objects.update_or_create(
                public_id=well_id,
                defaults=well_data
            )

            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1

        except Exception as e:
            stats['errors'] += 1
            logger.error(f"Erro ao processar poço {entry[1] if len(entry) > 1 else 'DESCONHECIDO'}: {e}")

    def extract_coordinates(self, shplink):
        """Extrai coordenadas do formato SIAGAS (centro da bbox)"""
        try:
            coords = shplink[2].split('+')
            if len(coords) >= 4:
                return (
                    self.parse_float(coords[0]),  # min_lon
                    self.parse_float(coords[1])   # min_lat
                )
        except (IndexError, AttributeError) as e:
            logger.warning(f"Formato de coordenadas inválido: {e}")
        return None, None

    def apply_coordinate_transform(self, lon, lat, well_id):
        """Aplica a transformação de coordenadas com verificação"""
        try:
            # Verifica se a transformação é necessária (SIRGAS2000 ≈ WGS84 para 2D)
            if self.coordinates_are_equivalent(lon, lat):
                logger.info(f"Poço {well_id}: Usando coordenadas originais (SIRGAS2000 ≈ WGS84)")
                return lon, lat
                
            # Aplica transformação
            transformed_lon, transformed_lat = self.transformer.transform(lon, lat)
            return transformed_lon, transformed_lat
            
        except Exception as e:
            logger.error(f"Poço {well_id}: Erro na transformação - {e}")
            return lon, lat  # Fallback para coordenadas originais

    def coordinates_are_equivalent(self, lon, lat):
        """Verifica se as coordenadas estão na área onde SIRGAS2000 ≈ WGS84"""
        # Brasil está aproximadamente entre -75 a -30 de longitude e -35 a 5 de latitude
        return (-75 <= lon <= -30) and (-35 <= lat <= 5)

    def coordinates_are_equal(self, lon1, lat1, lon2, lat2, tolerance=1e-8):
        """Verifica se duas coordenadas são iguais dentro de uma tolerância"""
        return (abs(lon1 - lon2) < tolerance) and (abs(lat1 - lat2) < tolerance)

    def parse_float(self, value):
        """Converte para float, tratando vírgula e valores vazios"""
        try:
            if not value:
                return None
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return None