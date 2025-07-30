// Select all elements needed
const modal = document.getElementById('user-modal');
const overlay = document.getElementById('modal-overlay');
const closeModalBtn = document.getElementById('close-user-modal');
const userPhoto = document.getElementById('modal-user-photo');
const userName = document.getElementById('modal-user-name');

// Add click event listeners to user-related elements (photos and names in places and reviews)
document.querySelectorAll(".place-owner-photo, .place-owner-name, .review-user-photo, .review-user-name").forEach(link => {
  link.addEventListener("click", event => {
    event.preventDefault(); // Prevent default action
    
    // Retrieve user name from data attribute or fallback to 'Nom inconnu'
    const name = link.dataset.userName || "Nom inconnu";
     // Retrieve user photo URL from data attribute or fallback to default image path
    const photo = link.dataset.userPhoto || '../static/images/default-user.png';

    userPhoto.src = photo; // Update modal photo with selected user's photo
    userName.textContent = name; // Update modal text with selected user's name

    modal.classList.remove('hidden'); // Show the modal
    overlay.classList.remove('hidden'); // Show the overlay
  });
});

// Function to close the modal and hide overlay
function closeModal() {
  modal.classList.add('hidden');
  overlay.classList.add('hidden');
}

// Attach event listeners to close modal when clicking close button or overlay
closeModalBtn.addEventListener('click', closeModal);
overlay.addEventListener('click', closeModal);
