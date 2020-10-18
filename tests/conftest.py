
EXAMPLE_RULE_MAPPING_FLAT = """source;destination;source_type;destination_type
winter;Winter;season;season
summer;Summer;season;season
"""

EXAMPLE_RULE_MAPPING = """source;destination;source_type;destination_type
winter;Winter;season;season
summer;Summer;season;season
NW 17-18;Winter Collection 2017/2018;collection;collection
EU;European sizes;size_group_code;size_group
EU|36;European size 36;size_group_code|size_code;size
EU|37;European size 37;size_group_code|size_code;size
EU|38;European size 38;size_group_code|size_code;size
EU|39;European size 39;size_group_code|size_code;size
EU|40;European size 40;size_group_code|size_code;size
EU|41;European size 41;size_group_code|size_code;size
EU|42;European size 42;size_group_code|size_code;size
4;Boot;article_structure_code;article_structure
5;Sneaker;article_structure_code;article_structure
6;Slipper;article_structure_code;article_structure
7;Loafer;article_structure_code;article_structure
8;Mocassin;article_structure_code;article_structure
9;Sandal;article_structure_code;article_structure
10;Pump;article_structure_code;article_structure
1;Nero;color_code;color
2;Marrone;color_code;color
3;Brandy Nero;color_code;color
4;Indaco Nero;color_code;color
5;Fucile;color_code;color
6;Bosco Nero;color_code;color
"""


def raw_rule_set(csv_like_str):
    """
    Read mapping rule set from CSV file and returns rule tree.
    :return:
    """
    rule_set = list()
    rule_mappings = csv_like_str.split("\n")
    headers = rule_mappings[0].split(';')
    for line in rule_mappings[1:]:
        if line:
            rule_attrs = dict(zip(headers, line.split(';')))
            rule_set.append(rule_attrs)
    return rule_set
