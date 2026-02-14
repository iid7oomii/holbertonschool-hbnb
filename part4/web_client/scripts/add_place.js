document.addEventListener('DOMContentLoaded', () => {
    const placeForm = document.getElementById('place-form');
    const amenitiesList = document.getElementById('amenities-list');
    
    // Helper function to get cookie value by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            const cookieValue = parts.pop().split(';').shift();
            return cookieValue;
        }
        return null;
    }
    
    // Check authentication
    function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            alert('You must be logged in to add a place');
            window.location.href = 'login.html';
            return null;
        }
        return token;
    }
    
    // Get token
    const token = checkAuthentication();
    if (!token) return;

    // Fetch and display amenities as checkboxes
    async function fetchAmenities() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/amenities/');
            const amenities = await response.json();
            
            amenitiesList.innerHTML = amenities.map(amenity => `
                <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;">
                    <input type="checkbox" name="amenity" value="${amenity.id}" style="cursor: pointer;">
                    <span>${amenity.name}</span>
                </label>
            `).join('');
        } catch (error) {
            console.error('Error loading amenities:', error);
        }
    }

    fetchAmenities();

    // Handle form submission
    if (placeForm) {
        placeForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const title = document.getElementById('title').value.trim();
            const description = document.getElementById('description').value.trim();
            const price = parseFloat(document.getElementById('price').value);
            const location = document.getElementById('location').value.trim();
            const imageFile = document.getElementById('place-image').files[0];
            
            // Get selected amenities
            const selectedAmenities = Array.from(document.querySelectorAll('input[name="amenity"]:checked'))
                .map(checkbox => checkbox.value);
            
            // Validation
            if (!title || !price || !location) {
                alert('Please fill in all required fields');
                return;
            }

            if (price <= 0) {
                alert('Price must be greater than 0');
                return;
            }

            // Decode JWT to get user ID
            try {
                const tokenParts = token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                const userId = payload.sub;

                const placeData = {
                    title: title,
                    description: description,
                    price: price,
                    latitude: 0,
                    longitude: 0,
                    owner_id: userId,
                    amenities: selectedAmenities,
                    location: location
                };

                console.log('Creating place with data:', placeData);

                // First, create the place
                const response = await fetch('http://127.0.0.1:8000/api/v1/places/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(placeData)
                });

                if (response.ok) {
                    const data = await response.json();
                    const placeId = data.id;
                    
                    // If image was uploaded, upload it
                    if (imageFile) {
                        const formData = new FormData();
                        formData.append('image', imageFile);
                        formData.append('place_id', placeId);
                        formData.append('place_title', title);

                        const imageResponse = await fetch('http://127.0.0.1:8000/api/v1/places/upload-image', {
                            method: 'POST',
                            headers: {
                                'Authorization': `Bearer ${token}`
                            },
                            body: formData
                        });

                        if (!imageResponse.ok) {
                            console.error('Image upload failed, but place was created');
                        }
                    }
                    
                    alert('Place added successfully!');
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const errorData = await response.json();
                    console.error('Server error:', errorData);
                    alert(`Failed to add place: ${errorData.message || response.statusText}`);
                }
            } catch (error) {
                console.error('Error adding place:', error);
                alert(`An error occurred: ${error.message || 'Please try again.'}`);
            }
        });
    }
});
