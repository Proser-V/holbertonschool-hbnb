import { apiFetch, formatPydanticError } from './refresh_token.js';

// Wait for the DOM to be fully loaded before attaching event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Get references to key elements for the review form UI
    const container = document.getElementById('add-review-container');
    const button = document.getElementById('open-review-form');
    const cancelBtn = document.getElementById('cancel-review-form');
    const form = document.getElementById('add-review-form');

    // Ensure all elements exist before adding event listeners
    if (button && cancelBtn && form && container) {
        // Show the review form with animation when "open review" button is clicked
        button.addEventListener('click', () => {
            container.classList.add('expanding'); // Start expansion animation
            button.classList.add('hide-text'); // Hide the button text during animation
            setTimeout(() => {
                container.classList.add('show-form'); // Show the form after animation delay
            }, 500);
        });

    // Hide the review form and revert UI when "cancel" button is clicked
    cancelBtn.addEventListener('click', () => {
        container.classList.remove('show-form'); // Hide the form immediately
        setTimeout(() => {
            container.classList.remove('expanding'); // Remove expansion animation class
            button.classList.remove('hide-text'); // Show the button text again
        }, 400);
    });

    // Handle the review form submission asynchronously
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission and page reload
        const bookingId = form.dataset.bookingId // Retrieve associated booking ID from data attribute

        // Gather data from form fields
        const data = {
            comment: form.comment.value,
            rating: form.rating.value,
        };

    try {
        // Send review data to backend API
        const response = await apiFetch(`/api/v1/reviews/from_booking/${bookingId}`, {
            method: 'POST',
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Merci d'avoir laissé votre avis.");
            location.reload(); // Reload page to show updated reviews
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur lors de l'enregistrement :\n${prettyMessage}`);
        }
        } catch (err) {
            console.error(err);
            alert('Erreur réseau ou serveur');
        }
    });
    }
});

/* Star rating management */

// Select all star rating containers on the page
const ratingContainers = document.querySelectorAll('.star-rating');

ratingContainers.forEach(container => {
  const stars = container.querySelectorAll('.star'); // Star elements representing rating points
  const hiddenInput = container.querySelector('input[name="rating"]'); // Hidden input to store rating value
  const ratingText = container.querySelector('.rating-value'); // Element to display numeric rating

    /**
   * Render stars visually according to a decimal rating.
   * - Full star (★) for whole points
   * - Half star (⯪) for half points
   * - Empty star (☆) otherwise
   * Also updates the textual rating display if present.
   *
   * @param {number} rating - Current rating value
   */

    const renderStars = (rating) => {
        stars.forEach(star => {
            const index = parseInt(star.dataset.index);

            if (rating >= index) {
                star.textContent = '★';
            } else if (rating >= index - 0.5) {
                star.textContent = '⯪';
            } else {
                star.textContent = '☆';
            }
        });

        // Update the textual rating display to show the rating rounded to one decimal place out of 5.
        if (ratingText) {
            ratingText.textContent = `${rating.toFixed(1)} / 5`;
        }
    };

    // Add event listeners to each star for interactive rating selection
    stars.forEach(star => {
        const index = parseInt(star.dataset.index);

        // On mouse move: highlight stars to preview potential rating (half star precision)
        star.addEventListener('mousemove', (e) => {
            const rect = star.getBoundingClientRect();
            const isLeft = e.clientX - rect.left < rect.width / 2; // Detect if cursor is on left half of star
            const value = isLeft ? index - 0.5 : index; // Assign half or full star accordingly
            renderStars(value);
        });

        // On mouse out: revert stars to current selected rating
        star.addEventListener('mouseout', () => {
            const rating = parseFloat(container.dataset.rating || 0);
            renderStars(rating);
        });

        // On click: set rating value with half-star precision, update hidden input and UI
        star.addEventListener('click', (e) => {
            const rect = star.getBoundingClientRect();
            const isLeft = e.clientX - rect.left < rect.width / 2;
            const rating = isLeft ? index - 0.5 : index;

            container.dataset.rating = rating; // Store rating as dataset for later retrieval
            hiddenInput.value = rating; // Update hidden form input for submission
            renderStars(rating); // Update star display
        });
    });
});
