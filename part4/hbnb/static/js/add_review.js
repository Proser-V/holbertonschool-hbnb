import { apiFetch } from './refresh_token.js';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('add-review-container');
  const button = document.getElementById('open-review-form');
  const cancelBtn = document.getElementById('cancel-review-form');
  const form = document.getElementById('add-review-form');

  button.addEventListener('click', () => {
    container.classList.add('expanding');
    button.classList.add('hide-text');
    setTimeout(() => {
      container.classList.add('show-form');
    }, 500);
  });

  cancelBtn.addEventListener('click', () => {
    container.classList.remove('show-form');
    setTimeout(() => {
      container.classList.remove('expanding');
      button.classList.remove('hide-text');
    }, 400);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const bookingId = form.dataset.bookingId

    const data = {
      comment: form.comment.value,
      rating: form.rating.value,
    };

    try {
      const response = await apiFetch(`/api/v1/reviews/from_booking/${bookingId}`, {
        method: 'POST',
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert("Merci d'avoir laissé votre avis.");
        location.reload();
      } else {
        const error = await response.json();
        alert(`Erreur : ${error.message || 'Impossible de laisser un avis.'}`);
      }
    } catch (err) {
      console.error(err);
      alert('Erreur réseau ou serveur');
    }
  });
});

/* Star rating management */

const ratingContainers = document.querySelectorAll('.star-rating');

ratingContainers.forEach(container => {
  const stars = container.querySelectorAll('.star');
  const hiddenInput = container.querySelector('input[name="rating"]');
  const ratingText = container.querySelector('.rating-value');

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

    if (ratingText) {
      ratingText.textContent = `${rating.toFixed(1)} / 5`;
    }
  };

  stars.forEach(star => {
    const index = parseInt(star.dataset.index);

    star.addEventListener('mousemove', (e) => {
      const rect = star.getBoundingClientRect();
      const isLeft = e.clientX - rect.left < rect.width / 2;
      const value = isLeft ? index - 0.5 : index;
      renderStars(value);
    });

    star.addEventListener('mouseout', () => {
      const rating = parseFloat(container.dataset.rating || 0);
      renderStars(rating);
    });

    star.addEventListener('click', (e) => {
      const rect = star.getBoundingClientRect();
      const isLeft = e.clientX - rect.left < rect.width / 2;
      const rating = isLeft ? index - 0.5 : index;
      container.dataset.rating = rating;
      hiddenInput.value = rating;
      renderStars(rating);
    });
  });
});