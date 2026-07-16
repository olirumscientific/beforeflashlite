// --- GLOBAL STATE ---
const API_URL = 'http://127.0.0.1:8000';
let quoteCart = JSON.parse(localStorage.getItem('quoteCart')) || [];
let allProductsCache = []; 

// --- UI HELPERS & NAVBAR ---
function toggleMenu() {
    document.getElementById('nav-links').classList.toggle('active');
}

function updateCartBadge() {
    const count = quoteCart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-count').innerText = count;
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
}

// --- BOOT UP ---
async function initializeCatalog() {
    try {
        const response = await fetch(`${API_URL}/products`);
        allProductsCache = await response.json();
    } catch (error) {
        console.error("Could not load catalog on boot:", error);
    }
}

// --- ROUTING CORE LOGIC ---
function handleRouting() {
    // Wait for products to load before trying to route
    if (allProductsCache.length === 0) return; 

    const hash = window.location.hash;

    // Handle all the different URL states
    if (!hash || hash === '' || hash === '#home') {
        navigateTo('home');
    } else if (hash === '#all-products') {
        navigateTo('all-products');
    } else if (hash === '#cart') {
        navigateTo('cart');
    } else if (hash.startsWith('#category-')) {
        const catId = parseInt(hash.replace('#category-', ''));
        filterCategory(catId);
    } else if (hash.startsWith('#product-')) {
        const prodId = parseInt(hash.replace('#product-', ''));
        viewProduct(prodId);
    }
}

// Listen for the user clicking the Back/Forward browser buttons
window.addEventListener('hashchange', handleRouting);


// --- PAGE VIEWS ---
function navigateTo(view) {
    const contentArea = document.getElementById('app-content');
    document.getElementById('nav-links').classList.remove('active'); 

    if (view === 'home') {
        contentArea.innerHTML = `
            <div class="hero-section">
                <div class="hero-overlay"></div>
                <div class="hero-content">
                    <h1>Advancing Research with Precision</h1>
                    <p>Olirum Scientific provides industry-leading cellular assays, microscopy solutions, and mycoplasma detection kits for modern bio-laboratories and research institutions.</p>
                    
                    <!-- FIX: Now changes the URL instead of calling navigateTo directly -->
                    <button onclick="window.location.hash = '#all-products'" style="background: var(--accent-blue); color: white; padding: 15px 35px; border: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: all 0.3s;">
                        Explore Our Catalog
                    </button>
                </div>
            </div>

            <div style="max-width: 1200px; margin: 60px auto; padding: 0 20px;">
                <h2 style="text-align: center; margin-bottom: 40px; color: var(--dark-slate); font-size: 2rem;">Comprehensive Solutions for Modern Labs</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
                    
                    <!-- Card 1: Assays -->
                    <!-- FIX: Made the whole card clickable and set the href to change the URL -->
                    <a href="#category-1" style="text-decoration: none; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid #10b981; display: flex; flex-direction: column;">
                        <h3 style="color: var(--primary-blue); margin-bottom: 15px; font-size: 1.3rem;">Cellular Assays</h3>
                        <p style="color: var(--text-main); font-size: 1rem; margin-bottom: 20px; line-height: 1.6; flex-grow: 1;">Achieve high-throughput, reliable viability testing and advanced ROS detection with minimal background noise.</p>
                        <span style="color: #10b981; font-weight: 600;">Explore Assays &rarr;</span>
                    </a>

                    <!-- Card 2: Microscopy -->
                    <a href="#category-2" style="text-decoration: none; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid #8b5cf6; display: flex; flex-direction: column;">
                        <h3 style="color: var(--primary-blue); margin-bottom: 15px; font-size: 1.3rem;">Advanced Imaging</h3>
                        <p style="color: var(--text-main); font-size: 1rem; margin-bottom: 20px; line-height: 1.6; flex-grow: 1;">Preserve fluorescence for long-term storage and enable deep tissue analysis with our next-generation microscopy media.</p>
                        <span style="color: #8b5cf6; font-weight: 600;">View Microscopy Tools &rarr;</span>
                    </a>

                    <!-- Card 3: Mycoplasma -->
                    <a href="#category-3" style="text-decoration: none; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid var(--accent-blue); display: flex; flex-direction: column;">
                        <h3 style="color: var(--primary-blue); margin-bottom: 15px; font-size: 1.3rem;">Contamination Control</h3>
                        <p style="color: var(--text-main); font-size: 1rem; margin-bottom: 20px; line-height: 1.6; flex-grow: 1;">Noticing slower growth or poor viability? Eradicate silent cell line disruptors like mycoplasma safely in just 7 days.</p>
                        <span style="color: var(--accent-blue); font-weight: 600;">View Mycoplasma Kits &rarr;</span>
                    </a>
                </div>
            </div>

            <div style="text-align: center; padding: 20px 20px 40px 20px;">
                <h2 style="margin-bottom: 20px;">Trusted by Research Facilities</h2>
                <p style="color: var(--text-light); max-width: 600px; margin: 0 auto;">We partner with top universities and private labs to ensure consistent, reliable, and high-quality results in every experiment.</p>
            </div>
        `;
    } 
    else if (view === 'all-products') {
        contentArea.innerHTML = `
            <h2 style="margin-bottom: 20px;">All Products</h2>
            <div id="product-list" class="product-grid"></div>
        `;
        renderProductCards(allProductsCache);
    }
    else if (view === 'cart') {
        renderCartPage(); 
    }
}

