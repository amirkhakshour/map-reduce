from collections import defaultdict


def group_products(products):
    """
    Group products on two level:
    A: article number
    B: product attribute variations
    :param products:
    :return:
    """
    catalog = dict()
    variation_attrs = defaultdict(list)
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
        product_branch = brand_branch[product['article_number']]
        if 'default_attrs' not in product_branch:
            product_branch['default_attrs'] = product
        else:
            """
            Our strategy:
            1- for each product attribute, check the values with the default 
            values that belongs to that article number, if any value is 
            different than the default one then:
             1-1: add the attr to variation_attrs list of that article number, 
             1-2: remove those attributes from default_attrs of that article 
                number
             1-3: add those attributes to each variations of 
             that article number
             1-4: build `new_variation` from current processing product and 
             list of variation_attrs and if this `new_variation` is unique 
             amongst other variations, add it as a new variation 
            """
            default_attrs = dict(product_branch['default_attrs'])
            new_diff_list = list()
            for attr, value in default_attrs.items():
                if product[attr] != value:
                    # remove variation from default values and add as variation
                    variation_attrs[product['article_number']].append(attr)
                    new_diff_list.append(attr)
                    del product_branch['default_attrs'][attr]

            removed_from_default = {
                attr: default_attrs[attr] for attr in
                new_diff_list
            }
            new_variation = {attr: product[attr] for attr in
                             variation_attrs[product['article_number']]}
            if new_variation:
                variations = product_branch['variations']
                if not variations:
                    # if the article is the first variation
                    variations.append(removed_from_default)
                else:
                    # we should add diff set to old variations
                    for var in variations:
                        var.update(removed_from_default)
                # check if the new variation is new if so, add it as a new
                # variation
                var_is_different = dict()
                for _var_id, var in enumerate(variations):
                    var_is_different[_var_id] = False
                    for attr, value in new_variation.items():
                        if var[attr] != value:
                            var_is_different[_var_id] = True
                            continue
                if all(var_is_different.values()):
                    variations.append(new_variation)
    return catalog
