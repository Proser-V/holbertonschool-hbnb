function openGalleryModal() {
    document.getElementById("gallery-modal").style.display = "block";
}

function closeGalleryModal() {
    document.getElementById("gallery-modal").style.display = "none";
}

closeModal.onclick = function() {
  modal.style.display ="none";
}

window.addEventListener('click', function (event) {
    const modal = document.getElementById("gallery-modal");
    if (event.target === modal) {
        closeGalleryModal();
    }
});