import { apiFetch } from "./refresh_token.js";

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