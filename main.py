from collections import namedtuple
import csv
import json

MAPPING_FILE_PATH = './data/mappings.csv'
PRICE_CATALOG_FILE_PATH = './data/price_catalog.csv'
mapping = namedtuple('Mapping', ['destination_type', 'destination'])


def append_rule_graph(rules, _graph, target_mapping=None):
    current_rule = rules[0]
    key = current_rule[0]
    val = current_rule[1]
    _graph.setdefault(key, dict())
    _graph[key].setdefault(val, dict())
    if '_mapping' not in _graph[key][val]:
        _graph[key][val]['_mapping'] = target_mapping

    if len(rules[1:]):
        _graph[key][val]['_has_child'] = True
        append_rule_graph(rules[1:], _graph[key][val],
                          target_mapping)


def get_rules_graph():
    rules = dict()
    graph = dict()
    with open(MAPPING_FILE_PATH) as f:
        f_csv = csv.DictReader(f, delimiter=';')
        for row in f_csv:
            source_types = row['source_type'].split('|')
            sources = row['source'].split('|')
            d = tuple(zip(source_types, sources))
            target_mapping = mapping(row['destination_type'],
                                     row['destination'])
            append_rule_graph(d, graph, target_mapping)
            rules[d] = mapping(row['destination_type'],
                               row['destination'])
    return graph


def find_product_rule_mapping(product, rule_branch, default_mapping):
    cols = [col for col in rule_branch.keys() if not col.startswith('_')]
    if not cols or '_has_child' not in rule_branch:
        return default_mapping
    for col_name in cols:
        _rule_branch = rule_branch[col_name]
        product_val = product[col_name]
        if product_val in _rule_branch:
            _parent_mapping = _rule_branch[product_val].get('_mapping') \
                              or default_mapping
            mapping = find_product_rule_mapping(
                product,
                _rule_branch,
                _parent_mapping
            )
            if mapping:
                return mapping


def convert_price_cat(rules_graph):
    with open(PRICE_CATALOG_FILE_PATH) as f:
        f_csv = csv.DictReader(f, delimiter=';')
        for product in f_csv:
            for col_name, rule in rules_graph.items():
                if product[col_name] in rule:
                    parent_mapping = rule[product[col_name]].get(
                        '_mapping',
                        None
                    )
                    _rule = rule[product[col_name]]
                    mapping = find_product_rule_mapping(
                        product,
                        rule[product[col_name]],
                        parent_mapping
                    )

                    if mapping:
                        del product[col_name]
                        product[
                            mapping.destination_type] = mapping.destination
            yield product


def group_products(products):
    catalog = dict()
    for product in products:
        catalog.setdefault(
            product['brand'], dict()
        )
        brand_branch = catalog[product['brand']]
        brand_branch.setdefault(
            product['article_number'], dict(
                article_number=product['article_number'],
                variations=list(),
            )
        )
        if 'default_values' not in brand_branch[product['article_number']]:
            brand_branch[product['article_number']]['default_values'] = product
        else:
            # add new variation
            diff_set = dict()
            default_values = dict(brand_branch[product['article_number']][
                                      'default_values'].items())
            for k, v in default_values.items():
                if product[k] != v:
                    # remove variation from default values and add as varition
                    diff_set[k] = v
                    del \
                    brand_branch[product['article_number']]['default_values'][k]
            if diff_set:
                variations = brand_branch[product['article_number']][
                    'variations']
                variations.append(diff_set)

    return catalog


def main():
    rules_graph = get_rules_graph()
    products = convert_price_cat(rules_graph)
    catalog = group_products(products)
    return json.dumps(catalog)


if __name__ == '__main__':
    main()
