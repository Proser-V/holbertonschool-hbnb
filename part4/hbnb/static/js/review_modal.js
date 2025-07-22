document.addEventListener('DOMContentLoaded', () => {
    const openReviewBtn = document.getElementById('open-review-modal');
    const reviewModal = document.getElementById('review-modal');
    const modalOverlay = document.getElementById('modal-overlay');
    const bookingInput = document.getElementById('booking-id');
    const closeBtn = document.querySelector('.review-modal-close-button');

    if (openReviewBtn && reviewModal && bookingInput) {
        openReviewBtn.addEventListener('click', () => {
            const bookingId = openReviewBtn.dataset.bookingId;
            bookingInput.value = bookingId;

            reviewModal.classList.remove('hidden');
            modalOverlay.classList.remove('hidden');
        });
    }

document.getElementById('review-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const data = {
        booking_id: this.booking_id.value,
        comment: this.comment.value,
        rating: this.rating.value
    };

    const res = await fetch('/api/v1/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert('Avis envoyé avec succès !');
        location.reload();
    } else {
        alert("Erreur lors de l'envoi.");
    }
});
});