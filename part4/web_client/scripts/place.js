document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
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
    
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review-section');
    const addPlaceLink = document.getElementById('add-place-link');
    const adminLink = document.getElementById('admin-link');
    
    // Get current user info from token
    let currentUserId = null;
    let isAdmin = false;
    
    if (token) {
        try {
            const tokenParts = token.split('.');
            const payload = JSON.parse(atob(tokenParts[1]));
            currentUserId = payload.sub;
            isAdmin = payload.is_admin || false;
        } catch (error) {
            console.error('Error decoding token:', error);
        }
    }
    
    console.log('Place page - Token check:', token ? 'Found' : 'Not found');
    console.log('Place page - All cookies:', document.cookie);
    
    // Delete place function
    async function deletePlace(placeId) {
        if (!confirm('هل أنت متأكد من حذف هذا المكان؟ سيتم حذف جميع التعليقات المرتبطة به.')) {
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/places/${placeId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                alert('تم حذف المكان بنجاح!');
                window.location.href = 'index.html'; // Redirect to home page
            } else {
                const error = await response.json();
                alert('خطأ في حذف المكان: ' + (error.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error deleting place:', error);
            alert('حدث خطأ أثناء حذف المكان');
        }
    }
    
    // Delete review function
    async function deleteReview(reviewId) {
        if (!confirm('هل أنت متأكد من حذف هذا التعليق؟')) {
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/reviews/${reviewId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                alert('تم حذف التعليق بنجاح!');
                location.reload(); // Reload to show updated reviews
            } else {
                const error = await response.json();
                alert('خطأ في حذف التعليق: ' + (error.message || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error deleting review:', error);
            alert('حدث خطأ أثناء حذف التعليق');
        }
    }
    
    // Check if user is admin and show appropriate links
    if (token) {
        try {
            const tokenParts = token.split('.');
            const payload = JSON.parse(atob(tokenParts[1]));
            const userIsAdmin = payload.is_admin || false;
            
            // Show Add Place link
            if (addPlaceLink) {
                addPlaceLink.style.display = 'inline';
            }
            
            // Show Admin link if user is admin
            if (userIsAdmin && adminLink) {
                adminLink.style.display = 'inline';
            }
        } catch (error) {
            console.error('Error decoding token:', error);
        }
    }
    
    // Always show add review section, but customize based on auth
    if (addReviewSection) {
        const addReviewLink = document.getElementById('add-review-link');
        
        if (token) {
            // User is logged in - show add review button
            addReviewLink.href = `add_review.html?id=${placeId}`;
            addReviewLink.style.display = 'inline-block';
            addReviewSection.querySelector('p').textContent = 'Share your experience with others!';
            addReviewSection.querySelector('p').style.color = '#000000';
            console.log('User authenticated - showing add review button');
        } else {
            // User not logged in - show login prompt
            addReviewLink.textContent = 'Login to Add Review';
            addReviewLink.href = 'login.html';
            addReviewLink.style.display = 'inline-block';
            addReviewSection.querySelector('p').textContent = 'Please login to add a review';
            addReviewSection.querySelector('p').style.color = '#000000';
            console.log('User not authenticated - showing login prompt');
        }
    }

    async function fetchPlaceDetails() {
        if (!placeId) {
            document.getElementById('place-info').innerHTML = '<p>Place not found</p>';
            return;
        }
        
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/places/${placeId}`);
            
            if (!response.ok) {
                throw new Error('Place not found');
            }
            
            const place = await response.json();
            renderPlace(place);
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('place-info').innerHTML = '<p style="color: var(--gold-color);">Failed to load place details. Place may not exist.</p>';
        }
    }

    function renderPlace(place) {
        const info = document.getElementById('place-info');
        
        // Try to use uploaded image first
        const cleanTitle = place.title.replace(/[^a-zA-Z0-9\s]/g, '').trim();
        const imageUrl = `images/${cleanTitle}.png`;
        
        // Check if user can delete this place (owner or admin)
        const canDelete = token && (isAdmin || (place.owner && place.owner.id === currentUserId));
        
        // Render basic place information with image
        let htmlContent = `
            <img src="${imageUrl}" alt="${place.title}" style="width: 100%; max-width: 800px; height: 400px; object-fit: cover; border-radius: 10px; margin-bottom: 20px;" 
                 onerror="this.src='images/${place.title}.png'; this.onerror=function(){this.style.display='none'};">
            <h1 style="color: #000000;">${place.title}</h1>
            <p style="color: #000000;"><strong>Description:</strong> ${place.description || 'No description available'}</p>
            <p style="color: #000000;"><strong>Price:</strong> $${place.price} per night</p>
            <p style="color: #000000;"><strong>Location:</strong> ${place.location || 'Not specified'}</p>
        `;
        
        // Add delete button if user is owner or admin
        if (canDelete) {
            htmlContent += `
                <div style="margin-top: 20px; text-align: center;">
                    <button onclick="deletePlace('${place.id}')" class="delete-button" style="background: #ffffff; color: #000000; padding: 12px 30px; border: 2px solid #333333; border-radius: 25px; cursor: pointer; font-weight: bold; position: relative; overflow: hidden; transition: all 0.5s ease;">
                        <img src="images/trach.png" alt="Delete" style="width: 20px; height: 20px; vertical-align: middle; margin-right: 8px;">
                        Delete Place
                    </button>
                </div>
            `;
        }
        
        // Render owner information
        if (place.owner) {
            htmlContent += `
                <div style="margin-top: 20px; padding: 15px; background: #000; border: 1px solid var(--gold-color); border-radius: 8px;">
                    <h3 style="color: var(--gold-color);">Host Information</h3>
                    <p style="color: #ffffff;"><strong>Name:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
                    <p style="color: #ffffff;"><strong>Email:</strong> ${place.owner.email}</p>
                </div>
            `;
        }
        
        // Render amenities with icons
        if (place.amenities && place.amenities.length > 0) {
            htmlContent += `
                <div style="margin-top: 20px;">
                    <h3 style="color: var(--gold-color);">Amenities</h3>
                    <ul style="list-style: none; padding: 0;">
                        ${place.amenities.map(amenity => {
                            // Map amenity names to icons
                            let icon = '';
                            const lowerName = amenity.name.toLowerCase();
                            
                            // All icons are now PNG images
                            if (lowerName.includes('wifi') || lowerName.includes('internet')) {
                                icon = '<img src="images/icon_wifi.png" alt="WiFi" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('bed') || lowerName.includes('bedroom')) {
                                icon = '<img src="images/icon_bed.png" alt="Bed" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('bath') || lowerName.includes('bathroom')) {
                                icon = '<img src="images/icon_bath.png" alt="Bath" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('parking') || lowerName.includes('موقف')) {
                                icon = '<img src="images/Free Parking.png" alt="Parking" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('pool') || lowerName.includes('swimming') || lowerName.includes('مسبح')) {
                                icon = '<img src="images/Swimming Pool.png" alt="Pool" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('gym') || lowerName.includes('fitness') || lowerName.includes('جيم')) {
                                icon = '<img src="images/Gym.png" alt="Gym" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('kitchen') || lowerName.includes('مطبخ')) {
                                icon = '<img src="images/Kitchen.png" alt="Kitchen" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('air') || lowerName.includes('conditioning') || lowerName.includes('تكييف')) {
                                icon = '<img src="images/Air_Conditioning.png" alt="AC" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('tv') || lowerName.includes('television')) {
                                icon = '<img src="images/TV.png" alt="TV" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('breakfast') || lowerName.includes('إفطار')) {
                                icon = '<img src="images/Kitchen.png" alt="Breakfast" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('pet') || lowerName.includes('حيوان')) {
                                icon = '<img src="images/Pet.png" alt="Pet" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('washer') || lowerName.includes('laundry') || lowerName.includes('غسالة')) {
                                icon = '<img src="images/Laundry.png" alt="Laundry" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('balcony') || lowerName.includes('شرفة')) {
                                icon = '<img src="images/Balcony.png" alt="Balcony" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            } else if (lowerName.includes('garden') || lowerName.includes('حديقة')) {
                                icon = '<img src="images/Garden.png" alt="Garden" style="width: 20px; height: 20px; margin-right: 8px; vertical-align: middle;">';
                            }
                            
                            return `
                            <li style="display: inline-block; background: #ffffff; color: #000000; padding: 8px 15px; margin: 5px; border-radius: 5px; font-weight: bold;">
                                ${icon}${amenity.name}
                            </li>
                        `}).join('')}
                    </ul>
                </div>
            `;
        }
        
        info.innerHTML = htmlContent;
        
        // Render reviews
        const reviewsList = document.getElementById('reviews-list');
        if (place.reviews && place.reviews.length > 0) {
            reviewsList.innerHTML = '';
            place.reviews.forEach(review => {
                const div = document.createElement('div');
                div.className = 'review-card';
                
                // Check if user can delete this review (owner or admin)
                const canDelete = token && (isAdmin || (review.user && review.user.id === currentUserId));
                
                const deleteButton = canDelete ? `
                    <button onclick="deleteReview('${review.id}')" 
                            class="delete-review-btn" 
                            title="حذف التعليق">
                        <img src="images/trach.png" alt="Delete">
                    </button>
                ` : '';
                
                const userName = review.user ? `${review.user.first_name} ${review.user.last_name}` : 'Anonymous';
                
                div.innerHTML = `
                    ${deleteButton}
                    <p style="color: #000000; margin-bottom: 5px;"><strong>${userName}</strong></p>
                    <p style="color: #000000;">${review.text}</p>
                    <p style="color: #000000;"><strong>Rating: ${'<img src="images/star.png" style="width: 16px; height: 16px; vertical-align: middle;">'.repeat(review.rating)}</strong> (${review.rating}/5)</p>
                `;
                reviewsList.appendChild(div);
            });
        } else {
            reviewsList.innerHTML = '<p style="color: #000000;">لا توجد تعليقات بعد. كن أول من يعلق!</p>';
        }
        
        // Make deleteReview and deletePlace functions globally accessible
        window.deleteReview = deleteReview;
        window.deletePlace = deletePlace;
    }
    
    if (placeId) {
        fetchPlaceDetails();
    } else {
        document.getElementById('place-info').innerHTML = '<p>No place ID provided</p>';
    }
});