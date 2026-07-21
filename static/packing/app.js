/* ── State ────────────────────────────────────────────────── */
const state = {
  products:   [],   // [{id, name, length, width, height, weight}]
  boxes:      [],   // [{id, name, inner_length, inner_width, inner_height, max_weight, cost}]
  orders:     [],   // [{id, created_at, items: [...]}]
  orderItems: [],   // [{product, quantity}]
};

/* ── API helpers ─────────────────────────────────────────── */
async function api(method, url, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}

function setMsg(el, text, type) {
  if (!el) return;
  el.textContent = text;
  el.className = 'form-msg ' + type;
}

function formatErrors(data) {
  if (typeof data === 'string') return data;
  return Object.values(data).flat().join(' ');
}

/* ── Modals ────────────────────────────────────────────────── */
function openModal(modalId) {
  document.getElementById(modalId).classList.add('open');
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove('open');
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('open');
  }
});

document.getElementById('btn-toggle-add-product').addEventListener('click', (e) => {
  e.preventDefault(); openModal('modal-add-product');
});

document.getElementById('btn-toggle-add-box').addEventListener('click', (e) => {
  e.preventDefault(); openModal('modal-add-box');
});

document.getElementById('btn-toggle-create-order').addEventListener('click', (e) => {
  e.preventDefault(); openModal('modal-create-order');
});

// Sidebar toggle
document.getElementById('sidebar-toggle').addEventListener('click', () => {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('collapsed');
  
  const icon = document.getElementById('sidebar-toggle-icon');
  if (sidebar.classList.contains('collapsed')) {
    icon.classList.remove('fa-chevron-left');
    icon.classList.add('fa-chevron-right');
  } else {
    icon.classList.remove('fa-chevron-right');
    icon.classList.add('fa-chevron-left');
  }
});

/* ── Data Loaders & Renderers ────────────────────────────── */

async function loadProducts() {
  const { ok, data } = await api('GET', '/products/');
  if (!ok) return;
  state.products = data;
  document.getElementById('badge-products').textContent = data.length;
  renderProducts();
  renderQuickProductSelect();
}

function renderProducts() {
  const tbody = document.getElementById('products-list');
  if (!state.products.length) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No products available.</td></tr>`;
    return;
  }
  // Max 4 products
  const displayProducts = state.products.slice(0, 4);
  tbody.innerHTML = displayProducts.map(p => `
    <tr>
      <td style="font-weight: 500;">${p.name}</td>
      <td>${p.length} × ${p.width} × ${p.height}</td>
      <td>${p.weight}</td>
      <td>${Math.floor(Math.random() * 100) + 10}</td>
      <td><span class="status-badge" style="background: rgba(16,185,129,0.1); color: #10B981;">Active</span></td>
    </tr>
  `).join('');
}

async function loadBoxes() {
  const { ok, data } = await api('GET', '/boxes/');
  if (!ok) return;
  state.boxes = data;
  document.getElementById('badge-boxes').textContent = data.length;
}

async function loadOrders() {
  const { ok, data } = await api('GET', '/orders/');
  if (!ok) return;
  // Sort descending by id
  state.orders = data.sort((a, b) => b.id - a.id);
  // We can just set a dummy badge for orders today
  document.getElementById('badge-orders').textContent = data.length;
  renderOrders();
}

function renderOrders() {
  const tbody = document.getElementById('orders-list');
  if (!state.orders.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No recent orders.</td></tr>`;
    return;
  }
  // Max 4 orders
  const displayOrders = state.orders.slice(0, 4);
  tbody.innerHTML = displayOrders.map(o => {
    const totalItems = o.items.reduce((sum, item) => sum + item.quantity, 0);
    const totalWeight = o.items.reduce((sum, item) => sum + (item.product.weight * item.quantity), 0);
    const date = new Date(o.created_at).toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'});
    // Render recommended box from DB or fallback
    return `
      <tr>
        <td style="font-weight: 500;">#ORD-${1000 + o.id}</td>
        <td>${date}</td>
        <td>${totalItems}</td>
        <td>${totalWeight.toFixed(2)} kg</td>
        <td>${o.recommended_box_name || 'No Box Found'}</td>
        <td><span class="status-badge" style="background: rgba(16,185,129,0.1); color: #10B981;">Completed</span></td>
      </tr>
    `;
  }).join('');
}

