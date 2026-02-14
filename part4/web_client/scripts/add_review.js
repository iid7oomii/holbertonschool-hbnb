document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    
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
    
    // Helper function to get place ID from URL
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }
    
    // Check authentication and redirect if not logged in
    function checkAuthentication() {
        const token = getCookie('token');
        console.log('Add review page - Token check:', token ? 'Found' : 'Not found');
        console.log('Add review page - All cookies:', document.cookie);
        if (!token) {
            alert('You must be logged in to add a review');
            window.location.href = 'index.html';
            return null;
        }
        return token;
    }
    
    // Get token and place ID
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    
    console.log('Place ID from URL:', placeId);
    console.log('Token:', token ? 'Present' : 'Missing');
    
    if (!placeId) {
        alert('No place specified');
        window.location.href = 'index.html';
        return;
    }
    
    // Handle form submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const reviewText = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value);
            
            // Validate rating
            if (rating < 1 || rating > 5) {
                alert('Rating must be between 1 and 5');
                return;
            }
            
            const reviewPayload = {
                text: reviewText,
                rating: rating,
                place_id: placeId
            };
            
            console.log('Submitting review with payload:', reviewPayload);
            
            try {
                const response = await fetch('http://127.0.0.1:8000/api/v1/reviews/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(reviewPayload)
                });
                
                if (response.ok) {
                    alert('Review submitted successfully!');
                    // Clear form
                    reviewForm.reset();
                    // Redirect to place details page
                    setTimeout(() => {
                        window.location.href = `place.html?id=${placeId}`;
                    }, 1000);
                } else {
                    const errorData = await response.json();
                    console.error('Server error response:', errorData);
                    alert(`Failed to submit review: ${errorData.message || response.statusText}`);
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert(`An error occurred: ${error.message || 'Please try again.'}`);
            }
        });
    }
});