// --- CATALOG & FILTERING LOGIC ---
function renderProductCards(products) {
    const container = document.getElementById('product-list');
    container.innerHTML = ''; 

    if (products.length === 0) {
        container.innerHTML = "<p>No products found in this category.</p>";
        return;
    }

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.style.cursor = 'pointer';
        
        // FIX: Now changes the URL hash to load the product page
        card.onclick = () => window.location.hash = `#product-${product.id}`;
        
        card.innerHTML = `
            <h3 style="margin-bottom: 10px; color: var(--primary-blue);">${product.name}</h3>
            <p style="color: var(--text-main); font-weight: 600; margin-bottom: 15px;">₹${product.price ? product.price.toFixed(2) : "0.00"}</p>
            
            <div onclick="event.stopPropagation();" style="display: flex; gap: 10px; margin-bottom: 10px; justify-content: center; align-items: center;">
                <input type="number" id="qty-${product.id}" value="1" min="1" style="width: 60px; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; text-align: center; font-family: 'Inter', sans-serif; font-weight: bold;">
                <button class="btn-add-quote" style="margin-top: 0; padding: 8px 15px; width: auto;" onclick="addToQuote(${product.id}, '${product.name}')">Add to Quote</button>
            </div>
        `;
        container.appendChild(card);
    });
}

function filterCategory(categoryId) {
    document.getElementById('nav-links').classList.remove('active'); 
    const contentArea = document.getElementById('app-content');
    
    const catNames = {1: "Cellular Assays", 2: "Microscopy", 3: "Mycoplasma"};
    
    contentArea.innerHTML = `
        <h2 style="margin-bottom: 20px;">${catNames[categoryId]}</h2>
        <div id="product-list" class="product-grid"></div>
    `;
    
    const filteredProducts = allProductsCache.filter(p => p.category_id === categoryId);
    renderProductCards(filteredProducts);
}