/* ── Order Builder ───────────────────────────────────────── */
function renderQuickProductSelect() {
  const container = document.getElementById('quick-product-select');
  container.innerHTML = state.products.map(p => `
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px; background: var(--surface-hover); border-radius: 4px;">
      <span style="font-size: 13px;">${p.name}</span>
      <button class="qty-btn" style="width: 20px; height: 20px; font-size: 12px;" onclick="addToOrder(${p.id})"><i class="fa-solid fa-plus"></i></button>
    </div>
  `).join('');
}

function addToOrder(productId) {
  const product = state.products.find(p => p.id === productId);
  if (!product) return;
  const existing = state.orderItems.find(i => i.product.id === productId);
  if (existing) {
    existing.quantity += 1;
  } else {
    state.orderItems.push({ product, quantity: 1 });
  }
  renderOrderItems();
  resetRecommendation();
}

function changeQty(productId, delta) {
  const item = state.orderItems.find(i => i.product.id === productId);
  if (!item) return;
  item.quantity += delta;
  if (item.quantity <= 0) {
    state.orderItems = state.orderItems.filter(i => i.product.id !== productId);
  }
  renderOrderItems();
  resetRecommendation();
}

document.getElementById('btn-clear-order').addEventListener('click', (e) => {
  e.preventDefault();
  state.orderItems = [];
  renderOrderItems();
  resetRecommendation();
});

function renderOrderItems() {
  const container = document.getElementById('order-items-list');
  const btn = document.getElementById('btn-get-recommendation');
  const countDisplay = document.getElementById('order-count');
  
  const totalItems = state.orderItems.reduce((acc, item) => acc + item.quantity, 0);
  countDisplay.textContent = totalItems;
  
  if (totalItems > 0) {
    btn.disabled = false;
    btn.style.color = "var(--text)";
  } else {
    btn.disabled = true;
    btn.style.color = "var(--text-muted)";
  }

  if (totalItems === 0) {
    container.innerHTML = `
      <div style="text-align: center; color: var(--text-muted); padding: 16px 0; font-size: 12px;">
        No items yet.
      </div>
    `;
    return;
  }

  container.innerHTML = state.orderItems.map(item => `
    <div class="order-item-row" style="padding: 8px; margin-bottom: 4px;">
      <div class="order-item-info">
        <strong style="font-size: 13px;">${item.product.name}</strong>
      </div>
      <div class="qty-control" style="background: transparent; border: none;">
        <button class="qty-btn" style="width: 20px; height: 20px;" onclick="changeQty(${item.product.id}, -1)">-</button>
        <span class="qty-value" style="font-size: 12px;">${item.quantity}</span>
        <button class="qty-btn" style="width: 20px; height: 20px;" onclick="changeQty(${item.product.id}, +1)">+</button>
      </div>
    </div>
  `).join('');
}

function resetRecommendation() {
  document.getElementById('box-match-badge').style.display = 'none';
  document.getElementById('result-content').innerHTML = `
    <div style="text-align: center; color: var(--text-muted);">
      <i class="fa-solid fa-box-open" style="font-size: 32px; opacity: 0.3; margin-bottom: 12px;"></i>
      <p>Order changed.</p>
      <p style="font-size: 12px;">Click 'Get Recommendation' again.</p>
    </div>
  `;
}

/* ── Forms Submissions ───────────────────────────────────── */
document.getElementById('form-add-product').addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = document.getElementById('msg-add-product');
  const payload = {
    name: document.getElementById('p-name').value.trim(),
    length: parseFloat(document.getElementById('p-length').value),
    width: parseFloat(document.getElementById('p-width').value),
    height: parseFloat(document.getElementById('p-height').value),
    weight: parseFloat(document.getElementById('p-weight').value),
  };
  const { ok, data } = await api('POST', '/products/', payload);
  if (ok) {
    setMsg(msg, "Added!", "success");
    e.target.reset();
    await loadProducts();
    setTimeout(() => { closeModal('modal-add-product'); setMsg(msg, "", ""); }, 1000);
  } else {
    setMsg(msg, formatErrors(data), "error");
  }
});

