const API_URL = "http://127.0.0.1:5000/api";
let selectedBrand = "All";

// ================== AUTH LOGIC ==================
let isSignup = false;
function showAuth(isSignUpMode = false) {
    document.getElementById('auth-modal').style.display = 'flex';
    document.getElementById('main-ui').style.display = 'none';
    document.getElementById('main-header').style.display = 'none';
    document.getElementById('bg-img').style.display = 'block';
    isSignup = isSignUpMode;
    document.getElementById('auth-title').innerText = isSignup ? 'Sign Up' : 'Login';
    document.getElementById('auth-action').innerText = isSignup ? 'Sign Up' : 'Login';
    document.getElementById('switch-auth').innerText = isSignup ? 'Already have an account? Login' : "Don't have an account? Sign up";
    document.getElementById('auth-error').innerText = '';
    document.getElementById('auth-email').value = '';
    document.getElementById('auth-password').value = '';
}
document.getElementById('switch-auth').onclick = function() {
    showAuth(!isSignup);
};

document.getElementById('auth-action').onclick = function() {
    const email = document.getElementById('auth-email').value.trim();
    const pw = document.getElementById('auth-password').value.trim();
    if (!email || !pw) {
        document.getElementById('auth-error').innerText = "Please enter email and password.";
        return;
    }
    const endpoint = isSignup ? '/signup' : '/login';
    fetch(API_URL.replace('/api','') + '/api' + endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password: pw })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('auth-error').innerText = data.error;
        } else {
            // Login/Signup successful
            document.getElementById('auth-modal').style.display = 'none';
            document.getElementById('bg-img').style.display = 'none';
            document.getElementById('main-ui').style.display = '';
            document.getElementById('main-header').style.display = '';
            showSection('men');
            loadBrands();
        }
    })
    .catch(err => {
        document.getElementById('auth-error').innerText = "Server error: " + err;
    });
};

function logout() {
    document.getElementById('main-ui').style.display = 'none';
    document.getElementById('main-header').style.display = 'none';
    document.getElementById('bg-img').style.display = 'none';
    showAuth(false);
}

// ================== SHOP LOGIC ==================

function showSection(section) {
    document.querySelectorAll('.shop-section').forEach(sec => sec.style.display = 'none');
    document.getElementById(`${section}-section`).style.display = '';
    if (section === 'men') loadProducts('Men');
    if (section === 'women') loadProducts('Women');
    if (section === 'cart') renderCart();
    if (section === 'orders') renderOrders();
}

function loadBrands() {
    fetch(API_URL + '/brands')
        .then(res => res.json())
        .then(brands => {
            const sidebar = document.getElementById('brands-list');
            sidebar.innerHTML = '';
            brands.forEach(brand => {
                const btn = document.createElement('button');
                btn.className = 'brand-btn';
                btn.innerText = brand;
                if (brand === selectedBrand) btn.classList.add('active');
                btn.onclick = () => {
                    selectedBrand = brand;
                    if (document.getElementById('men-section').style.display !== 'none')
                        loadProducts('Men');
                    if (document.getElementById('women-section').style.display !== 'none')
                        loadProducts('Women');
                    loadBrands();
                };
                sidebar.appendChild(btn);
            });
        });
}

function loadProducts(gender) {
    let url = `${API_URL}/products?gender=${gender}`;
    if (selectedBrand && selectedBrand !== "All") url += `&brand=${selectedBrand}`;
    fetch(url)
        .then(res => res.json())
        .then(products => {
            const grid = document.getElementById(gender === 'Men' ? 'men-products' : 'women-products');
            grid.innerHTML = '';
            if (products.length === 0) {
                grid.innerHTML = '<p>No products found.</p>';
                return;
            }
            products.forEach(p => {
                grid.innerHTML += `
                <div class="product-card">
                    <img src="http://127.0.0.1:5000${p.img}" alt="${p.name}">
                    <h3>${p.name}</h3>
                    <p>RM ${p.price.toFixed(2)}</p>
                    <div class="btn-row">
                        <button onclick="addToCart(${p.id})">Add to Cart</button>
                        <button onclick="orderNow(${p.id})">Order</button>
                    </div>
                </div>`;
            });
        });
}

// --- Cart and Orders logic ---
function renderCart() {
    fetch(API_URL + '/cart')
        .then(res => res.json())
        .then(cart => {
            const cl = document.getElementById('cart-list');
            if (cart.length === 0) {
                cl.innerHTML = '<p>Your cart is empty.</p>';
                document.getElementById('order-btn').style.display = 'none';
                return;
            }
            document.getElementById('order-btn').style.display = '';
            cl.innerHTML = cart.map(c => `
                <div class="cart-item">
                    <span>${c.name}</span>
                    <input type="number" min="1" value="${c.qty}" onchange="updateQty(${c.id}, this.value)">
                    <button onclick="removeItem(${c.id})">Remove</button>
                </div>
            `).join('');
        });
}
function updateQty(id, qty) {
    fetch(API_URL + '/cart', {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id, qty: Number(qty)})
    }).then(renderCart);
}
function removeItem(id) {
    fetch(API_URL + '/cart', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id})
    }).then(renderCart);
}
document.getElementById('order-btn').onclick = function() {
    fetch(API_URL + '/order', {method: 'POST'})
        .then(res => res.json())
        .then(msg => {
            alert(msg.message || msg.error);
            renderCart();
        });
};

function renderOrders() {
    fetch(API_URL + '/orders')
        .then(res => res.json())
        .then(orders => {
            const ol = document.getElementById('orders-list');
            if (orders.length === 0) {
                ol.innerHTML = '<p>No orders yet.</p>';
                return;
            }
            ol.innerHTML = orders.map(order =>
                `<div class="order">
                    <h3>Order #${order.order_id}</h3>
                    <ul>
                        ${order.items.map(item =>
                            `<li>${item.name} x ${item.qty} (RM${item.price * item.qty})</li>`
                        ).join('')}
                    </ul>
                    <button style="background:red;color:white;" onclick="cancelOrder(${order.order_id})">Cancel Order</button>
                </div>`
            ).join('');
        });
}

// -- CANCEL ORDER FUNCTION --
function cancelOrder(orderId) {
    if (!confirm("Are you sure you want to cancel this order?")) return;
    fetch(API_URL + '/order', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({order_id: orderId})
    })
    .then(res => res.json())
    .then(msg => {
        alert(msg.message || msg.error || "Order canceled.");
        renderOrders();
    })
    .catch(err => alert("Error: " + err));
}

function addToCart(id) {
    fetch(API_URL + '/products')
        .then(res => res.json())
        .then(products => {
            const prod = products.find(p => p.id === id);
            fetch(API_URL + '/cart', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: prod.id, name: prod.name, price: prod.price})
            }).then(() => alert('Added to cart!'));
        });
}
function orderNow(id) {
    addToCart(id);
    setTimeout(() => showSection('cart'), 300);
}

// --- Initialize on page load ---
showAuth(false);
