import csv
import sys
import json
import argparse

from collections import namedtuple
from mapreduce.mapper import build_rule_tree, find_product_rule_mapping
from mapreduce.grouper import group_products

MAPPING_FILE_PATH = './data/mappings.csv'
PRICE_CATALOG_FILE_PATH = './data/price_catalog.csv'
OUTPUT_FILE = './output.json'
mapping = namedtuple('Mapping', ['destination_type', 'destination'])


def get_rules_tree(source_csv_io):
    """
    Read mapping rule set from CSV file and returns rule tree.
    :return:
    """
    tree = dict()
    f_csv = csv.DictReader(source_csv_io, delimiter=';')
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


def gen_price_cat_opener(source_file_io):
    f_csv = csv.DictReader(source_file_io, delimiter=';')
    for product_dict in f_csv:
        yield product_dict


def main():
    parser = argparse.ArgumentParser(description='Map Reduce a list of '
                                                 'entities.')
    parser.add_argument('--map_file', type=argparse.FileType('r'),
                        default=MAPPING_FILE_PATH,
                        help='Source CSV mapping rules file')
    parser.add_argument('--data_file', type=argparse.FileType('r'),
                        default=PRICE_CATALOG_FILE_PATH,
                        help='Source CSV entity list file')

    parser.add_argument('--output_file', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Catalog output file')

    args = parser.parse_args()
    rules_tree = get_rules_tree(args.map_file)
    products = gen_price_cat_opener(args.data_file)
    converted_products = gen_converted_products(products, rules_tree)
    catalog = group_products(converted_products)
    args.output_file.write(json.dumps(catalog))


if __name__ == '__main__':
    main()
