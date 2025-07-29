import { apiFetch } from "./refresh_token.js";

document.addEventListener('DOMContentLoaded', () => {
    const cancelBookingButton = document.querySelectorAll('.cancel-booking-btn');

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