import { apiFetch, formatPydanticError } from './refresh_token.js';

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button-to-update-review');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const container = button.closest('.review-container');
            const formWrapper = container.querySelector('.review-form-wrapper');

            container.classList.add('expanding');
            button.classList.add('hide-text');
            setTimeout(() => {
                container.classList.add('show-form');
                formWrapper.querySelector('textarea[name="comment"]').focus();
            }, 500);

            const cancelBtn = formWrapper.querySelector('.btn-cancel');
            cancelBtn.addEventListener('click', () => {
                container.classList.remove('show-form');
                setTimeout(() => {
                    container.classList.remove('expanding');
                    button.classList.remove('hide-text');
                }, 400);
            });

            const form = formWrapper.querySelector('form');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const reviewId = form.dataset.reviewId;
                const data = {
                    comment: form.comment.value,
                    rating: form.rating.value,
                };

                try {
                    const response = await apiFetch(`/api/v1/reviews/${reviewId}`, {
                        method: 'PUT',
                        body: JSON.stringify(data)
                    });

                    if (response.ok) {
                        alert("Votre avis a bien été mis à jour.");
                        location.reload();
                    } else {
                        const errorData = await response.json();
                        const prettyMessage = formatPydanticError(errorData);
                        alert(`Erreur lors de l'enregistrement :\n${prettyMessage}`);
                    }
                } catch (err) {
                    console.error(err);
                    alert('Erreur réseau ou serveur');
                }
            });
        });
    });
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
    const initialRating = parseFloat(container.dataset.rating || 0);
    renderStars(initialRating);

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
