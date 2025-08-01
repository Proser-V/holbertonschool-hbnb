import { apiFetch, formatPydanticError } from "./refresh_token.js";

/* Toggle admin panel sections visibility when corresponding buttons are clicked */
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
    // Get the admin registration form element
    const adminRegistrationForm = document.getElementById('admin-registration-form');
    if (!adminRegistrationForm) return;

    // Listen for the form submit event
    adminRegistrationForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the default form submission (page reload)

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const first_name = document.getElementById('first_name').value;
        const last_name = document.getElementById('last_name').value;
        let photo_url = document.getElementById('new_user_photo_url').value.trim();
        // Set photo_url to null if empty or equals "none"
        if (photo_url === "" || photo_url.toLowerCase() === "none") {
            photo_url = null;
        }

        const body = { first_name, last_name, email, password, photo_url };

        // Send POST request to create the new admin user
        const res = await apiFetch('/api/v1/users/admin_creation', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        // On success, reload page and alert user
        if (res.ok) {
            location.reload();
            alert(`Administrateur créé.`)
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur :\n${prettyMessage}`);
        }
    });
});

/* Toggle new amenity creation form visibility */
document.getElementById('admin-new-amenity-btn').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-amenity-creation');
    });

/* New amenity registration */
document.addEventListener("DOMContentLoaded", () => {
    // Get the new amenity registration form element
    const adminRegistrationForm = document.getElementById('new-amenity-registration-form');
    if (!adminRegistrationForm) return;

    // Listen for the form submit event
    adminRegistrationForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the default form submission (page reload)

        const name = document.getElementById('new-amenity-name').value;
        const description = document.getElementById('new-amenity-description').value;
        const icon_file_input = document.getElementById('new-amenity-icon-file').value;
        // Use default icon if no icon file was provided
        const icon_file = icon_file_input !== "" ? icon_file_input: "default-amenities.png"

        const body = { name, description, icon_file };

        // Send POST request to create the new amenity
        const res = await apiFetch('/api/v1/amenities', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            location.reload(); // Reload the page to show the updated list and notify user
            alert(`Equipement créé.`)
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur :\n${prettyMessage}`);
        }
    });
});

