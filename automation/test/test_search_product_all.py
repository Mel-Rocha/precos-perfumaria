from automation.product.search import AutomationSearchProduct


def test_search_product_all():
    automation = AutomationSearchProduct()
    product = "Cabelo"
    site_domain = "https://www.ikesaki.com.br/"
    urls = automation.search_product_all(product, site_domain)
    print(urls)


if __name__ == "__main__":
    test_search_product_all()
