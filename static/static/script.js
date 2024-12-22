// ------------------------------------------------------------
// 0) Глобальные переменные
// ------------------------------------------------------------
let originalCards = [];
const filterPopover = document.getElementById('filterPopover');
let popoverVisible = false;

document.addEventListener('DOMContentLoaded', () => {
  const productContainer = document.getElementById('productContainer');
  if (productContainer) {
    originalCards = Array.from(productContainer.querySelectorAll('.product-card'));
  }
  renderSearchHistory();
});

// ------------------------------------------------------------
// 1) Мобильное меню
// ------------------------------------------------------------
function toggleMenu() {
  const navList = document.querySelector('.nav-list');
  if (navList) {
    navList.classList.toggle('open');
  }
}

// ------------------------------------------------------------
// 2) changeQuantity
// ------------------------------------------------------------
function changeQuantity(delta, id) {
  const input = document.getElementById(`quantity-${id}`);
  if (!input) return;
  let currentValue = parseInt(input.value);
  const minValue = parseInt(input.min);
  const maxValue = parseInt(input.max);

  const newValue = currentValue + delta;
  if (newValue >= minValue && newValue <= maxValue) {
    input.value = newValue;
  }
}

// ------------------------------------------------------------
// 3) toggleFavorite
// ------------------------------------------------------------
async function toggleFavorite(event, productId, isFavorite) {
  event.stopPropagation();
  const icon = event.target;
  
  try {
    const url = isFavorite ? '/remove_from_favorites' : '/add_to_favorites';
    const formData = new FormData();
    formData.append('product_id', productId);

    const response = await fetch(url, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();

    if (response.ok && data.success) {
      if (isFavorite) {
        icon.classList.remove('red');
        icon.classList.add('gray');
        icon.setAttribute('onclick', `toggleFavorite(event, '${productId}', false)`);
      } else {
        icon.classList.remove('gray');
        icon.classList.add('red');
        icon.setAttribute('onclick', `toggleFavorite(event, '${productId}', true)`);
      }
    } else {
      alert(data.error || 'Ошибка при работе с «Избранным»');
    }
  } catch (error) {
    console.error('toggleFavorite error:', error);
    alert('Ошибка сети при работе с «Избранным».');
  }
}

// ------------------------------------------------------------
// 4) Иконка "Фильтр" (popover)
// ------------------------------------------------------------
function toggleFilterPopover() {
  popoverVisible = !popoverVisible;
  if (popoverVisible) {
    filterPopover.classList.add('visible');
  } else {
    filterPopover.classList.remove('visible');
  }
}

// Закрыть popover, если кликнули вне иконки
document.addEventListener('click', (event) => {
  const filterIconContainer = document.querySelector('.filter-icon-container');
  if (
    popoverVisible &&
    !filterPopover.contains(event.target) &&
    !filterIconContainer.contains(event.target)
  ) {
    filterPopover.classList.remove('visible');
    popoverVisible = false;
  }
});

// ------------------------------------------------------------
// 5) Применение сортировки
// ------------------------------------------------------------
function applyFilter() {
  let sortOption = document.querySelector('input[name="sortOption"]:checked');
  if (!sortOption) {
    alert('Выберите параметр сортировки');
    return;
  }
  sortOption = sortOption.value;

  toggleFilterPopover();

  const productContainer = document.getElementById('productContainer');
  if (!productContainer) return;

  let productCards = originalCards.slice();

  let productsData = productCards.map(card => {
    const nameElem = card.querySelector('.product-title');
    const priceElem = card.querySelector('.product-price');
    const name = nameElem ? nameElem.textContent.trim() : '';
    const priceText = priceElem ? priceElem.textContent : '0';
    const priceNum = parseFloat(priceText.replace(/[^\d.]/g, '')) || 0;
    return { name, price: priceNum, element: card };
  });

  switch (sortOption) {
    case 'nameAsc':
      productsData.sort((a, b) => a.name.localeCompare(b.name, 'ru', {sensitivity: 'base'}));
      break;
    case 'nameDesc':
      productsData.sort((a, b) => b.name.localeCompare(a.name, 'ru', {sensitivity: 'base'}));
      break;
    case 'priceAsc':
      productsData.sort((a, b) => a.price - b.price);
      break;
    case 'priceDesc':
      productsData.sort((a, b) => b.price - a.price);
      break;
  }

  productContainer.innerHTML = '';
  productsData.forEach(item => {
    productContainer.appendChild(item.element);
  });
}

// ------------------------------------------------------------
// 6) "Умный" поиск (fuzzy) + История (даже если 0 товаров)
// ------------------------------------------------------------
function smartSearchSubmit(event) {
  event.preventDefault();

  const input = document.getElementById('searchInput');
  if (!input) return false;

  const query = input.value.trim().toLowerCase();
  if (!query) {
    showAllProducts();
    return false;
  }

  // Сразу сохраняем запрос в историю (даже если 0 товаров)
  addSearchToHistory(input.value.trim());

  const productContainer = document.getElementById('productContainer');
  if (!productContainer) return false;

  let productCards = originalCards.slice();

  // 1) Точное вхождение
  let matchedCards = productCards.filter(card => {
    const productName = (card.dataset.productName || '').toLowerCase();
    return productName.includes(query);
  });

  // 2) Если нет, fuzzy
  if (matchedCards.length === 0) {
    const THRESHOLD = 0.7;
    matchedCards = productCards.filter(card => {
      const productName = (card.dataset.productName || '').toLowerCase();
      const ratio = similarityRatio(query, productName);
      return ratio >= THRESHOLD;
    });
  }

  // 3) Вывод
  if (matchedCards.length === 0) {
    productContainer.innerHTML = `<p class="no-products">Продукты не найдены.</p>`;
  } else {
    productContainer.innerHTML = '';
    matchedCards.forEach(card => {
      productContainer.appendChild(card);
    });
  }

  return false;
}

function showAllProducts() {
  const productContainer = document.getElementById('productContainer');
  if (!productContainer) return;

  productContainer.innerHTML = '';
  originalCards.forEach(card => {
    productContainer.appendChild(card);
  });
}

// ------------------------------------------------------------
// 7) История поиска (LocalStorage)
// ------------------------------------------------------------
function addSearchToHistory(query) {
  if (!query) return;
  let history = loadSearchHistory();

  // Не дублируем подряд одинаковый запрос
  if (history.length > 0 && history[history.length - 1] === query) {
    return;
  }

  history.push(query);
  saveSearchHistory(history);
  renderSearchHistory();
}

function removeSearchItem(index) {
  let history = loadSearchHistory();
  history.splice(index, 1);
  saveSearchHistory(history);
  renderSearchHistory();
}

function clearSearchHistory() {
  localStorage.removeItem('searchHistory');
  renderSearchHistory();
}

function renderSearchHistory() {
  const listEl = document.getElementById('historyList');
  if (!listEl) return;

  let history = loadSearchHistory();
  listEl.innerHTML = '';

  history.forEach((item, idx) => {
    const li = document.createElement('li');

    // Текст запроса
    const span = document.createElement('span');
    span.textContent = item;

    // Кнопка удаления отдельного запроса
    const delBtn = document.createElement('button');
    delBtn.classList.add('delete-history-item');
    delBtn.innerHTML = '<i class="fas fa-times"></i>';
    delBtn.onclick = () => {
      history.splice(idx, 1);
      saveSearchHistory(history);
      renderSearchHistory();
    };

    li.appendChild(span);
    li.appendChild(delBtn);
    listEl.appendChild(li);
  });
}

function loadSearchHistory() {
  let data = localStorage.getItem('searchHistory');
  if (!data) return [];
  try {
    return JSON.parse(data);
  } catch(e) {
    console.warn('Ошибка парсинга localStorage:', e);
    return [];
  }
}

function saveSearchHistory(arr) {
  localStorage.setItem('searchHistory', JSON.stringify(arr));
}

// ------------------------------------------------------------
// 8) Левенштейн + similarityRatio
// ------------------------------------------------------------
function levenshteinDistance(a, b) {
  const matrix = [];
  const lenA = a.length;
  const lenB = b.length;

  for (let i = 0; i <= lenA; i++) {
    matrix[i] = [i];
  }
  for (let j = 1; j <= lenB; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= lenA; i++) {
    for (let j = 1; j <= lenB; j++) {
      const cost = (a[i - 1] === b[j - 1]) ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  return matrix[lenA][lenB];
}

function similarityRatio(a, b) {
  const dist = levenshteinDistance(a, b);
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 1;
  return 1 - dist / maxLen;
}
