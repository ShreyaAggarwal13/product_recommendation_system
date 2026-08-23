const stored = sessionStorage.getItem('recommendations');
const grid = document.getElementById('rec-grid');

if (!stored) {
  grid.innerHTML = '<p>No recommendations yet. <a href="/preferences">Set your preferences</a> first.</p>';
} else {
  const recs = JSON.parse(stored);
  grid.innerHTML = recs.length
    ? recs.map(p => productCardHTML(p, true)).join('')
    : '<p>No matching products found. Try broadening your preferences.</p>';
}