/* Amenity deletion */
document.addEventListener('DOMContentLoaded', () => {
    // Select all delete buttons for amenities in admin panel
    const deleteAmenityButtons = document.querySelectorAll('.admin-delete-amenity-btn');

    deleteAmenityButtons.forEach(button => {
        button.addEventListener('click', async () => {
            // Get amenity ID from data attribute
            const amenityId = button.getAttribute('data-id')
            if (!amenityId) return;
            
            // Confirm deletion with the user
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet équipement?");
            if (!confirmDelete) return;

            try {
                // Call API DELETE endpoint to remove the amenity
                const result = await apiFetch(`/api/v1/amenities/${amenityId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Equipement supprimé avec succès");
                    location.reload(); // Reload page to reflect changes
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* Amenity update */
let currentAmenityId = null;

function openModalWithData(button) {
    // Get current amenity info from data attributes on button
    currentAmenityId = button.getAttribute('data-id');
    const name = button.getAttribute('data-name');
    const description = button.getAttribute('data-description');
    const icon = button.getAttribute('data-icon');

    // Find modal element within the same table cell (<td>)
    const modalElement = button.closest('td').querySelector('.amenity-modal');
    if (!modalElement) return;

    // Pre-fill modal inputs with current values or empty strings
    modalElement.querySelector('.update-amenity-name').value = name || '';
    modalElement.querySelector('.update-amenity-description').value = description || '';
    modalElement.querySelector('.update-amenity-icon-file').value = icon || '';

    // Show modal and overlay by removing 'hidden' class
    modalElement.classList.remove('hidden');
    modalElement.previousElementSibling.classList.remove('hidden');
}

function closeModal() {
    // Select the opened modal and overlay
    const openModal = document.querySelector('.amenity-modal:not(.hidden)');
    const openOverlay = document.querySelector('.amenity-modal-overlay:not(.hidden)');

    if (openModal) openModal.classList.add('hidden'); // Hide the opened modal
    if (openOverlay) openOverlay.classList.add('hidden'); // Hide the opened overlay
    currentAmenityId = null;
}

document.querySelectorAll(".admin-update-amenity-btn").forEach(button => {
    button.addEventListener("click", event => {
        event.preventDefault(); // Prevent default behavior
        openModalWithData(button); // Open modal with pre-filled data
    });
});

// Close modal on close button or overlay click
document.getElementById('close-amenity-modal').addEventListener('click', closeModal);
document.getElementById('amenity-modal-overlay').addEventListener('click', closeModal);

document.querySelectorAll('.submit-amenity-update').forEach(button => {
    button.addEventListener('click', async () => {
        // Get modal containing the clicked button
        const parentModal = button.closest('.amenity-modal');

        // Get updated values or undefined if empty
        const amenityName = parentModal.querySelector('.update-amenity-name').value || undefined;
        const amenityDescription = parentModal.querySelector('.update-amenity-description').value || undefined;
        let amenityIcon = parentModal.querySelector('.update-amenity-icon-file').value || undefined;

        // Set icon to null if empty string or "none"
        if (amenityIcon === '' || amenityIcon.toLowerCase() === 'none') {
            amenityIcon = null;
        }

        // Get the amenity ID either from closest button or fallback to currentAmenityId
        const amenityId = button.closest('td').querySelector('.admin-update-amenity-btn')?.getAttribute('data-id')
            || currentAmenityId;

        try {
            // Call API PUT to update the amenity data
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
                location.reload(); // Refresh page to reflect changes
            } else {
                // Attempt to parse the JSON error response
                const errorData = await res.json();
                // Format Pydantic-style validation errors into a user-friendly message
                const prettyMessage = formatPydanticError(errorData);
                // Display the formatted error to the user
                alert(`Erreur :\n${prettyMessage}`);
            }
        } catch (error) {
            console.error(error);
            alert("Une erreur est survenue.");
        }
    })
});


/* User deletion */
document.addEventListener('DOMContentLoaded', () => {
    // Select all user deletion buttons in admin panel
    const deleteUserButton = document.querySelectorAll('.admin-delete-user-btn');

    deleteUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            // Get user ID from data attribute
            const userId = button.getAttribute('data-id')
            if (!userId) return;

            // Confirm with user before deleting
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet utilisateur?");
            if (!confirmDelete) return;

            try {
                // Call API DELETE to remove user
                const result = await apiFetch(`/api/v1/users/${userId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Utilisateur supprimé avec succès");
                    location.reload(); // Refresh page to reflect changes
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* To User profile */
document.addEventListener('DOMContentLoaded', () => {
    // Select buttons that redirect to user profile
    const goToUserButton = document.querySelectorAll('.admin-to-user-profile-btn');

    goToUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            // Get user ID from data attribute
            const userId = button.getAttribute('data-id')
            if (!userId) return;

            try {
                // Verify user exists before redirecting
                const result = await apiFetch(`/api/v1/users/${userId}`, {
                    method: "GET"
                })
                if (result.ok) {
                    // Redirect to user's profile page
                    window.location.href = `/user/${userId}/profile`;
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* User is_active ON/OFF */
document.addEventListener('DOMContentLoaded', () => {
    // Select buttons toggling user active status
    const moderateUserButton = document.querySelectorAll('.admin-moderate-user-btn');

    moderateUserButton.forEach(button => {
        button.addEventListener('click', async () => {
            const userId = button.getAttribute('data-id');
            // The attribute is string, compare to "True"
            const userIsActive = button.getAttribute('data-is-active') === "True";
            if (!userId) return;
            if (userIsActive) {
                try {
                    // If user is active, prepare to deactivate (PATCH with is_active: false)
                    const body = { "is_active": false };
                    const result = await apiFetch(`/api/v1/users/${userId}/moderate`, {
                        method: "PATCH",
                        body: JSON.stringify(body)
                    })
                    if (result.ok) {
                        alert("Utilisateur passé inactif avec succès");
                        location.reload();
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
                    alert("Une erreur est survenue.");
                }
            } else {
                try {
                    // If user is inactive, prepare to activate (PATCH with is_active: true
                    const body = { "is_active": true };
                    const result = await apiFetch(`/api/v1/users/${userId}/moderate`, {
                        method: "PATCH",
                        body: JSON.stringify(body)
                    })
                    if (result.ok) {
                        alert("Utilisateur passé actif avec succès");
                        location.reload();
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
                    alert("Une erreur est survenue.");
                }
            }
        });
    });
});

/* Place deletion */
document.addEventListener('DOMContentLoaded', () => {
    // Select all delete buttons for places
    const deletePlaceButton = document.querySelectorAll('.admin-delete-place-btn');

    deletePlaceButton.forEach(button => {
        button.addEventListener('click', async () => {
            // Get place ID from data attribute
            const placeId = button.getAttribute('data-id')
            if (!placeId) return;

            // Confirm deletion with the user
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet hébergement?");
            if (!confirmDelete) return;

            try {
                // API call to DELETE the place
                const result = await apiFetch(`/api/v1/places/${placeId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Hébergement supprimé avec succès");
                    location.reload(); // Reload to render results
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* To Place details */
document.addEventListener('DOMContentLoaded', () => {
    // Select buttons that redirect to place details
    const goToPlaceButton = document.querySelectorAll('.admin-to-place-details-btn');

    goToPlaceButton.forEach(button => {
        button.addEventListener('click', async () => {
            const placeId = button.getAttribute('data-id')
            if (!placeId) return;

            try {
                // Check if place exists before redirecting
                const result = await apiFetch(`/api/v1/places/${placeId}`, {
                    method: "GET"
                })
                if (result.ok) {
                    // Redirect to place details page
                    window.location.href = `/place/${placeId}`;
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* Review deletion */
document.addEventListener('DOMContentLoaded', () => {
    // Select all review deletion buttons
    const deleteReviewButton = document.querySelectorAll('.admin-delete-review-btn');

    deleteReviewButton.forEach(button => {
        button.addEventListener('click', async () => {
            const reviewId = button.getAttribute('data-id')
            if (!reviewId) return;
            
            // Confirm review deletion with user
            const confirmDelete = confirm("Voulez vous vraiment supprimer cet avis?");
            if (!confirmDelete) return;

            try {
                // API call to DELETE review
                const result = await apiFetch(`/api/v1/reviews/${reviewId}`, {
                    method: "DELETE"
                })
                if (result.ok) {
                    alert("Avis supprimé avec succès");
                    location.reload(); // Reload to render results
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
                alert("Une erreur est survenue.");
            }
        });
    });
});

/* Booking status update (refresh bookings list) */
document.addEventListener('DOMContentLoaded', () => {
    // Button that triggers bookings refresh
    const cancelBookingButton = document.getElementById('admin-refresh-bookings-btn');

    cancelBookingButton.addEventListener('click', async function() {
        try {
            // Call API GET to refresh bookings list
            const result = await apiFetch(`/api/v1/bookings`, {
                method: "GET",
            })
            if (result.ok) {
                alert("Liste de réservation mise à jour.");
                location.reload(); // Reload to show refreshed bookings
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
            alert("Une erreur est survenue.");
        }
    });
});

/* Booking cancellation */
document.addEventListener('DOMContentLoaded', () => {
    // Select all booking cancellation buttons
    const cancelBookingButton = document.querySelectorAll('.admin-cancel-booking-btn');

    cancelBookingButton.forEach(button => {
        button.addEventListener('click', async () => {
            const bookingId = button.getAttribute('data-id')
            if (!bookingId) return;
            
            // Confirm cancellation with user
            const confirmCancel = confirm("Voulez vous vraiment annuler cette réservation?");
            if (!confirmCancel) return;

            try {
                // API PUT call to update booking status to "CANCELLED"
                const result = await apiFetch(`/api/v1/bookings/${bookingId}`, {
                    method: "PUT",
                    body: JSON.stringify({ "status": "CANCELLED" })
                })
                if (result.ok) {
                    alert("Réservation annulée avec succès");
                    location.reload(); // Reload to show results
                } else {
                    // Attempt to parse the JSON error response
                    const errorData = await result.json();
                    // Format Pydantic-style validation errors into a user-friendly message
                    const prettyMessage = formatPydanticError(errorData);
                    // Display the formatted error to the user
                    alert(`Erreur :\n${prettyMessage}`);
                }
            } catch (err) {
                console.error(err);
                alert("Une erreur est survenue.");
            }
        });
    });
});
