from collections import defaultdict


def get_or_create_brand(product, catalog):
    # add brand if not exists
    if product['brand'] not in catalog:
        catalog[product['brand']] = dict()
    return catalog.get(product['brand'])


def get_or_create_article(product, root):
    # add article number if not exists
    if product['article_number'] not in root:
        root[product['article_number']] = dict(
            article_number=product['article_number'],
            variations=list(),
        )
    return root.get(product['article_number'])


def add_product_to_article(product, article):
    if '_default_attrs' not in article:
        article['_default_attrs'] = product

    product_diff_article = dict()
    for attr, value in product.items():
        if attr not in article['_default_attrs'] or \
                article['_default_attrs'][attr] != value:
            product_diff_article[attr] = value

    article_diff = dict()
    for attr, value in dict(article['_default_attrs']).items():
        if attr in product_diff_article:
            article_diff[attr] = value
            del article['_default_attrs'][attr]

    if article_diff and not article['variations']:
        article['variations'].append(article_diff)

    new_variation = product_diff_article

    # add diff_attrs to already variations
    variation_is_new = True
    for var in article['variations']:
        var.update(article_diff)
        if new_variation == var:
            variation_is_new = False

    if variation_is_new:
        article['variations'].append(new_variation)


def add_product_to_brand(product, brand):
    if '_default_attrs' not in brand:
        brand['_default_attrs'] = product

    brand_diff = dict()
    # find new variation by comparing product and brand default attrs
    product_diff_brand = dict()
    for attr, value in product.items():
        if attr not in brand['_default_attrs'] or \
                brand['_default_attrs'][attr] != value:
            product_diff_brand[attr] = value

    for attr, value in dict(brand['_default_attrs']).items():
        if attr in product_diff_brand:
            brand_diff[attr] = value
            del brand['_default_attrs'][attr]

    if brand_diff:
        # move brand diff to article default values
        for _article_no, _article in brand.items():
            if _article_no != '_default_attrs' and '_default_attrs' in _article:
                _article['_default_attrs'].update(
                    brand_diff
                )

    article = get_or_create_article(product, brand)
    add_product_to_article(product_diff_brand, article)


def group_product(product, catalog):
    brand = get_or_create_brand(product, catalog)
    add_product_to_brand(product, brand)


def group_products(products):
    """
    Group products on two level:
    A: article number
    B: product attribute variations
    :param products:
    :return:
    """
    catalog = defaultdict(dict)
    for product in products:
        group_product(product, catalog)
    return catalog
