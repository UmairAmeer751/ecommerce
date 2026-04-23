document.addEventListener('DOMContentLoaded', () => {
    let cart = [];
    const cartCountEl = document.getElementById('cart-count');
    const productGrid = document.getElementById('product-grid');
    const cartModal = document.getElementById('cart-modal');
    const cartBtn = document.getElementById('cart-btn');
    const closeCartBtn = document.getElementById('close-cart');
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalPrice = document.getElementById('cart-total-price');
    let allProducts = [];

    // Fetch products from API
    fetch('/api/products')
        .then(response => response.json())
        .then(products => {
            allProducts = products;
            productGrid.innerHTML = '';
            products.forEach((product, index) => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <img src="${product.image_url}" alt="${product.name}" class="product-img">
                    <div class="product-info">
                        <h3 class="product-title">${product.name}</h3>
                        <p class="product-desc">${product.description}</p>
                        <div class="product-price">$${product.price.toFixed(2)}</div>
                        <button class="btn-add" onclick="addToCart(${index})">Add to Cart</button>
                    </div>
                `;
                productGrid.appendChild(card);
            });
        })
        .catch(error => {
            productGrid.innerHTML = '<p class="loader">Failed to load products. Please try again later.</p>';
            console.error('Error fetching products:', error);
        });

    // Global add to cart function
    window.addToCart = function(productIndex) {
        const product = allProducts[productIndex];
        cart.push(product);
        updateCartCount();
        updateCartUI();
        
        // Simple animation
        cartCountEl.style.transform = 'scale(1.5)';
        setTimeout(() => {
            cartCountEl.style.transform = 'scale(1)';
        }, 200);
    };

    function updateCartCount() {
        cartCountEl.textContent = cart.length;
    }

    function updateCartUI() {
        cartItemsContainer.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="empty-cart">Your cart is currently empty.</p>';
        } else {
            cart.forEach((item, index) => {
                total += item.price;
                const itemEl = document.createElement('div');
                itemEl.className = 'cart-item';
                itemEl.innerHTML = `
                    <div class="cart-item-info">
                        <img src="${item.image_url}" alt="${item.name}" class="cart-item-img">
                        <div>
                            <div class="cart-item-title">${item.name}</div>
                            <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                        </div>
                    </div>
                    <button class="btn-pay" onclick="payForItem(${index})">Pay</button>
                `;
                cartItemsContainer.appendChild(itemEl);
            });
        }
        cartTotalPrice.textContent = total.toFixed(2);
    }

    window.payForItem = function(cartIndex) {
        // Payment logic: show alert, remove from cart, update UI
        alert('Payment successful for ' + cart[cartIndex].name + '!');
        cart.splice(cartIndex, 1);
        updateCartCount();
        updateCartUI();
    };

    // Modal Events
    cartBtn.addEventListener('click', () => {
        cartModal.style.display = 'block';
    });

    closeCartBtn.addEventListener('click', () => {
        cartModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === cartModal) {
            cartModal.style.display = 'none';
        }
    });
});
