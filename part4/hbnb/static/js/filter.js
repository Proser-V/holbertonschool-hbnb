const addressInput = document.getElementById('address-filter');
const minPriceInput = document.getElementById('min-price-filter');
const maxPriceInput = document.getElementById('max-price-filter');
const filterButton = document.getElementById('filter-btn');
const latInput = document.getElementById('latitude-filter');
const lonInput = document.getElementById('longitude-filter');

// Create a container to show address suggestions (in case of multiple results)
const choicesContainer = document.createElement("div");
choicesContainer.id = "choices-container";
addressInput.parentNode.appendChild(choicesContainer);

// Utility function to calculate distance (in km) between two geo points using Haversine formula
function getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180; // Delta lat in radians
    const dLon = (lon2 - lon1) * Math.PI / 180; // Delta lon in radians

    // Calculate the square of half the chord length between the points
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    // Calculate the angular distance in radians
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    // Multiply by Earth's radius to get distance in kilometers
    return R * c; // Final distance (in km)
};

// Function to apply filters on place cards
function applyFilters() {
    const placeCards = document.querySelectorAll('.place-card');
    // Extract and normalize price values
    address = addressInput.value.trim() || undefined;
    minPriceValue = minPriceInput.value.trim() || undefined;
    let minPrice;
    if (minPriceValue === "") {
        minPrice = undefined;
    } else {
        minPrice = parseFloat(minPriceValue);
    }
    maxPriceValue = maxPriceInput.value.trim() || undefined;
    let maxPrice;
    if (maxPriceValue === "") {
        maxPrice = undefined;
    } else {
        maxPrice = parseFloat(maxPriceValue);
    };
    // Extract and normalize max distance
    const maxDistanceValue = document.getElementById("distance-filter").value;
    let maxDistance;
    if (maxDistanceValue === "") {
        maxDistance = undefined;
    } else {
        maxDistance = parseFloat(maxDistanceValue);
    };

    // Latitude and longitude for distance calculation
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);

    let visibleCount = 0; // To track number of matching cards

    placeCards.forEach(card => {
        const price = parseFloat(card.querySelector(".place-card-price").dataset.price);
        const locationDiv = card.querySelector(".place-location");
        const latPlace = parseFloat(locationDiv.dataset.lat);
        const lonPlace = parseFloat(locationDiv.dataset.lon);

        let priceOk = true; // Price filtering
        if (minPrice !== undefined && price < minPrice) priceOk = false;
        if (maxPrice !== undefined && price > maxPrice) priceOk = false;

        let distanceOk = true; // Distance filtering
        if (maxDistance !== undefined && latInput.value && lonInput.value) {
        const dist = getDistance(lat, lon, latPlace, lonPlace);
        // Check if calculated distance is smaller than the filter distance (bool)
        distanceOk = dist <= maxDistance;
        }

        // Show or hide card based on both filters
        if (priceOk && distanceOk) {
            card.style.display = "";
            visibleCount++;
        } else {
            card.style.display = "none";
        }
    });

    // Display "no results" message if no cards are visible
    const noResultMessage = document.getElementById('no-results-msg');
    if (visibleCount === 0) {
        noResultMessage.style.display = "block";
    } else {
        noResultMessage.style.display = "none";
    }
};

// When filter button is clicked
filterButton.addEventListener('click', async function(event) {
    event.preventDefault(); // No reloading

    // Collect and normalize all filter inputs
    address = addressInput.value.trim() || undefined;
    minPriceValue = minPriceInput.value.trim() || undefined;
    let minPrice;
    if (minPriceValue === "") {
        minPrice = undefined;
    } else {
        minPrice = parseFloat(minPriceValue);
    }
    maxPriceValue = maxPriceInput.value.trim() || undefined;
    let maxPrice;
    if (maxPriceValue === "") {
        maxPrice = undefined;
    } else {
        maxPrice = parseFloat(maxPriceValue);
    }
    const maxDistanceValue = document.getElementById("distance-filter").value;
    let maxDistance;
    if (maxDistanceValue === "") {
        maxDistance = undefined;
    } else {
        maxDistance = parseFloat(maxDistanceValue);
    }

    // If an address is provided, try to geocode it
    if (address) {
        try {
            const result = await fetch("/geocode-address", {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                credentials: 'include',
                body: JSON.stringify({ address })
            });
            const text = await result.text();
            let data;

            if (!result.ok) {
            alert("Erreur serveur : " + (data.error || res.status));
            return;
            }

            // Try to parse response as JSON
            try {
                data = JSON.parse(text);
            } catch (jsonError) {
                console.error("Réponse non-JSON :", text);
                alert('Erreur: Réponse invalide du serveur');
                return;
            }

            if (data.multiple_results) {
                // If server returns multiple possible addresses, show them
                choicesContainer.innerHTML = data.choices.map((choice, i) => `
                <div class="choice-item" data-lat="${choice.lat}" data-lon="${choice.lon}">
                    ${choice.display_name}
                </div>
                `).join("");

                // On click, populate inputs with selected choice and apply filters
                choicesContainer.querySelectorAll(".choice-item").forEach(item => {
                    item.addEventListener("click", () => {
                    addressInput.value = item.textContent;
                    document.getElementById("latitude-filter").value = item.dataset.lat;
                    document.getElementById("longitude-filter").value = item.dataset.lon;
                    choicesContainer.innerHTML = "";
                    applyFilters();
                    });
                });
            } else if (!data.error) {
                // If only one address is found, update inputs and filter
                document.getElementById("latitude-filter").value = data.lat;
                document.getElementById("longitude-filter").value = data.lon;
                choicesContainer.innerHTML = "";
                applyFilters();
            } else {
                // If there’s an error field in response
                choicesContainer.innerHTML = "";
                console.error(data.error);
            }

        } catch (e) {
        console.error("Erreur réseau :", e);
        alert("Erreur réseau ou serveur inaccessible.");
        }
    } else {
        // If no address, reset coordinates and apply filters
        latInput.value = "";
        lonInput.value = "";
        applyFilters();
    }
});
