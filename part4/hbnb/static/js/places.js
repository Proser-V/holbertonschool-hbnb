async function fetchPlaces() {
  const container = document.getElementById("places-list");
  container.innerHTML = ""; //clean befor insertion
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/');
    if (!response.ok) {
      throw new Error("Erreur lors du chargement des lieux");
    }

    const places = await response.json();
    if (places.length === 0) {
      const message = document.createElement("p");
        message.textContent = "Aucun lieu trouvé.";
        container.appendChild(message);
    } else {
      displayPlaces(places);
    }
  } catch (error) {
    console.error("Erreur :", error);

    const errorMsg = document.createElement("p");
    errorMsg.textContent = "Erreur: Impossible de charger la liste des lieux.";
    container.appendChild(errorMsg);
  }
}

function displayPlaces(places) {
  const container = document.getElementById("places-list");

  places.forEach(place => {
    const DEFAULT_PLACE_PHOTO_URL = "https://static.vecteezy.com/system/resources/previews/006/059/989/large_2x/crossed-camera-icon-avoid-taking-photos-image-is-not-available-illustration-free-vector.jpg";
    const img_url = place.photos_url[0] || DEFAULT_PLACE_PHOTO_URL;

    const link =document.createElement("a");
    link.href = `place.html?id=${place.id}`;
    link.className = "place-card";

    const img = document.createElement("img");
    img.className = "place-front-pic";
    img.src = img_url;
    img.alt = place.title;
    img.style.width = "100%";
    img.style.borderRadius = "10px 10px 0 0";
    img.onerror = function () {
      this.onerror = null;
      this.src = DEFAULT_PLACE_PHOTO_URL;
    }

    const content = document.createElement("div");
    content.className = "place-content";

    const title = document.createElement("h2");
    title.className = "place-title";
    title.textContent = place.title;

    const price = document.createElement("p");
    price.className = "place-price";
    price.textContent = `${place.price}€ / nuit`;

    const rate = document.createElement("p");
    rate.className = "place-rating";

    const note = Math.round((place.rating || 0) * 2) / 2;
    if (note === 0) {
      rate.textContent = "Pas encore de note";
    } else {
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement("span");
      star.className = "star";
      if (i <= note) {
        star.textContent = "★";
      } else if ( i - 0.5 === note) {
        star.textContent = "⯪";
      } else {
        star.textContent = "☆";
      }
      rate.appendChild(star);
    }
    const num_note = document.createElement("span");
    num_note.className = "rating-value";
    num_note.textContent = ` ${note}`;

    rate.appendChild(num_note);
  }
    content.appendChild(title);
    content.appendChild(price);
    content.appendChild(rate);
    link.appendChild(img);
    link.appendChild(content);
    container.appendChild(link);
  });
}

document.addEventListener("DOMContentLoaded", fetchPlaces);
