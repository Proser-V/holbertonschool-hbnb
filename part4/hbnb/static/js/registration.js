// Wait until the full HTML document is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Select the registration form element
    const registrationForm = document.getElementById('registration-form');
    if (!registrationForm) return;

    // Attach a submit event listener to the form
    registrationForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the reloading on form submit

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const first_name = document.getElementById('first_name').value;
        const last_name = document.getElementById('last_name').value;
        // Get and clean the optional photo_url input
        let photo_url = document.getElementById('new_user_photo_url').value.trim();
        // If photo_url is empty or "none", treat it as null
        if (photo_url === "" || photo_url.toLowerCase() === "none") {
            photo_url = null;
        }

        const body = { first_name, last_name, email, password, photo_url };

        // Send a POST request to register the user
        const res = await fetch('/api/v1/users/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            window.location.href = '/login'; // Redirect to login page
            alert(`Bienvenue sur HBnB ${first_name}.`)
        } else {
            alert("Enregistrement échouée.");
        }
    });
});