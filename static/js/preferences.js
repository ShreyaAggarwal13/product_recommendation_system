async function initForm() {
  const categories = await fetchJSON('/api/categories');
  const catSel = document.getElementById('pref-category');
  categories.forEach(c => catSel.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`));

  const brands = await fetchJSON('/api/brands');
  const box = document.getElementById('brand-checkboxes');
  box.innerHTML = brands.map(b => `
    <label><input type="checkbox" value="${b}" name="brand"> ${b}</label>`).join('');
}
initForm();

document.getElementById('preferences-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const brands = Array.from(document.querySelectorAll('input[name="brand"]:checked')).map(cb => cb.value);
  const payload = {
    category: document.getElementById('pref-category').value || null,
    min_price: document.getElementById('pref-min-price').value || null,
    max_price: document.getElementById('pref-max-price').value || null,
    brands: brands,
    keywords: document.getElementById('pref-keywords').value
  };
  const recs = await fetchJSON('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  sessionStorage.setItem('recommendations', JSON.stringify(recs));
  window.location.href = '/recommendations';
});
