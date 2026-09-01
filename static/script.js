document.addEventListener('DOMContentLoaded', () => {
  const searchForm = document.querySelector('.search-form');

  if (!searchForm) {
    return;
  }

  const searchInput = searchForm.querySelector('input[type="text"]');

  if (!searchInput) {
    return;
  }

  searchForm.addEventListener('submit', (event) => {
    if (!searchInput.value.trim()) {
      event.preventDefault();
      searchInput.focus();
    }
  });
});