// --- SINGLE PRODUCT VIEW (FULLY DYNAMIC MATRIX) ---
function viewProduct(productId) {
    document.getElementById('nav-links').classList.remove('active'); 
    const contentArea = document.getElementById('app-content');
    
    const product = allProductsCache.find(p => p.id === productId);
    if (!product) {
        contentArea.innerHTML = `<h2 style="color: red; text-align: center; padding: 40px;">Product not found</h2>`;
        return;
    }

    const catNo = product.catalog_number || `OS-PROD-${product.id}`;
    const subTitle = product.subtitle || "Premium Laboratory Reagent";
    const downloadPath = product.download_link || "#";

    contentArea.innerHTML = `
        <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            
            <!-- Left Side: Carousel -->
            <div>
                <div style="background: #f1f5f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; min-height: 350px;">
                    <span id="main-product-display-text" style="color: var(--text-light); font-size: 1.2rem; font-weight: 500;">🔬 Main Product View (Amber Tubes)</span>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <div onclick="document.getElementById('main-product-display-text').innerText='🔬 Main Product View (Amber Tubes)'" style="flex: 1; background: #e2e8f0; height: 50px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; color: var(--text-main);">Pack</div>
                    <div onclick="document.getElementById('main-product-display-text').innerText='📊 [Example] MCF10CA1a Timeline'" style="flex: 1; background: #e2e8f0; height: 50px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; color: var(--text-main);">MCF10CA1a</div>
                    <div onclick="document.getElementById('main-product-display-text').innerText='📊 [Example] HEK293 Timeline'" style="flex: 1; background: #e2e8f0; height: 50px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; color: var(--text-main);">HEK293</div>
                    <div onclick="document.getElementById('main-product-display-text').innerText='🖼️ DAPI Stain Comparison'" style="flex: 1; background: #e2e8f0; height: 50px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 600; color: var(--text-main);">DAPI Stain</div>
                </div>
            </div>
            
            <!-- Right Side: Details -->
            <div style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span style="color: var(--text-light); font-size: 0.9rem; font-weight: 700; letter-spacing: 0.5px;">CAT NO. ${catNo}</span>
                    <h1 style="font-size: 2.5rem; margin: 5px 0 10px 0; color: var(--primary-blue); font-family: 'Montserrat';">${product.name}</h1>
                    <p style="font-style: italic; color: var(--accent-blue); margin-bottom: 15px; font-weight: 500; font-size: 1.1rem;">${subTitle}</p>
                    
                    <div style="display: flex; gap: 10px; margin-bottom: 25px;">
                        <span style="background: #eff6ff; color: var(--accent-blue); padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Store at -20°C</span>
                        <span style="background: #f0fdf4; color: #16a34a; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Research Use Only</span>
                    </div>

                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--dark-slate); margin-bottom: 20px;">Lorem Price: ₹${product.price ? product.price.toFixed(2) : "0.00"}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 15px;">
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <div style="display: flex; flex-direction: column; gap: 5px;">
                            <label style="font-size: 0.75rem; font-weight: 700; color: var(--dark-slate);">QUANTITY</label>
                            <input type="number" id="qty-${product.id}" value="1" min="1" style="width: 70px; padding: 10px; border: 1px solid #cbd5e1; border-radius: 4px; text-align: center; font-weight: bold;">
                        </div>
                        <button style="margin-top: 18px; padding: 12px; flex: 1; background: white; border: 1px solid var(--primary-blue); color: var(--primary-blue); font-weight: 600; border-radius: 4px; cursor: pointer;" onclick="addToQuote(${product.id}, '${product.name}')">Add to Quote Cart</button>
                    </div>
                </div>

                <a href="${downloadPath}" onclick="showToast('Downloading document...', 'success')" style="display: flex; align-items: center; justify-content: center; gap: 8px; background: white; border: 1px solid #cbd5e1; color: var(--text-main); padding: 12px; border-radius: 4px; font-weight: 500; text-align: center; text-decoration: none;">
                    📄 Download Full Protocol Datasheet (PDF)
                </a>
            </div>
        </div>

        <!-- 3 Tabs Layout -->
        <div style="max-width: 1200px; margin: 30px auto 0 auto; background: white; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden;">
            <div style="display: flex; background: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                <button id="tab-btn-overview" onclick="switchTab('overview', ${product.id})" style="padding: 15px 25px; border: none; background: white; font-weight: 600; color: var(--primary-blue); border-top: 2px solid var(--primary-blue); border-right: 1px solid #e2e8f0; cursor: pointer;">Product Overview</button>
                <button id="tab-btn-protocol" onclick="switchTab('protocol', ${product.id})" style="padding: 15px 25px; border: none; background: transparent; font-weight: 600; color: var(--text-light); border-right: 1px solid #e2e8f0; cursor: pointer; border-top: 2px solid transparent;">Method & Protocol</button>
                <button id="tab-btn-support" onclick="switchTab('support', ${product.id})" style="padding: 15px 25px; border: none; background: transparent; font-weight: 600; color: var(--text-light); cursor: pointer; border-top: 2px solid transparent;">Troubleshooting & Support</button>
            </div>
            <div id="tab-content-box" style="padding: 30px; line-height: 1.6; color: var(--text-main);">
                ${product.specs_html || "<p>Data pending.</p>"}
            </div>
        </div>
    `;
}

