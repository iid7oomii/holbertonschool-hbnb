document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const firstName = document.getElementById('first_name').value.trim();
            const lastName = document.getElementById('last_name').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // Validation
            if (!firstName || !lastName || !email || !password) {
                alert('Please fill in all fields');
                return;
            }

            if (password.length < 6) {
                alert('Password must be at least 6 characters');
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/api/v1/users/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        first_name: firstName,
                        last_name: lastName,
                        email: email,
                        password: password,
                        is_admin: false
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    alert('Registration successful! Please login.');
                    window.location.href = 'login.html';
                } else {
                    const errorData = await response.json();
                    alert('Registration failed: ' + (errorData.message || response.statusText));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Registration failed. Please try again.');
            }
        });
    }
});
