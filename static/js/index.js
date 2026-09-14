const CATEGORY_EMOJI = {
  Electronics: '💻', Clothing: '👕', Shoes: '👟', Beauty: '💄',
  Home: '🏠', Books: '📚', Accessories: '👜'
};

async function loadCategories() {
  const categories = await fetchJSON('/api/categories');
  const grid = document.getElementById('category-grid');
  grid.innerHTML = categories.map(c => `
    <a class="category-card" href="/products?category=${encodeURIComponent(c)}"
       style="background-image: url('https://picsum.photos/seed/${encodeURIComponent(c)}/400/300')">
      <span class="info-chip">
        <span class="emoji">${CATEGORY_EMOJI[c] || '🛍️'}</span>
        <span class="cat-name">${c}</span>
      </span>
    </a>`).join('');
}
loadCategories();