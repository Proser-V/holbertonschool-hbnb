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

    adminRegistrationForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('new-amenity-name').value;
        const description = document.getElementById('new-amenity-description').value;
        const icon_file_input = document.getElementById('new-amenity-icon-file').value;
        const icon_file = icon_file_input !== "" ? icon_file_input: "default-amenities.png"

        const body = { name, description, icon_file };

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

/* Amenity update */
const modal = document.getElementById('amenity-modal');
const overlay = document.getElementById('amenity-modal-overlay');
const closeModalBtn = document.getElementById('close-amenity-modal');

let currentAmenityId = null;

function openModalWithData(button) {
    currentAmenityId = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const description = button.getAttribute('data-description');
    const icon = button.getAttribute('data-icon');

    const modalElement = button.closest('td').querySelector('.amenity-modal');
    if (!modalElement) return;


    modalElement.querySelector('.update-amenity-name').value = name || '';
    modalElement.querySelector('.update-amenity-description').value = description || '';
    modalElement.querySelector('.update-amenity-icon-file').value = icon || '';

    modalElement.classList.remove('hidden');
    modalElement.previousElementSibling.classList.remove('hidden');
}

function closeModal() {
    modal.classList.add('hidden');
    overlay.classList.add('hidden');
    currentAmenityId = null;
}

document.querySelectorAll(".admin-update-amenity-btn").forEach(button => {
    button.addEventListener("click", event => {
        event.preventDefault();
        openModalWithData(button);
    });
});

closeModalBtn.addEventListener('click', closeModal);
overlay.addEventListener('click', closeModal);

document.querySelectorAll('.submit-amenity-update').forEach(button => {
    button.addEventListener('click', async () => {
        const parentModal = button.closest('.amenity-modal');
        const amenityName = parentModal.querySelector('.update-amenity-name').value || undefined;
        const amenityDescription = parentModal.querySelector('.update-amenity-description').value || undefined;
        let amenityIcon = parentModal.querySelector('.update-amenity-icon-file').value || undefined;

        if (amenityIcon === '' || amenityIcon.toLowerCase() === 'none') {
            amenityIcon = null;
        }

        const amenityId = button.closest('td').querySelector('.admin-update-amenity-btn')?.getAttribute('data-id')
            || currentAmenityId;

        try {
            const result = await apiFetch(`/api/v1/amenities/${amenityId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    name: amenityName,
                    description: amenityDescription,
                    icon_file: amenityIcon
                })
            });

            if (result.ok) {
                alert("Équipement modifié avec succès.");
                location.reload();
            } else {
                const error = await result.json();
                alert(`Erreur lors de la mise à jour : ${error?.error || 'Inconnue'}`);
            }
        } catch (error) {
            console.error(error);
            alert("Une erreur est survenue.");
        }
    })
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
    const goToUserButton = document.querySelectorAll('.admin-to-user-profile-btn');

    goToUserButton.forEach(button => {
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
    const moderateUserButton = document.querySelectorAll('.admin-moderate-user-btn');

    moderateUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.getAttribute('data-id');
            const userIsActive = button.getAttribute('data-is-active') === "True";
            if (!userId) return;
            if (userIsActive) {
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

/* Place deletion */
document.addEventListener('DOMContentLoaded', () => {
    const deletePlaceButton = document.querySelectorAll('.admin-delete-place-btn');

    deletePlaceButton.forEach(button => {
        button.addEventListener('click', async () => {
            const placeId = button.getAttribute('data-id')
            if (!placeId) return;
            
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet hébergement?");
            if (!confirmDelete) return;

            try {
                const result = await apiFetch(`/api/v1/places/${placeId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Hébergement supprimé avec succès");
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

/* To Place details */
document.addEventListener('DOMContentLoaded', () => {
    const goToPlaceButton = document.querySelectorAll('.admin-to-place-details-btn');

    goToPlaceButton.forEach(button => {
        button.addEventListener('click', async () => {
            const placeId = button.getAttribute('data-id')
            if (!placeId) return;

            try {
                const result = await apiFetch(`/api/v1/places/${placeId}`, {
                    method: "GET"
                })
                if (result.ok) {
                    window.location.href = `/place/${placeId}`;
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

/* Review deletion */
document.addEventListener('DOMContentLoaded', () => {
    const deleteReviewButton = document.querySelectorAll('.admin-delete-review-btn');

    deleteReviewButton.forEach(button => {
        button.addEventListener('click', async () => {
            const reviewId = button.getAttribute('data-id')
            if (!reviewId) return;
            
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet avis?");
            if (!confirmDelete) return;

            try {
                const result = await apiFetch(`/api/v1/reviews/${reviewId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Avis supprimé avec succès");
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

/* Booking status update */
document.addEventListener('DOMContentLoaded', () => {
    const cancelBookingButton = document.getElementById('admin-refresh-bookings-btn');

    cancelBookingButton.addEventListener('click', async function() {
        try {
            const result = await apiFetch(`/api/v1/bookings`, {
                method: "GET",
            })
            if (result.ok) {
                alert("Liste de réservation mise à jour.");
                location.reload();
            } else {
                const error = await result.json();
                alert(`Erreur lors de la mise à jour' : ${error?.error || 'Inconnue'}`)
            }
        } catch (err) {
            console.error(err);
            alert("Une erreur est survenue.");
        }
    });
});

/* Booking cancellation */
document.addEventListener('DOMContentLoaded', () => {
    const cancelBookingButton = document.querySelectorAll('.admin-cancel-booking-btn');

    cancelBookingButton.forEach(button => {
        button.addEventListener('click', async () => {
            const bookingId = button.getAttribute('data-id')
            if (!bookingId) return;
            
            const confirmCancel = confirm("Voulez vous vraiment annuler cette réservation?");
            if (!confirmCancel) return;

            try {
                const result = await apiFetch(`/api/v1/bookings/${bookingId}`, {
                    method: "PUT",
                    body: JSON.stringify({ "status": "CANCELLED" })
                })
                if (result.ok) {
                    alert("Réservation annulée avec succès");
                    location.reload();
                } else {
                    const error = await result.json();
                    alert(`Erreur lors de l'annulation' : ${error?.error || 'Inconnue'}`)
                }
            } catch (err) {
                console.error(err);
                alert("Une erreur est survenue.");
            }
        });
    });
});