function productCardHTML(product, isRecommended = false) {
  const image = product.image_url || product.image || '/static/images/placeholder.jpg';
  const name = product.name || 'Unnamed product';
  const description = product.description || 'No description available.';
  const category = product.category || 'General';
  const rating = Number(product.rating || 0).toFixed(1);
  const price = Number(product.price || 0).toFixed(2);

  return `
    <article class="product-card ${isRecommended ? 'recommended' : ''}">
      <a href="/product?id=${product.id}">
        <img src="${image}" alt="${name}" loading="lazy">
      </a>
      <div class="product-card-body">
        <div class="product-meta">
          <span>${category}</span>
          <span>⭐ ${rating}</span>
        </div>
        <h3><a href="/product?id=${product.id}">${name}</a></h3>
        <p>${description}</p>
        <div class="product-footer">
          <strong>$${price}</strong>
        </div>
      </div>
    </article>
  `;
}

const stored = sessionStorage.getItem('recommendations');
const grid = document.getElementById('rec-grid');

if (!grid) {
  console.warn('No recommendations grid found on this page.');
} else if (!stored) {
  grid.innerHTML = '<p>No recommendations yet. <a href="/preferences">Set your preferences</a> first.</p>';
} else {
  try {
    const recs = JSON.parse(stored);
    grid.innerHTML = recs.length
      ? recs.map((p) => productCardHTML(p, true)).join('')
      : '<p>No matching products found. Try broadening your preferences.</p>';
  } catch (err) {
    console.error('Failed to parse recommendations:', err);
    grid.innerHTML = '<p>Could not load recommendations.</p>';
  }
}