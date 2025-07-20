const modal = document.getElementById('user-modal');
const overlay = document.getElementById('modal-overlay');
const closeModalBtn = document.getElementById('close-user-modal');
const userPhoto = document.getElementById('modal-user-photo');
const userName = document.getElementById('modal-user-name');

document.querySelectorAll(".place-owner-photo, .place-owner-name, .review-user-photo, .review-user-name").forEach(link => {
  link.addEventListener("click", event => {
    event.preventDefault();
    
    const name = link.dataset.userName || "Nom inconnu";
    const photo = link.dataset.userPhoto || '../static/images/default-user.png';

    userPhoto.src = photo;
    userName.textContent = name;

    modal.classList.remove('hidden');
    overlay.classList.remove('hidden');
  });
});

function closeModal() {
  modal.classList.add('hidden');
  overlay.classList.add('hidden');
}

closeModalBtn.addEventListener('click', closeModal);
overlay.addEventListener('click', closeModal);
