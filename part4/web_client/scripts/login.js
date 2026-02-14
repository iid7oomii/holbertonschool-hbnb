document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const messageElement = document.getElementById('login-message');

            try {
                const response = await fetch('http://127.0.0.1:8000/api/v1/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=3600; SameSite=Lax`;
                    console.log('Login successful, token saved');
                    window.location.href = 'index.html';
                } else {
                    messageElement.innerText = 'Login Failed: Invalid credentials';
                    messageElement.style.color = '#8B0000';
                }
            } catch (error) {
                messageElement.innerText = 'An error occurred. Is the server running?';
                messageElement.style.color = '#8B0000';
            }
        });
    }
});