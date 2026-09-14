from flask import Flask, render_template, request, jsonify
from database import init_db, get_db
from recommender import Recommender

app = Flask(__name__)
init_db()
recommender = Recommender()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/products')
def products_page():
    return render_template('products.html')


@app.route('/preferences')
def preferences_page():
    return render_template('preferences.html')


@app.route('/recommendations')
def recommendations_page():
    return render_template('recommendations.html')


@app.route('/product')
def product_page():
    return render_template('product.html')


@app.route('/api/products')
def api_products():
    conn = get_db()
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    brand = request.args.get('brand', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = 'SELECT * FROM products WHERE 1=1'
    params = []
    if q:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params += [f'%{q}%', f'%{q}%']
    if category:
        query += ' AND category = ?'
        params.append(category)
    if brand:
        query += ' AND brand = ?'
        params.append(brand)
    if min_price is not None:
        query += ' AND price >= ?'
        params.append(min_price)
    if max_price is not None:
        query += ' AND price <= ?'
        params.append(max_price)
    query += ' ORDER BY rating DESC'

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/products/<int:pid>')
def api_product_detail(pid):
    conn = get_db()
    row = conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'not found'}), 404
    return jsonify(dict(row))


@app.route('/api/categories')
def api_categories():
    conn = get_db()
    rows = conn.execute('SELECT DISTINCT category FROM products ORDER BY category').fetchall()
    conn.close()
    return jsonify([r['category'] for r in rows])


@app.route('/api/brands')
def api_brands():
    conn = get_db()
    rows = conn.execute('SELECT DISTINCT brand FROM products ORDER BY brand').fetchall()
    conn.close()
    return jsonify([r['brand'] for r in rows])


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.get_json(force=True) or {}
    category = data.get('category') or None
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    brands = data.get('brands') or []
    keywords = data.get('keywords', '')

    conn = get_db()
    conn.execute('INSERT INTO user_preferences (category, min_price, max_price, brands, keywords) VALUES (?,?,?,?,?)',(category, min_price, max_price, ','.join(brands), keywords))
    conn.commit()
    conn.close()

    recs = recommender.recommend(category=category, min_price=min_price, max_price=max_price,brands=brands, keywords=keywords, top_n=12)
    return jsonify(recs)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
