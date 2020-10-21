from collections import namedtuple

MAPPING_FILE_PATH = './data/mappings.csv'
PRICE_CATALOG_FILE_PATH = './data/price_catalog.csv'
OUTPUT_FILE_PATH = './output.json'

mapping = namedtuple('Mapping', ['destination_type', 'destination'])
