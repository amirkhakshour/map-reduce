import pytest

from main import mapping
from mapper import build_rule_tree

_RULE_MAPPING_FLAT = """source;destination;source_type;destination_type
winter;Winter;season;season
summer;Summer;season;season
"""

_RULE_MAPPING_FLAT_TREE = {
    "season": {
        "winter": {"_mapping": mapping("season", "Winter")},
        "summer": {"_mapping": mapping("season", "Summer")},
    }
}

_RULE_MAPPING_NESTED = """source;destination;source_type;destination_type
EU;European sizes;size_group_code;size_group
EU|36;European size 36;size_group_code|size_code;size
EU|36|adult;European size 36 adults;size_group_code|size_code|group;size
EU|36|kid;European size 36 kids;size_group_code|size_code|group;size
EU|37;European size 37;size_group_code|size_code;size
"""

_RULE_MAPPING_NESTED_TREE = {
    "size_group_code": {
        "EU": {
            "_mapping": mapping("size_group", "European sizes"),
            "size_code": {
                "36": {
                    "_mapping": mapping("size", "European size 36"),
                    "group": {
                        "adult": {
                            "_mapping": mapping("size",
                                                "European size 36 adults"),
                        },
                        "kid": {
                            "_mapping": mapping("size",
                                                "European size 36 kids"),
                        },
                    },
                },
                "37": {
                    "_mapping": mapping("size",
                                        "European size 37")
                }
            }
        }
    }
}

_RULE_MAPPING_NESTED_WITH_NO_PARENT_MAPPING = """source;destination;source_type;destination_type
EU|36;European size 36;size_group_code|size_code;size
"""

_RULE_MAPPING_NESTED_WITH_NO_PARENT_MAPPING_TREE = {
    "size_group_code": {
        "EU": {
            "size_code": {
                "36": {
                    "_mapping": mapping("size", "European size 36")
                }
            }
        }
    }
}


def raw_rules_to_dict(raw_rules):
    rule_mappings = raw_rules.split("\n")
    headers = rule_mappings[0].split(';')
    for line in rule_mappings[1:]:
        if line:
            yield dict(zip(headers, line.split(';')))


@pytest.mark.parametrize("raw_ruleset, result_tree", [
    (_RULE_MAPPING_FLAT, _RULE_MAPPING_FLAT_TREE),
    (_RULE_MAPPING_NESTED, _RULE_MAPPING_NESTED_TREE),
    (_RULE_MAPPING_NESTED_WITH_NO_PARENT_MAPPING,
     _RULE_MAPPING_NESTED_WITH_NO_PARENT_MAPPING_TREE),
])
def test_build_rule_tree(raw_ruleset, result_tree):
    tree = dict()
    for rule in raw_rules_to_dict(raw_ruleset):
        build_rule_tree(rule, tree)
    assert tree == result_tree
