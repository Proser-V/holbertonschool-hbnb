const addressInput = document.getElementById('address-filter');
const minPriceInput = document.getElementById('min-price-filter');
const maxPriceInput = document.getElementById('max-price-filter');
const filterButton = document.getElementById('filter-btn');
const latInput = document.getElementById('latitude-filter');
const lonInput = document.getElementById('longitude-filter');

const choicesContainer = document.createElement("div");
choicesContainer.id = "choices-container";
addressInput.parentNode.appendChild(choicesContainer);

function getDistance(lat1, lon1, lat2, lon2) {
    // Haversine formula:

    const R = 6371; // Radius of the Earth in kilometers
    // Convert the difference in latitude to radians
    const dLat = (lat2 - lat1) * Math.PI / 180;
    // Convert the difference in longitude to radians
    const dLon = (lon2 - lon1) * Math.PI / 180;

    // Calculate the square of half the chord length between the points
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    // Calculate the angular distance in radians
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    // Multiply by Earth's radius to get distance in kilometers
    return R * c;
};

function applyFilters() {
    const placeCards = document.querySelectorAll('.place-card');
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
    const maxDistanceValue = document.getElementById("distance-filter").value;
    let maxDistance;
    if (maxDistanceValue === "") {
        maxDistance = undefined;
    } else {
        maxDistance = parseFloat(maxDistanceValue);
    };
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);

    placeCards.forEach(card => {
        const price = parseFloat(card.querySelector(".place-card-price").dataset.price);
        const locationDiv = card.querySelector(".place-location");
        const latPlace = parseFloat(locationDiv.dataset.lat);
        const lonPlace = parseFloat(locationDiv.dataset.lon);
        let visibleCount = 0;

        let priceOk = true;
        if (minPrice !== undefined && price < minPrice) priceOk = false;
        if (maxPrice !== undefined && price > maxPrice) priceOk = false;

        let distanceOk = true;

        if (maxDistance !== undefined && latInput.value && lonInput.value) {
        const dist = getDistance(lat, lon, latPlace, lonPlace);
        distanceOk = dist <= maxDistance;
        }
        if (priceOk && distanceOk) {
            card.style.display = "";
            visibleCount++;
        } else {
            card.style.display = "none";
        }
    });
    const noResultMessage = document.getElementById('no-results-msg');
    if (visibleCount === 0) {
        noResultMessage.style.display = "block";
    } else {
        noResultMessage.style.display = "none";
    }
};

filterButton.addEventListener('click', async function(event) {
    event.preventDefault(); // No reloading

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

            try {
                data = JSON.parse(text);
            } catch (jsonError) {
                console.error("Réponse non-JSON :", text);
                alert('Erreur: Réponse invalide du serveur');
                return;
            }

            if (data.multiple_results) { // Multiple choices
                choicesContainer.innerHTML = data.choices.map((choice, i) => `
                <div class="choice-item" data-lat="${choice.lat}" data-lon="${choice.lon}">
                    ${choice.display_name}
                </div>
                `).join("");

            choicesContainer.querySelectorAll(".choice-item").forEach(item => {
                item.addEventListener("click", () => {
                addressInput.value = item.textContent;
                document.getElementById("latitude-filter").value = item.dataset.lat;
                document.getElementById("longitude-filter").value = item.dataset.lon;
                choicesContainer.innerHTML = "";
                applyFilters();
                });
            });
            } else if (!data.error) { // One choice
            document.getElementById("latitude-filter").value = data.lat;
            document.getElementById("longitude-filter").value = data.lon;
            choicesContainer.innerHTML = "";
            applyFilters();
            } else {
            choicesContainer.innerHTML = "";
            console.error(data.error);
            }

        } catch (e) {
        console.error("Erreur réseau :", e);
        alert("Erreur réseau ou serveur inaccessible.");
        }
    } else {
        latInput.value = "";
        lonInput.value = "";
        applyFilters();
    }
});
