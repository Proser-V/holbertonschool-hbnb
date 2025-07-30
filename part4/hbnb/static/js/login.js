document.addEventListener('DOMContentLoaded', () => {
    // Select the login form
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    // Attach a submit event listener to the form
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the default form submission (page reload if login failed)

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // API POST Login route called
        const res = await fetch('/api/v1/users/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        if (res.ok) {
            window.location.href = '/'; // Redirect to home page
        } else {
            alert("Login failed");
        }
    });
});
