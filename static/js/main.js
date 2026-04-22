document.addEventListener('DOMContentLoaded', () => {
    let cartCount = 0;
    const cartCountEl = document.getElementById('cart-count');
    const productGrid = document.getElementById('product-grid');

    // Fetch products from API
    fetch('/api/products')
        .then(response => response.json())
        .then(products => {
            productGrid.innerHTML = '';
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <img src="${product.image_url}" alt="${product.name}" class="product-img">
                    <div class="product-info">
                        <h3 class="product-title">${product.name}</h3>
                        <p class="product-desc">${product.description}</p>
                        <div class="product-price">$${product.price.toFixed(2)}</div>
                        <button class="btn-add" onclick="addToCart()">Add to Cart</button>
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
    window.addToCart = function() {
        cartCount++;
        cartCountEl.textContent = cartCount;
        
        // Simple animation
        cartCountEl.style.transform = 'scale(1.5)';
        setTimeout(() => {
            cartCountEl.style.transform = 'scale(1)';
        }, 200);
    };
});
