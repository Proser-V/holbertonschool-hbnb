// Get the address input field
const addressInput = document.getElementById("new-place-address");

// When the input field loses focus (blur), start geocoding
addressInput.addEventListener("blur", async () => {
    // Trim the input value
    const address = addressInput.value.trim();
    if (!address) return;

    try {
        // Send a POST request to the geocoding endpoint
        const res = await fetch("/geocode-address", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include", // Include cookies
            body: JSON.stringify({ address }),
        });

        // Read the response as plain text
        const text = await res.text();
        let data;

        // Try to parse the response as JSON
        try {
            data = JSON.parse(text);
        } catch (jsonError) {
            console.error("Réponse non-JSON :", text);
            alert("Erreur : réponse invalide du serveur.");
            return;
        }

        // If response status is not OK, show error
        if (!res.ok) {
            alert("Erreur serveur : " + (data.error || res.status));
            return;
        }

        // If lat/lon are missing from response, show error
        if (!data.lat || !data.lon) {
            alert("Adresse non reconnue.");
            return;
        }

        // Get the hidden input fields for latitude and longitude
        const latInput = document.getElementById("new-place-latitude");
        const lonInput = document.getElementById("new-place-longitude");

        // If hidden fields are missing, show internal error
        if (!latInput || !lonInput) {
            console.error("Un des champs hidden est manquant !");
            alert("Erreur interne : champs d'adresse manquants.");
            return;
        }

        // Set the values of the hidden fields
        latInput.value = data.lat;
        lonInput.value = data.lon;

    } catch (e) {
        // Catch any network or unexpected errors
        console.error("Erreur réseau :", e);
        alert("Erreur réseau ou serveur inaccessible.");
    }
});
