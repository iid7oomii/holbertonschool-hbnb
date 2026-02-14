document.addEventListener('DOMContentLoaded', () => {
    const addUserForm = document.getElementById('add-user-form');
    const usersList = document.getElementById('users-list');
    const logoutLink = document.getElementById('logout-link');
    
    // Helper function to get cookie value by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return parts.pop().split(';').shift();
        }
        return null;
    }
    
    // Check if user is admin
    function checkAdminAuth() {
        const token = getCookie('token');
        if (!token) {
            alert('You must be logged in');
            window.location.href = 'login.html';
            return null;
        }

        try {
            const tokenParts = token.split('.');
            const payload = JSON.parse(atob(tokenParts[1]));
            
            if (!payload.is_admin) {
                alert('Admin access required');
                window.location.href = 'index.html';
                return null;
            }
            
            return token;
        } catch (error) {
            console.error('Error decoding token:', error);
            window.location.href = 'login.html';
            return null;
        }
    }
    
    const token = checkAdminAuth();
    if (!token) return;

    // Logout handler
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = 'token=; path=/; max-age=0; SameSite=Lax';
            window.location.href = 'index.html';
        });
    }

    // Fetch and display all users
    async function fetchUsers() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/users/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            
            const users = await response.json();
            displayUsers(users);
        } catch (error) {
            console.error('Error fetching users:', error);
            usersList.innerHTML = '<p style="color: #8B0000; text-align: center;">Failed to load users</p>';
        }
    }

    // Display users in a table
    function displayUsers(users) {
        if (users.length === 0) {
            usersList.innerHTML = '<p style="text-align: center;">No users found</p>';
            return;
        }

        usersList.innerHTML = `
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--gold-color); color: #000;">
                        <th style="padding: 10px; text-align: left;">Name</th>
                        <th style="padding: 10px; text-align: left;">Email</th>
                        <th style="padding: 10px; text-align: center;">Admin</th>
                        <th style="padding: 10px; text-align: center;">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.map(user => `
                        <tr style="border-bottom: 1px solid #ccc;">
                            <td style="padding: 10px; color: #000000;">${user.first_name} ${user.last_name}</td>
                            <td style="padding: 10px; color: #000000;">${user.email}</td>
                            <td style="padding: 10px; text-align: center; color: #000000;">${user.is_admin ? '✓' : '-'}</td>
                            <td style="padding: 10px; text-align: center;">
                                <button onclick="deleteUser('${user.id}')" class="delete-button">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    // Delete user function (global scope for onclick)
    window.deleteUser = async function(userId) {
        if (!confirm('Are you sure you want to delete this user?')) {
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/v1/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                alert('User deleted successfully');
                fetchUsers(); // Refresh list
            } else {
                const errorData = await response.json();
                alert(`Failed to delete user: ${errorData.message || response.statusText}`);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            alert('An error occurred while deleting the user');
        }
    };

    // Handle add user form submission
    if (addUserForm) {
        addUserForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const firstName = document.getElementById('first_name').value.trim();
            const lastName = document.getElementById('last_name').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const isAdmin = document.getElementById('is_admin').checked;
            
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
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        first_name: firstName,
                        last_name: lastName,
                        email: email,
                        password: password,
                        is_admin: isAdmin
                    })
                });

                if (response.ok) {
                    alert('User added successfully!');
                    addUserForm.reset();
                    fetchUsers(); // Refresh list
                } else {
                    const errorData = await response.json();
                    alert(`Failed to add user: ${errorData.message || response.statusText}`);
                }
            } catch (error) {
                console.error('Error adding user:', error);
                alert('An error occurred while adding the user');
            }
        });
    }

    // Initial load
    fetchUsers();
});