window.switchTab = function(tabName, productId) {
    const box = document.getElementById('tab-content-box');
    const product = allProductsCache.find(p => p.id === productId);
    
    const btns = {
        overview: document.getElementById('tab-btn-overview'),
        protocol: document.getElementById('tab-btn-protocol'),
        support: document.getElementById('tab-btn-support')
    };

    // Reset all tabs to inactive styles
    for (let key in btns) {
        if(btns[key]) {
            btns[key].style.background = 'transparent'; 
            btns[key].style.color = 'var(--text-light)';
            btns[key].style.borderTop = '2px solid transparent';
        }
    }

    // Activate selected tab and load database content
    if(btns[tabName]) { 
        btns[tabName].style.background = 'white'; 
        btns[tabName].style.color = 'var(--primary-blue)'; 
        btns[tabName].style.borderTop = '2px solid var(--primary-blue)';
    }

    if (tabName === 'overview') {
        box.innerHTML = product.specs_html || "<p>Data pending.</p>";
    } else if (tabName === 'protocol') {
        box.innerHTML = product.protocol_html || "<p>Protocol pending.</p>";
    } else if (tabName === 'support') {
        box.innerHTML = product.support_html || "<p>Support details pending.</p>";
    }
}

// --- CART LOGIC ---
function addToQuote(productId, productName) {
    const qtyInput = document.getElementById(`qty-${productId}`);
    const quantityToAdd = qtyInput ? parseInt(qtyInput.value) : 1;

    const existingItem = quoteCart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += quantityToAdd;
    } else {
        quoteCart.push({ id: productId, name: productName, quantity: quantityToAdd });
    }
    
    localStorage.setItem('quoteCart', JSON.stringify(quoteCart));
    updateCartBadge();
    
    if (qtyInput) qtyInput.value = 1;
    showToast(`Added ${quantityToAdd}x ${productName} to your quote request.`, 'success');
}

function changeQuantity(productId, change) {
    const item = quoteCart.find(i => i.id === productId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            quoteCart = quoteCart.filter(i => i.id !== productId);
        }
        localStorage.setItem('quoteCart', JSON.stringify(quoteCart));
        updateCartBadge();
        renderCartPage(); 
    }
}

// --- CART UI & SUBMISSION ---
function renderCartPage() {
    const contentArea = document.getElementById('app-content');
    
    contentArea.innerHTML = `
        <div class="dashboard-layout" style="margin-top: 0;">
            <section class="catalog-section">
                <h2 style="margin-bottom: 20px;">Review Your Request</h2>
                <div id="cart-items-container" style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0;">
                </div>
            </section>
            
            <aside class="cart-sidebar">
                <div class="cart-container">
                    <h3 style="margin-bottom: 20px; color: var(--primary-blue);">Lead Details</h3>
                    <div class="form-group">
                        <label>Official Email *</label>
                        <input type="email" id="buyer-email" placeholder="lab@institution.edu" required>
                    </div>
                    <div class="form-group">
                        <label>Institution / Company</label>
                        <input type="text" id="buyer-company" placeholder="e.g. BioTech Inc.">
                    </div>
                    <button id="submit-btn" onclick="submitQuote()" style="width: 100%; background: var(--accent-blue); color: white; padding: 12px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px;">
                        Submit Request
                    </button>
                </div>
            </aside>
        </div>
    `;

    const cartContainer = document.getElementById('cart-items-container');
    if (quoteCart.length === 0) {
        cartContainer.innerHTML = '<p style="color: var(--text-light);">Your quote cart is empty.</p>';
        document.getElementById('submit-btn').disabled = true;
        document.getElementById('submit-btn').style.background = '#cbd5e1';
        return;
    }

    quoteCart.forEach(item => {
        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.justifyContent = 'space-between';
        row.style.alignItems = 'center';
        row.style.padding = '15px 0';
        row.style.borderBottom = '1px solid #eee';
        
        row.innerHTML = `
            <span style="font-weight: 500; font-size: 1.1rem;">${item.name}</span>
            <div style="display: flex; align-items: center; gap: 12px;">
                <button class="qty-btn" onclick="changeQuantity(${item.id}, -1)">-</button>
                <span style="width: 25px; text-align: center; font-weight: bold;">${item.quantity}</span>
                <button class="qty-btn" onclick="changeQuantity(${item.id}, 1)">+</button>
            </div>
        `;
        cartContainer.appendChild(row);
    });
}

