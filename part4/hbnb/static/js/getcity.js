document.addEventListener("DOMContentLoaded", function () {
    const locationDiv = document.querySelector(".place-location");
    const latitude = locationDiv.dataset.latitude;
    const longitude = locationDiv.dataset.longitude;

    if (latitude && longitude) {
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`, {
        headers: {
            'User-Agent': 'HBnB-App/1.0 (contact@monapp.com)' // obligatoire
        }
        })
        .then(response => response.json())
        .then(data => {
        const city = data.address.city ||
                        data.address.town ||
                        data.address.village ||
                        data.address.municipality ||
                        data.address.county ||
                        'Localisation impossible';
        document.getElementById("location-name").textContent = `${city}`;
        })
        .catch(error => {
        console.error("Erreur récupération localisation :", error);
        document.getElementById("location-name").textContent = "Localisation inconnue";
        });
    }
});
