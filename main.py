import csv
import json

from collections import namedtuple
from mapper import build_rule_tree, find_product_rule_mapping
from grouper import group_products


MAPPING_FILE_PATH = './data/mappings.csv'
PRICE_CATALOG_FILE_PATH = './data/price_catalog.csv'
OUTPUT_FILE = './output.json'
mapping = namedtuple('Mapping', ['destination_type', 'destination'])


def get_rules_tree(source_csv_path):
    """
    Read mapping rule set from CSV file and returns rule tree.
    :return:
    """
    tree = dict()
    with open(source_csv_path) as f:
        f_csv = csv.DictReader(f, delimiter=';')
        for row in f_csv:
            build_rule_tree(row, tree)
    return tree


def gen_converted_products(products: iter, rules_tree: dict):
    """
    Converts product list using rule tree.
    :param products: generator list of products in dict format
    :param rules_tree:
    :return:
    """
    for product in products:
        for col_name, rule in rules_tree.items():
            target_mapping = find_product_rule_mapping(
                product, col_name, rule
            )
            if target_mapping:
                del product[col_name]
                product[
                    target_mapping.destination_type
                ] = target_mapping.destination
        yield product


def gen_price_cat_opener(source_file):
    with open(source_file) as f:
        f_csv = csv.DictReader(f, delimiter=';')
        for product_dict in f_csv:
            yield product_dict


def main():
    rules_tree = get_rules_tree(MAPPING_FILE_PATH)
    products = gen_price_cat_opener(PRICE_CATALOG_FILE_PATH)
    converted_products = gen_converted_products(products, rules_tree)
    catalog = group_products(converted_products)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(json.dumps(catalog))


if __name__ == '__main__':
    main()