async function submitQuote() {
    const emailInput = document.getElementById('buyer-email').value;
    const companyInput = document.getElementById('buyer-company').value; 
    const btn = document.getElementById('submit-btn');
    
    if (!emailInput) {
        showToast("Please provide an official email address.", "error");
        return;
    }

    btn.innerText = "Sending...";
    btn.disabled = true;
    btn.style.background = '#ccc';

    const payload = {
        email: emailInput,
        company: companyInput, 
        items: quoteCart.map(item => ({ id: item.id, quantity: item.quantity }))
    };

    try {
        const response = await fetch(`${API_URL}/quotes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("Quote requested successfully! Our team will contact you shortly.", "success");
            quoteCart = [];
            localStorage.removeItem('quoteCart');
            updateCartBadge();
            window.location.hash = '#home'; // FIX: Changed to use router
        } else {
            showToast("Something went wrong on the server.", "error");
            btn.innerText = "Submit Request";
            btn.disabled = false;
            btn.style.background = '#27ae60';
        }
    } catch (error) {
        showToast("Could not connect to the server.", "error");
        btn.innerText = "Submit Request";
        btn.disabled = false;
        btn.style.background = '#27ae60';
    }
}

// --- SEARCH FUNCTIONALITY ---
function handleSearch(event) {
    const query = event.target.value.toLowerCase().trim();
    const contentArea = document.getElementById('app-content');
    
    // If they clear the search bar, just go back to the home view
    if (query === "") {
        window.location.hash = '#home';
        navigateTo('home');
        return;
    }

    // Filter products by name or description
    const searchResults = allProductsCache.filter(p => 
        p.name.toLowerCase().includes(query) || 
        (p.description && p.description.toLowerCase().includes(query))
    );

    // Setup the screen for search results
    document.getElementById('nav-links').classList.remove('active');
    
    contentArea.innerHTML = `
        <h2 style="margin-bottom: 20px;">Search Results for "${query}"</h2>
        <div id="product-list" class="product-grid"></div>
    `;
    
    // Draw the matching products using your existing function!
    renderProductCards(searchResults);
}

// --- BOOT SEQUENCE ---
initializeCatalog().then(() => {
    updateCartBadge();
    // FIX: This now triggers the router instead of forcing the home page!
    handleRouting(); 
});

//previous thing different design 
// function viewProduct(productId) {
//     document.getElementById('nav-links').classList.remove('active'); 
//     const contentArea = document.getElementById('app-content');
    
//     const product = allProductsCache.find(p => p.id === productId);
//     if (!product) {
//         contentArea.innerHTML = `<h2 style="color: red; text-align: center; padding: 40px;">Product not found</h2>`;
//         return;
//     }

//     // Default fallbacks for other catalog items, with full data loaded for MaRK (ID: 6)
//     let catNo = product.id === 6 ? "OS-MRK" : `OS-PROD-${product.id}`;
//     let storageTemp = product.id === 6 ? "-20°C" : "4°C";
//     let subTitle = product.id === 6 ? "Eliminating mycoplasma within 7 days" : "Premium Laboratory Reagent";
    
//     contentArea.innerHTML = `
//         <!-- Top Half: Presentation Block -->
//         <div style="max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            
//             <!-- Left Column: Image Carousel Area -->
//             <div>
//                 <div style="background: #f1f5f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; min-height: 350px; position: relative;">
//                     <span id="main-product-display-text" style="color: var(--text-light); font-size: 1.2rem; font-weight: 500;">🔬 Main Product View (Amber Tubes)</span>
//                 </div>
                
//                 <!-- Carousel Thumbnails -->
//                 <div style="display: flex; gap: 10px; margin-top: 15px;">
//                     <div onclick="document.getElementById('main-product-display-text').innerText='🔬 Main Product View (Amber Tubes)'" style="flex: 1; background: #e2e8f0; height: 60px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; text-align: center; font-weight: 600;">Pack</div>
//                     <div onclick="document.getElementById('main-product-display-text').innerText='📊 [Example Image] MCF10CA1a Cell Line Timeline (Days 1-5)'" style="flex: 1; background: #e2e8f0; height: 60px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; text-align: center; font-weight: 600;">MCF10CA1a</div>
//                     <div onclick="document.getElementById('main-product-display-text').innerText='📊 [Example Image] HEK293 Cell Line Timeline (Days 1-5)'" style="flex: 1; background: #e2e8f0; height: 60px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; text-align: center; font-weight: 600;">HEK293</div>
//                     <div onclick="document.getElementById('main-product-display-text').innerText='🖼️ [DAPI Stain] Before vs After Microscopic Clearance'" style="flex: 1; background: #e2e8f0; height: 60px; border-radius: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; text-align: center; font-weight: 600;">DAPI Stain</div>
//                 </div>
//             </div>
            
//             <!-- Right Column: Quick Info Box -->
//             <div style="display: flex; flex-direction: column; justify-content: space-between;">
//                 <div>
//                     <span style="color: var(--text-light); font-size: 0.9rem; font-weight: 600; letter-spacing: 0.5px;">CAT NO. ${catNo}</span>
//                     <h1 style="font-size: 2.2rem; margin: 5px 0 10px 0; color: var(--primary-blue); font-family: 'Montserrat';">${product.name}</h1>
//                     <p style="font-style: italic; color: var(--accent-blue); margin-bottom: 15px; font-weight: 500;">${subTitle}</p>
                    
//                     <div style="display: flex; gap: 10px; margin-bottom: 25px;">
//                         <span style="background: #eff6ff; color: var(--accent-blue); padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Store at ${storageTemp}</span>
//                         <span style="background: #f0fdf4; color: #16a34a; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Research Use Only</span>
//                     </div>

//                     <p style="font-size: 1.8rem; font-weight: 700; color: var(--dark-slate); margin-bottom: 20px;">Lorem Price: ₹${product.price.toFixed(2)}</p>
//                 </div>
                
//                 <!-- B2B Order Form Box -->
//                 <div style="background: var(--light-bg); padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 15px;">
//                     <div style="display: flex; gap: 15px; align-items: center;">
//                         <div style="display: flex; flex-direction: column; gap: 5px;">
//                             <label style="font-size: 0.75rem; font-weight: 700; color: var(--text-main);">QUANTITY</label>
//                             <input type="number" id="qty-${product.id}" value="1" min="1" style="width: 70px; padding: 8px; border: 1px solid #cbd5e1; border-radius: 4px; text-align: center; font-weight: bold;">
//                         </div>
//                         <button class="btn-add-quote" style="margin-top: 18px; padding: 12px;" onclick="addToQuote(${product.id}, '${product.name}')">Add to Quote Cart</button>
//                     </div>
//                 </div>

//                 <!-- PDF Link -->
//                 <a href="#" onclick="showToast('Protocol PDF download started...', 'success')" style="display: flex; align-items: center; justify-content: center; gap: 8px; background: #fff; border: 1px solid #cbd5e1; color: var(--text-main); padding: 12px; border-radius: 6px; font-weight: 500; text-align: center; cursor: pointer; transition: var(--transition);">
//                     📄 Download Full Protocol Datasheet (PDF)
//                 </a>
//             </div>
//         </div>

//         <!-- Bottom Half: Technical Specifications Tabs -->
//         <div style="max-width: 1200px; margin: 30px auto 0 auto; background: white; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden;">
//             <!-- Tab Headers -->
//             <div style="display: flex; background: #f8fafc; border-bottom: 1px solid #e2e8f0;">
//                 <button id="tab-btn-overview" onclick="switchTab('overview')" style="padding: 15px 25px; border: none; background: white; font-weight: 600; color: var(--primary-blue); border-right: 1px solid #e2e8f0; cursor: pointer;">Product Overview</button>
//                 <button id="tab-btn-protocol" onclick="switchTab('protocol')" style="padding: 15px 25px; border: none; background: transparent; font-weight: 600; color: var(--text-light); border-right: 1px solid #e2e8f0; cursor: pointer;">Method & Protocol</button>
//                 <button id="tab-btn-support" onclick="switchTab('support')" style="padding: 15px 25px; border: none; background: transparent; font-weight: 600; color: var(--text-light); cursor: pointer;">Troubleshooting & Support</button>
//             </div>

//             <!-- Tab Dynamic Box Context -->
//             <div id="tab-content-box" style="padding: 30px; line-height: 1.6; color: var(--text-main);">
//                 <!-- Default Tab content loaded directly -->
//                 ${getOverviewHTML(product.id)}
//             </div>
//         </div>
//     `;
// }

// // Global scope helpers for dealing with technical tab navigation
// window.switchTab = function(tabName) {
//     const box = document.getElementById('tab-content-box');
//     const btns = {
//         overview: document.getElementById('tab-btn-overview'),
//         protocol: document.getElementById('tab-btn-protocol'),
//         support: document.getElementById('tab-btn-support')
//     };

//     // Reset styles
//     for (let key in btns) {
//         if(btns[key]) {
//             btns[key].style.background = 'transparent';
//             btns[key].style.color = 'var(--text-light)';
//         }
//     }

//     // Highlight selected tab active header
//     if(btns[tabName]) {
//         btns[tabName].style.background = '#fff';
//         btns[tabName].style.color = 'var(--primary-blue)';
//     }

//     // Insert structured content text based on datasheet mapping
//     if (tabName === 'overview') {
//         box.innerHTML = getOverviewHTML(6);
//     } else if (tabName === 'protocol') {
//         box.innerHTML = `
//             <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Treatment Regimen Method</h3>
//             <p style="margin-bottom: 15px;">The working concentration for MaRK is fully optimized across multiple vulnerable lines, utilizing a recommended dosage baseline of <strong>0.5 - 1.0 μl/ml</strong> volume-per-volume ratio.</p>
//             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">1. Prepare Cells</h4>
//             <ul style="margin-left: 20px; margin-bottom: 15px;">
//                 <li>Completely aspirate old medium from contaminated cell growth vessel.</li>
//                 <li>Rinse monolayer structures twice using clean Phosphate-Buffered Saline (PBS) to clear excess cell debris and active surface contaminants.</li>
//             </ul>
//             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">2. Treatment Setup</h4>
//             <ul style="margin-left: 20px; margin-bottom: 15px;">
//                 <li>Passage or split your actively dividing culture into freshly prepared growth media containing exactly <strong>1.0 μl/ml</strong> concentration of MaRK.</li>
//                 <li>Ensure targets are established explicitly within their exponential growth phase by planning seed distributions effectively.</li>
//             </ul>
//             <h4 style="margin-bottom: 5px; color: var(--dark-slate);">3. Maintenance & Timeline</h4>
//             <p>Every 3-4 days, run clean passage evaluations and refresh structural fluid tables with fresh MaRK-infused solutions consistently over a total timeframe spanning 2 weeks.</p>
//         `;
//     } else if (tabName === 'support') {
//         box.innerHTML = `
//             <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Troubleshooting & Asset Guidelines</h3>
//             <p style="margin-bottom: 15px;"><strong>Handling Infection Severity:</strong> For heavy localized target density, add 1.0 μl of MaRK per ml of background medium. For lower initial structural threat tracking, maintain a lower baseline of 0.6 μl/ml. Always validate initial line tolerances across minor volumes before scaling dosages.</p>
//             <p style="margin-bottom: 15px;"><strong>Cellular Recovery:</strong> Certain lines may experience brief growth slowdown phases while undergoing direct treatments. Normal replication configurations typically recover completely once target context clearance is validated and active media additions cease.</p>
//             <div style="background: #fff8e1; border-left: 4px solid #ffb300; padding: 15px; border-radius: 4px; margin-top: 20px;">
//                 <strong>Technical Support:</strong> For analytical support inquiries, connection validation issues, or testing questions, reach our technical lab team directly at <a href="mailto:admin@olirumscience.com" style="color: var(--accent-blue); font-weight: 600;">admin@olirumscience.com</a>.
//             </div>
//         `;
//     }
// }

// function getOverviewHTML(id) {
//     return `
//         <h3 style="margin-bottom: 10px; color: var(--dark-slate);">Product Information & Background</h3>
//         <p style="margin-bottom: 15px;">MaRK™ (Mycoplasma Removal Kit) functions as a highly specific dual-inhibitor complex formulated to rapidly eliminate standard laboratory mycoplasma variants within 7 days. Designed to circumvent structural workflow limitations common to slow commercial alternatives, this sterile-filtered, cell culture-tested matrix clears targets comprehensively within brief intervention windows.</p>
//         <h4 style="margin-bottom: 10px; color: var(--dark-slate);">Advanced Mechanism Composition:</h4>
//         <ol style="margin-left: 20px; margin-bottom: 20px;">
//             <li><strong>Protein Synthesis Inhibitor:</strong> Disrupts targeted translation and core protein production loops inside localized mycoplasma cells.</li>
//             <li><strong>DNA Gyrase Inhibitor:</strong> Systematically blocks replication cycles unique to specific mycoplasma DNA profiles.</li>
//         </ol>
//         <p>Because these internal micro-components possess zero corresponding biological targets inside standard eukaryotic cells, treatment remains highly safe and localized for mammalian cell lines.</p>
//     `;
// }