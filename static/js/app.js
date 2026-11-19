const CATEGORY_FALLBACK = {
  Accessories: '/static/Images/Accessories.jpg',
  Beauty:      '/static/Images/Beauty.jpg',
  Books:       '/static/Images/Books.jpg',
  Clothing:    '/static/Images/Clothing.jpg',
  Electronics: '/static/Images/Electronics.jpg',
  Home:        '/static/Images/Home.jpg',
  Shoes:       '/static/Images/Shoes.jpg'
};

function productCardHTML(p, showReason) {
  const reason = showReason && p.reason ? `<div class="reason">${p.reason}</div>` : '';
  return `
  <a class="product-card" href="/product?id=${p.id}">
    <img src="${p.image_url}" alt="${p.name}" onerror="this.onerror=null;this.src=CATEGORY_FALLBACK['${p.category}']">
    <div class="card-body">
      <span class="cat-tag">${p.category}</span>
      <h4>${p.name}</h4>
      <span class="brand">${p.brand}</span>
      <div class="price-row">
        <span class="price">₹${p.price}</span>
        <span class="rating">★ ${p.rating}</span>
      </div>
      ${reason}
    </div>
  </a>`;
}

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error('Request failed: ' + url);
  return res.json();
}
