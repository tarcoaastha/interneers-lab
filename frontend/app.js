async function fetchProducts() {
    const url = "http://127.0.0.1:8000/products/all/";

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Network response was not ok");
        
        const data = await response.json();
        console.log("Data Received:", data);

        const container = document.getElementById('inventory-container');
        container.innerHTML = ""; // Clear existing content

        // Access the array inside the 'products' key
        const productList = data.products;

        if (productList && Array.isArray(productList)) {
            productList.forEach((product, index) => {
                const card = document.createElement('div');
                card.className = 'product-card';
                
                // Add staggered animation delay
                card.style.animationDelay = `${index * 0.1}s`;

                card.innerHTML = `
                    <div class="product-category-tag">${product.category || 'General'}</div>
                    <h2 class="product-title">${product.title}</h2>
                    <p class="product-brand">${product.brand}</p>
                    <p class="product-description">${product.description || 'No description available for this product.'}</p>
                    <div class="product-stats">
                        <span class="price">$${product.price}</span>
                        <span class="quantity">Stock: ${product.quantity}</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error("❌ Error fetching products:", error);
    }
}

// Initial call
fetchProducts();