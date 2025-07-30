import { apiFetch } from './refresh_token.js';

// Store the default image URL on initial page load
const defaultGalleryImage = document.querySelector('.photo-gallery img')?.getAttribute('src');

// Validate an image URL by sending it to the backend.
async function validateImageWithBackend(url) {
try {
    const res = await apiFetch('/validate-photo', {
        method: 'POST',
        body: JSON.stringify({ url })
    });

    const contentType = res.headers.get("content-type");
    let data = {};

    // Try to parse JSON response if available
    if (contentType && contentType.includes("application/json")) {
        data = await res.json();
    }

    // If the response indicates failure, return invalid with the backend's reason or the HTTP status code.
    if (!res.ok) {
        return { valid: false, reason: data.reason || `Code HTTP ${res.status}` };
    }

    return data;
} catch (error) { // Catch network or parsing errors
    console.error("Erreur réseau ou JSON:", error);
    return { valid: false, reason: "Erreur réseau ou JSON invalide" };
}
}

let photoUrls = [];  // Array to store image URLs

/**
 * Update the main photo gallery preview with selected photo URLs.
 * Fills missing slots with the default image.
 */

function updateGallery() {
    const galleryImgs = document.querySelectorAll('.photo-gallery img');

    // Set gallery image to photo URL if available, or use default image as fallback.
    for (let i = 0; i < 5; i++) {
        const img = galleryImgs[i];
        img.src = photoUrls[i] || defaultGalleryImage;
    }
}

// Adds a new input field for a photo URL and connects it to the validation logic.
function addPhotoInput() {
    const container = document.getElementById('photo-url-inputs');
    const index = photoUrls.length; // Current index for new image

    photoUrls.push(""); // Reserve slot in array for the new input

    // Create wrapper element for input and button
    const wrapper = document.createElement('div');
    wrapper.className = 'photo-url-input';

    // Input for the image URL
    const input = document.createElement('input');
    input.type = 'url';
    input.placeholder = `URL de la photo ${index + 1}`;
    input.value = "";

    // Validation button
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Valider';

    // Validate photo URL on button click
    button.addEventListener('click', async (event) => {
        event.preventDefault();
        const url = input.value.trim();
        if (!url) return;

        const result = await validateImageWithBackend(url);
        console.log("Validation result:", result);

        if (result.valid) {
            // Save the URL and update preview
            photoUrls[index] = url;
            updateGallery();
            input.classList.remove('invalid');
        } else {
            input.classList.add('invalid');
            alert("Image invalide : " + result.reason);
        }
    });
    // Live update of the URL in photoUrls array
    input.addEventListener('input', () => {
        photoUrls[index] = input.value.trim();
    });

    wrapper.appendChild(input);
    wrapper.appendChild(button);
    container.appendChild(wrapper);
}


// Fetch amenities from backend and dynamically display them with icons and checkboxes.
async function loadAmenities() {
    try {
        const res = await apiFetch('/api/v1/amenities/', {
            method: 'GET',
        });

        const amenities = await res.json();
        const container = document.getElementById('new-place-amenities-list');
        container.classList.add('new-place-place-amenities');

        // For each amenity, create a checkbox with label and icon
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

// Register click listeners to add a photo input
document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add-photo-btn');
    const addText = document.querySelector('.add-photo-text');

    if (addBtn) {
        addBtn.addEventListener('click', addPhotoInput);
    }
    if (addText) {
        addText.addEventListener('click', addPhotoInput);
    }

    loadAmenities(); // Fetch and render amenities
});

// Character counter logic
const inputTitle = document.getElementById('new-place-title');
const inputDescription = document.getElementById('new-place-comment');
const counterTitle = document.getElementById('new-place-title-counter');
const counterComment = document.getElementById('new-place-comment-counter');

// Update character count for title in real-time
inputTitle.addEventListener('input', () => {
    counterTitle.textContent = `${inputTitle.value.length} / ${inputTitle.maxLength}`;
});

// Update character count for description in real-time
inputDescription.addEventListener('input', () => {
    counterComment.textContent = `${inputDescription.value.length} / ${inputDescription.maxLength}`;
});

// Form submission
const form = document.getElementById('new-place-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default page reload

    const userId = document.getElementById('current-user-id').value;
    const title = document.getElementById('new-place-title').value;
    const description = document.getElementById('new-place-comment').value;
    const price = parseFloat(document.getElementById('new-place-price').value);
    const latitude = parseFloat(document.getElementById('new-place-latitude').value);
    const longitude = parseFloat(document.getElementById('new-place-longitude').value);
    // Get IDs of all checked amenities as an array of strings.
    const checkedAmenityIds = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(input => input.value);
    // Only keep non-empty photo URLs
    const filteredPhotos = photoUrls.filter(url => url && url.trim() !== "");

    const body = {
        title,
        description,
        price,
        latitude,
        longitude,
        amenity_ids: checkedAmenityIds || undefined,
        // Include photos only if there are valid URLs; omit the field otherwise.
        photos_url: filteredPhotos.length > 0 ? filteredPhotos : undefined,
    };

    // Prevent submission if geocoding failed
    if (latitude === null || longitude === null) {
        alert("Veuillez renseigner une adresse valide pour obtenir les coordonnées.");
        return;
    }

    // Send POST request to create a new place
    try {
        const res = await apiFetch('/api/v1/places/', {
            method: 'POST',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            // Redirect to user profile after successful creation
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
