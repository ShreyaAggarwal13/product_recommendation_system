import random

random.seed(42)

CATEGORY_DATA = {
    'Electronics': {
        'brands': ['Sony', 'Samsung', 'Boat', 'JBL', 'Mi', 'OnePlus'],
        'nouns': ['Wireless Headphones', 'Bluetooth Speaker', 'Smartwatch', 'Power Bank',
                  'Laptop Sleeve', 'Gaming Mouse', 'USB-C Hub', 'Earbuds', 'Fitness Band', 'Portable Charger'],
        'adjectives': ['compact', 'lightweight', 'durable', 'high-performance', 'noise-cancelling', 'fast-charging', 'waterproof', 'sleek'],
        'features_pool': ['long battery life', 'quick charge support', 'bluetooth 5.0', 'touch controls', 'IP67 rated',
                           'HD sound quality', 'ergonomic design', 'sweat resistant', 'voice assistant support', 'wireless connectivity'],
        'price_range': (499, 8999)
    },
    'Clothing': {
        'brands': ['Levis', 'H&M', 'Zara', 'Roadster', 'Allen Solly', 'US Polo'],
        'nouns': ['Cotton T-Shirt', 'Denim Jacket', 'Slim Fit Jeans', 'Formal Shirt', 'Hoodie',
                  'Track Pants', 'Casual Blazer', 'Sweatshirt', 'Chinos', 'Polo Shirt'],
        'adjectives': ['comfortable', 'stylish', 'breathable', 'trendy', 'classic', 'slim-fit', 'premium', 'casual'],
        'features_pool': ['pure cotton fabric', 'machine washable', 'wrinkle resistant', 'all season wear', 'regular fit',
                           'soft fabric', 'stretchable material', 'colorfast', 'quick dry', 'durable stitching'],
        'price_range': (399, 3499)
    },
    'Shoes': {
        'brands': ['Nike', 'Adidas', 'Puma', 'Woodland', 'Bata', 'Skechers'],
        'nouns': ['Running Shoes', 'Sneakers', 'Formal Loafers', 'Sports Shoes', 'Sandals',
                  'Casual Sneakers', 'Trekking Shoes', 'Slip-Ons', 'Basketball Shoes', 'Walking Shoes'],
        'adjectives': ['lightweight', 'cushioned', 'durable', 'breathable', 'anti-skid', 'comfortable', 'stylish', 'shock-absorbing'],
        'features_pool': ['memory foam insole', 'rubber sole', 'mesh upper', 'anti-slip grip', 'shock absorption',
                           'arch support', 'lace-up closure', 'lightweight design', 'water resistant', 'breathable mesh'],
        'price_range': (799, 6999)
    },
    'Beauty': {
        'brands': ['Lakme', 'Nykaa', 'Mamaearth', 'LOreal', 'Maybelline', 'Dove'],
        'nouns': ['Face Serum', 'Matte Lipstick', 'Sunscreen Lotion', 'Face Wash', 'Moisturizer',
                  'Hair Oil', 'Shampoo', 'Foundation', 'Lip Balm', 'Night Cream'],
        'adjectives': ['nourishing', 'hydrating', 'gentle', 'long-lasting', 'natural', 'lightweight', 'non-greasy', 'organic'],
        'features_pool': ['paraben free', 'vitamin C enriched', 'suitable for all skin types', 'dermatologically tested', 'SPF protection',
                           'cruelty free', 'natural ingredients', 'non-comedogenic', 'long lasting formula', 'travel friendly'],
        'price_range': (149, 1999)
    },
    'Home': {
        'brands': ['IKEA', 'Prestige', 'Milton', 'Cello', 'Philips', 'Bajaj'],
        'nouns': ['Non-Stick Cookware Set', 'LED Table Lamp', 'Storage Organizer', 'Ceramic Dinner Set', 'Air Fryer',
                  'Wall Clock', 'Bedsheet Set', 'Vacuum Flask', 'Study Table', 'Curtain Set'],
        'adjectives': ['durable', 'space-saving', 'elegant', 'easy-to-clean', 'energy-efficient', 'modern', 'compact', 'sturdy'],
        'features_pool': ['scratch resistant', 'energy efficient', 'easy to assemble', 'dishwasher safe', 'rust proof',
                           'compact design', 'long lasting build', 'stylish finish', 'heat resistant', 'eco friendly material'],
        'price_range': (299, 5999)
    },
    'Books': {
        'brands': ['Penguin', 'HarperCollins', 'Bloomsbury', 'Rupa', 'Scholastic', 'Oxford'],
        'nouns': ['Self-Help Book', 'Mystery Novel', 'Fantasy Novel', 'Biography', 'Science Fiction Novel',
                  'Business Book', 'Poetry Collection', 'Children Storybook', 'History Book', 'Thriller Novel'],
        'adjectives': ['bestselling', 'gripping', 'inspiring', 'thought-provoking', 'award-winning', 'must-read', 'engaging', 'insightful'],
        'features_pool': ['paperback edition', 'hardcover edition', 'award winning author', 'bestseller list', 'illustrated pages',
                           'easy to read', 'compact size', 'gift edition', 'includes bonus chapter', 'popular series'],
        'price_range': (149, 999)
    },
    'Accessories': {
        'brands': ['Fossil', 'Titan', 'Fastrack', 'Wildcraft', 'Da Milano', 'Ray-Ban'],
        'nouns': ['Leather Wallet', 'Analog Watch', 'Sunglasses', 'Backpack', 'Belt',
                  'Tote Bag', 'Cap', 'Neck Tie', 'Keychain', 'Travel Duffel Bag'],
        'adjectives': ['premium', 'stylish', 'durable', 'classic', 'lightweight', 'elegant', 'trendy', 'water-resistant'],
        'features_pool': ['genuine leather', 'water resistant', 'scratch resistant', 'adjustable strap', 'UV protection',
                           'spacious compartments', 'classic design', 'sturdy zippers', 'lightweight build', 'gift box packaging'],
        'price_range': (299, 4999)
    }
}


def generate_products():
    products = []
    pid = 1
    for category, data in CATEGORY_DATA.items():
        combos = [(b, n) for b in data['brands'] for n in data['nouns']]
        random.shuffle(combos)
        selected = combos[:22]
        for brand, noun in selected:
            adj = random.choice(data['adjectives'])
            feats = random.sample(data['features_pool'], k=4)
            price = round(random.uniform(*data['price_range']), 2)
            rating = round(random.uniform(3.3, 5.0), 1)
            name = f"{brand} {adj.title()} {noun}"
            description = (f"{adj.capitalize()} {noun.lower()} by {brand}, crafted for everyday "
                            f"{category.lower()} needs. Combines quality, value and reliable performance.")
            features = ', '.join(feats)
            image_url = f"https://picsum.photos/seed/{pid}/400/300"
            products.append({
                'name': name, 'category': category, 'brand': brand,
                'price': price, 'rating': rating, 'description': description,
                'features': features, 'image_url': image_url
            })
            pid += 1
    return products
