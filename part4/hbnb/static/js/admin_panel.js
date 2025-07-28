import { apiFetch } from "./refresh_token.js";

document.getElementById('open-admin-panel-user').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-user');
    });

document.getElementById('open-admin-panel-place').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-place');
    });

document.getElementById('open-admin-panel-review').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-review');
    });

document.getElementById('open-admin-panel-booking').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-booking');
    });

document.getElementById('open-admin-panel-amenity').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-amenity');
    });

document.getElementById('admin-new-admin-btn').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-admin-creation');
    });

/* New admin registration */
document.addEventListener("DOMContentLoaded", () => {
    const adminRegistrationForm = document.getElementById('admin-registration-form');
    if (!adminRegistrationForm) return;

    adminRegistrationForm.addEventListener('submit', async (e) => {
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

        const res = await apiFetch('/api/v1/users/admin_creation', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            location.reload();
            alert(`Administrateur créé.`)
        } else {
            alert("Enregistrement échouée.");
        }
    });
});

document.getElementById('admin-new-amenity-btn').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-amenity-creation');
    });

/* New amenity registration */
document.addEventListener("DOMContentLoaded", () => {
    const adminRegistrationForm = document.getElementById('new-amenity-registration-form');
    if (!adminRegistrationForm) return;
    console.log("Formulaire détecté");
    adminRegistrationForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('new-amenity-name').value;
        const description = document.getElementById('new-amenity-description').value;
        let icon_file = document.getElementById('new-amenity-icon-file').value;
        if (icon_file === "" || icon_file.toLowerCase() === "none") {
            icon_file = null;
        }

        const body = { name, description, icon_file };
        console.log(JSON.stringify(body));
        const res = await apiFetch('/api/v1/amenities', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            location.reload();
            alert(`Equipement créé.`)
        } else {
            alert("Enregistrement échouée.");
        }
    });
});

/* Amenity deletion */
document.addEventListener('DOMContentLoaded', () => {
    const deleteAmenityButtons = document.querySelectorAll('.admin-delete-amenity-btn');

    deleteAmenityButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const amenityId = button.getAttribute('data-id')
            if (!amenityId) return;
            
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet équipement?");
            if (!confirmDelete) return;

            try {
                const result = await apiFetch(`/api/v1/amenities/${amenityId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Equipement supprimé avec succès");
                    location.reload();
                } else {
                    const error = await result.json();
                    alert(`Erreur lors de la suppression : ${error?.error || 'Inconnue'}`)
                }
            } catch (err) {
                console.error(err);
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* User deletion */
document.addEventListener('DOMContentLoaded', () => {
    const deleteUserButton = document.querySelectorAll('.admin-delete-user-btn');

    deleteUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.getAttribute('data-id')
            if (!userId) return;
            
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet utilisateur?");
            if (!confirmDelete) return;

            try {
                const result = await apiFetch(`/api/v1/users/${userId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Utilisateur supprimé avec succès");
                    location.reload();
                } else {
                    const error = await result.json();
                    alert(`Erreur lors de la suppression : ${error?.error || 'Inconnue'}`)
                }
            } catch (err) {
                console.error(err);
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* To User profile */
document.addEventListener('DOMContentLoaded', () => {
    const deleteUserButton = document.querySelectorAll('.admin-to-user-profile-btn');

    deleteUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.getAttribute('data-id')
            if (!userId) return;

            try {
                const result = await apiFetch(`/api/v1/users/${userId}`, {
                    method: "GET"
                })
                if (result.ok) {
                    window.location.href = `/user/${userId}/profile`;
                } else {
                    const error = await result.json();
                    alert(`Erreur lors de la redirection : ${error?.error || 'Inconnue'}`)
                }
            } catch (err) {
                console.error(err);
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* User is_active ON/OFF */
document.addEventListener('DOMContentLoaded', () => {
    const deleteUserButton = document.querySelectorAll('.admin-moderate-user-btn');

    deleteUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.getAttribute('data-id')
            const userIsActive = button.getAttribute('data-is-active')
            if (!userId) return;
            if (userIsActive == true) {
                try {
                    const body = { "is_active": false };
                    const result = await apiFetch(`/api/v1/users/${userId}/moderate`, {
                        method: "PATCH",
                        body: JSON.stringify(body)
                    })
                    if (result.ok) {
                        alert("Utilisateur passé inactif avec succès");
                        location.reload();
                    } else {
                        const error = await result.json();
                        alert(`Erreur lors de la redirection : ${error?.error || 'Inconnue'}`)
                    }
                } catch (err) {
                    console.error(err);
                    alert("Une erreur est survenue.");
                }
            } else {
                try {
                    const body = { "is_active": true };
                    const result = await apiFetch(`/api/v1/users/${userId}/moderate`, {
                        method: "PATCH",
                        body: JSON.stringify(body)
                    })
                    if (result.ok) {
                        alert("Utilisateur passé actif avec succès");
                        location.reload();
                    } else {
                        const error = await result.json();
                        alert(`Erreur lors de la redirection : ${error?.error || 'Inconnue'}`)
                    }
                } catch (err) {
                    console.error(err);
                    alert("Une erreur est survenue.");
                }
            }
        });
    });
});