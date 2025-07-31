import { apiFetch, formatPydanticError } from "./refresh_token.js";

document.addEventListener('DOMContentLoaded', () => {
    // Select all booking cancellation buttons
    const cancelBookingButton = document.querySelectorAll('.cancel-booking-btn');

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
                    location.reload(); // Reload the page to show results
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