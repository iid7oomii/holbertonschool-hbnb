document.addEventListener('DOMContentLoaded', () => {
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    let allPlaces = [];
    
    // Helper function to get cookie value by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            const cookieValue = parts.pop().split(';').shift();
            console.log(`getCookie(${name}):`, cookieValue);
            return cookieValue;
        }
        console.log(`getCookie(${name}): not found`);
        return null;
    }
    
    // Check authentication and update login button
    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        const addPlaceLink = document.getElementById('add-place-link');
        const adminLink = document.getElementById('admin-link');
        
        console.log('Token check:', token ? 'Found' : 'Not found');
        console.log('All cookies:', document.cookie);
        
        if (token && loginLink) {
            // Decode token to check if admin
            try {
                const tokenParts = token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                const isAdmin = payload.is_admin || false;
                
                // User is logged in - change to logout
                loginLink.textContent = 'Logout';
                loginLink.href = '#';
                loginLink.onclick = (e) => {
                    e.preventDefault();
                    document.cookie = 'token=; path=/; max-age=0; SameSite=Lax';
                    window.location.reload();
                };
                
                // Show Add Place link
                if (addPlaceLink) {
                    addPlaceLink.style.display = 'inline';
                }
                
                // Show Admin link if user is admin
                if (isAdmin && adminLink) {
                    adminLink.style.display = 'inline';
                }
            } catch (error) {
                console.error('Error decoding token:', error);
            }
        } else if (loginLink) {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
            loginLink.onclick = null;
            
            // Hide Add Place and Admin links
            if (addPlaceLink) addPlaceLink.style.display = 'none';
            if (adminLink) adminLink.style.display = 'none';
        }
    }

    async function fetchPlaces() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/places/');
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
            setupPriceFilter();
        } catch (error) {
            console.error('Error:', error);
            placesList.innerHTML = '<p style="color: var(--gold-color); text-align: center;">Failed to load places. Please make sure the server is running.</p>';
        }
    }

    function displayPlaces(places) {
        placesList.innerHTML = '';
        
        if (places.length === 0) {
            placesList.innerHTML = '<p style="color: var(--gold-color); text-align: center; width: 100%;">No places available. Please add some data to the database.</p>';
            return;
        }
        
        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.setAttribute('data-price', place.price);
            
            // Try to use uploaded image first, otherwise use default mapping
            // Clean the title for filename (replace spaces with underscores, etc.)
            const cleanTitle = place.title.replace(/[^a-zA-Z0-9\s]/g, '').trim();
            
            // Try multiple image formats
            const possibleImages = [
                `images/${cleanTitle}.png`,
                `images/${cleanTitle}.jpg`,
                `images/${cleanTitle}.jpeg`,
                `images/${place.title}.png`,
                `images/${place.title}.jpg`
            ];
            
            // Use first possible image as default, actual loading handled by onerror
            const imageUrl = possibleImages[0];
            
            // Create amenities preview with icons (show first 3)
            let amenitiesHtml = '';
            if (place.amenities && place.amenities.length > 0) {
                const firstThree = place.amenities.slice(0, 3);
                amenitiesHtml = '<div style="margin: 10px 0; font-size: 0.85em; display: flex; flex-wrap: wrap; gap: 8px;">';
                firstThree.forEach(amenity => {
                    let icon = '';
                    const lowerName = amenity.name.toLowerCase();
                    
                    // All icons are now PNG images
                    if (lowerName.includes('wifi') || lowerName.includes('internet')) {
                        icon = '<img src="images/icon_wifi.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('bed') || lowerName.includes('bedroom')) {
                        icon = '<img src="images/icon_bed.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('bath') || lowerName.includes('bathroom')) {
                        icon = '<img src="images/icon_bath.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('parking')) {
                        icon = '<img src="images/Free Parking.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('pool') || lowerName.includes('swimming')) {
                        icon = '<img src="images/Swimming Pool.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('gym') || lowerName.includes('fitness')) {
                        icon = '<img src="images/Gym.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('kitchen')) {
                        icon = '<img src="images/Kitchen.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('air') || lowerName.includes('conditioning')) {
                        icon = '<img src="images/Air_Conditioning.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('tv')) {
                        icon = '<img src="images/TV.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('breakfast')) {
                        icon = '<img src="images/Kitchen.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('pet')) {
                        icon = '<img src="images/Pet.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('washer') || lowerName.includes('laundry')) {
                        icon = '<img src="images/Laundry.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('balcony')) {
                        icon = '<img src="images/Balcony.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    } else if (lowerName.includes('garden')) {
                        icon = '<img src="images/Garden.png" style="width: 16px; height: 16px; vertical-align: middle;">';
                    }
                    
                    amenitiesHtml += `<span style="background: rgba(0,0,0,0.8); color: #ffffff; padding: 4px 8px; border-radius: 4px; white-space: nowrap;">${icon} ${amenity.name}</span>`;
                });
                amenitiesHtml += '</div>';
            }
            
            card.innerHTML = `
                <img src="${imageUrl}" alt="${place.title}" class="place-image" onerror="this.style.display='none'">
                <h2>${place.title}</h2>
                ${amenitiesHtml}
                <p style="font-weight: bold; font-size: 1.1em; margin-top: 10px;">Price: $${place.price} per night</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
            `;
            placesList.appendChild(card);
        });
    }
    
    // Setup price filter with predefined values
    function setupPriceFilter() {
        if (!priceFilter) return;
        
        // Add price filter options
        const priceOptions = [
            { value: 'all', text: 'All Prices' },
            { value: '50', text: 'Under $50' },
            { value: '100', text: 'Under $100' },
            { value: '200', text: 'Under $200' }
        ];
        
        priceFilter.innerHTML = '';
        priceOptions.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option.value;
            opt.textContent = option.text;
            priceFilter.appendChild(opt);
        });
        
        // Add event listener for filtering
        priceFilter.addEventListener('change', filterByPrice);
    }
    
    // Filter places by price
    function filterByPrice() {
        const selectedPrice = priceFilter.value;
        
        if (selectedPrice === 'all') {
            displayPlaces(allPlaces);
        } else {
            const maxPrice = parseFloat(selectedPrice);
            const filteredPlaces = allPlaces.filter(place => place.price <= maxPrice);
            displayPlaces(filteredPlaces);
        }
    }
    
    // Initialize
    checkAuthentication();
    fetchPlaces();
});