const params = new URLSearchParams(window.location.search);

async function initFilters() {
  const [categories, brands] = await Promise.all([
    fetchJSON('/api/categories'), fetchJSON('/api/brands')
  ]);
  const catSel = document.getElementById('filter-category');
  categories.forEach(c => catSel.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`));
  const brandSel = document.getElementById('filter-brand');
  brands.forEach(b => brandSel.insertAdjacentHTML('beforeend', `<option value="${b}">${b}</option>`));

  if (params.get('category')) catSel.value = params.get('category');
}

function buildQuery() {
  const q = new URLSearchParams();
  if (params.get('q')) q.set('q', params.get('q'));
  const category = document.getElementById('filter-category').value;
  const brand = document.getElementById('filter-brand').value;
  const min = document.getElementById('filter-min').value;
  const max = document.getElementById('filter-max').value;
  if (category) q.set('category', category);
  if (brand) q.set('brand', brand);
  if (min) q.set('min_price', min);
  if (max) q.set('max_price', max);
  return q.toString();
}

async function loadProducts() {
  const products = await fetchJSON('/api/products?' + buildQuery());
  document.getElementById('results-count').textContent = `${products.length} product(s) found`;
  document.getElementById('product-grid').innerHTML = products.map(p => productCardHTML(p, false)).join('') ||
    '<p>No products match your filters.</p>';
}

document.getElementById('apply-filters').addEventListener('click', loadProducts);
document.getElementById('clear-filters').addEventListener('click', () => {
  document.getElementById('filter-category').value = '';
  document.getElementById('filter-brand').value = '';
  document.getElementById('filter-min').value = '';
  document.getElementById('filter-max').value = '';
  window.history.replaceState({}, '', '/products');
  loadProducts();
});

(async () => {
  await initFilters();
  loadProducts();
})();
