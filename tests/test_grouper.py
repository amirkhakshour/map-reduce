import json
import os
from tests.conftest import TESTS_ROOT_DIR
from mapreduce.grouper import (group_product, get_or_create_brand,
                               get_or_create_article)


def get_test_group_fixtures(group_id):
    input_file_path = os.path.join(
        TESTS_ROOT_DIR,
        f"./fixtures/{group_id}.input.json"
    )
    output_file_path = os.path.join(
        TESTS_ROOT_DIR,
        f"./fixtures/{group_id}.output.json"
    )
    input = json.loads(open(input_file_path, 'r').read())
    output = json.loads(open(output_file_path, 'r').read())
    return input, output


def test_add_single_product_to_brand_creates_article():
    input, expected_catalog = get_test_group_fixtures('g1')
    catalog = dict()
    for product in input:
        group_product(product, catalog)
    assert catalog == expected_catalog


def test_ident_products_not_adds_variation():
    input, expected_catalog = get_test_group_fixtures('g2')
    catalog = dict()
    for product in input:
        group_product(product, catalog)
    assert catalog == expected_catalog


def test_diff_products_same_article_adds_variation():
    input, expected_catalog = get_test_group_fixtures('g3')
    catalog = dict()
    for product in input:
        group_product(product, catalog)
    assert catalog == expected_catalog


def test_uniq_products_diff_article_adds_variation():
    input, expected_catalog = get_test_group_fixtures('g4')
    catalog = dict()
    for product in input:
        group_product(product, catalog)
    assert catalog == expected_catalog


def test_diff_products_diff_article_removes_all_brand_defaults():
    input, expected_catalog = get_test_group_fixtures('g5')
    catalog = dict()
    for product in input:
        group_product(product, catalog)
    assert catalog == expected_catalog


def test_get_or_create_brand_adds_brand_if_not_exists():
    input, _ = get_test_group_fixtures('g1')
    product = input[0]
    catalog = dict()
    get_or_create_brand(product, catalog)
    assert product['brand'] in catalog


def test_get_or_create_article_adds_article_if_not_exists():
    input, _ = get_test_group_fixtures('g1')
    product = input[0]
    catalog = dict()
    get_or_create_article(product, catalog)
    assert product['article_number'] in catalog
