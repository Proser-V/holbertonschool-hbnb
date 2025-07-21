document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("lightbox-overlay");
  const overlayImg = document.getElementById("lightbox-img");

  document.querySelectorAll(".photo-gallery img").forEach(photo => {
    photo.addEventListener("click", function () {
      overlayImg.src = this.src;
      overlay.classList.remove("hidden");
    });
  });

  overlay.addEventListener("click", function (e) {
    if (e.target === overlay || e.target === overlayImg) {
      overlay.classList.add("hidden");
      overlayImg.src = "";
    }
  });
});