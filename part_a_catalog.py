# Part A - E-Commerce Product Catalog System
# Uses nested dicts, defaultdict, and dict comprehensions

from collections import defaultdict

# ---- Data Setup ----

catalog = {
    'SKU001': {'name': 'Laptop',          'price': 65000, 'category': 'electronics', 'stock': 15, 'rating': 4.5, 'tags': ['computer', 'work', 'portable']},
    'SKU002': {'name': 'Wireless Mouse',  'price': 799,   'category': 'electronics', 'stock': 0,  'rating': 4.1, 'tags': ['computer', 'accessory']},
    'SKU003': {'name': 'Mechanical Keyboard', 'price': 3500, 'category': 'electronics', 'stock': 8, 'rating': 4.7, 'tags': ['computer', 'accessory', 'work']},
    'SKU004': {'name': 'Bluetooth Speaker', 'price': 2200, 'category': 'electronics', 'stock': 20, 'rating': 4.3, 'tags': ['audio', 'portable']},
    'SKU005': {'name': 'USB-C Hub',       'price': 1599,  'category': 'electronics', 'stock': 0,  'rating': 3.9, 'tags': ['accessory', 'work', 'computer']},
    'SKU006': {'name': 'Men\'s T-Shirt',  'price': 499,   'category': 'clothing',    'stock': 50, 'rating': 3.8, 'tags': ['casual', 'summer', 'men']},
    'SKU007': {'name': 'Women\'s Kurti',  'price': 799,   'category': 'clothing',    'stock': 30, 'rating': 4.2, 'tags': ['ethnic', 'women', 'summer']},
    'SKU008': {'name': 'Denim Jacket',    'price': 2499,  'category': 'clothing',    'stock': 0,  'rating': 4.4, 'tags': ['casual', 'winter', 'unisex']},
    'SKU009': {'name': 'Sports Shorts',   'price': 699,   'category': 'clothing',    'stock': 25, 'rating': 3.6, 'tags': ['sports', 'summer', 'men']},
    'SKU010': {'name': 'Python Programming', 'price': 650, 'category': 'books',     'stock': 100,'rating': 4.8, 'tags': ['tech', 'programming', 'python']},
    'SKU011': {'name': 'Data Structures & Algorithms', 'price': 899, 'category': 'books', 'stock': 60, 'rating': 4.6, 'tags': ['tech', 'programming', 'dsa']},
    'SKU012': {'name': 'Atomic Habits',   'price': 399,   'category': 'books',       'stock': 80, 'rating': 4.9, 'tags': ['self-help', 'productivity']},
    'SKU013': {'name': 'Rich Dad Poor Dad', 'price': 299, 'category': 'books',      'stock': 0,  'rating': 4.5, 'tags': ['finance', 'self-help']},
    'SKU014': {'name': 'Basmati Rice 5kg', 'price': 550,  'category': 'food',        'stock': 200,'rating': 4.2, 'tags': ['grocery', 'staple', 'rice']},
    'SKU015': {'name': 'Mixed Dry Fruits', 'price': 1299, 'category': 'food',        'stock': 45, 'rating': 4.4, 'tags': ['snack', 'healthy', 'premium']},
    'SKU016': {'name': 'Green Tea 100g',  'price': 349,   'category': 'food',        'stock': 90, 'rating': 4.3, 'tags': ['beverage', 'healthy', 'tea']},
}


# 1. Search products by tag (uses defaultdict to group all products under each tag)
def search_by_tag(tag):
    tag_map = defaultdict(list)
    for sku, details in catalog.items():
        for t in details.get('tags', []):
            tag_map[t].append({'sku': sku, 'name': details.get('name')})
    return tag_map.get(tag, [])


# 2. Out of stock products (dict comprehension with filter on stock == 0)
def out_of_stock():
    return {sku: info for sku, info in catalog.items() if info.get('stock', 1) == 0}


# 3. Filter products within a price range
def price_range(min_price, max_price):
    return {
        sku: info for sku, info in catalog.items()
        if min_price <= info.get('price', 0) <= max_price
    }


# 4. Category summary: count, avg price, avg rating per category
def category_summary():
    cat_data = defaultdict(list)
    for info in catalog.values():
        cat = info.get('category', 'unknown')
        cat_data[cat].append(info)

    summary = {}
    for cat, products in cat_data.items():
        prices = [p.get('price', 0) for p in products]
        ratings = [p.get('rating', 0) for p in products]
        summary[cat] = {
            'count': len(products),
            'avg_price': round(sum(prices) / len(prices), 2),
            'avg_rating': round(sum(ratings) / len(ratings), 2)
        }
    return summary


# 5. Apply discount to a category (dict comprehension updates price)
def apply_discount(category, percent):
    multiplier = 1 - (percent / 100)
    return {
        sku: {**info, 'price': round(info.get('price', 0) * multiplier, 2)}
        if info.get('category') == category else {**info}
        for sku, info in catalog.items()
    }


# 6. Merge two catalogs; if duplicate SKU, second catalog wins
def merge_catalogs(catalog1, catalog2):
    return {**catalog1, **catalog2}
    # In Python 3.9+ you can also write: catalog1 | catalog2


# ---- Demo / Output ----

if __name__ == "__main__":
    print("=" * 55)
    print("  E-Commerce Product Catalog System")
    print("=" * 55)

    print("\n--- search_by_tag('computer') ---")
    results = search_by_tag('computer')
    for r in results:
        print(f"  {r['sku']}: {r['name']}")

    print("\n--- out_of_stock() ---")
    oos = out_of_stock()
    for sku, info in oos.items():
        print(f"  {sku}: {info['name']}")

    print("\n--- price_range(500, 2000) ---")
    pr = price_range(500, 2000)
    for sku, info in pr.items():
        print(f"  {sku}: {info['name']} - ₹{info['price']}")

    print("\n--- category_summary() ---")
    cs = category_summary()
    for cat, stats in cs.items():
        print(f"  {cat}: {stats}")

    print("\n--- apply_discount('electronics', 10) ---")
    discounted = apply_discount('electronics', 10)
    for sku, info in discounted.items():
        if info.get('category') == 'electronics':
            print(f"  {sku}: {info['name']} -> ₹{info['price']}")

    print("\n--- merge_catalogs() ---")
    extra_catalog = {
        'SKU017': {'name': 'Smart Watch', 'price': 8999, 'category': 'electronics',
                   'stock': 10, 'rating': 4.6, 'tags': ['wearable', 'tech']}
    }
    merged = merge_catalogs(catalog, extra_catalog)
    print(f"  Original catalog size: {len(catalog)}")
    print(f"  Merged catalog size:   {len(merged)}")
    print(f"  New product: {merged['SKU017']['name']}")
