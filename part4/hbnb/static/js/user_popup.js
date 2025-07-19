const modal = document.getElementById('user-modal');
const overlay = document.getElementById('modal-overlay');
const closeModalBtn = document.getElementById('close-user-modal');
const userPhoto = document.getElementById('modal-user-photo');
const userName = document.getElementById('modal-user-name');

document.querySelectorAll(".place-owner-photo, .place-owner-name, .review-user-photo, .review-user-name").forEach(link => {
  link.addEventListener("click", event => {
    event.preventDefault();
    
    const name = link.getAttribute('data-user-name') || "Nom inconnu";
    const img = link.querySelector('img');
    let photo;
    if (img) {
      photo = img.src;
    } else {
      photo = 'https://cdn0.iconfinder.com/data/icons/mobile-basic-vol-1/32/Profile-256.png';
    }

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