document.getElementById('form-add-box').addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = document.getElementById('msg-add-box');
  const payload = {
    name: document.getElementById('b-name').value.trim(),
    inner_length: parseFloat(document.getElementById('b-length').value),
    inner_width: parseFloat(document.getElementById('b-width').value),
    inner_height: parseFloat(document.getElementById('b-height').value),
    max_weight: parseFloat(document.getElementById('b-weight').value),
    cost: parseFloat(document.getElementById('b-cost').value),
  };
  const { ok, data } = await api('POST', '/boxes/', payload);
  if (ok) {
    setMsg(msg, "Added!", "success");
    e.target.reset();
    await loadBoxes();
    setTimeout(() => { closeModal('modal-add-box'); setMsg(msg, "", ""); }, 1000);
  } else {
    setMsg(msg, formatErrors(data), "error");
  }
});

/* ── Get Recommendation ──────────────────────────────────── */
document.getElementById('btn-get-recommendation').addEventListener('click', async () => {
  const btn = document.getElementById('btn-get-recommendation');
  const resultContent = document.getElementById('result-content');
  const badge = document.getElementById('box-match-badge');
  
  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="color: var(--accent);"></i> Processing...';

  // 1. Create Order
  const payload = {
    items: state.orderItems.map(i => ({ product_id: i.product.id, quantity: i.quantity })),
  };
  const { ok: orderOk, data: orderData } = await api('POST', '/orders/', payload);
  
  if (!orderOk) {
    alert("Error creating order: " + formatErrors(orderData));
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-bolt" style="color: var(--accent);"></i> Get Recommendation';
    return;
  }
  
  // Reload orders list
  await loadOrders();

  // 2. Fetch Recommendation
  const { ok: recOk, data: recData } = await api('GET', `/orders/${orderData.id}/recommend/`);
  
  btn.disabled = false;
  btn.innerHTML = '<i class="fa-solid fa-bolt" style="color: var(--accent);"></i> Get Recommendation';

  if (recOk) {
    badge.style.display = 'inline-block';
    const svgTemplate = document.getElementById('box-svg-template').innerHTML;
    
    resultContent.innerHTML = `
      <div style="display: flex; gap: 24px; align-items: center; margin-bottom: 24px;">
        <div style="width: 140px; height: 140px; flex-shrink: 0;">
          ${svgTemplate}
        </div>
        <div>
          <h3 style="font-size: 22px; font-weight: 700; margin-bottom: 8px;">${recData.name}</h3>
          <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 4px;">${recData.inner_length} × ${recData.inner_width} × ${recData.inner_height} cm</p>
          <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 4px;">Max Weight: ${recData.max_weight} kg</p>
          <div style="color: var(--success); font-weight: 600; margin-top: 8px; font-size: 16px;">Cost: ₹${parseFloat(recData.cost).toFixed(2)}</div>
        </div>
      </div>
      <div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--surface-hover); border: 1px solid var(--border); border-radius: var(--radius-sm); color: var(--success); font-size: 13px; font-weight: 500;">
        <i class="fa-regular fa-circle-check"></i> Fits all items in your order
      </div>
    `;
  } else {
    badge.style.display = 'none';
    resultContent.innerHTML = `
      <div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--danger-bg); border: 1px solid var(--danger); border-radius: var(--radius-sm); color: var(--danger); font-size: 13px; font-weight: 500;">
        <i class="fa-solid fa-circle-exclamation"></i> ${recData.detail || 'No suitable box found for this order.'}
      </div>
    `;
  }
  
  // Clear cart since order was made
  state.orderItems = [];
  renderOrderItems();
  
  // Scroll to result
  document.getElementById('section-result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

/* ── Init ────────────────────────────────────────────────── */
(async () => {
  await Promise.all([loadProducts(), loadBoxes(), loadOrders()]);
})();
