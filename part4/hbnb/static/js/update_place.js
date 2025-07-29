import { apiFetch } from './refresh_token.js';

let selectedAmenityIds = [];

/* If an input is empty for parseFloat */
function parseFloatOrUndefined(value) {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? undefined : parsed;
}

/* Valdation d'image via le backend */
async function validateImageWithBackend(url) {
try {
    const res = await apiFetch('/validate-photo', {
        method: 'POST',
        body: JSON.stringify({ url })
    });

    const contentType = res.headers.get("content-type");
    let data = {};

    if (contentType && contentType.includes("application/json")) {
        data = await res.json();
    }

    if (!res.ok) {
        return { valid: false, reason: data.reason || `Code HTTP ${res.status}` };
    }

    return data;
} catch (error) {
    console.error("Erreur réseau ou JSON:", error);
    return { valid: false, reason: "Erreur réseau ou JSON invalide" };
}
}

let photoUrls = [];

function updateGallery() {
    const galleryImgs = document.querySelectorAll('.photo-gallery img');
    const defaultImg = galleryImgs[0]?.src;

    for (let i = 0; i < 5; i++) {
        const img = galleryImgs[i];
        img.src = photoUrls[i] || defaultImg;
    }
}

function loadPhotoInputs() {
  const container = document.getElementById('update-photo-url-inputs');
  const urls = JSON.parse(document.getElementById('existing-photo-urls')?.value || '[]');

  photoUrls = urls.slice();

  urls.forEach((url, index) => {
    const wrapper = document.createElement('div');
    wrapper.classList.add('update-photo-url-input')

    const input = document.createElement('input');
    input.type = 'url';
    input.placeholder = `URL de la photo ${index + 1}`;
    input.value = url;

    input.addEventListener('input', () => {
      photoUrls[index] = input.value.trim();
    });

    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Valider';

    button.addEventListener('click', async (event) => {
      event.preventDefault();
      const result = await validateImageWithBackend(input.value.trim());
      if (result.valid) {
        photoUrls[index] = input.value.trim();
        updateGallery();
        input.classList.remove('invalid');
      } else {
        input.classList.add('invalid');
        alert("Image invalide : " + result.reason);
      }
    });

    wrapper.appendChild(input);
    wrapper.appendChild(button);
    container.appendChild(wrapper);
  });

  updateGallery();
}

function addPhotoInput() {
    const container = document.getElementById('update-photo-url-inputs');
    const wrapper = document.createElement('div');
    wrapper.classList.add('update-photo-url-input');

    const index = photoUrls.length;
    photoUrls.push("");

    const input = document.createElement('input');
    input.type = 'url';
    input.placeholder = `URL de la photo ${index + 1}`;
    input.value = "";

    input.addEventListener('input', () => {
        photoUrls[index] = input.value.trim();
    });

    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Valider';

    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const url = input.value.trim();
        if (!url) return;

        const result = await validateImageWithBackend(url);
        if (result.valid) {
            photoUrls[index] = url;
            updateGallery();
            input.classList.remove('invalid');
        } else {
            input.classList.add('invalid');
            alert("Image invalide : " + result.reason);
        }
    });

    wrapper.appendChild(input);
    wrapper.appendChild(button);
    container.appendChild(wrapper);
}

// Charger dynamiquement les amenities
async function loadAmenities() {
try {
    const res = await apiFetch('/api/v1/amenities/', {
        method: 'GET',
    });

    const amenities = await res.json();
    const container = document.getElementById('update-place-amenities-list');
    container.classList.add('update-place-place-amenities');

    amenities.forEach(amenity => {
        const isChecked = selectedAmenityIds.includes(amenity.id);
        const wrapper = document.createElement('label');
        wrapper.className = 'update-place-amenity-item';
        const iconUrl = `/static/icons/${amenity.icon_file}`;

        wrapper.innerHTML = `
            <input type="checkbox" name="amenities" value="${amenity.id}" ${isChecked ? 'checked' : ''}>
            <img src="${iconUrl}" alt="${amenity.name}" class="amenity-icon">
            <span>${amenity.name}</span>
        `;

        container.appendChild(wrapper);
    });
} catch (e) {
    console.error("Erreur lors du chargement des équipements :", e);
}
}

document.addEventListener('DOMContentLoaded', () => {
    loadPhotoInputs();
     
    const addBtn = document.getElementById('add-photo-btn');
    const addText = document.querySelector('.add-photo-text');

    if (addBtn) {
        addBtn.addEventListener('click', addPhotoInput);
    }
    if (addText) {
        addText.addEventListener('click', addPhotoInput);
    }
    const currentAmenitiesInput = document.getElementById('current-amenities')
    selectedAmenityIds = JSON.parse(currentAmenitiesInput?.value || '[]')
    loadAmenities();
});

// Gestion du compteur de caractères
const inputTitle = document.getElementById('update-place-title');
const inputDescription = document.getElementById('update-place-comment');
const counterTitle = document.getElementById('update-place-title-counter');
const counterComment = document.getElementById('update-place-comment-counter');

inputTitle.addEventListener('input', () => {
    counterTitle.textContent = `${inputTitle.value.length} / ${inputTitle.maxLength}`;
});

inputDescription.addEventListener('input', () => {
    counterComment.textContent = `${inputDescription.value.length} / ${inputDescription.maxLength}`;
});

// Soumission du formulaire
const form = document.getElementById('update-place-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const placeId = document.getElementById('current-place-id').value || undefined;
    const title = document.getElementById('update-place-title').value || undefined;
    const description = document.getElementById('update-place-comment').value || undefined;
    const price = parseFloatOrUndefined(document.getElementById('update-place-price').value);
    const latitude = parseFloatOrUndefined(document.getElementById('update-place-latitude').value);
    const longitude = parseFloatOrUndefined(document.getElementById('update-place-longitude').value);
    const checkedAmenityIds = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(input => input.value);
    const filteredPhotos = photoUrls.filter(url => url && url.trim() !== "");

    const body = {
        title,
        description,
        price,
        latitude,
        longitude,
        amenity_ids: checkedAmenityIds || undefined,
        photos_url: filteredPhotos.length > 0 ? filteredPhotos : undefined,
    };

    if (latitude === null || longitude === null) {
        alert("Veuillez renseigner une adresse valide pour obtenir les coordonnées.");
        return;
    }

    try {
        const res = await apiFetch(`/api/v1/places/${placeId}`, {
            method: 'PUT',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            window.location.href = `/place/${placeId}`;
            alert('Hébergement modifié avec succès.')
        } else {
            const err = await res.json();
            alert("Erreur : " + (err.message || res.statusText));
        }
    } catch (error) {
        alert("Erreur réseau lors de la création.");
        console.error(error);
    }
});
