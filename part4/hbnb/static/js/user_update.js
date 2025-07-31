import { apiFetch, formatPydanticError } from './refresh_token.js';

// Wait until the full HTML document is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Select what is needed for the form inside a button
    const container = document.getElementById('user-update-container');
    const button = document.getElementById('button-to-update-user');
    const cancelBtn = document.getElementById('cancel-update-form');
    const form = document.getElementById('user-update-form');

    button.addEventListener('click', () => {
        container.classList.add('expanding'); // Add class to start expansion animation
        setTimeout(() => {
            container.classList.add('show-form'); // Show the form after animation delay
        }, 400);
    });

    cancelBtn.addEventListener('click', () => {
        container.classList.remove('show-form'); // Hide the form immediately
        setTimeout(() => {
            container.classList.remove('expanding'); // Remove expansion after delay
        }, 400);
    });

    // Handle the user update form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submit behavior (page reload)
        const userId = form.dataset.userId;

        // Prepare data from form inputs, trimming whitespace and setting undefined if empty
        const data = {
            first_name: form.first_name.value.trim() || undefined,
            last_name: form.last_name.value.trim() || undefined,
            email: form.email.value.trim() || undefined,
            password: form.password.value.trim() || undefined,
            photo_url: form.photo_url.value.trim() || undefined,
        };

        try {
            // Send PUT request to update user profile with JSON data
            const response = await apiFetch(`/api/v1/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });

        if (response.ok) {
            alert('Profil mis à jour !');
            location.reload(); // Reload the page to reflect changes
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur :\n${prettyMessage}`);
        }
        } catch (err) {
            console.error(err);
            alert('Erreur réseau ou serveur');
        }
    });
});
