const id = new URLSearchParams(window.location.search).get('id');
const wrap = document.getElementById('product-detail');

async function loadProduct() {
  if (!id) { wrap.innerHTML = '<p>No product selected.</p>'; return; }
  try {
    const p = await fetchJSON(`/api/products/${id}`);
    const features = p.features.split(',').map(f => `<li>${f.trim()}</li>`).join('');
    wrap.innerHTML = `
      <img src="${p.image_url}" alt="${p.name}">
      <div class="info">
        <span class="cat-tag">${p.category}</span>
        <h1>${p.name}</h1>
        <p class="brand">Brand: ${p.brand}</p>
        <div class="price-large">₹${p.price}</div>
        <p class="rating">★ ${p.rating} / 5</p>
        <p>${p.description}</p>
        <h4>Key Features</h4>
        <ul class="feature-list">${features}</ul>
        <a href="/products" class="btn btn-outline">Back to Products</a>
      </div>`;
  } catch (e) {
    wrap.innerHTML = '<p>Product not found.</p>';
  }
}
loadProduct();
