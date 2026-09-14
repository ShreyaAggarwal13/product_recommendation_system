async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      Accept: 'application/json',
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Request failed (${response.status}): ${text}`);
  }

  return response.json();
}

async function initForm() {
  try {
    const [categories, brands] = await Promise.all([
      fetchJson('/api/categories'),
      fetchJson('/api/brands')
    ]);

    const catSel = document.getElementById('pref-category');
    if (catSel) {
      catSel.innerHTML = '<option value="">Any category</option>';
      categories.forEach((c) => {
        catSel.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`);
      });
    }

    const box = document.getElementById('brand-checkboxes');
    if (box) {
      box.innerHTML = brands
        .map((b) => `
          <label>
            <input type="checkbox" value="${b}" name="brand">
            ${b}
          </label>
        `)
        .join('');
    }
  } catch (err) {
    console.error('Failed to load filter options:', err);
  }
}

initForm();

document.getElementById('preferences-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const brands = Array.from(document.querySelectorAll('input[name="brand"]:checked')).map((cb) => cb.value);
  const payload = {
    category: document.getElementById('pref-category').value || null,
    min_price: document.getElementById('pref-min-price').value || null,
    max_price: document.getElementById('pref-max-price').value || null,
    brands,
    keywords: document.getElementById('pref-keywords').value || ''
  };

  try {
    const recs = await fetchJson('/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    sessionStorage.setItem('recommendations', JSON.stringify(recs || []));
    window.location.href = '/recommendations';
  } catch (err) {
    console.error('Failed to fetch recommendations:', err);
    alert('Could not load recommendations. Please try again.');
  }
});