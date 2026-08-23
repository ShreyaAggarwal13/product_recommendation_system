# ShopSmart — AI Personalized Product Recommendation System

Content-based recommendation engine (TF-IDF + Cosine Similarity) built with
Flask, SQLite, Pandas/Scikit-learn, and a vanilla HTML/CSS/JS frontend.

## Setup

```
cd product_recommender
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

## Run

```
python app.py
```

Open **http://127.0.0.1:5000** in your browser.
The SQLite database (`database/products.db`) and ~150 sample products are
created automatically on first run.

## Project Structure

```
product_recommender/
├── app.py              # Flask routes / API
├── database.py          # SQLite setup + access
├── recommender.py       # TF-IDF + cosine similarity engine
├── generate_data.py     # Sample product dataset generator
├── requirements.txt
├── database/             # products.db created at runtime
├── templates/            # HTML pages (Jinja)
└── static/
    ├── css/style.css
    └── js/                # app.js, index.js, products.js,
                            # preferences.js, recommendations.js, product.js
```

## API Endpoints

- `GET /api/products?q=&category=&brand=&min_price=&max_price=`
- `GET /api/products/<id>`
- `GET /api/categories`
- `GET /api/brands`
- `POST /api/recommend` — body: `{category, min_price, max_price, brands[], keywords}`

## Test Checklist

1. Home page loads, category tiles link to filtered product listing.
2. `/products` — search box, category/brand/price filters return correct results.
3. Click a product card → detail page shows image, price, rating, features.
4. `/preferences` — select category, price range, brands, keywords → submit.
5. Redirects to `/recommendations` showing ranked products with a
   "Recommended because..." reason for each.
