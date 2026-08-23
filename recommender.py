import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import get_db


def _load_products_df():
    conn = get_db()
    df = pd.read_sql_query('SELECT * FROM products', conn)
    conn.close()
    return df


def _combined_text(row):
    return f"{row['category']} {row['brand']} {row['description']} {row['features']}"


class Recommender:
    def __init__(self):
        self.refresh()

    def refresh(self):
        self.df = _load_products_df()
        self.df['combined'] = self.df.apply(_combined_text, axis=1)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined'])

    def recommend(self, category=None, min_price=None, max_price=None, brands=None, keywords='', top_n=12):
        df = self.df
        mask = pd.Series(True, index=df.index)
        if category:
            mask &= df['category'] == category
        if min_price not in (None, ''):
            mask &= df['price'] >= float(min_price)
        if max_price not in (None, ''):
            mask &= df['price'] <= float(max_price)

        candidates = df[mask]
        if candidates.empty:
            candidates = df  # fallback: ignore strict filters rather than return nothing

        query_parts = []
        if category:
            query_parts.append(category)
        if brands:
            query_parts.append(' '.join(brands))
        if keywords:
            query_parts.append(keywords)
        query_text = ' '.join(query_parts) if query_parts else 'popular quality product'

        query_vec = self.vectorizer.transform([query_text])
        cand_idx = candidates.index
        cand_vectors = self.tfidf_matrix[cand_idx]
        sims = cosine_similarity(query_vec, cand_vectors).flatten()

        results = candidates.copy()
        results['similarity'] = sims
        results['brand_match'] = results['brand'].isin(brands).astype(float) * 0.15 if brands else 0.0
        results['score'] = results['similarity'] + results['brand_match'] + (results['rating'] / 5.0) * 0.1
        results = results.sort_values('score', ascending=False).head(top_n)

        recs = []
        for _, r in results.iterrows():
            reasons = []
            if category and r['category'] == category:
                reasons.append(f"matches your preferred category '{category}'")
            if brands and r['brand'] in brands:
                reasons.append(f"from a brand you like ({r['brand']})")
            if keywords:
                kw_hits = [w for w in keywords.lower().split() if w in r['combined'].lower()]
                if kw_hits:
                    reasons.append(f"matches your keywords: {', '.join(kw_hits[:3])}")
            if r['rating'] >= 4.5:
                reasons.append('highly rated by other users')
            if not reasons:
                reasons.append('similar to your preference profile based on content similarity')
            recs.append({
                'id': int(r['id']), 'name': r['name'], 'category': r['category'],
                'brand': r['brand'], 'price': r['price'], 'rating': r['rating'],
                'description': r['description'], 'features': r['features'],
                'image_url': r['image_url'], 'score': round(float(r['score']), 4),
                'reason': 'Recommended because it ' + '; '.join(reasons) + '.'
            })
        return recs
