from collections import namedtuple

mapping = namedtuple('Mapping', ['destination_type', 'destination'])


def build_rule_tree(rule_item: dict, tree: dict):
    """
    Recursively add a raw rule to the tree with the following structure:

    {
        'season': {
            'winter': {'_mapping': Mapping(destination_type='season',
            destination='Winter')},
            'summer': {'_mapping': Mapping(destination_type='season',
            destination='Summer')}
        },
        'collection': {
            'NW 17-18': {'_mapping': Mapping(destination_type='collection',
            destination='Winter Collection 2017/2018')}
        },
        'size_group_code': {
            'EU': {
                '_mapping': Mapping(destination_type='size_group',
                destination='European sizes'),
                '_has_child': True,
                'size_code': {
                    '36': {'_mapping': Mapping(destination_type='size',
                    destination='European size 36')},
                    ...
                }
            }
        }
    }
    """
    source_types = rule_item['source_type'].split('|')
    sources = rule_item['source'].split('|')
    rule_attrs = tuple(zip(source_types, sources))
    target_mapping = mapping(
        rule_item['destination_type'],
        rule_item['destination']
    )

    while True:
        if not rule_attrs:
            tree['_mapping'] = target_mapping
            return
        col_name, col_val = rule_attrs[0]
        rule_attrs = rule_attrs[1:]
        tree.setdefault(col_name, dict())
        tree[col_name].setdefault(col_val, dict())
        tree = tree[col_name][col_val]


def find_product_rule_mapping(product, rule_name, rule_tree,
                              parent_mapping=None):
    next_rule_val = product[rule_name]
    branch = rule_tree[next_rule_val]
    if '_mapping' in branch:
        parent_mapping = branch['_mapping']
    child_rule_attrs = [_col for _col in branch if not _col.startswith('_')]
    if not child_rule_attrs:
        return parent_mapping
    for attr in child_rule_attrs:
        mapping = find_product_rule_mapping(product, attr, branch[attr],
                                            parent_mapping)
        # return the first matched mapping
        if mapping:
            return mapping
