import { apiFetch } from "./refresh_token.js";

document.addEventListener('DOMContentLoaded', () => {
    // Select all delete buttons for places
    const deletePlaceButton = document.getElementById('place-deletion-btn');
    if (!deletePlaceButton) return;

    deletePlaceButton.addEventListener('click', async function() {
        // Get place ID from data attribute
        const placeId = deletePlaceButton.getAttribute('data-id')
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
                window.location.href = '/'; // Redirect to home page
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