document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registration-form');
    if (!registrationForm) return;

    registrationForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const first_name = document.getElementById('first_name').value;
        const last_name = document.getElementById('last_name').value;
        let photo_url = document.getElementById('new_user_photo_url').value.trim();
        if (photo_url === "" || photo_url.toLowerCase() === "none") {
            photo_url = null;
        }

        const body = { first_name, last_name, email, password, photo_url };
        console.log(JSON.stringify(body));
        const res = await fetch('/api/v1/users/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            window.location.href = '/login';
            alert(`Bienvenue sur HBnB ${first_name}.`)
        } else {
            alert("Enregistrement échouée.");
        }
    });
});