/* Valdation d'image via le backend */
async function validateImageWithBackend(url) {
try {
    const res = await fetch('/validate-photo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
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
const defaultImg = galleryImgs[0]?.src; // assume first is default

for (let i = 0; i < 5; i++) {
    const img = galleryImgs[i];
    img.src = photoUrls[i] || defaultImg;
}
}

function addPhotoInput() {
const container = document.getElementById('photo-url-inputs');
const index = photoUrls.length;

photoUrls.push("");

const wrapper = document.createElement('div');
wrapper.className = 'photo-url-input';

const input = document.createElement('input');
input.type = 'url';
input.placeholder = `URL de la photo ${index + 1}`;
input.value = "";

const button = document.createElement('button');
button.type = 'button';
button.textContent = 'Valider';

button.addEventListener('click', async (event) => {
    event.preventDefault();
    const url = input.value.trim();
    if (!url) return;

    const result = await validateImageWithBackend(url);
    console.log("Validation result:", result);

    if (result.valid) {
        photoUrls[index] = url;
        updateGallery();
        input.classList.remove('invalid');
    } else {
        input.classList.add('invalid');
        alert("Image invalide : " + result.reason);
    }
});

input.addEventListener('input', () => {
    photoUrls[index] = input.value.trim();
});

wrapper.appendChild(input);
wrapper.appendChild(button);
container.appendChild(wrapper);
}

// ✅ Charger dynamiquement les amenities
async function loadAmenities() {
try {
    const res = await fetch('/api/v1/amenities/', {
        method: 'GET',
        credentials: 'include'
    });

    const amenities = await res.json();
    const container = document.getElementById('new-place-amenities-list');
    container.classList.add('new-place-place-amenities');

    amenities.forEach(amenity => {
        const wrapper = document.createElement('label');
        wrapper.className = 'new-place-amenity-item';
        const iconUrl = `/static/icons/${amenity.icon_file}`;

        wrapper.innerHTML = `
            <input type="checkbox" name="amenities" value="${amenity.id}">
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
const addBtn = document.getElementById('add-photo-btn');
const addText = document.querySelector('.add-photo-text');

if (addBtn) {
    addBtn.addEventListener('click', addPhotoInput);
}
if (addText) {
    addText.addEventListener('click', addPhotoInput);
}

loadAmenities();
});

// ✅ Gestion du compteur de caractères
const inputTitle = document.getElementById('new-place-title');
const inputDescription = document.getElementById('new-place-comment');
const counterTitle = document.getElementById('new-place-title-counter');
const counterComment = document.getElementById('new-place-comment-counter');

inputTitle.addEventListener('input', () => {
    counterTitle.textContent = `${inputTitle.value.length} / ${inputTitle.maxLength}`;
});

inputDescription.addEventListener('input', () => {
    counterComment.textContent = `${inputDescription.value.length} / ${inputDescription.maxLength}`;
});

// ✅ Soumission du formulaire
const form = document.getElementById('new-place-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const userId = document.getElementById('current-user-id').value;
    const title = document.getElementById('new-place-title').value;
    const description = document.getElementById('new-place-comment').value;
    const price = parseFloat(document.getElementById('new-place-price').value);
    const latitude = parseFloat(document.getElementById('new-place-latitude').value);
    const longitude = parseFloat(document.getElementById('new-place-longitude').value);
    const checkedAmenityIds = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(input => input.value);

    const body = {
        title,
        description,
        price,
        latitude,
        longitude,
        amenity_ids: checkedAmenityIds || undefined,
        photos_url: photoUrls || undefined,
    };

    if (latitude === null || longitude === null) {
        alert("Veuillez renseigner une adresse valide pour obtenir les coordonnées.");
        return;
    }
    console.log("Body envoyé :", body);
    try {
        const res = await fetch('/api/v1/places/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            window.location.href = `/user/${userId}/profile`;
        } else {
            const err = await res.json();
            alert("Erreur : " + (err.message || res.statusText));
        }
    } catch (error) {
        alert("Erreur réseau lors de la création.");
        console.error(error);
    }
});
