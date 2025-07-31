import { apiFetch, formatPydanticError } from './refresh_token.js';

// Store the default image URL on initial page load
const defaultGalleryImage = document.querySelector('.photo-gallery img')?.getAttribute('src');
let selectedAmenityIds = [];

// Helper: parse a string to float, return undefined if invalid
function parseFloatOrUndefined(value) {
    const parsed = parseFloat(value);
    return isNaN(parsed) ? undefined : parsed;
}

// Validate an image URL by sending it to the backend for verification
async function validateImageWithBackend(url) {
    try {
        // API helper POST call to validate a photo
        const res = await apiFetch('/validate-photo', {
            method: 'POST',
            body: JSON.stringify({ url })
        });

        const contentType = res.headers.get("content-type");
        let data = {};

        // Parse JSON response if content-type is JSON
        if (contentType && contentType.includes("application/json")) {
            data = await res.json();
        }

        // If response is not OK, return invalid with reason from backend or HTTP status
        if (!res.ok) {
            return { valid: false, reason: data.reason || `Code HTTP ${res.status}` };
        }

        return data; // Return backend validation result (expecting {valid: true} or similar)
    } catch (error) {
        console.error("Erreur réseau ou JSON:", error);
        return { valid: false, reason: "Erreur réseau ou JSON invalide" };
    }
}

let photoUrls = [];

// Update the photo gallery thumbnails using current photo URLs
function updateGallery() {
    const galleryImgs = document.querySelectorAll('.photo-gallery img');

    // Set gallery image to photo URL if available, or use default image as fallback.
    for (let i = 0; i < 5; i++) {
        const img = galleryImgs[i];
        img.src = photoUrls[i] || defaultImg;
    }
}

// Load existing photo URLs and dynamically create input fields for each
function loadPhotoInputs() {
    const container = document.getElementById('update-photo-url-inputs');
    // Get existing photo URLs from hidden input as JSON array
    const urls = JSON.parse(document.getElementById('existing-photo-urls')?.value || '[]');

    photoUrls = urls.slice(); // clone array

    urls.forEach((url, index) => {
        // Create wrapper div for input and button
        const wrapper = document.createElement('div');
        wrapper.classList.add('update-photo-url-input')

        // Create input field for URL
        const input = document.createElement('input');
        input.type = 'url';
        input.placeholder = `URL de la photo ${index + 1}`;
        input.value = url;

        // Update photoUrls array on input change
        input.addEventListener('input', () => {
            photoUrls[index] = input.value.trim();
        });

        // Create validation button for this input
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = 'Valider';

        // On click, validate image URL with backend and update gallery accordingly
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            const result = await validateImageWithBackend(input.value.trim());
            if (result.valid) {
                photoUrls[index] = input.value.trim(); // If valid, update the photo URL at this index
                updateGallery(); // Refresh the gallery display with the new URLs
                input.classList.remove('invalid'); // Remove "invalid" visual indicator from input
            } else {
                // If invalid, mark the input visually and show an alert
                input.classList.add('invalid');
                alert("Image invalide : " + result.reason);
            }
        });

        // Append the input and button to the wrapper, and then to the DOM
        wrapper.appendChild(input);
        wrapper.appendChild(button);
        container.appendChild(wrapper);
    });

    updateGallery(); // Refresh the gallery view with current photo URLs
}

// Add a new empty photo URL input field
function addPhotoInput() {
    // Select the container where new photo inputs will be added
    const container = document.getElementById('update-photo-url-inputs');
    // Create a wrapper <div> for the input + button
    const wrapper = document.createElement('div');
    wrapper.classList.add('update-photo-url-input');

    // Get the index for the new input (next available position in the photoUrls array)
    const index = photoUrls.length; 
    photoUrls.push(""); // Add empty slot for new photo URL

    // Create an <input> element for the photo URL
    const input = document.createElement('input');
    input.type = 'url';
    input.placeholder = `URL de la photo ${index + 1}`;
    input.value = "";

    // Update photoUrls array on input change
    input.addEventListener('input', () => {
        photoUrls[index] = input.value.trim();
    });

    // Validate newly added input on button click
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Valider';

    // When the button is clicked, validate the URL via backend
    button.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form behavior if any
        const url = input.value.trim();
        if (!url) return;

        const result = await validateImageWithBackend(url);
        if (result.valid) {
            photoUrls[index] = url; // If valid, update the photo URL at this index
            updateGallery(); // Refresh the gallery display with the new URLs
            input.classList.remove('invalid'); // Remove "invalid" visual indicator from input
        } else {
            // If not valid, visually mark the input and show error message
            input.classList.add('invalid');
            alert("Image invalide : " + result.reason);
        }
    });

    // Add the input and button to a wrapper container
    wrapper.appendChild(input);
    wrapper.appendChild(button);
    // Add the wrapper to the main photo input container
    container.appendChild(wrapper);
}

// Load all amenities from backend and display them as checkbox list
async function loadAmenities() {
try {
    const res = await apiFetch('/api/v1/amenities/', {
        method: 'GET',
    });

    const amenities = await res.json();
    const container = document.getElementById('update-place-amenities-list');
    container.classList.add('update-place-place-amenities');

    amenities.forEach(amenity => {
        // Check if this amenity is already selected
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

    // Attach event listeners to add photo inputs via button or text click
    if (addBtn) {
        addBtn.addEventListener('click', addPhotoInput);
    }
    if (addText) {
        addText.addEventListener('click', addPhotoInput);
    }
    // Initialize selected amenities from hidden input and load amenities checkboxes
    const currentAmenitiesInput = document.getElementById('current-amenities')
    selectedAmenityIds = JSON.parse(currentAmenitiesInput?.value || '[]')
    loadAmenities();
});

// Character counters for title and description inputs
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

// Form submission: update place details
const form = document.getElementById('update-place-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const placeId = document.getElementById('current-place-id').value || undefined;
    const title = document.getElementById('update-place-title').value || undefined;
    const description = document.getElementById('update-place-comment').value || undefined;
    const price = parseFloatOrUndefined(document.getElementById('update-place-price').value);
    const latitude = parseFloatOrUndefined(document.getElementById('update-place-latitude').value);
    const longitude = parseFloatOrUndefined(document.getElementById('update-place-longitude').value);
    // Get IDs of all checked amenities
    const checkedAmenityIds = Array.from(document.querySelectorAll('input[name="amenities"]:checked'))
        .map(input => input.value);
    // Filter out empty or blank photo URLs
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

    // Ensure valid coordinates before submitting
    if (latitude === null || longitude === null) {
        alert("Veuillez renseigner une adresse valide pour obtenir les coordonnées.");
        return;
    }

    try {
        // API PUT request to update the place
        const res = await apiFetch(`/api/v1/places/${placeId}`, {
            method: 'PUT',
            body: JSON.stringify(body)
        });

        if (res.ok) {
            window.location.href = `/place/${placeId}`; // Redirection to the place public page
            alert('Hébergement modifié avec succès.')
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur :\n${prettyMessage}`);
        }
    } catch (error) {
        alert("Erreur réseau lors de la création.");
        console.error(error);
    }
});
