import { apiFetch } from "./refresh_token.js";

document.addEventListener('DOMContentLoaded', () => {
    const deletePlaceButton = document.getElementById('place-deletion-btn');
    if (!deletePlaceButton) return;

    deletePlaceButton.addEventListener('click', async function() {
        const placeId = deletePlaceButton.getAttribute('data-id')
        if (!placeId) return;
        
        const confirmDelete = confirm("Voulez vous vraiment supprimer cet hébergement?");
        if (!confirmDelete) return;

        try {
            const result = await apiFetch(`/api/v1/places/${placeId}`, {
                method: "DELETE"
            })
            if (result.ok) {
                alert("Hébergement supprimé avec succès");
                window.location.href = '/';
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